import streamlit as st
import requests
from PIL import Image

# Load secrets
SLACK_WEBHOOK_URL = st.secrets["SLACK_WEBHOOK_URL"]

# Load your image
profile_image = Image.open("feldpic.jpg")  # Ensure this is in the same folder or provide full path

# Streamlit page setup
st.set_page_config(page_title="Group Chat Plug", page_icon="💬", layout="centered")

# Top: profile photo + intro
st.image(profile_image, width=200)
st.title("💬 Group Chat Plug")

st.markdown("""
Hi, I'm **Yonah** 👋  
When I moved to Israel, I found tremendous benefit in local group chats — but I *hated* finding them.

So I have now (and I'm not exaggerating) **thousands of group chats**, all organized by city and interest, and I want to share them with you.

Just let me know **where** you are and **what you're looking for**, and I’ll email you a link to join.
""")

st.markdown("---")

# Form input
city = st.text_input("🌍 What city are you in?", placeholder="e.g. Tel Aviv, Haifa, Jerusalem")
email = st.text_input("📧 Your email (so I can send you the link)", placeholder="you@example.com")

st.markdown("💡 Here are some examples of group I have, but I'm not joking when I say I have thousands")
st.markdown("""
- **Sports** → Tennis, Basketball, Surfing  
- **Hobbies** → Photography, Hiking, Baking  
- **Services** → Babysitting, Plumbing, Pets  
- **Jobs** → Tech, Healthcare, Education  
- **Apartments** → Roommates, Sublets, For Rent  
""")

interest = st.text_area("💭 What are you looking for?", placeholder="e.g. 'Looking for a volleyball group in Tel Aviv'")

# Submission
if st.button("Send Request"):
    if not email.strip():
        st.error("Email is required.")
    elif not city.strip() or not interest.strip():
        st.error("Please complete all fields.")
    else:
        message = f"""
📍 *City*: {city.strip()}
📧 *Email*: {email.strip()}
🔍 *Request*: {interest.strip()}
"""

        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})

        if response.status_code == 200:
            st.success("Got it! I’ll get back to you with a group chat link ASAP 💌")
        else:
            st.error(f"Slack API error: {response.status_code} - {response.text}")
