import streamlit as st
import requests
from PIL import Image

# Load secrets
SLACK_WEBHOOK_URL = st.secrets["SLACK_WEBHOOK_URL"]

# Load your image
profile_image = Image.open("feldpic.jpg")  # Ensure this is in the same folder or provide full path

# Streamlit page setup
st.set_page_config(page_title="Group Chat Plug", page_icon="💬", layout="centered")

# Language toggle
language = st.radio("🌐 Language / שפה", ["English", "עברית"], horizontal=True)

# Translations
texts = {
    "English": {
        "title": "💬 Israeli Group Chat Finder",
        "intro": """
Hi, I'm **Yonah** 👋  
When I moved to Israel, I found tremendous benefit in local group chats — but I *hated* finding them.

So I have now (and I'm not exaggerating) **thousands of group chats**, all organized by city and interest, and I want to share them with you.

Just let me know **where** you are and **what you're looking for**, and I’ll email you a link to a group chat.
""",
        "city": "🌍 What city are you in?",
        "city_ph": "e.g. Tel Aviv, Haifa, Jerusalem",
        "email": "📧 Your email (so I can send you the link. Don't use the Hide Email feature!)",
        "email_ph": "you@example.com",
        "examples_title": "💡 Here are some examples of group I have, but I'm not joking when I say I have thousands",
        "examples": """
- **Sports** → Tennis, Basketball, Surfing  
- **Hobbies** → Photography, Hiking, Baking  
- **Services** → Babysitting, Plumbing, Pets  
- **Jobs/Networking** → Tech, Healthcare, Education  
- **Apartments** → Roommates, Sublets, For Rent  
- **Buy/Sell** → Furniture, Clothing, Free Stuff
""",
        "interest": "💭 What are you looking for?",
        "interest_ph": "e.g. 'Looking for a volleyball group in Tel Aviv'",
        "submit": "Send Request",
        "error_email": "Email is required.",
        "error_fields": "Please complete all fields.",
        "success": "Got it! I’ll get back to you with a group chat link ASAP 💌"
    },
    "עברית": {
        "title": "💬 מחפש קבוצת צ'אט",
        "intro": """
היי, אני **יונה** 👋  
כשעברתי לישראל, מצאתי המון ערך בקבוצות צ'אט מקומיות — אבל שנאתי לחפש אותן.

אז עכשיו יש לי (ואני לא מגזים) **אלפי קבוצות**, מסודרות לפי עיר ותחום עניין — ואני רוצה לשתף אותן איתך.

רק תגיד לי **איפה אתה נמצא** ו**מה אתה מחפש**, ואני אשלח לך קישור להצטרף.
""",
        "city": "🌍 באיזו עיר אתה?",
        "city_ph": "לדוגמה: תל אביב, חיפה, ירושלים",
        "email": "📧 האימייל שלך ( 'Hide Email'כדי שאוכל לשלוח לך את הקישור — אל תשתמש ב)",
        "email_ph": "you@example.com",
        "examples_title": "💡 הנה כמה דוגמאות לקבוצות שיש לי, אבל באמת יש לי אלפים",
        "examples": """
- **ספורט**: טניס, כדורסל, גלישה  
- **תחביבים**: צילום, טיולים, אפייה  
- **שירותים**: בייביסיטר, אינסטלטור, חיות  
- **עבודה/נטוורקינג**: הייטק, חינוך, בריאות  
- **דירות**: שותפים, להשכרה, סאבלט  
- **קנייה / מכירה / למסירה**: ריהוט, בגדים, חינם
""",
        "interest": "💭 מה אתה מחפש?",
        "interest_ph": "לדוגמה: 'מחפש קבוצה של כדורעף בתל אביב'",
        "submit": "שלח בקשה",
        "error_email": "חייבים למלא אימייל.",
        "error_fields": "נא למלא את כל השדות.",
        "success": "מעולה! אשלח לך קישור להצטרף בהקדם 💌"
    }
}

# Use current language block
t = texts[language]

# UI
st.image(profile_image, width=200)
st.title(t["title"])
st.markdown(t["intro"])
st.markdown("---")

# Inputs
city = st.text_input(t["city"], placeholder=t["city_ph"])
email = st.text_input(t["email"], placeholder=t["email_ph"])

st.markdown(t["examples_title"])
st.markdown(t["examples"])

interest = st.text_area(t["interest"], placeholder=t["interest_ph"])

# Submit
if st.button(t["submit"]):
    if not email.strip():
        st.error(t["error_email"])
    elif not city.strip() or not interest.strip():
        st.error(t["error_fields"])
    else:
        message = f"""
📍 *City*: {city.strip()}
📧 *Email*: {email.strip()}
🔍 *Request*: {interest.strip()}
"""
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})

        if response.status_code == 200:
            st.success(t["success"])
        else:
            st.error(f"Slack API error: {response.status_code} - {response.text}")
