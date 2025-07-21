import streamlit as st
import pandas as pd
import time

from PIL import Image

# Load your image
profile_image = Image.open("feldpic.jpg")  # Ensure this is in the same folder or provide full path

# Streamlit page setup
st.set_page_config(page_title="Israeli Group chat Finder", page_icon="💬", layout="centered")

# Language toggle
language = st.radio("🌐 Language / שפה", ["English", "עברית"], horizontal=True)

# Translations
texts = {
    "English": {
        "title": "💬 Israeli Group Chat Finder",
        "intro": """
Hi, I'm **Yonah** 👋  
When I moved to Israel, I found tremendous benefit in local group chats — but I *hated* finding them.

So I created (and I'm not exaggerating) **thousands of group chats**, all organized by city and interest, and now I want to share them with you.

Just tell me **where you are** and **what you're interested in**, and I'll instantly show you links to relevant group chats — no email, no waiting, just click and join!
""",
        "city": "🌍 Which city are you in?",
        "interest": "💭 What kind of group chats are you looking for? Select all that apply.",
        "submit": "Show Me Group Links",
        "error_fields": "Please select a city and at least one group chat.",
        "searching": "Searching for the best WhatsApp groups...",
        "searching2": "Now checking Telegram groups...",
        "results_title": "Your group chat links are ready!"
    },
    "עברית": {
        "title": "💬 מחפש קבוצת צ'אט",
        "intro": """
היי, אני **יונה** 👋  
כשעברתי לישראל, מצאתי המון ערך בקבוצות צ'אט מקומיות — אבל היה קשה למצוא אותן.

אז יצרתי (באמת!) **אלפי קבוצות**, מסודרות לפי עיר ותחום עניין — ואני רוצה לשתף אותן איתך.

פשוט תבחר **איפה אתה גר** ו**מה מעניין אותך**, ותקבל מיד קישורים לקבוצות — בלי אימייל, בלי לחכות, רק לבחור ולהצטרף!
""",
        "city": "🌍 באיזו עיר אתה?",
        "interest": "💭 אילו קבוצות מעניינות אותך? בחר כמה שתרצה.",
        "submit": "הצג קישורים לקבוצות",
        "error_fields": "נא לבחור עיר ולפחות קבוצה אחת.",
        "searching": "מחפש את קבוצות הוואטסאפ הכי טובות...",
        "searching2": "בודק גם קבוצות טלגרם...",
        "results_title": "הקישורים שלך מוכנים!"
    }
}

t = texts[language]

# Load cities from CSV for dropdown
city_df = pd.read_csv("deep-links-2025-07-21.csv")
cities = sorted(city_df[city_df["City"].str.contains("Israel")]["City"].drop_duplicates())

# Remove the examples markdown from the UI
def render_intro():
    st.image(profile_image, width=200)
    st.title(t["title"])
    st.markdown(t["intro"])
    st.markdown("---")

render_intro()

# Inputs
city = st.selectbox(t["city"], cities)
email = st.text_input("📧 Your email (required)")

# Get interests for the selected city
city_interest_df = city_df[city_df["City"] == city][["Interest", "Category", "Deep Link"]].drop_duplicates()

# Define category order and display names
category_order = [
    ("Marketplace", "Buy/Sell"),
    ("Apartments/Houses", "Apartments"),
    ("Jobs", "Jobs"),
    ("Services", "Services"),
    ("Sports", "Sports"),
    ("Hobbies", "Hobbies"),
]
category_order_dict = {cat: i for i, (cat, _) in enumerate(category_order)}
category_display_dict = dict(category_order)

# Prepare display options
interest_options = []
for _, row in city_interest_df.iterrows():
    cat = row["Category"]
    interest = row["Interest"]
    display = f"[{category_display_dict.get(cat, cat)}] {interest}"
    interest_options.append((category_order_dict.get(cat, 99), display, interest, row["Deep Link"]))

# Sort by category order, then interest
interest_options.sort()
multiselect_labels = [x[1] for x in interest_options]
multiselect_values = [x[2] for x in interest_options]
multiselect_links = [x[3] for x in interest_options]

# Remove st.markdown(t["examples_title"])
# Remove st.markdown(t["examples"])

selected_labels = st.multiselect(t["interest"], multiselect_labels, format_func=lambda x: x, help="Choose one or more group chats", key="interest_multiselect")
selected_indices = [multiselect_labels.index(lbl) for lbl in selected_labels]

import requests

if st.button(t["submit"]):
    if not city or not selected_labels or not email.strip():
        st.error(t["error_fields"] + " (Email is required.)")
    else:
        # Send Slack webhook
        try:
            SLACK_WEBHOOK_URL = st.secrets["SLACK_WEBHOOK_URL"]
            interests_str = ', '.join([multiselect_values[idx] for idx in selected_indices])
            message = f"""
📧 *Email*: {email.strip()}
🌍 *City*: {city}
💭 *Requested Groups*: {interests_str}
"""
            requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        except Exception as e:
            st.warning(f"Could not send Slack notification: {e}")

        with st.spinner(t["searching"]):
            status_area = st.empty()
            status_area.info("Checking for WhatsApp groups...")
            time.sleep(1.5)
            status_area.info("Checking for Telegram groups...")
            time.sleep(1.5)
            status_area.empty()
        st.success(t["results_title"])
        if language == "עברית":
            st.markdown(f"""
<div style='direction: rtl; text-align: right;'>
לא מצאתי קישורים לוואטסאפ או טלגרם...<br>
<b>{city}</b><br>
אבל הנה קישורים לקבוצות רלוונטיות שכדאי לבדוק.<br>
כדי להצטרף, תוריד את האפליקציה <b>'Places: Local Group Chats'</b>!
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
I didn't find WhatsApp or Telegram links...<br>
**{city}**<br>
But here are links to relevant group chats that you should check out.<br>
Be sure to download the app <b>Places: Local Group Chats</b> to join!
""", unsafe_allow_html=True)
        for idx in selected_indices:
            interest = multiselect_values[idx]
            link = multiselect_links[idx]
            st.markdown(f"**{interest}**: [Join Group]({link})")
