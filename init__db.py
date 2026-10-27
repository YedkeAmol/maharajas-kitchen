import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'food_billing.db')
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    
    cur.execute('DROP TABLE IF EXISTS order_items')
    cur.execute('DROP TABLE IF EXISTS orders')
    cur.execute('DROP TABLE IF EXISTS items')
    
    # Items Table
    cur.execute('''
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT,
            is_active BOOLEAN NOT NULL DEFAULT 1
        )
    ''')

    # Orders Table - added order_type and delivery_fee
    cur.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_number TEXT UNIQUE NOT NULL,
            subtotal REAL NOT NULL,
            tax REAL NOT NULL,
            delivery_fee REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL,
            order_type TEXT NOT NULL DEFAULT 'Dine-In',
            customer_name TEXT,
            customer_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Order Items Table
    cur.execute('''
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
    ''')

    dummy_items = [
        # Thalis
        ('Maharaja Thali', 'Thalis', 999.00, 'img/downloaded/maharaja_thali.jpg'),
        ('Non-Veg Royal Thali', 'Thalis', 1299.00, 'img/downloaded/non-veg_royal_thali.jpg'),
        ('Gujarati Thali', 'Thalis', 350.00, 'img/downloaded/gujarati_thali.jpg'),
        ('Punjabi Thali', 'Thalis', 380.00, 'img/downloaded/punjabi_thali.jpg'),
        ('Bengali Fish Thali', 'Thalis', 450.00, 'img/downloaded/bengali_fish_thali.jpg'),
        
        # Starters
        ('Samosa (2 pcs)', 'Starters', 50.00, 'img/downloaded/samosa_2_pcs.jpg'),
        ('Paneer Tikka', 'Starters', 220.00, 'img/downloaded/paneer_tikka.jpg'),
        ('Chicken Tikka', 'Starters', 280.00, 'img/downloaded/chicken_tikka.jpg'),
        ('Mutton Seekh Kebab', 'Starters', 350.00, 'img/downloaded/mutton_seekh_kebab.jpg'),
        ('Chicken 65', 'Starters', 260.00, 'img/indian_starters.jpg'),
        ('Prawn Koliwada', 'Starters', 400.00, 'img/indian_starters.jpg'),
        
        # Mains (Veg)
        ('Palak Paneer', 'Mains', 240.00, 'img/downloaded/palak_paneer.jpg'),
        ('Dal Makhani', 'Mains', 210.00, 'img/downloaded/dal_makhani.jpg'),
        ('Paneer Butter Masala', 'Mains', 250.00, 'img/downloaded/paneer_butter_masala.jpg'),
        
        # Mains (Non-Veg)
        ('Butter Chicken', 'Mains', 350.00, 'img/downloaded/butter_chicken.jpg'),
        ('Chicken Biryani', 'Mains', 280.00, 'img/downloaded/chicken_biryani.jpg'),
        ('Mutton Biryani', 'Mains', 420.00, 'img/downloaded/mutton_biryani.jpg'),
        ('Mutton Rogan Josh', 'Mains', 450.00, 'img/downloaded/mutton_rogan_josh.jpg'),
        ('Goan Fish Curry', 'Mains', 380.00, 'img/butter_chicken.jpg'),
        ('Kadai Chicken', 'Mains', 320.00, 'img/butter_chicken.jpg'),
        ('Prawn Masala', 'Mains', 450.00, 'img/butter_chicken.jpg'),
        ('Chicken Kolhapuri', 'Mains', 330.00, 'img/butter_chicken.jpg'),
        
        # South Indian Specials
        ('Masala Dosa', 'South Indian', 120.00, 'img/downloaded/masala_dosa.jpg'),
        ('Idli Sambar', 'South Indian', 80.00, 'img/downloaded/idli_sambar.jpg'),
        ('Chicken Chettinad', 'South Indian', 340.00, 'img/downloaded/chicken_chettinad.jpg'),
        
        # Breads
        ('Garlic Naan', 'Breads', 60.00, 'img/downloaded/garlic_naan.jpg'),
        ('Butter Naan', 'Breads', 50.00, 'img/downloaded/butter_naan.jpg'),
        ('Tandoori Roti', 'Breads', 30.00, 'img/downloaded/tandoori_roti.jpg'),
        
        # Desserts
        ('Gulab Jamun (2 pcs)', 'Desserts', 80.00, 'img/downloaded/gulab_jamun_2_pcs.jpg'),
        ('Rasmalai (2 pcs)', 'Desserts', 110.00, 'img/downloaded/rasmalai_2_pcs.jpg'),
        
        # Drinks
        ('Mango Lassi', 'Drinks', 90.00, 'img/mango_lassi.jpg'),
        ('Masala Chai', 'Drinks', 40.00, 'img/indian_drinks.jpg')
    ]
    cur.executemany("INSERT INTO items (name, category, price, image_url) VALUES (?, ?, ?, ?)", dummy_items)
    print(f"Inserted {len(dummy_items)} Indian dummy items.")
    
    connection.commit()
    connection.close()
    print("Database initialized successfully at:", db_path)

if __name__ == '__main__':
    init_db()