import sqlite3
import random
import time
import uuid
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'food_billing.db')

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Cleaning existing orders...")
    cur.execute("DELETE FROM order_items")
    cur.execute("DELETE FROM orders")
    conn.commit()
    
    cur.execute("SELECT id, price FROM items WHERE is_active = 1")
    items = cur.fetchall()
    if not items:
        print("No items found. Please add items before seeding.")
        return

    print("Seeding ~60 past orders...")
    
    # 7 days ago to now
    now = time.time()
    seven_days_ago = now - (7 * 24 * 60 * 60)
    
    names = ["Rahul Sharma", "Priya Patel", "Amit Singh", "Neha Gupta", "Vikram Verma", "Anjali Desai", "Rajesh Kumar"]
    addresses = ["101 Main St", "202 Elm St", "303 Oak St", "404 Pine St", "505 Maple St"]
    
    for i in range(60):
        # Random timestamp
        order_time = random.uniform(seven_days_ago, now)
        order_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(order_time))
        
        order_type = random.choice(["Dine-In", "Delivery"])
        payment_mode = random.choice(["Cash", "Card", "UPI"])
        status = "Completed"
        
        customer_name = ""
        customer_address = ""
        customer_phone = ""
        table_number = ""
        delivery_fee = 0.0
        
        if order_type == "Delivery":
            customer_name = random.choice(names)
            customer_address = random.choice(addresses)
            customer_phone = f"98765{random.randint(10000, 99999)}"
            delivery_fee = 40.0
            status = random.choice(["Delivered", "Delivered", "Delivered", "Out for Delivery"])
        else:
            table_number = f"T{random.randint(1, 10)}"
            
        bill_number = f"BILL-{int(order_time)}-{uuid.uuid4().hex[:4]}"
        
        # Pick 1 to 4 random items
        order_items = random.sample(items, k=random.randint(1, min(4, len(items))))
        
        subtotal = 0.0
        selected_items = []
        for itm in order_items:
            qty = random.randint(1, 3)
            price = itm[1]
            subtotal += price * qty
            selected_items.append((itm[0], qty, price))
            
        tax = subtotal * 0.05
        total = subtotal + tax + delivery_fee
        
        # Insert Order
        cur.execute('''
            INSERT INTO orders (bill_number, subtotal, tax, delivery_fee, total, order_type, customer_name, customer_address, customer_phone, table_number, payment_mode, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bill_number, subtotal, tax, delivery_fee, total, order_type, customer_name, customer_address, customer_phone, table_number, payment_mode, status, order_time_str))
        
        order_id = cur.lastrowid
        
        # Insert Items
        for sitm in selected_items:
            cur.execute('''
                INSERT INTO order_items (order_id, item_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, sitm[0], sitm[1], sitm[2]))

    conn.commit()
    conn.close()
    print("Seed complete! Added 60 orders.")

if __name__ == '__main__':
    seed_data()
