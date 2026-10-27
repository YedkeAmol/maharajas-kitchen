import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'food_billing.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Check if is_veg exists
    cur.execute("PRAGMA table_info(items)")
    columns = [info[1] for info in cur.fetchall()]
    
    if 'is_veg' not in columns:
        print("Adding is_veg column...")
        cur.execute("ALTER TABLE items ADD COLUMN is_veg BOOLEAN NOT NULL DEFAULT 1")
        
        # Mark sensible items as non-veg
        non_veg_keywords = ['chicken', 'fish', 'mutton', 'non-veg', 'egg']
        
        cur.execute("SELECT id, name FROM items")
        items = cur.fetchall()
        for item in items:
            name_lower = item[1].lower()
            if any(kw in name_lower for kw in non_veg_keywords):
                cur.execute("UPDATE items SET is_veg = 0 WHERE id = ?", (item[0],))
        
        print("is_veg column added successfully.")
    else:
        print("is_veg column already exists.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
