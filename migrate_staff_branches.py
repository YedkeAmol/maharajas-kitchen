import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'food_billing.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Create branches table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            manager_name TEXT,
            tables_count INTEGER DEFAULT 20,
            opening_time TEXT DEFAULT '11:00 AM - 11:00 PM',
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Create staff table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            shift TEXT DEFAULT 'Morning',
            branch_id INTEGER,
            salary REAL DEFAULT 25000.00,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL
        )
    ''')

    # 3. Check and populate default branches if empty
    cur.execute('SELECT COUNT(*) FROM branches')
    if cur.fetchone()[0] == 0:
        default_branches = [
            (
                "Connaught Place Flagship", 
                "New Delhi", 
                "Block B, Inner Circle, Connaught Place", 
                "+91 11 4321 9876", 
                "cp.delhi@maharajaskitchen.com", 
                "Rajesh Sharma", 
                28, 
                "11:00 AM - 11:30 PM", 
                "Active"
            ),
            (
                "Bandra West Bistro", 
                "Mumbai", 
                "Hill Road, Near Bandra Station, Bandra West", 
                "+91 22 2640 1122", 
                "bandra.mumbai@maharajaskitchen.com", 
                "Priya Nair", 
                22, 
                "12:00 PM - 12:00 AM", 
                "Active"
            ),
            (
                "Indiranagar Central", 
                "Bengaluru", 
                "100 Feet Road, 12th Main, HAL 2nd Stage", 
                "+91 80 4125 3344", 
                "indiranagar@maharajaskitchen.com", 
                "Arvind Swamy", 
                30, 
                "11:30 AM - 11:00 PM", 
                "Active"
            ),
            (
                "Cyber City Express", 
                "Gurugram", 
                "DLF Cyber Hub, Ground Floor, Sector 24", 
                "+91 124 405 8899", 
                "cybercity@maharajaskitchen.com", 
                "Vikram Singh", 
                18, 
                "10:30 AM - 11:00 PM", 
                "Active"
            )
        ]
        cur.executemany('''
            INSERT INTO branches (name, city, address, phone, email, manager_name, tables_count, opening_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_branches)
        print("Inserted default branches.")

    # 4. Check and populate default staff if empty
    cur.execute('SELECT COUNT(*) FROM staff')
    if cur.fetchone()[0] == 0:
        default_staff = [
            (
                "Rajesh Sharma",
                "Branch Manager",
                "9811223344",
                "rajesh.sharma@maharajaskitchen.com",
                "Morning (9 AM - 6 PM)",
                1,
                48000.0,
                "Active"
            ),
            (
                "Priya Nair",
                "Head Cashier",
                "9822334455",
                "priya.nair@maharajaskitchen.com",
                "Morning (8 AM - 4 PM)",
                2,
                32000.0,
                "Active"
            ),
            (
                "Chef Sanjeev Verma",
                "Executive Chef",
                "9811998877",
                "sanjeev.verma@maharajaskitchen.com",
                "Evening (3 PM - 11 PM)",
                1,
                55000.0,
                "Active"
            ),
            (
                "Arvind Swamy",
                "Floor Supervisor",
                "9844556677",
                "arvind.swamy@maharajaskitchen.com",
                "Full Day",
                3,
                34000.0,
                "Active"
            ),
            (
                "Neha Gupta",
                "Billing Cashier",
                "9811554433",
                "neha.gupta@maharajaskitchen.com",
                "Evening (4 PM - 12 AM)",
                1,
                26000.0,
                "Active"
            ),
            (
                "Amit Patel",
                "Senior Waiter",
                "9877112233",
                "amit.patel@maharajaskitchen.com",
                "Evening (4 PM - 12 AM)",
                4,
                22000.0,
                "Active"
            ),
            (
                "Sunil Yadav",
                "Delivery Coordinator",
                "9899332211",
                "sunil.yadav@maharajaskitchen.com",
                "Morning (10 AM - 7 PM)",
                4,
                20000.0,
                "Active"
            )
        ]
        cur.executemany('''
            INSERT INTO staff (name, role, phone, email, shift, branch_id, salary, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_staff)
        print("Inserted default staff.")

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    migrate()
