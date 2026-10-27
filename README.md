# Maharaja's Kitchen - Restaurant Billing System (POS)

A beautiful, responsive, and robust Point of Sale (POS) & Billing System built as a graduation showcase project for a hypothetical Indian restaurant: **Maharaja's Kitchen**.

## Features

*   **Offline-First & Local:** Entirely functional without an internet connection. Data is stored safely in a local SQLite database, and all external libraries (like Chart.js) are bundled locally.
*   **Role-Based Access Control:** 
    *   **Admin:** Full access to Dashboard, Menu Management, Staff, Branches, and History.
    *   **Cashier:** Secure restricted access to only the Billing System and Order History.
*   **Smart Billing System:**
    *   Dynamic Dine-in table selection (with visual occupation indicators).
    *   Delivery order management with customer details capturing.
    *   Cash calculator built into the payment modal to easily calculate change to return.
*   **Printable Receipts & QR Payments:** Auto-generates fully formatted 80mm printable thermal receipts, complete with dynamically generated UPI QR codes for seamless payments.
*   **Beautiful Dashboard:** Interactive daily, weekly, and monthly sales trend charts using Chart.js.
*   **Delivery Tracking:** Easily track delivery status (Preparing -> Out for Delivery -> Delivered) from the History panel.
*   **Responsive UI:** Carefully designed UI that gracefully scales from standard laptops (1366x768) down to tablet screens (768px width) and mobile.

## Tech Stack

*   **Backend:** Python 3, Flask framework.
*   **Database:** SQLite (`food_billing.db`).
*   **Frontend:** HTML5, JavaScript, Tailwind CSS (via CDN fallback or custom styles).
*   **Key Libraries:** `qrcode[pil]` (Receipt QR Generation), `werkzeug.security` (Auth).

## Setup Instructions

1.  **Clone or Extract the Project:** 
    Open a terminal and navigate to the project directory (e.g. `C:\Project Sem 5`).
2.  **Install Requirements:**
    Make sure you have Python installed, then run:
    ```bash
    pip install flask qrcode[pil] pillow werkzeug
    ```
3.  **Run the App:**
    ```bash
    python app.py
    ```
4.  **Access the System:**
    Open your web browser and go to: `http://127.0.0.1:5001`

## Demo Login Credentials

You can log in to the system using the pre-seeded demo accounts:

*   **Admin Access:**
    *   Username: `admin`
    *   Password: `admin123`
*   **Cashier Access:**
    *   Username: `cashier`
    *   Password: `cashier123`

## Populating Demo Data

To see the Dashboard charts and Order History in action, a seed script is provided that generates 60 realistic past orders across the last 7 days.
**To run it, stop the server, and execute:**
```bash
python seed_demo_data.py
```
*(Warning: This will clear all existing orders in the database before generating new ones!)*

## Screenshots

*(Add your project screenshots here before submitting!)*

- **Login Screen:** `[Insert screenshot of login.html]`
- **Billing POS System:** `[Insert screenshot of index.html with cart]`
- **Dashboard & Charts:** `[Insert screenshot of dashboard.html]`
- **Printable Receipt:** `[Insert screenshot of receipt.html print view]`

---
*Created as a Graduation Showcase Project.*
