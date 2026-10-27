import sqlite3
from werkzeug.security import generate_password_hash
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'food_billing.db')

def setup_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    cur.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0:
        print("Seeding demo users...")
        cur.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                    ('admin', generate_password_hash('admin123'), 'Admin'))
        cur.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                    ('cashier', generate_password_hash('cashier123'), 'Cashier'))
                    
    conn.commit()
    conn.close()
    print("Users setup complete.")

if __name__ == '__main__':
    setup_users()
