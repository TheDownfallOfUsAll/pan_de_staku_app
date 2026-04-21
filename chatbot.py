import os
import streamlit as st
import pandas as pd
import time
import random
import re

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None

st.set_page_config(
    page_title="Pan de Staku AI",
    page_icon="🥐",
    layout="wide"
)

# ------------------------------------------------
# PREMIUM CAFE STYLE UI
# ------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

:root {
  --bg-dark: #2a1a14;
  --bg-mid: #6a4a3c;
  --bg-light: #d7b07d;
  --cream: #f6efe6;
  --accent: #f2c97d;
  --card: rgba(255, 248, 236, 0.12);
  --card-strong: rgba(255, 248, 236, 0.18);
  --border: rgba(255, 248, 236, 0.20);
  --shadow: 0 12px 32px rgba(0, 0, 0, 0.32);
  --glow: rgba(243, 194, 122, 0.4);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-30px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}

.stApp {
  background: 
    radial-gradient(circle at 25% 25%, rgba(255,224,178,0.4), transparent 45%),
    radial-gradient(circle at 75% 75%, rgba(214,176,125,0.3), transparent 45%),
    linear-gradient(135deg, #3E2723, #6D4C41, #D7A86E);
  background-attachment: fixed;
  color: var(--cream);
  font-family: 'Space Grotesk', sans-serif;
  animation: fadeInUp 1s ease;
}

h1, h2, h3, p, li {
  color: var(--cream);
}

h1, h2, h3 {
  font-family: 'Fraunces', serif;
  letter-spacing: 0.5px;
}

.chat-card {
  background: var(--card-strong);
  padding: 2rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  animation: fadeInUp 0.6s ease;
  position: relative;
  overflow: hidden;
}

.chat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent), #ffe1b3, var(--accent));
  animation: glow 2s ease-in-out infinite alternate;
}

.menu-card {
  background: var(--card);
  padding: 1.5rem;
  border-radius: 18px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  backdrop-filter: blur(8px);
  animation: slideInLeft 0.5s ease;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.menu-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px var(--shadow), 0 0 15px var(--glow);
}

.stChatMessage {
  border-radius: 16px;
  padding: 1rem 1.2rem;
  margin: 0.5rem 0;
  animation: slideInRight 0.4s ease;
}

.stChatMessage[data-testid="stChatMessage-user"] {
  background: linear-gradient(135deg, var(--accent), #ffe1b3);
  color: #2a1a0f;
  border: 1px solid var(--border);
  box-shadow: 0 8px 20px var(--glow);
}

.stChatMessage[data-testid="stChatMessage-assistant"] {
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.stButton > button {
  background: linear-gradient(135deg, var(--accent), #ffe1b3);
  color: #2a1a0f;
  border: none;
  border-radius: 50px;
  padding: 0.8rem 1.8rem;
  font-weight: 600;
  font-size: 0.95rem;
  box-shadow: 0 10px 24px var(--glow);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stButton > button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.stButton > button:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 15px 35px var(--glow);
}

.stButton > button:hover::before {
  left: 100%;
}

.stTextInput > div > div > input {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 50px;
  padding: 0.8rem 1.2rem;
  color: var(--cream);
  font-family: 'Space Grotesk', sans-serif;
  transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--glow);
}

.stSelectbox > div > div {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 50px;
  transition: all 0.3s ease;
}

.stSelectbox > div > div:hover {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--glow);
}

.recipe-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  backdrop-filter: blur(8px);
  animation: fadeInUp 0.5s ease;
  margin: 1rem 0;
}

.recipe-card h4 {
  color: var(--accent);
  font-family: 'Fraunces', serif;
  margin-bottom: 0.5rem;
}

