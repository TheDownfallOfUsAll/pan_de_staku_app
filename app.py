import hashlib
import random
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
    st.session_state.setdefault("doughbot_last_item", None)
    st.session_state.setdefault("doughbot_last_intent", None)


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
    words = set(re.findall(r"[a-z]+", p))

    item_aliases = {
        "croissant": "Croissant",
        "baguette": "Baguette",
        "brioche": "Brioche",
        "pain au chocolat": "Pain au Chocolat",
        "fougasse": "Fougasse",
        "sourdough": "Sourdough",
        "danish": "Danish",
        "espresso": "Espresso",
        "americano": "Americano",
        "cappuccino": "Cappuccino",
        "latte": "Latte",
        "mocha": "Mocha",
        "macchiato": "Macchiato",
        "flat white": "Flat White",
    }
    pairings = {
        "Croissant": "Latte",
        "Baguette": "Americano",
        "Brioche": "Cappuccino",
        "Pain au Chocolat": "Mocha",
        "Fougasse": "Espresso",
        "Sourdough": "Flat White",
        "Danish": "Macchiato",
    }
    greet_words = {"hi", "hello", "hey", "bonjour"}
    thanks_words = {"thanks", "thank", "salamat"}
    price_words = {"price", "cost", "how", "much"}
    recommend_words = {"recommend", "suggest", "best"}
    order_words = {"order", "buy", "checkout", "cart"}
    delivery_words = {"delivery", "deliver", "ship"}
    branch_words = {"branch", "location", "store"}
    payment_words = {"payment", "gcash", "maya", "otp"}
    hours_words = {"hours", "open", "close", "time"}

    detected_item = None
    for alias, canonical in item_aliases.items():
        if alias in p:
            detected_item = canonical
            break
    if not detected_item and st.session_state.get("doughbot_last_item"):
        follow_up = {"it", "that", "this", "one"}
        if words.intersection(follow_up):
            detected_item = st.session_state.doughbot_last_item

    if detected_item:
        st.session_state.doughbot_last_item = detected_item

    if words.intersection(greet_words):
        st.session_state.doughbot_last_intent = "greeting"
        return random.choice(
            [
                "Bonjour! I am DoughBot. Looking for bread, coffee, or a combo today?",
                "Welcome to Pan de Staku. I can suggest items, prices, and pairings.",
                "Hi! Ask me for recommendations, menu details, or order help.",
            ]
        )

    if words.intersection(thanks_words):
        st.session_state.doughbot_last_intent = "thanks"
        return random.choice(
            [
                "You are welcome. Enjoy your order.",
                "Happy to help. Let me know if you want another suggestion.",
                "Anytime. I can also suggest a coffee pairing.",
            ]
        )

    if "menu" in words:
        st.session_state.doughbot_last_intent = "menu"
        return "Full menu:\n\n" + ", ".join(all_menu.keys())

    if "bread" in words or any(x in p for x in ["croissant", "baguette", "brioche", "sourdough"]):
        if not detected_item:
            st.session_state.doughbot_last_intent = "bread"
            return "Our breads:\n\n" + ", ".join(bread_menu.keys())

    if "coffee" in words or any(x in p for x in ["espresso", "latte", "americano", "cappuccino"]):
        if not detected_item:
            st.session_state.doughbot_last_intent = "coffee"
            return "Coffee selection:\n\n" + ", ".join(coffee_menu.keys())

    if words.intersection(recommend_words):
        st.session_state.doughbot_last_intent = "recommend"
        picks = [
            "Croissant with Latte",
            "Brioche with Cappuccino",
            "Pain au Chocolat with Mocha",
            "Sourdough with Flat White",
        ]
        return f"My recommendation: {random.choice(picks)}."

    if detected_item and ("pair" in words or "with" in words or "goes" in words):
        st.session_state.doughbot_last_intent = "pairing"
        paired = pairings.get(detected_item)
        if paired:
            return f"{detected_item} pairs well with {paired}."

    if detected_item and words.intersection(price_words):
        st.session_state.doughbot_last_intent = "item_price"
        price = all_menu.get(detected_item)
        if price is not None:
            return f"{detected_item} is PHP {price}."

    if words.intersection(price_words):
        st.session_state.doughbot_last_intent = "price_range"
        min_price = min(all_menu.values())
        max_price = max(all_menu.values())
        return f"Prices range from PHP {min_price} to PHP {max_price}."

    if words.intersection(delivery_words):
        st.session_state.doughbot_last_intent = "delivery"
        return random.choice(
            [
                "Delivery fee starts at PHP 40, depending on distance.",
                "Yes, delivery is available. Base fee is PHP 40.",
            ]
        )

    if words.intersection(branch_words):
        st.session_state.doughbot_last_intent = "branch"
        return "Branches are available in Manila, Cebu, and Davao."

    if words.intersection(payment_words):
        st.session_state.doughbot_last_intent = "payment"
        return "We accept GCash and Maya. Enter an 11-digit mobile number and 6-digit OTP."

    if words.intersection(hours_words):
        st.session_state.doughbot_last_intent = "hours"
        return "Store hours are managed per branch. Choose a branch and check announcements for exact opening times."

    if words.intersection(order_words):
        st.session_state.doughbot_last_intent = "order"
        return "To order: login, open Order page, add items to cart, then checkout in Cart."

    if detected_item:
        st.session_state.doughbot_last_intent = "item_info"
        paired = pairings.get(detected_item, "a coffee of your choice")
        price = all_menu.get(detected_item)
        if price is not None:
            return (
                f"{detected_item} is available for PHP {price}. "
                f"Popular pairing: {paired}."
            )

    st.session_state.doughbot_last_intent = "fallback"
    return (
        "I can help with menu, prices, pairings, delivery, payment, branches, and order steps. "
        "Try: 'recommend a combo' or 'price of brioche'."
    )


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
        "Product",
        "Service",
        "Contact",
        "Admin Dashboard",
    ],
)

