import streamlit as st
import pandas as pd
import time
import random

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

.stApp{
background:
radial-gradient(circle at 20% 20%, rgba(255,224,178,0.35), transparent 40%),
linear-gradient(135deg,#3E2723,#6D4C41,#D7A86E);
background-attachment:fixed;
}

h1,h2,h3,p{
color:white;
}

.chat-card{
background: rgba(255,255,255,0.12);
padding:18px;
border-radius:15px;
backdrop-filter: blur(8px);
box-shadow:0 5px 25px rgba(0,0,0,0.3);
}

.menu-card{
background: rgba(255,255,255,0.18);
padding:20px;
border-radius:15px;
}

.stChatMessage{
border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# CHATBOT NAME
# ------------------------------------------------
CHATBOT_NAME = "DoughBot"

# ------------------------------------------------
# MENU DATA
# ------------------------------------------------
menu_items = {
    "🥐 Croissant":120,
    "🍞 Baguette":100,
    "🥖 Brioche":150,
    "🥯 Pain au Chocolat":140,
    "☕ Espresso":90,
    "☕ Latte":130,
    "☕ Cappuccino":120
}

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {}

# ------------------------------------------------
# HEADER
# ------------------------------------------------
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

    st.markdown("### 📋 Bakery Menu")

    df = pd.DataFrame(menu_items.items(), columns=["Item","Price"])
    df["Price"] = df["Price"].apply(lambda x: f"₱{x}")

    st.dataframe(df, use_container_width=True)

    st.markdown("### ⭐ Popular Combo")

    st.info("""
🥐 Croissant + ☕ Latte  
Perfect buttery breakfast combo.
""")

# ------------------------------------------------
# DOUGHBOT AI ENGINE
# ------------------------------------------------
def doughbot_ai(prompt):

    text = prompt.lower()

    greetings = ["hello","hi","hey","good morning","good evening"]
    thanks = ["thanks","thank you"]
    recommend = ["recommend","suggest","best"]
    coffee = ["coffee","espresso","latte","cappuccino"]
    bread = ["bread","croissant","baguette","brioche"]
    delivery = ["delivery","deliver"]
    price = ["price","cost","how much"]

    # Greeting
    if any(x in text for x in greetings):
        return random.choice([
            "Bonjour! I'm **DoughBot**, your bakery assistant 🥐",
            "Hello! Welcome to **Pan de Staku**. What would you like today?",
            "Hi there! Looking for fresh bread or coffee?"
        ])

    # Recommendation
    if any(x in text for x in recommend):
        return """
I recommend this combo:

🥐 **Croissant**  
☕ **Latte**

It’s our **most loved breakfast pair**.
"""

    # Coffee
    if any(x in text for x in coffee):
        return """
Our coffee selection includes:

☕ Espresso  
☕ Latte  
☕ Cappuccino

Best pairing: **Brioche + Cappuccino**
"""

    # Bread
    if any(x in text for x in bread):
        return """
Our artisan breads:

🥐 Croissant  
🍞 Baguette  
🥖 Brioche  
🥯 Pain au Chocolat
"""

    # Price
    if any(x in text for x in price):
        return "Our items range between **₱90 and ₱150**."

    # Delivery
    if any(x in text for x in delivery):
        return "Yes! We deliver within the city for **₱40 delivery fee 🚚**."

    # Thanks
    if any(x in text for x in thanks):
        return "You're welcome! Enjoy Pan de Staku 🥐"

    # Menu direct question
    if "menu" in text:
        items = ", ".join(menu_items.keys())
        return f"Our menu includes: {items}"

    # fallback
    return """
I'm **DoughBot 🤖**

Try asking me things like:

• "Recommend a breakfast combo"
• "What breads do you have?"
• "Do you offer delivery?"
• "What coffee goes with croissant?"
"""

# ------------------------------------------------
# CHAT UI
# ------------------------------------------------
with col2:

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

                response = doughbot_ai(user_prompt)

                st.write(response)

        st.session_state.messages.append({
            "role":"assistant",
            "content":response
        })