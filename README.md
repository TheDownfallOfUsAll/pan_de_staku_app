# 🥐 Pan de Staku – Enterprise Bakery & Coffee System

**Pan de Staku** is a premium French-inspired bakery and coffee Streamlit application with multi-branch support, secure authentication, inventory management, profit calculation, and GCash-style payment simulation. Perfect for small to medium bakery chains looking for a digital POS and admin dashboard.

---

## 🚀 Features

* Multi-branch support (Manila, Cebu, Davao)
* Customer login and registration with hashed passwords
* Admin login with dashboard analytics
* SQLite database storage for users, orders, and inventory
* Real profit calculation for each sale
* Inventory management (auto deduction after purchase)
* GCash-style payment simulation
* Promo code support and discount calculation
* Animated premium UI
* Exportable sales CSV for business reporting

---

## 🛠 Installation & Setup

### 1️⃣ Install Python (≥ 3.10 recommended)

Download and install Python from [python.org](https://www.python.org/downloads/).

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/pan-de-staku.git
cd pan-de-staku
```

---

### 3️⃣ Install Required Packages

```bash
pip install streamlit pandas
```

> Optional: For a clean environment, use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install streamlit pandas
```

---

### 4️⃣ Run the App Locally

```bash
streamlit run app.py
```

Your browser should open the app at `http://localhost:8501`.

---

### 5️⃣ Default Accounts

* **Admin:**

  * Username: `admin`
  * Password: `admin123`
* **Customer:**

  * Can register a new account using the Register page

---

## 📝 How to Use

1. **Login/Register:** Customers must log in to order. Admins log in to access dashboard.
2. **Select Branch:** Choose your bakery branch (Manila, Cebu, Davao).
3. **Order Items:** Add breads and coffee to your cart.
4. **Checkout:** Pay via GCash simulation. Inventory and profit update automatically.
5. **Admin Dashboard:** Monitor total sales, profits, inventory, and download CSV reports.

---

## 📦 Database Structure (SQLite)

* **users:** Stores admin and customer accounts
* **inventory:** Tracks available stock and cost per item
* **orders:** Logs all completed orders with total sales, profit, and payment method

---

## 🌐 Deployment

You can deploy this app to **Streamlit Cloud**, **Heroku**, or **any VPS** that supports Python:

```bash
git push origin main
```

Streamlit Cloud will automatically detect `app.py` and dependencies.

---

## 💡 Next Steps

* Integrate real payment gateways (GCash, PayMaya, Stripe)
* Add multi-language support
* Implement franchise-wide analytics across branches

---

## ⚡ License

MIT License – Free to use and customize for personal or commercial bakery projects.

Do you want me to do that?