if menu == "Home":
    st.title("Pan de Staku")
    st.subheader("Enterprise French Bakery and Coffee Management System")

    st.markdown(
        """
Pan de Staku is a modern bakery and coffee concept built around a simple promise: deliver artisan-quality bread,
carefully brewed coffee, and reliable digital service in one connected experience. The name represents a fusion of
traditional baking roots and smart operations. "Pan" points to bread craftsmanship, while "Staku" reflects structured,
technology-assisted business flow for daily bakery operations.

At its core, Pan de Staku is both a customer-facing food brand and an internal management platform. For customers,
it provides a consistent way to browse products, place orders, pay digitally, and receive support through an assistant.
For the business team, it supports inventory visibility, branch-level control, and operational decision making through
real sales and profit records.

The long-term vision of Pan de Staku is to create a bakery ecosystem where quality and convenience are not separate.
Each branch follows the same product standards and service approach while still serving local demand efficiently.
From handcrafted croissants to classic espresso drinks, every menu item is positioned to maintain premium value,
balanced pricing, and customer trust.

Pan de Staku also emphasizes sustainability in operations: reducing waste through stock tracking, improving fulfillment
accuracy through branch assignment, and enabling repeatable service standards through guided digital workflows. The goal
is not only to sell bakery products, but to establish a dependable food-and-service system that can scale across cities
without losing the feel of a neighborhood bakery.
"""
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Brand Definition")
        st.write(
            "Pan de Staku is an integrated bakery management model that combines artisan baking, specialty coffee, "
            "and branch-based digital commerce into one operational platform."
        )
    with col2:
        st.subheader("Why It Matters")
        st.write(
            "It improves customer convenience while giving the business better control over stock, sales, and service "
            "quality across multiple locations."
        )

elif menu == "Product":
    st.header("Products")
    st.write(
        "Our product line is designed for customers who want high-quality baked goods and coffee with predictable taste, "
        "freshness, and value."
    )

    st.subheader("Signature Bread Collection")
    for item, price in bread_menu.items():
        st.write(f"- {item}: PHP {price}")

    st.subheader("Coffee Program")
    for item, price in coffee_menu.items():
        st.write(f"- {item}: PHP {price}")

    st.subheader("Product Direction")
    st.write(
        "Pan de Staku products focus on daily freshness, balanced flavor profiles, and curated bread-and-coffee pairings "
        "to improve customer satisfaction and repeat purchases."
    )

elif menu == "Service":
    st.header("Services")
    st.write("Pan de Staku provides a complete service flow from product discovery to post-order assistance.")

    st.markdown(
        """
- In-store and branch-based ordering for walk-in and local fulfillment.
- Digital cart and checkout flow for fast order placement.
- GCash and Maya payment support with verification flow.
- Multi-branch coverage in Manila, Cebu, and Davao.
- DoughBot support for menu guidance, pairings, prices, and ordering steps.
- Inventory-aware ordering to reduce out-of-stock frustration.
"""
    )

    st.subheader("Service Commitment")
    st.write(
        "We aim to deliver accurate orders, transparent pricing, and responsive customer support while continuously "
        "improving branch-level performance."
    )

elif menu == "Contact":
    st.header("Contact Us")
    st.write("Reach Pan de Staku for orders, partnerships, branch concerns, or customer support.")

    st.markdown(
        """
**Head Office Email:** support@pandestaku.com  
**Customer Hotline:** +63 917 555 0123  
**Business Hours:** Monday to Sunday, 7:00 AM - 9:00 PM  
**Main Branches:** Manila, Cebu, Davao
"""
    )

    st.subheader("Contact Channels")
    st.write("- General Inquiries: support@pandestaku.com")
    st.write("- Franchise and Partnerships: partnerships@pandestaku.com")
    st.write("- Billing and Payments: billing@pandestaku.com")
    st.write("- Branch Operations: operations@pandestaku.com")

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
