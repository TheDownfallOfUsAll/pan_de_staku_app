import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Pan de Staku", page_icon="🥐", layout="wide")

# ==========================================================
# DATABASE SETUP
# ==========================================================
conn = sqlite3.connect("pan_de_staku.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    item TEXT PRIMARY KEY,
    stock INTEGER,
    cost REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    branch TEXT,
    total REAL,
    profit REAL,
    payment TEXT,
    timestamp TEXT
)
""")

conn.commit()

# ==========================================================
# PASSWORD HASHING
# ==========================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create default admin
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute(
        "INSERT INTO users (username,password,role) VALUES (?,?,?)",
        ("admin", hash_password("admin123"), "admin")
    )
    conn.commit()

# ==========================================================
# SESSION STATE
# ==========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "user" not in st.session_state:
    st.session_state.user = None

if "branch" not in st.session_state:
    st.session_state.branch = "Manila"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ==========================================================
# UI STYLE
# ==========================================================
st.markdown("""
<style>

@keyframes fadeIn {
    from {opacity:0; transform: translateY(20px);}
    to {opacity:1; transform: translateY(0);}
}

.stApp {
    animation: fadeIn 0.8s ease-in-out;
    background:
        radial-gradient(circle at 20% 20%, rgba(255,224,178,0.3), transparent 40%),
        linear-gradient(135deg,#3E2723,#6D4C41,#D7A86E);
}

/* Sidebar Gradient */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#3E2723,#5D4037,#8D6E63);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

h1,h2,h3{
    color:#FFF3E0;
}

p{
    color:#FFE0B2;
}

.metric-card{
    background:rgba(255,255,255,0.95);
    padding:25px;
    border-radius:18px;
    box-shadow:0 8px 25px rgba(0,0,0,0.25);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# MENU DATA
# ==========================================================
bread_menu = {
    "🥐 Croissant":120,
    "🍞 Baguette":100,
    "🥖 Brioche":150,
    "🥯 Pain au Chocolat":140,
    "🥪 Fougasse":130,
    "🍞 Sourdough":160,
    "🥐 Danish":135
}

coffee_menu = {
    "☕ Espresso":90,
    "☕ Americano":100,
    "☕ Cappuccino":120,
    "☕ Latte":130,
    "☕ Mocha":140,
    "☕ Macchiato":115,
    "☕ Flat White":125
}

all_menu = {**bread_menu, **coffee_menu}

# Initialize inventory
for item, price in all_menu.items():
    cursor.execute(
        "INSERT OR IGNORE INTO inventory VALUES (?,?,?)",
        (item,50,price*0.6)
    )
conn.commit()

# ==========================================================
# DOUGHBOT CHATBOT
# ==========================================================
def doughbot_response(prompt):

    p = prompt.lower()

    if any(x in p for x in ["hi","hello","hey"]):
        return "Bonjour! I'm **DoughBot 🤖**, your Pan de Staku assistant."

    elif "menu" in p:
        return "Our menu includes:\n\n" + ", ".join(all_menu.keys())

    elif "bread" in p:
        return "Our breads:\n\n" + ", ".join(bread_menu.keys())

    elif "coffee" in p:
        return "Coffee selection:\n\n" + ", ".join(coffee_menu.keys())

    elif "recommend" in p:
        return "I recommend **🥐 Croissant with ☕ Latte**."

    elif "delivery" in p:
        return "Delivery fee starts at **₱40 🚚**."

    elif "branch" in p:
        return "Branches available in **Manila, Cebu, and Davao**."

    elif "price" in p:
        return "Prices range between **₱90 – ₱160**."

    elif "order" in p:
        return "Go to **Order page → Add items → Checkout in Cart**."

    else:
        return """
I'm **DoughBot 🤖**

Ask me about:

• Menu  
• Coffee  
• Bread  
• Delivery  
• Branch locations  
• Recommendations
"""

# ==========================================================
# SIDEBAR
# ==========================================================
cart_count = sum(qty for _,qty,_ in st.session_state.cart)

menu = st.sidebar.radio(
    f"Navigation 🛒({cart_count})",
    [
        "Home",
        "Login",
        "Register",
        "Branch",
        "Menu List",
        "Order",
        "Cart",
        "DoughBot Chat",
        "Admin Dashboard"
    ]
)

# ==========================================================
# HOME
# ==========================================================
if menu == "Home":

    st.title("🥐 Pan de Staku")
    st.subheader("Enterprise French Bakery & Coffee Management System")

    st.write("Welcome to Pan de Staku — a premium bakery platform with AI assistant, multi-branch ordering, and digital payments.")

# ==========================================================
# LOGIN
# ==========================================================
elif menu == "Login":

    st.header("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and user[2] == hash_password(password):
            st.session_state.user = user[1]
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")

# ==========================================================
# REGISTER
# ==========================================================
elif menu == "Register":

    st.header("📝 Register")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password",type="password")

    if st.button("Create Account"):

        try:
            cursor.execute(
                "INSERT INTO users (username,password,role) VALUES (?,?,?)",
                (new_user,hash_password(new_pass),"customer")
            )
            conn.commit()
            st.success("Account Created")

        except:
            st.error("Username already exists")

# ==========================================================
# BRANCH
# ==========================================================
elif menu == "Branch":

    branches = ["Manila","Cebu","Davao"]

    branch = st.selectbox("Select Branch",branches)

    st.session_state.branch = branch

    st.success(f"Branch set to {branch}")

# ==========================================================
# MENU LIST
# ==========================================================
elif menu == "Menu List":

    st.header("📋 Full Menu")

    df = pd.DataFrame(list(all_menu.items()),columns=["Item","Price"])

    st.dataframe(df)

# ==========================================================
# ORDER
# ==========================================================
elif menu == "Order":

    if not st.session_state.user:
        st.warning("Login first.")

    else:

        st.header("🛒 Add to Cart")

        item = st.selectbox("Item",list(all_menu.keys()))
        qty = st.number_input("Quantity",1,20,1)

        if st.button("Add to Cart"):

            st.session_state.cart.append((item,qty,all_menu[item]))

            st.success("Added to cart")

# ==========================================================
# CART WITH GCASH + MAYA
# ==========================================================
elif menu == "Cart":

    if not st.session_state.cart:
        st.info("Cart is empty")

    else:

        total = 0
        profit_total = 0

        for item,qty,price in st.session_state.cart:

            subtotal = qty * price
            total += subtotal

            cursor.execute("SELECT cost FROM inventory WHERE item=?", (item,))
            cost = cursor.fetchone()[0]

            profit_total += (price-cost)*qty

            st.write(f"{item} x{qty} = ₱{subtotal}")

        st.subheader(f"Total: ₱{total}")

        st.subheader("💳 Payment Method")

        payment_method = st.selectbox(
            "Choose Payment",
            ["GCash","Maya"]
        )

        phone = st.text_input("Mobile Number")
        otp = st.text_input("OTP")

        if st.button("Confirm Payment"):

            if len(phone)==11 and len(otp)==6:

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                INSERT INTO orders (username,branch,total,profit,payment,timestamp)
                VALUES (?,?,?,?,?,?)
                """,(
                    st.session_state.user,
                    st.session_state.branch,
                    total,
                    profit_total,
                    payment_method,
                    timestamp
                ))

                conn.commit()

                for item,qty,_ in st.session_state.cart:
                    cursor.execute(
                        "UPDATE inventory SET stock=stock-? WHERE item=?",
                        (qty,item)
                    )

                conn.commit()

                st.session_state.cart.clear()

                st.success(f"{payment_method} Payment Successful!")

            else:
                st.error("Invalid Payment Details")

# ==========================================================
# DOUGHBOT CHAT
# ==========================================================
elif menu == "DoughBot Chat":

    st.title("🤖 DoughBot AI Assistant")

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask DoughBot something...")

    if prompt:

        st.session_state.chat_messages.append(
            {"role":"user","content":prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        response = doughbot_response(prompt)

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.chat_messages.append(
            {"role":"assistant","content":response}
        )

# ==========================================================
# ADMIN DASHBOARD
# ==========================================================
elif menu == "Admin Dashboard":

    st.header("📊 Admin Panel")

    admin_pass = st.text_input("Admin Password",type="password")

    if st.button("Access"):

        if admin_pass == "admin123":

            df_orders = pd.read_sql_query("SELECT * FROM orders",conn)
            df_inventory = pd.read_sql_query("SELECT * FROM inventory",conn)

            st.subheader("Total Sales")
            st.metric("₱",int(df_orders["total"].sum()) if not df_orders.empty else 0)

            st.subheader("Total Profit")
            st.metric("₱",int(df_orders["profit"].sum()) if not df_orders.empty else 0)

            st.subheader("Orders")
            st.dataframe(df_orders)

            st.subheader("Inventory")
            st.dataframe(df_inventory)

        else:
            st.error("Wrong Password")