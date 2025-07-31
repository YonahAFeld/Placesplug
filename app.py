import streamlit as st
import pandas as pd
import time

from PIL import Image

# Load your image
profile_image = Image.open("feldpic.jpg")  # Ensure this is in the same folder or provide full path

# Streamlit page setup
st.set_page_config(page_title="Looking for local group chats in Israel?", page_icon="💬", layout="centered")

# Language toggle
language = st.radio("🌐 Language / שפה", ["English", "עברית"], horizontal=True)

# Translations
texts = {
    "English": {
        "title": "Looking for local group chats in Israel?",
        "about_me": """
👤 **About Me**  
Hi, I'm Yonah Feld 👋  
I made Aliyah in 2017, and like many new arrivals, I had to figure out everything from scratch — finding furniture, pickup basketball games, sublets, Hebrew tutors, you name it.  
Over time, I started stumbling across public WhatsApp and Telegram groups that made life so much easier. Local group chats are one of Israel's most powerful (but hidden) resources.

So I created thousands of group chats all organized by city and topic and I want to share them with you.

🧠 Follow me on IG, I promise I'm real: [@yonahfeld](https://instagram.com/yonahfeld)
""",
  
        "how_it_works": """
🎯 **How it works**  
1. Pick your city  
2. Pick what you need  
3. Get links instantly
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
        "about_me": """
👤 **אודותיי**  
היי, אני יונה פלד 👋  
עליתי לארץ ב-2017, וכמו הרבה עולים חדשים, הייתי צריך להבין הכל מאפס — מציאת רהיטים, משחקי כדורסל מזדמנים, דירות זמניות, מורים לעברית, הכל.  
עם הזמן, התחלתי להיתקל בקבוצות וואטסאפ וטלגרם ציבוריות שהפכו את החיים להרבה יותר קלים. קבוצות צ'אט מקומיות הן אחד המשאבים החזקים ביותר (אבל נסתרים) של ישראל.

אז יצרתי אלפי קבוצות צ'אט מסודרות לפי עיר ונושא ואני רוצה לשתף אותן איתך.

🧠 עקבו אחרי באינסטגרם, אני מבטיח שאני אמיתי: [@yonahfeld](https://instagram.com/yonahfeld)
""",
       
        "how_it_works": """
🎯 **איך זה עובד**  
1. בחר את העיר שלך  
2. בחר מה אתה צריך  
3. קבל קישורים מיד
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
    # Create two columns for photo and about me
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(profile_image, width=200)
    
    with col2:
        st.markdown(t["about_me"])
    
    st.markdown("")  # Add some space
    st.title(t["title"])
    st.markdown("")  # Add space after title
    st.markdown(t["how_it_works"])
    st.markdown("")  # Add space before divider
    st.markdown("---")
    st.markdown("")  # Add space after divider

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

# Grouped multiselect with headings
selected_interests = []
category_to_interests = {cat: city_interest_df[city_interest_df['Category'] == cat]['Interest'].tolist() for cat, _ in category_order}
for cat, cat_display in category_order:
    options = category_to_interests.get(cat, [])
    if options:
        st.markdown(f"**{cat_display}**")
        selected = st.multiselect("", options, key=f"cat_{cat}")
        selected_interests.extend(selected)
selected_indices = [city_interest_df[city_interest_df['Interest'] == interest].index[0] for interest in selected_interests]

import requests

if st.button(t["submit"]):
    if not city or not selected_interests or not email.strip():
        st.error(t["error_fields"] + " (Email is required.)")
    else:
        # Send Slack webhook
        try:
            SLACK_WEBHOOK_URL = st.secrets["SLACK_WEBHOOK_URL"]
            interests_str = ', '.join(selected_interests)
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
<div style='direction: rtl; text-align: right; background-color: #f0f4fa; border-radius: 12px; padding: 18px 24px; margin-bottom: 18px; border: 1px solid #e0e6ed;'>
<span style='font-size: 2em;'>💬</span><br>
<b>לא מצאנו קבוצות וואטסאפ או טלגרם</b><br>
אבל הנה כל קבוצות הצ'אט עבור <b>{city}</b>!
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style='background-color: #f0f4fa; border-radius: 12px; padding: 18px 24px; margin-bottom: 18px; border: 1px solid #e0e6ed;'>
<span style='font-size: 2em;'>💬</span><br>
<b>We couldn't find any WhatsApp or Telegram group chats</b><br>
But here are all group chats for <b>{city}</b>!
</div>
""", unsafe_allow_html=True)

        # Show app download links
        st.markdown("""
**You'll have to download this free app to join:**  
[<img src='https://upload.wikimedia.org/wikipedia/commons/6/67/App_Store_%28iOS%29.svg' width='24' style='vertical-align:middle'/> iOS](https://apps.apple.com/us/app/places-local-group-chats/id6482985182)  
[<img src='https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg' width='24' style='vertical-align:middle'/> Android](https://play.google.com/store/apps/details?id=com.zackebenfeld.Places&pcampaignid=web_share)
""", unsafe_allow_html=True)
        for idx in selected_indices:
            interest = city_interest_df.loc[idx, 'Interest']
            link = city_interest_df.loc[idx, 'Deep Link']
            st.markdown(f"**{interest}**: [Join Group]({link})")
