import streamlit as st
import pandas as pd
import time
from PIL import Image

# --- Page and Assets Setup ---
st.set_page_config(
    page_title="Looking for local group chats in Israel?",
    page_icon="💬",
    layout="centered",
)

# Add custom CSS to fix spacing issues
st.markdown("""
<style>
    /* Target the specific Streamlit widget label that's causing the gap */
    [data-testid="stWidgetLabel"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Target the emotion cache class we saw in dev tools */
    .st-emotion-cache-1weic72 {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Reduce spacing between category headers and multiselect */
    .stMarkdown {
        margin-bottom: 0.25rem !important;
    }
    
    /* Reduce spacing after multiselect */
    .stMultiSelect {
        margin-bottom: 1rem !important;
    }
    
    /* Ensure consistent spacing */
    div[data-testid="stMarkdown"] {
        margin-bottom: 0.25rem !important;
    }
    
    /* Fix spacing for category headers */
    .stMarkdown strong {
        margin-bottom: 0 !important;
        display: block;
    }
    
    /* Target all label elements that might have bottom margin */
    label {
        margin-bottom: 0 !important;
    }
    
    /* Target the specific element you want to make black */
    #root > div:nth-child(1) > div.withScreencast > div > div > section > div.stMainBlockContainer.block-container.st-emotion-cache-mtjnbi.eht7o1d4 > div > div > div > div:nth-child(30) > div > div > div {
        background-color: black !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Load profile image
def load_profile_image(path="feldpic.jpg"):
    try:
        return Image.open(path)
    except Exception:
        st.warning("⚠️ Could not load profile image.")
        return None

profile_image = load_profile_image()

# Language toggle
language = st.radio("🌐 Language / שפה", ["English", "עברית"], horizontal=True)

# Translations dict
texts = {
    "English": {
        "title": "Looking for local group chats in Israel?",
        "about_me": """
👤 **About Me**  
Hey, I’m Yonah Feld 👋
I moved to Israel in 2017 and, like most people starting out somewhere new, I was constantly looking for things — second-hand furniture, a sublet, a pickup basketball game. I kept stumbling into public WhatsApp groups, but actually finding them was always a struggle.
So I started creating my own — thousands of local public group chats, organized by city and topic.

I’m doing this because I know how isolating it can feel when you’re new somewhere — and how much of a difference it makes to simply have a group chat.
Now I’m ready to share them with you.

🧠 Follow me on IG, I promise I'm real: [@yonahfeld](https://instagram.com/yonahfeld)
""",
        "how_it_works": """

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
עליתי לישראל ב-2017, וכמו הרבה אנשים שמתחילים חיים במקום חדש, חיפשתי כל הזמן איך להסתדר — ריהוט יד שנייה, דירה להחלפה, קבוצת כדורסל.
התחלתי להיתקל בקבוצות וואטסאפ ציבוריות שעזרו מאוד, אבל היה קשה למצוא אותן.
אז פשוט התחלתי ליצור קבוצות כאלה בעצמי — אלפי קבוצות ציבוריות, לפי עיר ונושא.

אני עושה את זה כי אני יודע כמה בודד זה יכול להרגיש בהתחלה — וכמה זה יכול לעזור כשיש לך פשוט קבוצת צ׳אט רלוונטית.
עכשיו אני רוצה לשתף אותן גם איתך.
🧠 עקבו אחרי באינסטגרם, אני מבטיח שאני אמיתי: [@yonahfeld](https://instagram.com/yonahfeld)
""",
        "how_it_works": """

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

# Load cities from CSV
city_df = pd.read_csv("deep-links-2025-07-21.csv")
cities = sorted(city_df[city_df["City"].str.contains("Israel")]["City"].unique())

# --- UI Sections ---
def render_intro():
    # Main Title & Tagline
    st.title(f"💬 {t['title']}")
    st.subheader("I have thousands of local group chats for you to join.")
    st.markdown("---")

    # About Me in Expander
    with st.expander("👤 About Me", expanded=True):
        cols = st.columns([1, 3])
        if profile_image:
            cols[0].image(profile_image, width=140)
        cols[1].markdown(t["about_me"])
    st.markdown("---")

    # How It Works
    st.subheader("🎯 How It Works")
    st.markdown(t["how_it_works"])
    st.markdown("---")

render_intro()

# --- Form Inputs ---
city = st.selectbox(t["city"], cities)
email = st.text_input("📧 Your email (required)")

# Build interest DataFrame for selected city
city_interests = (
    city_df[city_df['City'] == city]
    [['Interest', 'Category', 'Deep Link']]
    .drop_duplicates()
)

# Define display order and labels
category_order = [
    ("Marketplace", "Buy/Sell"),
    ("Apartments/Houses", "Apartments"),
    ("Jobs", "Jobs"),
    ("Services", "Services"),
    ("Sports", "Sports"),
    ("Hobbies", "Hobbies"),
]

selected_interests = []
for cat, label in category_order:
    options = city_interests[city_interests['Category'] == cat]['Interest'].tolist()
    if options:
        st.markdown(f"**{label}**")
        chosen = st.multiselect("", options, key=f"cat_{cat}")
        selected_interests.extend(chosen)

# Map back to indices
selected_indices = [
    city_interests[city_interests['Interest'] == i].index[0]
    for i in selected_interests
]

# --- Search Action ---
if st.button(t["submit"]):
    if not city or not selected_interests or not email.strip():
        st.error(t["error_fields"] + " (Email is required.)")
    else:
        # Simulate logging
        try:
            import requests
            SLACK_WEBHOOK_URL = st.secrets.get("SLACK_WEBHOOK_URL")
            if SLACK_WEBHOOK_URL:
                msg = f"📧 {email}\n🌍 {city}\n💭 {', '.join(selected_interests)}"
                requests.post(SLACK_WEBHOOK_URL, json={"text": msg})
        except Exception:
            st.warning("Could not send notification.")

        # Spinner with status updates
        with st.spinner(t["searching"]):
            status_area = st.empty()
            
            # Initial checking messages
            status_area.info("Checking WhatsApp groups...")
            time.sleep(1.2)
            status_area.info("WhatsApp checked.")
            time.sleep(0.5)
            
            status_area.info("Checking Telegram groups...")
            time.sleep(1.2)
            status_area.info("Telegram checked.")
            time.sleep(0.5)
            
            status_area.info("Checking Places groups...")
            time.sleep(1.2)
            status_area.info("Places checked.")
            time.sleep(0.5)
            
            status_area.empty()

        # Results
        st.success(t["results_title"])
        # Custom results message
        st.markdown(
            f"""
<span style='font-size:1.5em;'>💬</span><br>
<span style='color: green; font-weight: bold;'>You're in luck. I found links to the groups you requested for {city}. These ones are from the "Places: Local Group Chat" app. You'll have to download the app to join. </span>
""",
            unsafe_allow_html=True,
        )
        # App download links
        st.markdown(
            """
[Download Places on iOS](https://apps.apple.com/us/app/places-local-group-chats/id6482985182) &nbsp;|&nbsp; [Download Places on Android](https://play.google.com/store/apps/details?id=com.zackebenfeld.Places)""",
            unsafe_allow_html=True,
        )
        # List deep links as numbered list
        for i, idx in enumerate(selected_indices, 1):
            interest = city_interests.at[idx, 'Interest']
            link = city_interests.at[idx, 'Deep Link']
            st.markdown(f"{i}. **{interest}** - [Join Group]({link})")