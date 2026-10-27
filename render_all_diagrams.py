import os
import requests

DIAGRAMS_DIR = r"C:\Project Sem 5\diagrams"
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

diagrams = {
    "diag_01_class": """@startuml
skinparam classAttributeIconSize 0
skinparam roundcorner 8
skinparam shadowing false
skinparam class {
    BackgroundColor white
    ArrowColor #E8590C
    BorderColor #E8590C
}

class User {
    +id: Integer [PK]
    +username: String [Unique]
    +password_hash: String
    +role: String <<Admin | Cashier>>
    --
    +check_password(password: String): Boolean
}

class Item {
    +id: Integer [PK]
    +name: String
    +category: String <<Mains|Starters|Thalis|Breads|Desserts|Drinks>>
    +price: Float
    +image_url: String
    +is_active: Boolean
    +is_veg: Boolean
    --
    +get_display_image(): String
}

class Order {
    +id: Integer [PK]
    +bill_number: String [Unique]
    +order_date: Date
    +order_type: String <<Dine-In | Delivery>>
    +table_number: Integer
    +customer_name: String
    +customer_phone: String(10)
    +customer_address: Text
    +payment_mode: String <<UPI | Card | Cash>>
    +subtotal: Float
    +tax: Float
    +delivery_fee: Float
    +total_amount: Float
    +cash_received: Float
    +cash_change: Float
    +status: String <<Completed | Void>>
    +notes: Text
    +created_at: DateTime
    --
    +calculate_totals(): Void
}

class OrderItem {
    +id: Integer [PK]
    +order_id: Integer [FK]
    +item_id: Integer [FK]
    +quantity: Integer
    +price_per_unit: Float
    +total_price: Float
}

class Branch {
    +id: Integer [PK]
    +name: String
    +city: String
    +address: Text
    +phone: String(10)
    +email: String
    +manager_name: String
    +tables_count: Integer
    +opening_time: String
    +status: String <<Active | Renovating | Opening Soon>>
}

class Staff {
    +id: Integer [PK]
    +name: String
    +role: String <<Manager | Cashier | Chef | Supervisor | Waiter>>
    +phone: String(10)
    +email: String
    +shift: String <<Morning | Evening | Full Day>>
    +branch_id: Integer [FK]
    +salary: Float
    +status: String <<Active | On Leave | Inactive>>
}

Order "1" *-- "1..*" OrderItem : contains >
Item "1" -- "0..*" OrderItem : referenced in >
Branch "1" o-- "0..*" Staff : employs >
User "1" ..> "0..*" Order : processes >
@enduml""",

    "diag_02_object": """@startuml
skinparam objectAttributeIconSize 0
skinparam roundcorner 8
skinparam shadowing false
skinparam object {
    BackgroundColor white
    ArrowColor #E8590C
    BorderColor #E8590C
}

object "adminUser : User" as u1 {
    id = 1
    username = "admin"
    role = "Admin"
}

object "connaughtBranch : Branch" as b1 {
    id = 1
    name = "Connaught Place Flagship"
    city = "New Delhi"
    phone = "9811432198"
    tables_count = 20
    status = "Active"
}

object "cashierStaff : Staff" as s1 {
    id = 2
    name = "Priya Nair"
    role = "Billing Cashier"
    phone = "9822334455"
    shift = "Morning (8 AM - 4 PM)"
    status = "Active"
}

object "currentOrder : Order" as o1 {
    id = 101
    bill_number = "BILL-20261027-0101"
    order_type = "Dine-In"
    table_number = 4
    customer_name = "Amit Kumar"
    customer_phone = "9876543210"
    payment_mode = "UPI"
    subtotal = 780.00
    tax = 39.00
    total_amount = 819.00
    status = "Completed"
}

object "lineItem1 : OrderItem" as oi1 {
    quantity = 1
    price_per_unit = 500.00
    total_price = 500.00
}

object "lineItem2 : OrderItem" as oi2 {
    quantity = 4
    price_per_unit = 70.00
    total_price = 280.00
}

object "item1 : Item" as i1 {
    id = 33
    name = "Murg musallam"
    category = "Mains"
    price = 500.00
    is_veg = False
}

object "item2 : Item" as i2 {
    id = 26
    name = "Garlic Naan"
    category = "Breads"
    price = 70.00
    is_veg = True
}

s1 -- b1 : allocated to
u1 .. o1 : authenticated cashier
o1 *-- oi1
o1 *-- oi2
oi1 --> i1 : references
oi2 --> i2 : references
@enduml""",

    "diag_03_er": """@startuml
skinparam linetype ortho
skinparam roundcorner 8
skinparam shadowing false
skinparam entity {
    BackgroundColor white
    BorderColor #E8590C
    ArrowColor #E8590C
}

entity "users" as users {
    * id : INTEGER [PK]
    --
    * username : TEXT [UNIQUE]
    * password_hash : TEXT
    * role : TEXT
}

entity "items" as items {
    * id : INTEGER [PK]
    --
    * name : TEXT
    * category : TEXT
    * price : REAL
    image_url : TEXT
    is_active : BOOLEAN
    is_veg : BOOLEAN
}

entity "orders" as orders {
    * id : INTEGER [PK]
    --
    * bill_number : TEXT [UNIQUE]
    * order_date : DATE
    * order_type : TEXT
    table_number : INTEGER
    customer_name : TEXT
    customer_phone : TEXT(10)
    customer_address : TEXT
    * payment_mode : TEXT
    * subtotal : REAL
    * tax : REAL
    delivery_fee : REAL
    * total_amount : REAL
    cash_received : REAL
    cash_change : REAL
    * status : TEXT
    notes : TEXT
    created_at : TIMESTAMP
}

entity "order_items" as order_items {
    * id : INTEGER [PK]
    --
    * order_id : INTEGER [FK]
    * item_id : INTEGER [FK]
    * quantity : INTEGER
    * price_per_unit : REAL
    * total_price : REAL
}

entity "branches" as branches {
    * id : INTEGER [PK]
    --
    * name : TEXT
    * city : TEXT
    * address : TEXT
    * phone : TEXT(10)
    email : TEXT
    manager_name : TEXT
    tables_count : INTEGER
    opening_time : TEXT
    status : TEXT
}

entity "staff" as staff {
    * id : INTEGER [PK]
    --
    * name : TEXT
    * role : TEXT
    * phone : TEXT(10)
    email : TEXT
    shift : TEXT
    branch_id : INTEGER [FK]
    salary : REAL
    status : TEXT
}

orders ||--|{ order_items : "contains"
items ||--o{ order_items : "included in"
branches ||--o{ staff : "employs"
users ||--o{ orders : "audits / creates"
@enduml""",

    "diag_04_usecase": """@startuml
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam actorStyle awesome

actor "Cashier" as cashier
actor "Admin" as admin
actor "Customer" as customer

rectangle "Maharaja's Kitchen POS System" {
    usecase "Login & Authenticate" as UC_Login
    usecase "Create Order (Dine-In / Delivery)" as UC_Order
    usecase "Select Table / Delivery Info" as UC_Table
    usecase "Process Payment (UPI / Card / Cash)" as UC_Pay
    usecase "Print & Download PDF Receipt" as UC_Receipt
    usecase "View Billing History & Void Bill" as UC_History
    usecase "Manage Menu Items (CRUD & Photos)" as UC_Menu
    usecase "Manage Staff Members" as UC_Staff
    usecase "Manage Restaurant Branches" as UC_Branches
    usecase "View Sales Analytics & Trends" as UC_Analytics
}

cashier --> UC_Login
cashier --> UC_Order
cashier --> UC_Table
cashier --> UC_Pay
cashier --> UC_Receipt
cashier --> UC_History

admin --> UC_Login
admin --> UC_Menu
admin --> UC_Staff
admin --> UC_Branches
admin --> UC_Analytics
admin --> UC_History

UC_Order ..> UC_Table : <<include>>
UC_Order ..> UC_Pay : <<include>>
UC_Pay ..> UC_Receipt : <<include>>

customer -- UC_Receipt : receives
@enduml""",

    "diag_05_activity": """@startuml
skinparam shadowing false
skinparam startColor #E8590C
skinparam endColor #E8590C

start
:Cashier logs into POS system;
:Select Category & Click Dish Cards;
:Items added to live Cart;
:Select Order Type (Dine-In or Delivery);

if (Order Type?) then (Dine-In)
    :Select Table Number (1 - 20);
    :Enter Optional Customer Phone (10 digits);
else (Delivery)
    :Enter Customer Name;
    :Enter Customer 10-Digit Phone;
    :Enter Full Delivery Address;
    :Add Delivery Surcharge (₹40.00);
endif

:Click "Proceed to Pay";
:Choose Payment Mode;

if (Payment Mode?) then (UPI)
    :Scan Dynamic QR / Confirm UPI VPA;
elseif (Credit / Debit Card)
    :Swipe / Tap on POS Terminal;
else (Cash)
    :Input Cash Received;
    :System calculates Change to Return;
endif

:System writes Order & OrderItems to SQLite DB;
:Generate Unique Bill Number;
:Display Success Modal;

fork
    :Open Native Browser Print Dialog;
fork again
    :Generate Client PDF via html2pdf;
fork again
    :Update Sales Analytics & Daily KPI Stats;
end fork

stop
@enduml""",

    "diag_06_statemachine": """@startuml
skinparam state {
    BackgroundColor white
    BorderColor #E8590C
    ArrowColor #E8590C
}
skinparam shadowing false

[*] --> CartDraft : Cashier selects items

state CartDraft {
    [*] --> ModifyingCart
    ModifyingCart --> ItemAdded : Add dish
    ItemAdded --> ModifyingCart
    ModifyingCart --> ItemRemoved : Remove dish
    ItemRemoved --> ModifyingCart
    ModifyingCart --> CartCleared : Clear order
}

CartDraft --> TableAssigned : Choose Dine-In table
CartDraft --> DeliveryDetailsEntered : Enter Delivery address

state OrderReadyForPayment {
    TableAssigned --> PaymentPending
    DeliveryDetailsEntered --> PaymentPending
}

PaymentPending --> ProcessingUPI : Select UPI
PaymentPending --> ProcessingCard : Select Card
PaymentPending --> ProcessingCash : Select Cash

ProcessingUPI --> Paid : UPI Confirmation Received
ProcessingCard --> Paid : Card Terminal Approved
ProcessingCash --> Paid : Exact / Sufficient Cash Tendered

state Paid {
    [*] --> BillGenerated
    BillGenerated --> ReceiptPrinted
    ReceiptPrinted --> PDFDownloaded
}

Paid --> Completed : Order Fulfilled & Closed
Paid --> Voided : Admin Cancel / Refund

Completed --> [*]
Voided --> [*]
@enduml""",

    "diag_07_component": """@startuml
skinparam componentStyle uml2
skinparam shadowing false
skinparam component {
    BackgroundColor white
    BorderColor #E8590C
    ArrowColor #E8590C
}

package "Presentation Tier (Client Browser)" {
    [Tailwind CSS & Google Fonts] as UI_Style
    [Chart.js Visualization Engine] as UI_Chart
    [html2pdf.js Client Generator] as UI_PDF
    [POS Controller (main.js)] as UI_POS
}

package "Application Tier (Flask Web Server - Port 5001)" {
    [Route Controller (app.py)] as App_Core
    [Auth & Session Manager] as App_Auth
    [Order Processing Engine] as App_Order
    [Image Processing & Auto-Downloader] as App_Img
    [Staff & Branch API Controller] as App_Admin
}

package "Data Tier (Local Storage)" {
    database "SQLite 3 Database (food_billing.db)" as DB {
        [users table]
        [items table]
        [orders & order_items]
        [staff table]
        [branches table]
    }
    folder "Static Assets (/static/img/)" as FileStore {
        [Dish JPG / PNG Photos]
        [Logo & QR Codes]
    }
}

UI_POS --> App_Core : HTTP REST API (JSON)
UI_Chart <-- App_Core : /api/dashboard/charts
UI_PDF <-- App_Core : /receipt/<bill_no>

App_Core --> App_Auth : verifies session
App_Core --> App_Order : calculates tax & totals
App_Core --> App_Img : cleans & stores photos
App_Core --> App_Admin : validates phone & email

App_Order --> DB : SQL Queries
App_Admin --> DB : CRUD Operations
App_Img --> FileStore : file.save()
@enduml""",

    "diag_08_deployment": """@startuml
skinparam node {
    BackgroundColor white
    BorderColor #E8590C
    ArrowColor #E8590C
}
skinparam shadowing false

node "Client Tier\n(Smartphone / Tablet / PC)" as ClientNode {
    artifact "Web Browser\n(Chrome / Safari / Edge)" as Browser
}

cloud "Public Internet\n(Cloudflare Edge Network)" as CloudEdge {
    [Encrypted HTTPS Reverse Proxy] as CF_Edge
}

node "Local Host Machine\n(Windows 11 / Project PC)" as HostMachine {
    node "Cloudflare Daemon" {
        [cloudflared.exe (tunnel)] as CFTunnel
    }

    node "Python WSGI Runtime (Python 3.14)" {
        [Flask Application Server (port 5001)] as FlaskServer
    }

    node "Persistent Storage" {
        database "SQLite Database\n(food_billing.db)" as SQLiteDB
        folder "Local Disk (/static/img/)" as DiskAssets
    }
}

Browser --> CF_Edge : HTTPS (port 443)
CF_Edge --> CFTunnel : Secure Tunnel Connection
CFTunnel --> FlaskServer : Local Proxy (http://127.0.0.1:5001)
FlaskServer --> SQLiteDB : SQLite File I/O
FlaskServer --> DiskAssets : Media I/O
@enduml""",

    "diag_09_package": """@startuml
skinparam package {
    BackgroundColor white
    BorderColor #E8590C
    ArrowColor #E8590C
}
skinparam shadowing false

package "Project Root (C:\\Project Sem 5)" {
    
    package "Configuration & Runners" {
        [app.py]
        [requirements.txt]
        [Procfile]
        [render.yaml]
        [start_live.bat]
    }

    package "templates/" {
        [base.html]
        [login.html]
        [index.html (POS Billing)]
        [admin.html (Menu Management)]
        [staff.html (Staff Management)]
        [branches.html (Branch Management)]
        [dashboard.html (Analytics)]
        [history.html (Orders)]
        [receipt.html (Bill Print)]
    }

    package "static/" {
        package "css/" {
            [style.css]
        }
        package "js/" {
            [main.js]
            [chart.umd.js]
            [html2pdf.bundle.min.js]
        }
        package "img/" {
            [Dish Photos (*.jpg)]
            [logo.jpg]
            [live_qr.png]
        }
    }

    package "Database" {
        [food_billing.db]
    }
}

[app.py] ..> [templates/] : renders
[app.py] ..> [static/] : serves
[app.py] ..> [Database] : reads & writes
@enduml""",

    "diag_10_dfd_l0": """@startuml
skinparam monochrome false
skinparam shadowing false
skinparam roundcorner 10
skinparam defaultTextAlignment center

agent "Admin" as Admin
agent "Cashier" as Cashier
agent "Customer" as Customer

rectangle "0.0\nMaharaja's Kitchen\nRestaurant Billing & POS\nManagement System" as System #FFF1E6

Admin --> System : Login Credentials\nMenu Items & Photos\nStaff & Branch Details
System --> Admin : Analytics Reports & Charts\nAudit & Order History\nValidation Status

Cashier --> System : Login Credentials\nOrder Selections & Cart\nPayment Details\nTable / Delivery Info
System --> Cashier : Total Bill Calculation\nChange Amount\nBill Receipt Print / PDF

System --> Customer : Printed Thermal Receipt\nDownloadable PDF Bill\nChange Cash Return
@enduml""",

    "diag_11_dfd_l1": """@startuml
skinparam shadowing false
skinparam rectangleRoundCorner 10

actor "Cashier / Admin" as User

rectangle "1.0 User Authentication" as P1
rectangle "2.0 Menu Management" as P2
rectangle "3.0 Order & Cart Calculation" as P3
rectangle "4.0 Payment & Receipt Generation" as P4
rectangle "5.0 Staff & Branch Management" as P5
rectangle "6.0 Sales Analytics & Reporting" as P6

database "D1: Users Store" as D1
database "D2: Menu Items Store" as D2
database "D3: Orders & Line Items" as D3
database "D4: Staff & Branches Store" as D4

User --> P1 : Login credentials
P1 --> D1 : Verify password hash
D1 --> P1 : User role & session token
P1 --> User : Redirect to POS / Admin

User --> P2 : Add / Edit dish & photo
P2 --> D2 : Save dish & price
D2 --> P3 : Menu items catalog

User --> P3 : Select items, table / delivery
P3 --> P4 : Verified order totals & tax

User --> P4 : Tender payment (UPI/Card/Cash)
P4 --> D3 : Record completed order
P4 --> User : Generate Print & PDF receipt

User --> P5 : Manage staff & branches
P5 --> D4 : Store staff & branch records

D3 --> P6 : Historical sales data
P6 --> User : Render Monthly Sales & Payment Doughnut Charts
@enduml""",

    "diag_12_sequence": """@startuml
autonumber
skinparam shadowing false
skinparam sequence {
    ParticipantBorderColor #E8590C
    ParticipantBackgroundColor white
    LifeLineBorderColor #E8590C
    ArrowColor #E8590C
}

actor "Cashier" as Cashier
participant "POS UI (Browser)" as Browser
participant "Flask API (app.py)" as Server
database "SQLite DB" as DB
participant "Printer / PDF Engine" as Printer

Cashier -> Browser : Click dish card (e.g. "Murg musallam")
Browser -> Browser : updateCart() & calculate Subtotal + 5% GST
Cashier -> Browser : Click "Proceed to Pay"
Browser -> Browser : Open Checkout Modal (Dine-In or Delivery)

alt Order Type: Delivery
    Cashier -> Browser : Enter Name, 10-digit Phone, Address
    Browser -> Browser : validateCheckoutPhone() (enforces 10 digits)
else Order Type: Dine-In
    Cashier -> Browser : Select Dining Table Number (1 - 20)
end

Cashier -> Browser : Select Payment Mode (e.g. Cash)
Browser -> Browser : calculateChange(Cash Received - Total)
Cashier -> Browser : Click "Complete Order"

Browser -> Server : POST /api/orders (JSON payload)
activate Server

Server -> Server : Validate items, tax, and totals
Server -> DB : INSERT INTO orders (...)
Server -> DB : INSERT INTO order_items (...)
DB --> Server : Return new order_id & bill_number
Server --> Browser : HTTP 201 Created {"success": true, "bill_number": "..."}
deactivate Server

Browser -> Browser : Show Payment Success Modal
Browser -> Printer : Trigger window.print() / html2pdf.save()
Printer --> Cashier : Printed Tax Invoice Slip (with GST breakdown)
@enduml"""
}

for name, code in diagrams.items():
    png_path = os.path.join(DIAGRAMS_DIR, f"{name}.png")
    print(f"Rendering {name} via Kroki API...")
    try:
        resp = requests.post(
            "https://kroki.io/plantuml/png",
            headers={"Content-Type": "text/plain; charset=utf-8"},
            data=code.encode('utf-8'),
            timeout=15
        )
        if resp.status_code == 200:
            with open(png_path, "wb") as f:
                f.write(resp.content)
            print(f"  ✓ Saved {name}.png ({len(resp.content)} bytes)")
        else:
            print(f"  ✗ Failed {name}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  ✗ Error rendering {name}: {e}")

print(f"\nAll diagrams processed in: {DIAGRAMS_DIR}")
