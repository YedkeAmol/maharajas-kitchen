from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for
import sqlite3
import os
import time
import random
import uuid
import qrcode
import io
import base64
import re
import urllib.parse
import requests
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'maharajas-kitchen-secret-key-123'
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'food_billing.db')
app.config['TAX_RATE'] = 0.05  # 5% flat tax

PHONE_REGEX = re.compile(r'^\d{10}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row # To access columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'Admin':
            return "Unauthorized - Admin access required", 403
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_global_data():
    try:
        db = get_db()
        # Sum total for today
        cur = db.execute("SELECT SUM(total) as daily_total FROM orders WHERE date(created_at) = date('now')")
        row = cur.fetchone()
        daily_sales = row['daily_total'] if row and row['daily_total'] else 0.0
    except Exception:
        daily_sales = 0.0
    return dict(daily_sales=daily_sales)

# --- Page Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cur = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/history')
@login_required
def history():
    return render_template('history.html')

@app.route('/staff')
@admin_required
def staff():
    return render_template('staff.html')

@app.route('/branches')
@admin_required
def branches():
    return render_template('branches.html')

@app.route('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/receipt/<bill_number>')
@login_required
def receipt(bill_number):
    db = get_db()
    cur = db.execute('SELECT total FROM orders WHERE bill_number = ?', (bill_number,))
    order = cur.fetchone()
    qr_b64 = ""
    if order:
        upi_url = f"upi://pay?pa=restaurant@upi&pn=Maharaja's Kitchen&am={order['total']}&cu=INR"
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(upi_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
    return render_template('receipt.html', bill_number=bill_number, qr_b64=qr_b64)

# --- API Endpoints ---

@app.route('/api/dashboard/stats')
def api_dashboard_stats():
    range_filter = request.args.get('range', 'monthly')
    db = get_db()
    
    date_condition = "date(created_at) >= date('now', '-180 days')"
    if range_filter == 'today':
        date_condition = "date(created_at) = date('now')"
    elif range_filter == '7':
        date_condition = "date(created_at) >= date('now', '-7 days')"
    elif range_filter == '30':
        date_condition = "date(created_at) >= date('now', '-30 days')"
    elif range_filter == 'monthly':
        date_condition = "date(created_at) >= date('now', '-180 days')"

    cur = db.execute(f"SELECT COUNT(*) as orders, SUM(total) as sales FROM orders WHERE {date_condition} AND status != 'Void'")
    stats = cur.fetchone()
    
    orders = stats['orders'] or 0
    sales = stats['sales'] or 0.0
    aov = sales / orders if orders > 0 else 0.0
    
    cur = db.execute(f"""
        SELECT i.name, SUM(oi.quantity) as qty
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN items i ON oi.item_id = i.id
        WHERE {date_condition} AND o.status != 'Void'
        GROUP BY i.id
        ORDER BY qty DESC
        LIMIT 1
    """)
    top_dish = cur.fetchone()
    top_dish_name = top_dish['name'] if top_dish else 'N/A'
    
    return jsonify({
        "sales": sales,
        "orders": orders,
        "aov": aov,
        "top_dish": top_dish_name
    })

@app.route('/api/dashboard/charts')
def api_dashboard_charts():
    range_filter = request.args.get('range', 'monthly')
    db = get_db()
    
    month_names = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }

    if range_filter == 'today':
        date_condition = "date(created_at) = date('now')"
        group_by = "strftime('%H:00', created_at)"
    elif range_filter == '7':
        date_condition = "date(created_at) >= date('now', '-7 days')"
        group_by = "date(created_at)"
    elif range_filter == '30':
        date_condition = "date(created_at) >= date('now', '-30 days')"
        group_by = "date(created_at)"
    elif range_filter == 'monthly':
        date_condition = "date(created_at) >= date('now', '-180 days')"
        group_by = "strftime('%Y-%m', created_at)"
    else:
        date_condition = "date(created_at) >= date('now', '-180 days')"
        group_by = "strftime('%Y-%m', created_at)"

    # Sales trend
    cur = db.execute(f"""
        SELECT {group_by} as label, SUM(total) as value
        FROM orders
        WHERE {date_condition} AND status != 'Void'
        GROUP BY label
        ORDER BY label ASC
    """)
    raw_trend = [dict(row) for row in cur.fetchall()]
    
    trend = []
    for r in raw_trend:
        lbl = str(r['label'])
        val = round(r['value'] or 0.0, 2)
        # Format YYYY-MM into 'May 2026', 'Jun 2026', etc.
        if len(lbl) == 7 and '-' in lbl:
            parts = lbl.split('-')
            m_name = month_names.get(parts[1], parts[1])
            trend.append({'label': f"{m_name} {parts[0]}", 'value': val})
        # Format YYYY-MM-DD into '27 Sep', '06 Oct', etc.
        elif len(lbl) == 10 and lbl.count('-') == 2:
            parts = lbl.split('-')
            m_name = month_names.get(parts[1], parts[1])
            trend.append({'label': f"{parts[2]} {m_name}", 'value': val})
        else:
            trend.append({'label': lbl, 'value': val})
    
    # Top 5 dishes
    cur = db.execute(f"""
        SELECT i.name as label, SUM(oi.quantity) as value
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN items i ON oi.item_id = i.id
        WHERE {date_condition} AND o.status != 'Void'
        GROUP BY i.id
        ORDER BY value DESC
        LIMIT 5
    """)
    top_dishes = [dict(row) for row in cur.fetchall()]
    
    # Payment modes with percentage calculation
    cur = db.execute(f"""
        SELECT payment_mode as label, COUNT(*) as value
        FROM orders
        WHERE {date_condition} AND status != 'Void'
        GROUP BY payment_mode
        ORDER BY value DESC
    """)
    payments = [dict(row) for row in cur.fetchall()]
    total_payments = sum(p['value'] for p in payments) or 1
    for p in payments:
        p['percentage'] = round((p['value'] / total_payments) * 100, 1)
    
    return jsonify({
        "trend": trend,
        "top_dishes": top_dishes,
        "payments": payments
    })

@app.route('/api/items', methods=['GET'])
def get_items():
    db = get_db()
    cur = db.execute('''
        SELECT i.*, IFNULL(SUM(oi.quantity), 0) as sales_count
        FROM items i
        LEFT JOIN order_items oi ON i.id = oi.item_id
        WHERE i.is_active = 1
        GROUP BY i.id
    ''')
    items = [dict(row) for row in cur.fetchall()]
    return jsonify(items)

@app.route('/api/tables', methods=['GET'])
def get_tables():
    db = get_db()
    # Assuming status='Pending' means table is occupied
    cur = db.execute("SELECT table_number FROM orders WHERE order_type = 'Dine-In' AND status = 'Pending'")
    occupied = [row['table_number'] for row in cur.fetchall() if row['table_number']]
    return jsonify({"occupied": occupied})

@app.route('/api/orders', methods=['POST'])
def checkout():
    data = request.json
    items = data.get('items', [])
    order_type = data.get('order_type', 'Dine-In')
    delivery_fee = data.get('delivery_fee', 0.0)
    customer_name = data.get('customer_name', '')
    customer_address = data.get('customer_address', '')
    customer_phone = data.get('customer_phone', '')
    table_number = data.get('table_number', '')
    payment_mode = data.get('payment_mode', 'Cash')
    
    if not items:
        return jsonify({"error": "Cart is empty"}), 400
        
    db = get_db()
    cur = db.cursor()
    
    # Calculate subtotal
    subtotal = 0.0
    valid_items = []
    
    for item in items:
        cur.execute('SELECT id, price FROM items WHERE id = ? AND is_active = 1', (item['id'],))
        row = cur.fetchone()
        if row:
            price = row['price']
            qty = item['quantity']
            subtotal += price * qty
            valid_items.append({"id": row['id'], "price": price, "quantity": qty})
            
    if not valid_items:
        return jsonify({"error": "No valid items found"}), 400
        
    tax = subtotal * 0.05
    total = subtotal + tax + delivery_fee
    
    bill_number = f"BILL-{int(time.time())}-{uuid.uuid4().hex[:4]}"
    
    initial_status = 'Preparing' if order_type == 'Delivery' else 'Completed'
    
    cur.execute('''
        INSERT INTO orders (bill_number, subtotal, tax, delivery_fee, total, order_type, customer_name, customer_address, customer_phone, table_number, payment_mode, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (bill_number, subtotal, tax, float(delivery_fee), total, order_type, customer_name, customer_address, customer_phone, table_number, payment_mode, initial_status))
    order_id = cur.lastrowid
    
    for vi in valid_items:
        cur.execute('''
            INSERT INTO order_items (order_id, item_id, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (order_id, vi['id'], vi['quantity'], vi['price']))
        
    db.commit()
    
    return jsonify({
        "message": "Order created",
        "bill_number": bill_number,
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2)
    }), 201

@app.route('/api/orders/<bill_number>', methods=['GET'])
def get_order(bill_number):
    db = get_db()
    cur = db.execute('SELECT * FROM orders WHERE bill_number = ?', (bill_number,))
    order = cur.fetchone()
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
        
    order_dict = dict(order)
    
    cur = db.execute('''
        SELECT oi.*, i.name 
        FROM order_items oi
        JOIN items i ON oi.item_id = i.id
        WHERE oi.order_id = ?
    ''', (order_dict['id'],))
    
    order_dict['items'] = [dict(row) for row in cur.fetchall()]
    return jsonify(order_dict)

@app.route('/api/orders/<bill_number>/status', methods=['PUT'])
@login_required
def update_order_status(bill_number):
    data = request.json
    new_status = data.get('status')
    if not new_status:
        return jsonify({"error": "Status required"}), 400
        
    db = get_db()
    db.execute('UPDATE orders SET status = ? WHERE bill_number = ?', (new_status, bill_number))
    db.commit()
    return jsonify({"message": "Status updated successfully"})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    db = get_db()
    cur = db.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = [dict(row) for row in cur.fetchall()]
    return jsonify(orders)

def process_item_image(image_url, item_name):
    """
    Cleans Google image search URLs and downloads remote images locally to static/img/
    so the app works 100% offline during showcase/presentation.
    """
    if not image_url or not str(image_url).strip():
        return ''
    
    url = str(image_url).strip()
    
    # Extract true image URL if user pasted a Google Images search landing page
    if 'google.' in url and ('imgres' in url or 'imgurl=' in url):
        try:
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if 'imgurl' in params and params['imgurl']:
                url = params['imgurl'][0]
        except Exception:
            pass

    # Normalize local static paths
    if url.startswith('/static/') or url.startswith('static/'):
        return '/' + url.lstrip('/')
    
    # If external http/https image URL, attempt to save locally
    if url.startswith('http://') or url.startswith('https://'):
        try:
            slug = re.sub(r'[^a-z0-9]+', '_', (item_name or 'dish').lower()).strip('_') or 'dish'
            ext = '.jpg'
            for e in ['.png', '.jpeg', '.webp']:
                if e in url.lower():
                    ext = e
                    break
            filename = f"{slug}{ext}"
            filepath = os.path.join(app.root_path, 'static', 'img', filename)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200 and len(resp.content) > 500:
                with open(filepath, 'wb') as img_f:
                    img_f.write(resp.content)
                return f"/static/img/{filename}"
        except Exception:
            pass
            
    return url

@app.route('/api/upload-item-image', methods=['POST'])
def upload_item_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    filename = secure_filename(file.filename)
    name_slug = request.form.get('name', 'dish')
    clean_slug = re.sub(r'[^a-z0-9]+', '_', name_slug.lower()).strip('_') or 'dish'
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        ext = '.jpg'
    
    saved_filename = f"{clean_slug}_{int(time.time())}{ext}"
    dest_path = os.path.join(app.root_path, 'static', 'img', saved_filename)
    file.save(dest_path)
    
    return jsonify({
        "success": True,
        "image_url": f"/static/img/{saved_filename}"
    }), 200

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json or {}
    name = (data.get('name') or '').strip()
    category = data.get('category')
    price = data.get('price')
    raw_image_url = data.get('image_url', '')
    is_veg = data.get('is_veg', 1)
    
    if not all([name, category, price]):
        return jsonify({"error": "Missing fields"}), 400
        
    image_url = process_item_image(raw_image_url, name)
    
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        INSERT INTO items (name, category, price, image_url, is_veg)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, category, float(price), image_url, int(is_veg)))
    db.commit()
    
    return jsonify({"message": "Item added", "id": cur.lastrowid, "image_url": image_url}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json or {}
    price = data.get('price')
    is_active = data.get('is_active')
    name = data.get('name')
    category = data.get('category')
    raw_image_url = data.get('image_url')
    is_veg = data.get('is_veg')
    
    db = get_db()
    cur = db.cursor()
    
    if price is not None:
        cur.execute('UPDATE items SET price = ? WHERE id = ?', (float(price), item_id))
    if is_active is not None:
        cur.execute('UPDATE items SET is_active = ? WHERE id = ?', (int(is_active), item_id))
    if name is not None:
        cur.execute('UPDATE items SET name = ? WHERE id = ?', (name, item_id))
    if category is not None:
        cur.execute('UPDATE items SET category = ? WHERE id = ?', (category, item_id))
    if raw_image_url is not None:
        cur.execute('SELECT name FROM items WHERE id = ?', (item_id,))
        row = cur.fetchone()
        item_name = name or (row['name'] if row else 'dish')
        image_url = process_item_image(raw_image_url, item_name)
        cur.execute('UPDATE items SET image_url = ? WHERE id = ?', (image_url, item_id))
    if is_veg is not None:
        cur.execute('UPDATE items SET is_veg = ? WHERE id = ?', (int(is_veg), item_id))
        
    db.commit()
    return jsonify({"message": "Item updated"}), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    # Soft delete
    db = get_db()
    db.execute('UPDATE items SET is_active = 0 WHERE id = ?', (item_id,))
    db.commit()
    return jsonify({"message": "Item deleted"}), 200

# --- Staff API Endpoints ---
@app.route('/api/staff', methods=['GET'])
@login_required
def get_staff():
    db = get_db()
    cur = db.execute('''
        SELECT s.*, b.name as branch_name 
        FROM staff s 
        LEFT JOIN branches b ON s.branch_id = b.id 
        ORDER BY s.id DESC
    ''')
    staff_list = [dict(row) for row in cur.fetchall()]
    return jsonify(staff_list)

@app.route('/api/staff', methods=['POST'])
@admin_required
def add_staff():
    data = request.json or {}
    name = (data.get('name') or '').strip()
    role = data.get('role', 'Floor Waiter')
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    shift = data.get('shift', 'Morning (8 AM - 4 PM)')
    branch_id = data.get('branch_id')
    salary = data.get('salary', 25000.0)
    status = data.get('status', 'Active')

    if not name:
        return jsonify({"error": "Staff member name is required"}), 400
    if not phone or not PHONE_REGEX.match(phone):
        return jsonify({"error": "Phone number must be exactly 10 digits"}), 400
    if email and not EMAIL_REGEX.match(email):
        return jsonify({"error": "Please enter a valid email address format"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute('''
        INSERT INTO staff (name, role, phone, email, shift, branch_id, salary, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, role, phone, email, shift, branch_id if branch_id else None, float(salary) if salary else 0.0, status))
    db.commit()
    return jsonify({"message": "Staff member added successfully", "id": cur.lastrowid}), 201

@app.route('/api/staff/<int:staff_id>', methods=['PUT'])
@admin_required
def update_staff(staff_id):
    data = request.json or {}
    db = get_db()
    cur = db.cursor()
    
    if 'name' in data and not str(data['name']).strip():
        return jsonify({"error": "Staff name cannot be empty"}), 400
    if 'phone' in data and not PHONE_REGEX.match(str(data['phone']).strip()):
        return jsonify({"error": "Phone number must be exactly 10 digits"}), 400
    if 'email' in data and data['email'] and not EMAIL_REGEX.match(str(data['email']).strip()):
        return jsonify({"error": "Please enter a valid email address format"}), 400

    fields = ['name', 'role', 'phone', 'email', 'shift', 'branch_id', 'salary', 'status']
    for field in fields:
        if field in data:
            val = data[field]
            if field in ['name', 'phone']:
                val = str(val).strip()
            if field == 'email':
                val = str(val).strip() if val else ''
            if field == 'salary':
                val = float(val) if val is not None else 0.0
            if field == 'branch_id':
                val = int(val) if val else None
            cur.execute(f"UPDATE staff SET {field} = ? WHERE id = ?", (val, staff_id))
            
    db.commit()
    return jsonify({"message": "Staff updated successfully"}), 200

@app.route('/api/staff/<int:staff_id>', methods=['DELETE'])
@admin_required
def delete_staff(staff_id):
    db = get_db()
    db.execute('DELETE FROM staff WHERE id = ?', (staff_id,))
    db.commit()
    return jsonify({"message": "Staff deleted successfully"}), 200

# --- Branches API Endpoints ---
@app.route('/api/branches', methods=['GET'])
@login_required
def get_branches():
    db = get_db()
    cur = db.execute('''
        SELECT b.*, COUNT(s.id) as staff_count 
        FROM branches b 
        LEFT JOIN staff s ON b.id = s.branch_id 
        GROUP BY b.id 
        ORDER BY b.id ASC
    ''')
    branches_list = [dict(row) for row in cur.fetchall()]
    return jsonify(branches_list)

@app.route('/api/branches', methods=['POST'])
@admin_required
def add_branch():
    data = request.json or {}
    name = (data.get('name') or '').strip()
    city = (data.get('city') or '').strip()
    address = (data.get('address') or '').strip()
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    manager_name = (data.get('manager_name') or '').strip()
    tables_count = data.get('tables_count', 20)
    opening_time = data.get('opening_time', '11:00 AM - 11:00 PM')
    status = data.get('status', 'Active')

    if not all([name, city, address]):
        return jsonify({"error": "Branch Name, City, and Address are required"}), 400
    if not phone or not PHONE_REGEX.match(phone):
        return jsonify({"error": "Contact phone must be exactly 10 digits"}), 400
    if email and not EMAIL_REGEX.match(email):
        return jsonify({"error": "Please enter a valid email address format"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute('''
        INSERT INTO branches (name, city, address, phone, email, manager_name, tables_count, opening_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, city, address, phone, email, manager_name, int(tables_count) if tables_count else 20, opening_time, status))
    db.commit()
    return jsonify({"message": "Branch created successfully", "id": cur.lastrowid}), 201

@app.route('/api/branches/<int:branch_id>', methods=['PUT'])
@admin_required
def update_branch(branch_id):
    data = request.json or {}
    db = get_db()
    cur = db.cursor()

    if 'name' in data and not str(data['name']).strip():
        return jsonify({"error": "Branch Name cannot be empty"}), 400
    if 'city' in data and not str(data['city']).strip():
        return jsonify({"error": "City cannot be empty"}), 400
    if 'address' in data and not str(data['address']).strip():
        return jsonify({"error": "Address cannot be empty"}), 400
    if 'phone' in data and not PHONE_REGEX.match(str(data['phone']).strip()):
        return jsonify({"error": "Contact phone must be exactly 10 digits"}), 400
    if 'email' in data and data['email'] and not EMAIL_REGEX.match(str(data['email']).strip()):
        return jsonify({"error": "Please enter a valid email address format"}), 400
    
    fields = ['name', 'city', 'address', 'phone', 'email', 'manager_name', 'tables_count', 'opening_time', 'status']
    for field in fields:
        if field in data:
            val = data[field]
            if field in ['name', 'city', 'address', 'phone']:
                val = str(val).strip()
            if field == 'email':
                val = str(val).strip() if val else ''
            if field == 'tables_count':
                val = int(val) if val is not None else 20
            cur.execute(f"UPDATE branches SET {field} = ? WHERE id = ?", (val, branch_id))
            
    db.commit()
    return jsonify({"message": "Branch updated successfully"}), 200

@app.route('/api/branches/<int:branch_id>', methods=['DELETE'])
@admin_required
def delete_branch(branch_id):
    db = get_db()
    db.execute('DELETE FROM branches WHERE id = ?', (branch_id,))
    db.commit()
    return jsonify({"message": "Branch deleted successfully"}), 200

# --- Download Text Receipt Endpoint ---
@app.route('/receipt/<bill_number>/download-txt')
@login_required
def download_receipt_txt(bill_number):
    db = get_db()
    cur = db.execute('SELECT * FROM orders WHERE bill_number = ?', (bill_number,))
    order = cur.fetchone()
    if not order:
        return "Order not found", 404
        
    cur = db.execute('''
        SELECT oi.*, i.name 
        FROM order_items oi
        JOIN items i ON oi.item_id = i.id
        WHERE oi.order_id = ?
    ''', (order['id'],))
    items = cur.fetchall()
    
    width = 44
    lines = []
    lines.append("*" * width)
    lines.append("MAHARAJA'S KITCHEN".center(width))
    lines.append("Royal Indian Dining Experience".center(width))
    lines.append("Connaught Place, New Delhi - 110001".center(width))
    lines.append("Tel: +91 11 4321 9876 | GSTIN: 07AAAAA0000A1Z5".center(width))
    lines.append("*" * width)
    lines.append(f"Bill No : {order['bill_number']}")
    lines.append(f"Date    : {order['created_at']}")
    order_type_str = order['order_type']
    if order['table_number']:
        order_type_str += f" (Table {order['table_number']})"
    lines.append(f"Order   : {order_type_str}")
    if order['customer_name']:
        lines.append(f"Customer: {order['customer_name']}")
    if order['customer_phone']:
        lines.append(f"Phone   : {order['customer_phone']}")
    lines.append("-" * width)
    lines.append(f"{'Item':<22}{'Qty':>4}  {'Price':>7}  {'Total':>7}")
    lines.append("-" * width)
    for it in items:
        item_name = it['name'][:21]
        qty = it['quantity']
        price = it['price']
        total = qty * price
        lines.append(f"{item_name:<22}{qty:>4}  {price:>7.2f}  {total:>7.2f}")
    lines.append("-" * width)
    lines.append(f"{'Subtotal:':<30}{order['subtotal']:>14.2f}")
    tax_half = (order['tax'] or 0.0) / 2.0
    lines.append(f"{'CGST (2.5%):':<30}{tax_half:>14.2f}")
    lines.append(f"{'SGST (2.5%):':<30}{tax_half:>14.2f}")
    if order['delivery_fee'] and order['delivery_fee'] > 0:
        lines.append(f"{'Delivery Fee:':<30}{order['delivery_fee']:>14.2f}")
    lines.append("=" * width)
    lines.append(f"{'TOTAL AMOUNT (INR):':<28}Rs. {order['total']:>12.2f}")
    lines.append("=" * width)
    lines.append(f"Payment Mode: {order['payment_mode'] or 'Cash'}")
    lines.append(f"Bill Status : {order['status']}")
    lines.append("-" * width)
    lines.append("Thank you for your visit!".center(width))
    lines.append("Please visit Maharaja's Kitchen again!".center(width))
    lines.append("*" * width)
    
    text_content = "\n".join(lines)
    return text_content, 200, {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Disposition': f'attachment; filename="Maharaja_Kitchen_{bill_number}.txt"'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)