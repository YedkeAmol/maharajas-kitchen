import sqlite3
import os

def migrate_orders():
    db_path = os.path.join(os.path.dirname(__file__), 'food_billing.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("PRAGMA table_info(orders)")
    columns = [info[1] for info in cur.fetchall()]
    
    if 'table_number' not in columns:
        cur.execute("ALTER TABLE orders ADD COLUMN table_number TEXT")
    
    if 'customer_phone' not in columns:
        cur.execute("ALTER TABLE orders ADD COLUMN customer_phone TEXT")
        
    if 'payment_mode' not in columns:
        cur.execute("ALTER TABLE orders ADD COLUMN payment_mode TEXT")

    # For phase 3/4 status tracking
    if 'status' not in columns:
        cur.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'Completed'")

    conn.commit()
    conn.close()
    print("Orders table migrated.")

if __name__ == '__main__':
    migrate_orders()
