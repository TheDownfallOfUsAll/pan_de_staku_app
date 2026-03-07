import hashlib
import re
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

DB_PATH = "pan_de_staku.db"
ADMIN_USERNAME = "admin"
ADMIN_DEFAULT_PASSWORD = "admin123"
BRANCHES = ["Manila", "Cebu", "Davao"]

bread_menu = {
    "Croissant": 120,
    "Baguette": 100,
    "Brioche": 150,
    "Pain au Chocolat": 140,
    "Fougasse": 130,
    "Sourdough": 160,
    "Danish": 135,
}

coffee_menu = {
    "Espresso": 90,
    "Americano": 100,
    "Cappuccino": 120,
    "Latte": 130,
    "Mocha": 140,
    "Macchiato": 115,
    "Flat White": 125,
}

all_menu = {**bread_menu, **coffee_menu}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


@st.cache_resource
def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            item TEXT PRIMARY KEY,
            stock INTEGER,
            cost REAL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            branch TEXT,
            total REAL,
            profit REAL,
            payment TEXT,
            timestamp TEXT
        )
        """
    )
    conn.commit()


def seed_default_admin(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (ADMIN_USERNAME,))
    if cursor.fetchone():
        return
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (ADMIN_USERNAME, hash_password(ADMIN_DEFAULT_PASSWORD), "admin"),
    )
    conn.commit()


def seed_inventory(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    for item, price in all_menu.items():
        cursor.execute(
            "INSERT OR IGNORE INTO inventory (item, stock, cost) VALUES (?, ?, ?)",
            (item, 50, round(price * 0.6, 2)),
        )
    conn.commit()


def authenticate_user(conn: sqlite3.Connection, username: str, password: str):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role, password FROM users WHERE username = ?",
        (username.strip(),),
    )
    row = cursor.fetchone()
    if not row:
        return None
    db_username, db_role, db_hash = row
    if db_hash == hash_password(password):
        return {"username": db_username, "role": db_role}
    return None


def create_user(conn: sqlite3.Connection, username: str, password: str) -> tuple[bool, str]:
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        return False, "Username must be 3-20 chars and contain only letters, numbers, or underscore."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    try:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username.strip(), hash_password(password), "customer"),
        )
        conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."


def init_session_state() -> None:
    st.session_state.setdefault("cart", [])
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("role", None)
    st.session_state.setdefault("branch", BRANCHES[0])
    st.session_state.setdefault("chat_messages", [])


def get_stock(conn: sqlite3.Connection, item: str) -> int:
    row = conn.execute("SELECT stock FROM inventory WHERE item = ?", (item,)).fetchone()
    return int(row[0]) if row else 0


def add_to_cart(item: str, qty: int, price: float) -> None:
    for entry in st.session_state.cart:
        if entry["item"] == item:
            entry["qty"] += qty
            return
    st.session_state.cart.append({"item": item, "qty": qty, "price": price})


def validate_payment(phone: str, otp: str) -> bool:
    return bool(re.fullmatch(r"\d{11}", phone) and re.fullmatch(r"\d{6}", otp))


def doughbot_response(prompt: str) -> str:
    p = prompt.lower()
    if any(x in p for x in ["hi", "hello", "hey"]):
        return "Bonjour! I am DoughBot, your Pan de Staku assistant."
    if "menu" in p:
        return "Our menu includes:\n\n" + ", ".join(all_menu.keys())
    if "bread" in p:
        return "Our breads:\n\n" + ", ".join(bread_menu.keys())
    if "coffee" in p:
        return "Coffee selection:\n\n" + ", ".join(coffee_menu.keys())
    if "recommend" in p:
        return "I recommend Croissant with Latte."
    if "delivery" in p:
        return "Delivery fee starts at PHP 40."
    if "branch" in p:
        return "Branches are available in Manila, Cebu, and Davao."
    if "price" in p:
        return "Prices range between PHP 90 and PHP 160."
    if "order" in p:
        return "Go to Order page, add items, then checkout in Cart."
    return "Ask me about menu, coffee, bread, delivery, branches, or recommendations."


st.set_page_config(page_title="Pan de Staku", page_icon="🥐", layout="wide")

st.markdown(
    """
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stApp {
    animation: fadeIn 0.8s ease-in-out;
    background:
        radial-gradient(circle at 20% 20%, rgba(255,224,178,0.3), transparent 40%),
        linear-gradient(135deg, #3E2723, #6D4C41, #D7A86E);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #3E2723, #5D4037, #8D6E63);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3, .stTitle {
    color: #FFF3E0;
}

p {
    color: #FFE0B2;
}
</style>
""",
    unsafe_allow_html=True,
)

conn = get_db_connection()
init_db(conn)
seed_default_admin(conn)
seed_inventory(conn)
init_session_state()

cart_count = sum(entry["qty"] for entry in st.session_state.cart)
current_user = st.session_state.user or "Guest"
st.sidebar.caption(f"User: {current_user} | Branch: {st.session_state.branch}")

menu = st.sidebar.radio(
    f"Navigation Cart({cart_count})",
    [
        "Home",
        "Login",
        "Register",
        "Branch",
        "Menu List",
        "Order",
        "Cart",
        "DoughBot Chat",
        "Admin Dashboard",
    ],
)

if menu == "Home":
    st.title("Pan de Staku")
    st.subheader("Enterprise French Bakery and Coffee Management System")
    st.write(
        "Welcome to Pan de Staku, a premium bakery platform with AI assistant, "
        "multi-branch ordering, and digital payments."
    )

elif menu == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(conn, username, password)
        if user:
            st.session_state.user = user["username"]
            st.session_state.role = user["role"]
            st.success("Login successful.")
        else:
            st.error("Invalid credentials.")

elif menu == "Register":
    st.header("Register")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Create Account"):
        ok, message = create_user(conn, new_user, new_pass)
        if ok:
            st.success(message)
        else:
            st.error(message)

elif menu == "Branch":
    branch = st.selectbox("Select Branch", BRANCHES, index=BRANCHES.index(st.session_state.branch))
    st.session_state.branch = branch
    st.success(f"Branch set to {branch}.")

elif menu == "Menu List":
    st.header("Full Menu")
    df = pd.DataFrame(list(all_menu.items()), columns=["Item", "Price"])
    st.dataframe(df, use_container_width=True)

elif menu == "Order":
    if not st.session_state.user:
        st.warning("Login first.")
    else:
        st.header("Add to Cart")
        item = st.selectbox("Item", list(all_menu.keys()))
        available_stock = get_stock(conn, item)
        st.caption(f"Available stock: {available_stock}")
        qty = st.number_input("Quantity", min_value=1, max_value=20, value=1)
        if st.button("Add to Cart"):
            if qty > available_stock:
                st.error("Not enough stock for this item.")
            else:
                add_to_cart(item, int(qty), all_menu[item])
                st.success("Added to cart.")

elif menu == "Cart":
    if not st.session_state.cart:
        st.info("Cart is empty.")
    elif not st.session_state.user:
        st.warning("Login first.")
    else:
        total = 0.0
        profit_total = 0.0
        unavailable_items = []

        for entry in st.session_state.cart:
            item = entry["item"]
            qty = entry["qty"]
            price = entry["price"]
            stock = get_stock(conn, item)

            if qty > stock:
                unavailable_items.append(f"{item} (requested {qty}, stock {stock})")

            subtotal = qty * price
            total += subtotal

            row = conn.execute("SELECT cost FROM inventory WHERE item = ?", (item,)).fetchone()
            cost = float(row[0]) if row else 0.0
            profit_total += (price - cost) * qty

            st.write(f"{item} x{qty} = PHP {subtotal:.2f}")

        st.subheader(f"Total: PHP {total:.2f}")
        st.subheader("Payment Method")
        payment_method = st.selectbox("Choose Payment", ["GCash", "Maya"])
        phone = st.text_input("Mobile Number (11 digits)")
        otp = st.text_input("OTP (6 digits)")

        if unavailable_items:
            st.error("Insufficient stock: " + "; ".join(unavailable_items))

        if st.button("Confirm Payment"):
            if unavailable_items:
                st.error("Please adjust cart quantities before checkout.")
            elif not validate_payment(phone, otp):
                st.error("Invalid payment details.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn.execute(
                    """
                    INSERT INTO orders (username, branch, total, profit, payment, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        st.session_state.user,
                        st.session_state.branch,
                        total,
                        profit_total,
                        payment_method,
                        timestamp,
                    ),
                )
                for entry in st.session_state.cart:
                    conn.execute(
                        "UPDATE inventory SET stock = stock - ? WHERE item = ?",
                        (entry["qty"], entry["item"]),
                    )
                conn.commit()
                st.session_state.cart.clear()
                st.success(f"{payment_method} payment successful.")

elif menu == "DoughBot Chat":
    st.title("DoughBot Assistant")
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask DoughBot something...")
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        response = doughbot_response(prompt)
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.chat_messages.append({"role": "assistant", "content": response})

elif menu == "Admin Dashboard":
    st.header("Admin Panel")
    if not st.session_state.user:
        st.warning("Login as admin to view this page.")
    elif st.session_state.role != "admin":
        st.error("Admin access required.")
    else:
        df_orders = pd.read_sql_query("SELECT * FROM orders", conn)
        df_inventory = pd.read_sql_query("SELECT * FROM inventory", conn)

        total_sales = int(df_orders["total"].sum()) if not df_orders.empty else 0
        total_profit = int(df_orders["profit"].sum()) if not df_orders.empty else 0

        st.subheader("Total Sales")
        st.metric("PHP", total_sales)

        st.subheader("Total Profit")
        st.metric("PHP", total_profit)

        st.subheader("Orders")
        st.dataframe(df_orders, use_container_width=True)

        st.subheader("Inventory")
        st.dataframe(df_inventory, use_container_width=True)
