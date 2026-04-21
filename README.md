# 🥐 Pan de Staku - Enterprise Bakery & Coffee Management System with AI Chatbot 🤖
**Version:** 1.7.1 (April 21, 2026)

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

## 🆕 Recent Updates (April 21, 2026)

- 🛠 **DoughBot Crash Fix**: Resolved `KeyError: 'Croissant'` in recommendation flow by adding safe menu-price lookups for canonical item names
- 🔄 **Item Name Normalization**: DoughBot now normalizes menu names before pricing logic, preventing mismatches between emoji-labeled menu keys and chat item names
- 🧾 **Safer Price Logic**: Improved compare, budget combo, order estimate, and item-price responses to handle missing item mappings without crashing
- ✅ **Chat Stability Upgrade**: Recommendation and budget filtering now skip invalid items gracefully instead of throwing runtime errors

## 🗂 Previous Updates (April 20, 2026)

- ✨ **Major UI Design Overhaul**: Added modern animations (fadeIn, slideIn, pulse, glow), enhanced button effects with shimmer animations, improved hover states, and upgraded visual hierarchy across all pages
- 🎨 **Menu Enhancements**: Added emoji icons to all menu items (🥐, 🍞, ☕, etc.) for better visual appeal and user experience
- 🤖 **DoughBot Chatbot Improvements**: Redesigned chatbot interface with animated chat messages, recipe cards with structured HTML formatting, improved input styling with focus effects, and enhanced conversational capabilities for broader topic responses
- 🎭 **Theme System Refinements**: Polished all appearance themes (Light, Dark, Coffee, Cheese) with better gradients, shadows, and backdrop filters for a premium cafe aesthetic
- 📱 **Interactive Elements**: Added advanced CSS animations, transform effects, and glowing borders to cards, buttons, and navigation elements for a more engaging user interface  

## 🗂 Previous Updates (March 25, 2026)

- Added Nueva Vizcaya branches (Bayombong, Solano, Bambang) plus Paranaque across the app and DoughBot  
- Home hero image now embedded to avoid Streamlit media file cache/missing ID errors on rerun  

## 🗂 Previous Updates (March 23, 2026)

- 🧠 Added **optional OpenAI-powered responses** for DoughBot with automatic fallback to the local rules engine  
- 🧾 Updated the **Presentation** page to always render the PDF preview inline  
- 🧪 Added OpenAI connection status panel and environment-based tuning knobs  
- 🎁 Added **PHP 300 signup wallet credit** (auto-applied at checkout)  
- 💵 Added **Cash** as a payment option (mobile number only, no OTP)  
- 🧾 One-time **bonus migration** grants PHP 300 to existing users  
- ⚙️ Migrated Streamlit usage from deprecated `use_container_width` to `width="stretch"`  
---

# 🤖 AI Chatbot - DoughBot

The system includes an **AI bakery assistant** called **DoughBot**.  
DoughBot helps customers interact with the bakery using **natural conversation** and can respond to a wide variety of topics.

## 🧠 Capabilities

- 🍞 Answer questions about **menu items and prices**  
- ☕ Recommend **bread and coffee combinations**  
- 🚚 Provide **delivery and branch information**  
- 💳 Explain **payment steps (GCash, Maya, and Cash)**  
- 🛍 Guide users through **order and checkout steps**  
- 🧠 Optional OpenAI answers for **open-ended questions** (falls back if API key is missing)  
- 🎁 Explain the **PHP 300 signup wallet bonus**  
- 💬 **General Conversation**: Respond to greetings, small talk, and off-topic queries with friendly, context-aware replies  
- 📝 **Recipe Generation**: Create simple recipes based on user-provided ingredients or dish names  
- ❓ **Help & Support**: Provide assistance on any bakery-related or general inquiry  

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
- 💵 Cash payments with mobile number only  
- 🤖 DoughBot chat assistance  
- 🎁 PHP 300 signup wallet credit (auto-applied)  

Branch locations: 🏙 Manila • 🌆 Cebu • 🌃 Davao • 🌅 Iloilo • 🌇 General Santos • ⛰ Baguio • Nueva Vizcaya (Bayombong, Solano, Bambang) • Paranaque

---

# 🤖 AI Chatbot Features

DoughBot supports:

- 💬 Conversational menu browsing  
- 🥐 Product recommendations  
- ☕ Coffee and bread pairing suggestions  
- 🚚 Delivery and branch FAQs  
- 🛍 Ordering and payment guidance  
- 📝 **Recipe Generation**: Interactive recipe creation with ingredient-based suggestions  
- ❓ **General Assistance**: Responds to any topic with helpful, bakery-themed replies  
- 🎨 **Enhanced UI**: Animated chat interface with recipe cards and improved styling  

The chatbot uses **rule-based logic** by default and can switch to **OpenAI responses** when enabled.

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

- 🌍 Multi-branch support: 🏙 Manila • 🌆 Cebu • 🌃 Davao • 🌅 Iloilo • 🌇 General Santos • ⛰ Baguio • Nueva Vizcaya (Bayombong, Solano, Bambang) • Paranaque  
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

- ✨ **Advanced Animations**: Smooth fade-in, slide-in, pulse, and glow effects for dynamic page loading and interactions
- 🔠 **Premium Typography**: Custom Fraunces and Space Grotesk fonts with enhanced letter spacing and hierarchy
- 🧭 **Interactive Navigation**: Top horizontal navigation with hover animations and active state indicators
- 🥐 **Icon-Enhanced Menus**: Emoji icons (🥐, 🍞, ☕) added to all menu items for visual clarity and appeal
- 🎭 **Multi-Theme Support**: Four distinct themes (Light, Dark, Coffee, Cheese) with improved gradients and glassmorphism effects
- 💫 **Button Effects**: Shimmer animations, scaling transforms, and glowing shadows on hover for modern interactivity
- 🤖 **Enhanced Chatbot UI**: Animated chat bubbles, recipe cards with structured formatting, and improved input field styling
- 🖼 **Centered Hero Image**: Embedded home image with responsive design and glow effects
- 🌟 **Card Animations**: Hover effects with scaling, shadow enhancement, and border color transitions

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

Optional OpenAI SDK (for AI responses):

```bash
pip install openai
```

Optional PDF viewer (if available for your Python version):

```bash
pip install "streamlit[pdf]"
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

# 🔑 OpenAI Setup (Optional)

To enable OpenAI responses:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

Optional tuning (environment variables):

- `OPENAI_MODEL` (default: `gpt-4.1-mini`)  
- `OPENAI_MAX_HISTORY` (default: `12`)  
- `OPENAI_TEMPERATURE` (default: `0.7`)  

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

## 💳 `wallets`

Stores wallet credits.

```
username
balance
created_at
```

---

## 🎁 `wallet_awards`

Tracks one-time wallet bonuses.

```
username
amount
reason
granted_at
```

---

# 💳 Payment Simulation

The app includes a **digital payment simulation** with:

- 📱 **GCash, Maya, or Cash selection**  
- ☎️ **11-digit phone validation**  
- 🔐 **6-digit OTP validation** (GCash/Maya only)  
- 🧾 **Transaction logging into orders table**  
- 🎁 **Wallet credit auto-applied** when available  

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
A response listing Manila, Cebu, Davao, Iloilo, General Santos, Baguio, Nueva Vizcaya (Bayombong/Solano/Bambang), and Paranaque.
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
| 🤖 AI Logic  | Rule-based + OpenAI (optional) |

---

# 🔮 Future Improvements

Possible upgrades:

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
