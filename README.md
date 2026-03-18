# 🥐 Pan de Staku - Enterprise Bakery & Coffee Management System with AI Chatbot 🤖

**Pan de Staku** is a **French-inspired bakery and coffee management system** built with **Streamlit** ☕.  
It delivers a **complete digital bakery platform** with customer ordering, analytics, branch control, and an AI-style assistant.

## ✅ What It Delivers

- 🍞 Customer ordering system  
- 📊 Business analytics dashboard  
- 🏬 Multi-branch architecture  
- 🤖 AI-powered chatbot assistant (**DoughBot**)  

It simulates a **modern smart bakery platform** capable of handling:

- 🛒 Orders  
- 📦 Inventory  
- 📈 Analytics  
- 💬 AI customer assistance  
- 🖼 Home brand showcase with centered image and tagline  

---

## 🆕 Recent Updates (March 18, 2026)

- 🏬 Expanded branch coverage to **6 locations**: Manila, Cebu, Davao, Iloilo, General Santos, and Baguio  
- 🗺 Reworked **Branch page** into dynamic branch cards with selected-branch highlighting  
- 🏠 Updated **Home page** with centered brand image (`assets/pan_de_staku.png`) and tagline message  
- 🤖 Improved branch awareness in chatbot responses for both `app.py` and `chatbot.py`  
- ⚙️ Migrated Streamlit usage from deprecated `use_container_width` to `width="stretch"`  

---

# 🤖 AI Chatbot - DoughBot

The system includes an **AI bakery assistant** called **DoughBot**.  
DoughBot helps customers interact with the bakery using **natural conversation**.

## 🧠 Capabilities

- 🍞 Answer questions about **menu items and prices**  
- ☕ Recommend **bread and coffee combinations**  
- 🚚 Provide **delivery and branch information**  
- 💳 Explain **payment steps (GCash and Maya flow)**  
- 🛍 Guide users through **order and checkout steps**  

---

## 💬 Example Interaction

**User**

```text
Hi
```

**DoughBot**

```text
Bonjour! I am DoughBot. Looking for bread, coffee, or a combo today?
```

**User**

```text
Recommend breakfast
```

**DoughBot**

```text
My recommendation: Croissant with Latte.
```

---

# ✨ Features

## 🛒 Customer Side

- 🔐 Register and login securely  
- 🥖 Browse breads and coffee  
- 🛍 Add items to cart  
- 🌏 Branch-based ordering  
- 🔢 OTP-style payment validation simulation  
- 🤖 DoughBot chat assistance  

Branch locations: 🏙 Manila • 🌆 Cebu • 🌃 Davao • 🌅 Iloilo • 🌇 General Santos • ⛰ Baguio

---

# 🤖 AI Chatbot Features

DoughBot supports:

- 💬 Conversational menu browsing  
- 🥐 Product recommendations  
- ☕ Coffee and bread pairing suggestions  
- 🚚 Delivery and branch FAQs  
- 🛍 Ordering and payment guidance  

The chatbot uses **rule-based, prompt-driven conversational logic**.

---

# 🧑‍💼 Admin Dashboard

Admin features include:

- 🔐 Secure admin login  
- 💰 Total sales monitoring  
- 📈 Total profit monitoring  
- 📋 Full orders table view  
- 📦 Inventory table view  

---

# 🏢 Enterprise System Features

The system includes **enterprise-style functionality**:

- 🌍 Multi-branch support: 🏙 Manila • 🌆 Cebu • 🌃 Davao • 🌅 Iloilo • 🌇 General Santos • ⛰ Baguio  
- 🗄 SQLite database persistence  
- 📦 Inventory auto-deduction when items are sold  
- 💵 Profit calculation based on product cost  
- 📊 Real-time metrics in dashboard  
- 🤖 AI chatbot integration  

---

# 📑 Added Content Tabs

The app includes **business information tabs** for:

- 🏠 **Home** — Pan de Staku concept explanation with centered brand image and welcome tagline  
- 🥖 **Product** — Bread and coffee offerings  
- 🛎 **Service** — Service scope and commitments  
- 📞 **Contact** — Support channels and branch details  

---

# 🧭 Navigation Guide

Use the top navigation to move quickly:

- 🏠 Home  
- 🔐 Login / Register  
- 🏬 Branch  
- 📋 Menu List  
- 🧾 Order & Cart  
- 🤖 DoughBot Chat  
- 🧑‍💼 Admin Dashboard  

---

# 🎨 UI Highlights