.recipe-card p {
  line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

:root {
  --bg-dark: #2a1a14;
  --bg-mid: #6a4a3c;
  --bg-light: #d7b07d;
  --cream: #f6efe6;
  --accent: #f2c97d;
  --card: rgba(255, 248, 236, 0.10);
  --card-strong: rgba(255, 248, 236, 0.16);
  --border: rgba(255, 248, 236, 0.18);
  --shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
}

.stApp {
  color: var(--cream);
  font-family: "Space Grotesk", sans-serif;
}

h1, h2, h3, p, li {
  color: var(--cream);
}

h1, h2, h3 {
  font-family: "Fraunces", serif;
  letter-spacing: 0.5px;
}

@keyframes riseIn {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.chat-card, .menu-card, .recipe-card {
  background: var(--card);
  border: 1px solid var(--border);
  padding: 18px;
  border-radius: 16px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(8px);
  animation: riseIn 0.5s ease;
}

.menu-card {
  background: var(--card-strong);
}

.stChatMessage {
  border-radius: 14px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------
# CHATBOT NAME
# ------------------------------------------------
CHATBOT_NAME = "DoughBot"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
BRANCHES = [
    "Manila",
    "Cebu",
    "Davao",
    "Iloilo",
    "General Santos",
    "Baguio",
    "Nueva Vizcaya - Bayombong",
    "Nueva Vizcaya - Solano",
    "Nueva Vizcaya - Bambang",
    "Paranaque",
]
BRANCH_LIST_TEXT = ", ".join(BRANCHES)
SIGNUP_BONUS = 300
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_MAX_HISTORY = int(os.getenv("OPENAI_MAX_HISTORY", "12"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# ------------------------------------------------
# MENU DATA WITH PRICING & STOCK
# ------------------------------------------------
menu_items = {
    "🥐 Croissant": 120,
    "🍞 Baguette": 100,
    "🥖 Brioche": 150,
    "🥯 Pain au Chocolat": 140,
    "☕ Espresso": 90,
    "☕ Latte": 130,
    "☕ Cappuccino": 120
}

menu_items.update({
    "Fougasse": 130,
    "Sourdough": 160,
    "Danish": 135,
    "Americano": 100,
    "Mocha": 140,
    "Macchiato": 115,
    "Flat White": 125,
})

# Stock Status System (Real-time inventory)
STOCK_STATUS = {
    "🥐 Croissant": {"stock": 45, "status": "In Stock"},
    "🍞 Baguette": {"stock": 32, "status": "In Stock"},
    "🥖 Brioche": {"stock": 28, "status": "In Stock"},
    "🥯 Pain au Chocolat": {"stock": 15, "status": "Low Stock"},
    "Fougasse": {"stock": 22, "status": "In Stock"},
    "Sourdough": {"stock": 18, "status": "In Stock"},
    "Danish": {"stock": 8, "status": "Low Stock"},
    "☕ Espresso": {"stock": 999, "status": "Available"},
    "☕ Latte": {"stock": 999, "status": "Available"},
    "☕ Cappuccino": {"stock": 999, "status": "Available"},
    "Americano": {"stock": 999, "status": "Available"},
    "Mocha": {"stock": 999, "status": "Available"},
    "Macchiato": {"stock": 999, "status": "Available"},
    "Flat White": {"stock": 999, "status": "Available"},
}

# Best Pairings Database with Descriptions
BEST_PAIRINGS = {
    "🥐 Croissant": {
        "drink": "☕ Latte",
        "reason": "The buttery, flaky croissant pairs perfectly with smooth, creamy latte for a balanced breakfast.",
        "persona": "Classic Morning Enthusiast"
    },
    "🥖 Brioche": {
        "drink": "☕ Cappuccino",
        "reason": "Rich, sweet brioche complements the bold espresso and velvety foam of cappuccino beautifully.",
        "persona": "Coffee Lover's Choice"
    },
    "🥯 Pain au Chocolat": {
        "drink": "☕ Mocha",
        "reason": "Chocolate pastry with chocolate coffee - a match made in heaven for sweet mornings.",
        "persona": "Chocolate Devotee"
    },
    "🍞 Baguette": {
        "drink": "☕ Americano",
        "reason": "Crispy, artisan bread pairs wonderfully with strong, straightforward americano.",
        "persona": "Purist's Pick"
    },
    "Sourdough": {
        "drink": "☕ Flat White",
        "reason": "Tangy sourdough balances perfectly with smooth, velvety flat white espresso.",
        "persona": "Artisan Appreciator"
    },
    "Danish": {
        "drink": "☕ Macchiato",
        "reason": "Light pastry with layered coffee flavors - an elegant afternoon combination.",
        "persona": "Afternoon Sipper"
    },
    "Fougasse": {
        "drink": "☕ Espresso",
        "reason": "Herbaceous, savory bread with bold espresso - a sophisticated pairing.",
        "persona": "Flavor Explorer"
    },
}

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {}

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "pending_recipe_prompt" not in st.session_state:
    st.session_state.pending_recipe_prompt = None

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ------------------------------------------------
# OPENAI HELPERS
# ------------------------------------------------
def _get_openai_api_key() -> str | None:
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def _get_openai_client():
    if OpenAI is None:
        return None
    api_key = _get_openai_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _build_system_prompt() -> str:
    menu_lines = "\n".join([f"- {item}: PHP {price}" for item, price in menu_items.items()])
    return (
        "You are DoughBot, a friendly and knowledgeable AI assistant working at Pan de Staku bakery. "
        "You can help with bakery questions, menu recommendations, orders, and general conversation. "
        "Be warm, helpful, and engaging. You know about food, recipes, general knowledge, and can chat about many topics. "
        "When bakery-related, use the menu and prices below. For general topics, be informative and fun. "
        f"Signup bonus: new customers get PHP {SIGNUP_BONUS} wallet credit after registering.\n\n"
        f"Branches: {BRANCH_LIST_TEXT}\n"
        "Payment methods: GCash, Maya, Cash. GCash/Maya require mobile number + OTP. Cash requires mobile number only.\n"
        "Menu and prices:\n"
        f"{menu_lines}\n\n"
        "You can discuss: food, recipes, cooking tips, general knowledge, current events, entertainment, "
        "technology, health, fitness, travel, hobbies, and more. Keep responses concise but helpful."
    )


def _build_openai_messages() -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [{"role": "system", "content": _build_system_prompt()}]
    history = st.session_state.messages[-OPENAI_MAX_HISTORY:]
    for msg in history:
        role = msg.get("role")
        content = msg.get("content")
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": str(content)})
    return messages


def _extract_output_text(response) -> str | None:
    try:
        output = getattr(response, "output", None) or []
        for item in output:
            for content in getattr(item, "content", []) or []:
                if getattr(content, "type", "") == "output_text":
                    return getattr(content, "text", None)
    except Exception:
        return None
    return None


def _openai_reply() -> str | None:
    client = _get_openai_client()
    if not client:
        return None
    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=_build_openai_messages(),
            temperature=OPENAI_TEMPERATURE,
        )
        text = getattr(response, "output_text", None) or _extract_output_text(response)
        return text.strip() if text else None
    except Exception:
        return None

# ------------------------------------------------
# HEADER
# ------------------------------------------------
with st.sidebar:
    st.subheader("Admin Login")
    if st.session_state.admin_logged_in:
        st.success("Logged in as admin.")
        if st.button("Logout Admin"):
            st.session_state.admin_logged_in = False
    else:
        admin_user = st.text_input("Admin Username", key="admin_user")
        admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")
        if st.button("Login as Admin"):
            if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Admin login successful.")
            else:
                st.error("Invalid admin credentials.")

    if st.session_state.admin_logged_in:
        st.markdown("### Admin Panel")
        st.caption("Quick monitoring snapshot")
        st.metric("Chat Messages", len(st.session_state.messages))
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared.")

    st.divider()
    st.subheader("OpenAI Status")
    if _get_openai_client():
        st.success("OpenAI connected")
        st.caption(f"Model: {OPENAI_MODEL}")
    elif OpenAI is None:
        st.warning("OpenAI SDK not installed")
        st.caption("Install with: pip install openai")
    else:
        st.warning("OpenAI API key not set")
        st.caption("Set OPENAI_API_KEY or add it to Streamlit secrets.")

st.markdown("Tip: Try asking `Give me a recipe for chicken, garlic, onion`.")
st.title("🥐 Pan de Staku Smart Bakery")
st.subheader("AI Powered Bakery Assistant")

st.markdown("""
Welcome to **Pan de Staku**.

Chat with **DoughBot 🤖** to:

• Discover artisan breads  
• Get coffee pairings  
• Ask bakery questions  
• Get menu recommendations  
""")

# ------------------------------------------------
# LAYOUT
# ------------------------------------------------
col1, col2 = st.columns([1,1.2])

# ------------------------------------------------
# MENU DISPLAY
# ------------------------------------------------
with col1:

    st.markdown('<div class="menu-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Bakery Menu")

    cols = st.columns(2)
    with cols[0]:
        st.markdown("**🥐 Artisan Breads**")
        for item, price in list(menu_items.items())[:7]:
            st.markdown(f"- {item}: ₱{price}")

    with cols[1]:
        st.markdown("**☕ Coffee & Drinks**")
        for item, price in list(menu_items.items())[7:]:
            st.markdown(f"- {item}: ₱{price}")

    st.markdown("### ⭐ Popular Combo")
    st.info("🥐 Croissant + ☕ Latte - Perfect buttery breakfast combo.")

    st.markdown("### Recipe Helper")
    ingredients_input = st.text_input("Ingredients or dish name", key="ingredients_input")
    if st.button("Generate Recipe"):
        if ingredients_input.strip():
            st.session_state.pending_recipe_prompt = f"Give me a recipe for {ingredients_input.strip()}."

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# ENHANCED FEATURES: PRICE CHECK, STOCK, PAIRINGS, ORDER GUIDANCE
# ------------------------------------------------
def _get_price_check(item_query: str) -> str:
    """Return detailed price information"""
    item_query = item_query.lower().strip()
    
    # Find matching item
    matching_items = []
    for item, price in menu_items.items():
        if item_query in item.lower() or any(word in item.lower() for word in item_query.split()):
            matching_items.append((item, price))
    
    if not matching_items:
        return random.choice([
            "I didn't find that item. Try asking about: Croissant, Baguette, Brioche, Coffee, Latte, Cappuccino, etc.",
            "That item isn't on our menu. What else can I help you with?",
            "Let me know the specific item and I'll check the price for you!"
        ])
    
    if len(matching_items) == 1:
        item, price = matching_items[0]
        return f"💰 **{item}** costs **PHP {price}**. Fresh and delicious!"
    
    # Multiple matches
    response = "📋 **Price Check Results:**\n"
    for item, price in matching_items[:5]:
        response += f"- {item}: **PHP {price}**\n"
    return response


def _get_stock_status(item_query: str) -> str:
    """Return real-time stock information"""
    item_query = item_query.lower().strip()
    
    matching_items = []
    for item in STOCK_STATUS.keys():
        if item_query in item.lower() or any(word in item.lower() for word in item_query.split()):
            matching_items.append(item)
    
    if not matching_items:
        return "I couldn't find that item. Try asking about: Croissant, Latte, Brioche, etc."
    
    if len(matching_items) == 1:
        item = matching_items[0]
        stock_info = STOCK_STATUS[item]
        status = stock_info["status"]
        stock = stock_info["stock"]
        
        if "Low Stock" in status:
            emoji = "⚠️"
        elif "Available" in status:
            emoji = "✅"
        else:
            emoji = "📦"
        
        return f"{emoji} **{item}** - {status}\n📊 Available: {stock} units"
    
    # Multiple matches
    response = "📦 **Stock Status Check:**\n"
    for item in matching_items[:5]:
        stock_info = STOCK_STATUS[item]
        status = stock_info["status"]
        stock = stock_info["stock"]
        emoji = "⚠️" if "Low" in status else "✅"
        response += f"{emoji} {item}: {status} ({stock} units)\n"
    return response


def _get_best_pairing(item_query: str) -> str:
    """Return best pairing suggestions with persona descriptions"""
    item_query = item_query.lower().strip()
    
    matching_pairs = []
    for item, pairing_info in BEST_PAIRINGS.items():
        if item_query in item.lower() or any(word in item.lower() for word in item_query.split()):
            matching_pairs.append((item, pairing_info))
    
    if not matching_pairs:
        # Random suggestion if no specific match
        item, pairing_info = random.choice(list(BEST_PAIRINGS.items()))
        return f"✨ **Best Pairing Suggestion:**\n\n{item} + {pairing_info['drink']}\n\n💭 _{pairing_info['reason']}_\n\n🎯 Perfect for: **{pairing_info['persona']}**"
    
    item, pairing_info = matching_pairs[0]
    return f"""✨ **Best Pairing for {item}:**

🥐 **{item}** + ☕ **{pairing_info['drink']}**

💭 _{pairing_info['reason']}_

🎯 Perfect for: **{pairing_info['persona']}**

Want to order this combo?"""


def _get_order_guidance() -> str:
    """Guide users through the ordering process"""
    personas = [
        {
            "name": "☀️ Morning Enthusiast",
            "recommendation": "Croissant + Latte - Start your day right!",
            "description": "For those who love a balanced, smooth breakfast combo"
        },
        {
            "name": "💪 Energy Booster",
            "recommendation": "Espresso + Pain au Chocolat - Quick energy hit!",
            "description": "For busy mornings when you need a quick boost"
        },
        {
            "name": "🎨 Flavor Explorer",
            "recommendation": "Sourdough + Flat White - Artisan experience!",
            "description": "For those who appreciate complex flavors and craftsmanship"
        },
        {
            "name": "🍫 Sweet Tooth",
            "recommendation": "Danish + Mocha - Chocolate heaven!",
            "description": "For afternoon treats and sweet cravings"
        },
        {
            "name": "🌙 Evening Sipper",
            "recommendation": "Fougasse + Macchiato - Sophisticated choice!",
            "description": "For late afternoon or evening indulgence"
        }
    ]
    
    persona = random.choice(personas)
    return f"""🛍️ **Order Guidance - Find Your Perfect Match!**

**{persona['name']}**
→ {persona['recommendation']}

_{persona['description']}_

**Steps to Order:**
1. Choose your item from the menu
2. Check our stock status
3. Add to cart with quantity
4. Choose payment method (GCash, Maya, or Cash)
5. Proceed to checkout - get PHP 300 signup bonus! 💳

Which combo sounds good to you?"""


# ------------------------------------------------
# DOUGHBOT AI ENGINE
# ------------------------------------------------
def doughbot_ai(prompt):
    text = prompt.lower().strip()

    # Expanded keyword lists
    greetings = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "sup", "yo", "hiya"]
    thanks = ["thanks", "thank you", "appreciate", "ty", "thx"]
    recommend = ["recommend", "suggest", "best", "favorite", "fave"]
    coffee = ["coffee", "espresso", "latte", "cappuccino", "americano", "mocha", "macchiato", "flat white"]
    bread = ["bread", "croissant", "baguette", "brioche", "sourdough", "danish", "fougasse", "pandesal"]
    delivery = ["delivery", "deliver", "shipping"]
    price = ["price", "cost", "how much", "rates", "expensive", "cheap"]
    weather = ["weather", "rain", "sunny", "cloudy", "temperature", "hot", "cold"]
    time = ["time", "what time", "clock", "date", "today", "day"]
    jokes = ["joke", "funny", "laugh", "pun"]
    help_topics = ["help", "what can you do", "capabilities", "assist"]
    general_questions = ["what", "how", "why", "when", "where", "who"]
    food_general = ["food", "eat", "hungry", "recipe", "cook", "cooking", "ingredients"]
    entertainment = ["movie", "music", "game", "book", "tv", "show"]
    tech = ["computer", "phone", "internet", "app", "software", "tech"]
    health = ["health", "exercise", "workout", "diet", "sleep", "stress"]
    random_topics = ["random", "fact", "interesting", "tell me", "something"]
    animals = ["animal", "dog", "cat", "pet", "bird", "fish"]
    sports = ["sport", "football", "basketball", "tennis", "run", "exercise", "game"]
    travel = ["travel", "vacation", "trip", "holiday", "beach", "mountain"]
    music = ["music", "song", "band", "artist", "concert", "listen"]
    books = ["book", "read", "author", "novel", "story"]
    movies = ["movie", "film", "watch", "cinema", "actor", "director"]
    science = ["science", "space", "universe", "physics", "chemistry", "biology"]
    history = ["history", "past", "ancient", "war", "civilization"]
    math = ["math", "mathematics", "number", "calculate", "algebra", "geometry"]
    philosophy = ["philosophy", "think", "meaning", "life", "exist", "wisdom"]

    # Greeting responses
    if any(word in text for word in greetings):
        return random.choice([
            "Bonjour! I'm DoughBot, your friendly AI assistant at Pan de Staku 🥐",
            "Hello! Welcome to Pan de Staku. I'm DoughBot - how can I help?",
            "Hi there! I'm DoughBot, ready to chat about anything from bread to the universe!",
            "Hey! DoughBot here. Bakery expert and general knowledge bot at your service!"
        ])

    # Thanks responses
    if any(phrase in text for phrase in thanks):
        return random.choice([
            "You're welcome! Happy to help anytime 🥐",
            "No problem at all! Come back anytime.",
            "Glad I could help! What's next?",
            "Anytime! That's what I'm here for."
        ])

    # Recommendation (bakery focused but can expand)
    if any(word in text for word in recommend):
        if any(word in text for word in coffee):
            return random.choice([
                "For coffee, I recommend our Latte - smooth and creamy!",
                "Try our Cappuccino - perfect balance of espresso and foam.",
                "Our Mocha is amazing if you like chocolate with your coffee."
            ])
        elif any(word in text for word in bread):
            return random.choice([
                "Our Croissant is buttery and flaky - a classic choice!",
                "Try the Brioche - soft, sweet, and perfect for breakfast.",
                "Sourdough is great if you want something hearty and tangy."
            ])
        else:
            return random.choice([
                "I recommend our Croissant + Latte combo - perfect breakfast!",
                "Try Pain au Chocolat with Mocha - sweet and satisfying.",
                "Brioche with Cappuccino is always a winner!"
            ])

    # Coffee specific
    if any(word in text for word in coffee) and not any(word in text for word in recommend):
        return random.choice([
            "Our coffee selection: Espresso, Americano, Cappuccino, Latte, Mocha, Macchiato, Flat White.",
            "We have everything from strong Espresso to creamy Latte!",
            "Coffee pairings: Brioche with Cappuccino, or Croissant with Latte."
        ])

    # Bread specific
    if any(word in text for word in bread) and not any(word in text for word in recommend):
        return random.choice([
            "Our breads: Croissant, Baguette, Brioche, Pain au Chocolat, Fougasse, Sourdough, Danish, Pandesal.",
            "Fresh baked daily! From flaky Croissants to hearty Sourdough.",
            "Local favorites like Pandesal, plus French classics like Baguette."
        ])

    # Price queries
    if any(word in text for word in price):
        return random.choice([
            "Our items range from ₱25 (Pandesal) to ₱160 (Sourdough).",
            "Coffee: ₱90-₱140, Breads: ₱25-₱160. Ask for specific prices!",
            "Everything is reasonably priced for premium quality!"
        ])

    # Delivery
    if any(word in text for word in delivery):
        return "Yes! We deliver within the city for ₱40 delivery fee 🚚. Available in all our branches!"

    # Weather (general response since we can't access real weather)
    if any(word in text for word in weather):
        return random.choice([
            "I don't have access to current weather, but I hope it's nice where you are!",
            "Weather can be unpredictable! Stay safe out there.",
            "For weather updates, check your local weather app. Meanwhile, enjoy some coffee!"
        ])

    # Time/Date
    if any(word in text for word in time):
        from datetime import datetime
        now = datetime.now()
        return random.choice([
            f"It's currently {now.strftime('%I:%M %p')} here in the Philippines.",
            f"Right now it's {now.strftime('%A, %B %d, %Y at %I:%M %p')}.",
            "Time flies when you're having fun! Or eating good bread 😉"
        ])

    # Jokes
    if any(word in text for word in jokes):
        jokes_list = [
            "Why did the baker go to therapy? He had too many loaf issues! 🥖",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "What did the coffee say to its date? 'You mocha me very happy!' ☕"
        ]
        return random.choice(jokes_list)

    # Help/What can you do
    if any(phrase in text for phrase in help_topics):
        return random.choice([
            "I can help with bakery menu, prices, recommendations, recipes, and general chat! Ask me anything!",
            "From bread pairings to cooking tips, weather chat to jokes - I'm here for it all!",
            "Menu questions, food advice, general knowledge, entertainment - what's on your mind?"
        ])

    # Food/Cooking general
    if any(word in text for word in food_general) and not any(word in text for word in bread + coffee):
        return random.choice([
            "Food is amazing! Want a recipe? Just tell me ingredients or a dish name.",
            "Cooking is my jam! (Pun intended) What are you in the mood for?",
            "I love talking food! Recipes, tips, pairings - let's cook something up!"
        ])

    # Entertainment
    if any(word in text for word in entertainment):
        return random.choice([
            "Entertainment is great! What's your favorite movie/music/book?",
            "I enjoy discussing movies, music, games, and books. What's your latest favorite?",
            "Pop culture is fun! Tell me about your entertainment preferences."
        ])

    # Tech
    if any(word in text for word in tech):
        return random.choice([
            "Tech is fascinating! From apps to AI, what's your tech interest?",
            "I run on technology myself! What tech topic interests you?",
            "Digital world is amazing. Phones, computers, internet - what's your question?"
        ])

    # Health/Fitness
    if any(word in text for word in health):
        return random.choice([
            "Health is important! Eat well, stay active, get good sleep.",
            "Fitness and wellness matter. What's your health goal?",
            "Healthy living includes good food choices and regular exercise!"
        ])

    # Random facts/topics
    if any(word in text for word in random_topics):
        facts = [
            "Did you know? The world's largest pizza was over 13,000 square feet! 🍕",
            "Fun fact: A group of flamingos is called a 'flamboyance'! 🦅",
            "Interesting: Octopuses have three hearts and blue blood! 🐙",
            "Random: Bananas are berries, but strawberries aren't! 🍌"
        ]
        return random.choice(facts)

    # Animals/Pets
    if any(x in text for x in ["animal", "dog", "cat", "pet", "bird", "fish"]):
        return [
            "Pets are wonderful! Dogs, cats, birds - all bring joy.",
            "Animals are amazing. What's your favorite animal?",
            "I love talking about pets! Do you have any furry friends?"
        ]

    # Sports
    if any(x in text for x in ["sport", "football", "basketball", "tennis", "run", "exercise", "game"]):
        return [
            "Sports are exciting! What's your favorite sport to play or watch?",
            "Exercise is great for health. What activities do you enjoy?",
            "From basketball to running - sports keep us active!"
        ]

    # Travel
    if any(x in text for x in ["travel", "vacation", "trip", "holiday", "beach", "mountain"]):
        return [
            "Travel is amazing! Where's your dream destination?",
            "Exploring new places is so enriching. What's your favorite travel memory?",
            "Beaches or mountains? Travel opens up the world!"
        ]

    # Music
    if any(x in text for x in ["music", "song", "band", "artist", "concert", "listen"]):
        return [
            "Music is universal! What's your favorite genre or artist?",
            "Songs can change your mood. What's playing right now?",
            "Concerts are magical. Have you been to any recently?"
        ]

    # Books
    if any(x in text for x in ["book", "read", "author", "novel", "story"]):
        return [
            "Reading is wonderful! What's the last book you enjoyed?",
            "Books take us to new worlds. What's your favorite genre?",
            "Authors create magic. Who are your favorite writers?"
        ]

    # Movies
    if any(x in text for x in ["movie", "film", "watch", "cinema", "actor", "director"]):
        return [
            "Movies are entertaining! What's your favorite film?",
            "Cinema brings stories to life. What genre do you prefer?",
            "Actors and directors create amazing worlds. Who's your favorite?"
        ]

    # Science
    if any(x in text for x in ["science", "space", "universe", "physics", "chemistry", "biology"]):
        return [
            "Science is fascinating! Space, physics, biology - what's your interest?",
            "The universe is full of wonders. What scientific topic intrigues you?",
            "From atoms to galaxies, science explains everything!"
        ]

    # History
    if any(x in text for x in ["history", "past", "ancient", "war", "civilization"]):
        return [
            "History shapes us! What historical period interests you most?",
            "Learning from the past helps us understand the present.",
            "Ancient civilizations, wars, discoveries - history is rich!"
        ]

    # Math
    if any(x in text for x in ["math", "mathematics", "number", "calculate", "algebra", "geometry"]):
        return [
            "Math is the language of the universe! What's your favorite math topic?",
            "Numbers and patterns are everywhere. What math problem are you solving?",
            "From algebra to geometry, math helps us understand patterns!"
        ]

    # Philosophy
    if any(x in text for x in ["philosophy", "think", "meaning", "life", "exist", "wisdom"]):
        return [
            "Deep thoughts! Philosophy explores life's big questions.",
            "What is the meaning of life? Philosophers have pondered this forever.",
            "Wisdom comes from thinking deeply about existence and purpose."
        ]

    # Menu direct question
    if "menu" in text:
        items = ", ".join(menu_items.keys())
        return f"Our menu includes: {items}. All fresh and delicious!"

    # General questions fallback
    if any(word in text for word in general_questions) or "?" in text:
        return random.choice([
            "That's an interesting question! I'm here to help with that.",
            "Good question! Let me think about that for you.",
            "I can try to help with that. What's the context?",
            "That's something I can chat about! Tell me more."
        ])

    # Default engaging fallback
    return random.choice([
        "I'm DoughBot, your friendly AI assistant! I can chat about food, tech, entertainment, or just about anything. What would you like to talk about?",
        "Tell me what's on your mind! From bakery tips to general knowledge, I'm here to help.",
        "I'm up for any conversation! Ask me about menu items, recipes, or whatever interests you.",
        "What's up? I can help with bakery questions, general chat, or even tell you a joke!",
        "I'm DoughBot - bakery expert and general conversationalist. What's your question?"
    ])

def _primary_doughbot_ai(prompt):
    text = prompt.lower().strip()

    greetings = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"]
    thanks = ["thanks", "thank you", "appreciate", "ty"]
    recommend = ["recommend", "suggest", "best", "favorite", "fave", "best pairing"]
    coffee = ["coffee", "espresso", "latte", "cappuccino", "americano", "mocha", "macchiato", "flat white"]
    bread = ["bread", "croissant", "baguette", "brioche", "sourdough", "danish", "fougasse"]
    delivery = ["delivery", "deliver", "shipping"]
    branch = ["branch", "branches", "location", "store", "stores", "where are you", "where located"]
    price = ["price", "cost", "how much", "rates", "pricing", "price check"]
    stock = ["stock", "available", "in stock", "out of stock", "availability", "inventory"]
    pairing = ["pairing", "pair", "goes with", "combo", "together", "with"]
    order = ["order", "how to order", "ordering", "checkout", "purchase", "buy"]
    signup = ["signup", "sign up", "register", "registration", "welcome bonus", "signup bonus", "free 300", "p300"]
    payment = ["payment", "gcash", "maya", "otp", "cash"]
    weather = ["weather", "rain", "sunny", "cloudy", "temperature", "hot", "cold"]
    time = ["time", "what time", "clock", "date", "today", "day"]
    jokes = ["joke", "funny", "laugh", "pun"]
    help_topics = ["help", "what can you do", "capabilities", "assist"]
    food_general = ["food", "eat", "hungry", "recipe", "cook", "cooking"]
    entertainment = ["movie", "music", "game", "book", "tv", "show"]
    tech = ["computer", "phone", "internet", "app", "software", "tech"]
    health = ["health", "exercise", "workout", "diet", "sleep", "stress"]

    combos = [
        ("Croissant", "Latte"),
        ("Brioche", "Cappuccino"),
        ("Pain au Chocolat", "Mocha"),
        ("Sourdough", "Flat White"),
    ]
    combo = random.choice(combos)
    menu_list = ", ".join(menu_items.keys())
    price_min = min(menu_items.values())
    price_max = max(menu_items.values())

    # ✅ PRICE CHECK HANDLER
    if any(x in text for x in price):
        for item in menu_items.keys():
            if item.lower() in text:
                return _get_price_check(item)
        return _get_price_check(text)

    # ✅ STOCK STATUS HANDLER
    if any(x in text for x in stock):
        for item in STOCK_STATUS.keys():
            if item.lower() in text:
                return _get_stock_status(item)
        return _get_stock_status(text)

    # ✅ BEST PAIRINGS HANDLER
    if any(x in text for x in pairing):
        for item in BEST_PAIRINGS.keys():
            if item.lower() in text:
                return _get_best_pairing(item)
        return _get_best_pairing(text)

    # ✅ ORDER GUIDANCE HANDLER
    if any(x in text for x in order):
        return _get_order_guidance()

    if any(x in text for x in greetings):
        return random.choice([
            "Hello! I'm DoughBot 🥐 Ask about prices, stock, pairings, or orders!",
            "Hi there! Welcome to Pan de Staku. How can I help you today?",
            "Hey! DoughBot here. Ready to help with bakery questions!",
            "Bonjour! Ask me about our menu, prices, stock status, or orders!"
        ])

    if any(x in text for x in recommend):
        return random.choice([
            f"My top recommendation: {combo[0]} with {combo[1]}! A perfect balance.",
            f"Try {combo[0]} paired with {combo[1]} - it's our classic combo!",
            "Tell me which bread or coffee you like and I'll recommend the perfect match!"
        ])

    if any(x in text for x in coffee):
        return random.choice([
            "☕ Options: Espresso (₱90), Americano (₱100), Cappuccino (₱120), Latte (₱130), Mocha (₱140), Macchiato (₱115), Flat White (₱125)",
            "7 amazing coffee drinks! Want to know the best pairing for each?",
            "Strong or smooth? Espresso is bold, Latte is creamy. What's your preference?"
        ])

    if any(x in text for x in bread):
        return random.choice([
            "🥐 Breads: Croissant (₱120), Baguette (₱100), Brioche (₱150), Pain au Chocolat (₱140), Fougasse (₱130), Sourdough (₱160), Danish (₱135)",
            "Fresh baked daily! Classic French breads and local favorites.",
            "Buttery, hearty, or sweet? I can recommend what you'll love!"
        ])

    if any(x in text for x in delivery):
        return random.choice([
            "✅ We deliver locally! ₱40 delivery fee. Which branch are you near?",
            "Delivery available to nearby areas! Share your location and I'll confirm.",
            "Making orders convenient! Local delivery available."
        ])

    if any(x in text for x in branch):
        return random.choice([
            f"📍 We're in: {BRANCH_LIST_TEXT}",
            f"Visit us at: {BRANCH_LIST_TEXT}",
            "Which area are you in? We likely have a branch near you!"
        ])

    if any(x in text for x in thanks):
        return random.choice([
            "You're welcome! Need anything else? 🥐",
            "Happy to help! Any other questions?",
            "Anytime! Ready to order?",
            "Glad I could assist. What else can I help with?"
        ])

    if any(x in text for x in signup):
        return random.choice([
            f"🎁 New customers get PHP {SIGNUP_BONUS} wallet credit after registering!",
            f"Register now and get PHP {SIGNUP_BONUS} free credit instantly!",
            "Join us and enjoy PHP 300 welcome bonus on your first order!"
        ])

    if any(x in text for x in payment):
        return random.choice([
            "💳 Payment: GCash, Maya (need mobile + OTP), or 💰 Cash (mobile number only)",
            "Multiple payment options for your convenience!",
            "Flexible payment! Choose what works best."
        ])

    if any(x in text for x in weather):
        return random.choice([
            "☕ Rainy days are perfect for warm coffee and pastries!",
            "☀️ We're open rain or shine!",
            "For weather, check your app. For pan de staku, we're always ready! 🥐"
        ])

    if any(x in text for x in time):
        from datetime import datetime
        now = datetime.now()
        return random.choice([
            f"⏰ It's {now.strftime('%I:%M %p')} - perfect time for coffee and pastry! ☕",
            f"Today: {now.strftime('%A, %B %d, %Y')}",
            "Perfect timing for something delicious!"
        ])

    if any(x in text for x in jokes):
        jokes_list = [
            "Why did the baker go to therapy? Too many loaf issues! 🥖😄",
            "What do you call fake noodles? An impasta! 🍝",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "Coffee joke: You mocha me very happy! ☕💕"
        ]
        return random.choice(jokes_list)

    if any(x in text for x in help_topics):
        return random.choice([
            "I can help with: 💰 Prices, 📦 Stock, 🥐 Pairings, 🛍️ Orders!",
            "Ask about: menu items, prices, stock, pairings, or how to order!",
            "I'm your bakery expert! Need prices, stock, pairings, or order help?"
        ])

    if any(x in text for x in food_general):
        return random.choice([
            "Love food? Ask for recipes! Or let me suggest a pairing with our menu.",
            "Food is amazing! Want a recipe, menu tip, or pairing?",
            "Cooking fan? Share ingredients and I'll create a recipe!"
        ])

    if any(x in text for x in entertainment):
        return random.choice([
            "Entertainment is great! What's your favorite movie, music, or book?",
            "Movies, music, games - what's entertaining you lately?",
            "Love discussing pop culture! What's your latest obsession?"
        ])

    if any(x in text for x in tech):
        return random.choice([
            "Tech is fascinating! What topic interests you?",
            "I'm built on tech! What's your tech question?",
            "Digital world is amazing. What do you want to explore?"
        ])

    if any(x in text for x in health):
        return random.choice([
            "Health matters! Good food & exercise help. Enjoy our treats in moderation! 😊",
            "Wellness is important! Balance is key.",
            "Treat yourself sometimes! 🥐"
        ])

    if "menu" in text:
        return random.choice([
            f"**Our Menu:** {menu_list}",
            "Fresh breads and quality coffee - that's us!",
            "Full menu above! Any specific item you're interested in?"
        ])

    return random.choice([
        "Tell me what you need - prices, stock, pairings, or orders?",
        "Ask about our menu, prices, pairings, or how to order. I'm here!",
        "What can I help with? Try prices, stock, or best pairings!",
        "Any bakery questions or order guidance needed?",
        "From prices to pairings to ordering - I've got you covered! 🥐"
    ])


def _parse_ingredients(text: str) -> list[str]:
    parts = re.split(r"[,\n;]+", text)
    return [p.strip() for p in parts if p.strip()]


def _generate_recipe(query: str) -> str:
    ingredients = _parse_ingredients(query)
    if not ingredients:
        return "Tell me the ingredients or dish name and I will build a recipe."
    style_titles = ["Skillet", "Saute", "One-Pan", "Quick Bowl"]
    flavor_tips = [
        "Add a squeeze of citrus for brightness.",
        "Finish with fresh herbs if you have them.",
        "A splash of broth makes it richer.",
        "A little butter at the end makes it silky.",
    ]
    if len(ingredients) == 1:
        dish = ingredients[0].title()
        tip = random.choice(flavor_tips)
        steps = [
            "Prep and season the main ingredient.",
            "Warm oil in a pan over medium heat.",
            "Cook until browned, then reduce heat and finish gently.",
            "Taste and adjust seasoning.",
            "Serve hot with a simple side.",
        ]
        step_lines = "\n".join([f"{idx}. {step}" for idx, step in enumerate(steps, start=1)])
        return f"""
<div class="recipe-card">
  <h4>🍳 Recipe Idea: {dish}</h4>
  <p><strong>Ingredients:</strong></p>
  <ul>
    <li>{dish}</li>
    <li>Salt</li>
    <li>Pepper</li>
    <li>Oil</li>
  </ul>
  <p><strong>Steps:</strong></p>
  <ol>
    {"".join(f"<li>{step}</li>" for step in steps)}
  </ol>
  <p><em>💡 Tip: {tip}</em></p>
</div>
"""
    title = ingredients[0].title()
    pantry = ["salt", "pepper", "oil"]
    ingredient_lines = "\n".join([f"<li>{item}</li>" for item in ingredients + pantry])
    steps = [
        "Prep and chop all ingredients.",
        "Warm oil in a pan and cook aromatics first.",
        "Add the main ingredients and cook until tender.",
        "Season, stir, and let flavors combine for a few minutes.",
        "Taste, adjust, and serve hot.",
    ]
    if random.choice([True, False]):
        steps = [
            "Prep and portion ingredients.",
            "Sear the main ingredients for color.",
            "Add the rest and cook until fragrant.",
            "Lower heat and let flavors meld.",
            "Finish and serve.",
        ]
    step_lines = "\n".join([f"<li>{step}</li>" for step in steps])
    style = random.choice(style_titles)
    tip = random.choice(flavor_tips)
    return f"""
<div class="recipe-card">
  <h4>🍳 Recipe: Simple {title} {style}</h4>
  <p><strong>Ingredients:</strong></p>
  <ul>
    {ingredient_lines}
  </ul>
  <p><strong>Steps:</strong></p>
  <ol>
    {step_lines}
  </ol>
  <p><em>💡 Tip: {tip}</em></p>
</div>
"""


def _avoid_repeat(response) -> str:
    last = st.session_state.get("last_response")
    if isinstance(response, list):
        choices = response[:]
        if last in choices and len(choices) > 1:
            choices = [item for item in choices if item != last]
        response = random.choice(choices)
    if last and response == last:
        followups = [
            "Want a faster version or a baked version instead?",
            "Tell me your dietary preference and I will adapt it.",
            "If you want a different flavor, give me 2 to 3 ingredients.",
        ]
        response = response + "\n\n" + random.choice(followups)
    st.session_state.last_response = response
    return response


def _recipe_query(text: str) -> str | None:
    match = re.search(r"recipe\s+(?:for|with)\s+(.+)", text)
    if match:
        return match.group(1).strip(" .")
    if "ingredients:" in text:
        return text.split("ingredients:", 1)[1].strip()
    if "recipe" in text:
        cleaned = text.replace("recipe", "").strip(" .")
        return cleaned if cleaned else None
    return None


_base_doughbot_ai = _primary_doughbot_ai


def doughbot_ai(prompt):
    text = prompt.lower().strip()
    recipe_query = _recipe_query(text)
    if recipe_query:
        return _avoid_repeat(_generate_recipe(recipe_query))
    if "recipe" in text and not recipe_query:
        return _avoid_repeat(
            [
                "Tell me the ingredients or dish name and I will build a recipe.",
                "Share ingredients or a dish name and I will create a recipe.",
                "Give me ingredients and I will make a quick recipe.",
            ]
        )
    if "menu" in text or "list" in text:
        items = ", ".join(menu_items.keys())
        return _avoid_repeat(
            [
                f"Our menu includes: {items}.",
                "We serve artisan breads and coffee. Ask about any item.",
            ]
        )
    response = _base_doughbot_ai(prompt)
    return _avoid_repeat(response)


def generate_response(prompt: str) -> str:
    openai_text = _openai_reply()
    if openai_text:
        return openai_text
    return doughbot_ai(prompt)


if st.session_state.pending_recipe_prompt:
    prompt_text = st.session_state.pending_recipe_prompt
    st.session_state.pending_recipe_prompt = None
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    recipe_response = generate_response(prompt_text)
    st.session_state.messages.append({"role": "assistant", "content": recipe_response})

# ------------------------------------------------
# CHAT UI
# ------------------------------------------------
with col2:

    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    st.markdown(f"### 🤖 Chat with {CHATBOT_NAME}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Ask DoughBot something...")

    if user_prompt:

        st.session_state.messages.append({
            "role":"user",
            "content":user_prompt
        })

        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):

            with st.spinner("DoughBot is thinking..."):
                time.sleep(1)

                response = generate_response(user_prompt)

                st.write(response)

        st.session_state.messages.append({
            "role":"assistant",
            "content":response
        })

    st.markdown("</div>", unsafe_allow_html=True)