- ✨ Glow-up themed interface with gradients and shadows  
- 🔠 Custom fonts for modern bakery branding  
- 🧭 Top horizontal navigation for fast access  
- 🧾 Menu lists styled like real café menus  
- 🖼 Centered Home image spotlight (`assets/pan_de_staku.png`) with branding message

---

# ⚙️ Installation & Setup

## 1️⃣ Install Python

Install **Python 3.10 or higher**:

```
https://www.python.org/downloads/
```

---

## 2️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/pan-de-staku.git
cd pan-de-staku
```

---

## 3️⃣ Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac / Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install streamlit pandas
```

---

## 5️⃣ Run the Application

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

Optional standalone chatbot page:

```bash
streamlit run chatbot.py
```

---

# 🧩 Streamlit Compatibility Note

To align with newer Streamlit versions (post-2025 deprecation window), this project now uses:

- `width="stretch"` instead of `use_container_width=True`  
- `width="content"` instead of `use_container_width=False`  

This avoids repeated deprecation warnings and keeps UI rendering future-safe.

---

# 🔑 Default Accounts

| Role        | Username        | Password |
| ----------- | --------------- | -------- |
| 👑 Admin    | admin           | admin123 |
| 👤 Customer | Register in app | N/A      |

---

# 🗄 Database Structure (SQLite)

The system uses **SQLite** for persistent storage.

## 👤 `users`

Stores account information.

```
id
username
password
role
```

---

## 📦 `inventory`

Tracks stock levels and cost basis.

```
item
stock
cost
```

---

## 🧾 `orders`

Logs confirmed checkout transactions.

```
id
username
branch
total
profit
payment
timestamp
```

---

# 💳 Payment Simulation

The app includes a **digital payment simulation** with:

- 📱 **GCash or Maya selection**  
- ☎️ **11-digit phone validation**  
- 🔐 **6-digit OTP validation**  
- 🧾 **Transaction logging into orders table**  

---

# 🧪 Prompt Testing (Chatbot Testing)

You can test **DoughBot behavior** using sample prompts.

### 🧪 Test 1 – Greeting

Input:

```text
Hello
```

Expected:

```text
A greeting response from DoughBot.
```

---

### 🧪 Test 2 – Menu Inquiry

Input:

```text
What breads do you have?
```

Expected:

```text
A list of available bread items.
```

---

### 🧪 Test 3 – Recommendation

Input:

```text
Recommend a coffee and bread combo
```

Expected:

```text
A pairing recommendation such as Croissant with Latte.
```

---

### 🧪 Test 4 – Delivery

Input:

```text
Do you offer delivery?
```

Expected:

```text
Delivery availability and base fee information.
```

---

### 🧪 Test 5 - Branches

Input:

```text
What branches do you have?
```

Expected:

```text
A response listing Manila, Cebu, Davao, Iloilo, General Santos, and Baguio.
```

---

# 🚀 Deployment Guide

## ☁️ Streamlit Community Cloud

1. Push the repository to **GitHub**.  
2. Open:

```
https://share.streamlit.io
```

3. Connect your **GitHub repository**.  
4. Select `app.py`.  
5. Deploy.  

---

## 🖥 Alternative Deployment Options

### VPS

```bash
streamlit run app.py --server.port=8501
```

### 🐳 Docker

Containerize the app for **scalable deployment across branches**.

---

# 🏗 System Architecture

The system follows a **multi-layer structure**:

1. 🛒 **Customer Layer** — UI for browsing and placing orders  
2. 🤖 **AI Layer** — DoughBot conversational assistance  
3. 🏬 **Branch Layer** — Branch-aware ordering system  
4. 🧑‍💼 **Admin Layer** — Dashboard analytics and inventory visibility  
5. 🗄 **Database Layer** — SQLite storage for users, inventory, and orders  

---

# 🧰 Technology Stack

| Component    | Technology         |
| ------------ | ------------------ |
| 🎨 Frontend  | Streamlit          |
| ⚙️ Backend   | Python             |
| 🗄 Database  | SQLite             |
| 📊 Analytics | Pandas             |
| 🤖 AI Logic  | Rule-based chatbot |

---

# 🔮 Future Improvements

Possible upgrades:

- 🧠 Real **LLM integration** (OpenAI or local models)  
- 🎤 **Voice ordering workflow**  
- 📱 Mobile-first responsive UI refinement  
- 💳 Real **payment gateway integration** (GCash, Maya, Stripe)  
- 📈 **AI-based inventory demand forecasting**  
- 🧾 Printable receipts and invoice export  

---

# 📜 License

MIT License.

✅ Free to **use, modify, and deploy** for:

- 🎓 Educational projects  
- 🧑‍💻 Personal development  
- 🏢 Commercial bakery applications  

---
