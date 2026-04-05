import streamlit as st
import requests
import urllib.parse
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

MODEL = "models/gemini-2.0-flash"

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

st.markdown("# 🏥 DURGA PSYCHIATRIC CENTRE")
st.markdown("## 🧠 AI Mental Health Assistant")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= OFFLINE AI =================
def offline_response(text):

    text = text.lower()

    responses = {
        "stress": [
            "It sounds like you're under a lot of pressure. Try taking a few slow breaths and focus on one small task at a time.",
            "Stress can feel overwhelming. A short break and deep breathing can help calm your mind."
        ],
        "anxiety": [
            "Anxiety often comes with racing thoughts. Try grounding yourself by noticing 5 things around you.",
            "You're not alone. Slow breathing can reduce anxiety quickly."
        ],
        "anger": [
            "Anger is natural. Pause, step away, and allow yourself time before reacting.",
            "Take a deep breath. Responding calmly is more powerful than reacting instantly."
        ],
        "depression": [
            "I'm sorry you're feeling this way. Even small steps like talking to someone can help.",
            "You matter. Try doing one small positive activity today."
        ],
        "default": [
            "I'm here for you. Can you tell me a bit more about what you're experiencing?",
            "That sounds important. I'm listening."
        ]
    }

    for key in responses:
        if key in text:
            return random.choice(responses[key])

    return random.choice(responses["default"])


# ================= HTTP SESSION =================
def get_session():
    s = requests.Session()
    retries = Retry(total=1, backoff_factor=0.3)
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("https://", adapter)
    return s

HTTP = get_session()

# ================= ONLINE AI =================
def online_response(prompt):

    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are a psychologist. Give short helpful advice.\nUser: {prompt}"}
                ]
            }
        ]
    }

    try:
        res = HTTP.post(url, json=payload, timeout=(2, 6))

        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None

    return None


# ================= SMART AI =================
def smart_ai(prompt):

    # ⚡ INSTANT response first
    instant = offline_response(prompt)

    # 🔁 Try improving with real AI (non-blocking feel)
    api_reply = online_response(prompt)

    if api_reply:
        return api_reply  # better answer

    return instant  # fallback instantly


# ================= CHAT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area(
        "Tell me what you're feeling:",
        placeholder="Example: I feel stressed due to work pressure"
    )

    send = st.form_submit_button("Send")

    if send and user_input.strip():

        st.session_state.messages.append(("You", user_input))

        # ⚡ instant response
        reply = smart_ai(user_input)

        st.session_state.messages.append(("Assistant", reply))


# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")


# ================= BOOKING =================
st.markdown("---")
st.subheader("📅 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

concern = st.selectbox(
    "Select Your Concern",
    ["Stress", "Anxiety", "Depression", "Relationship Issue", "Addiction", "Other"]
)

# ================= WHATSAPP =================
if name and phone:

    message = f"""Hello Durga Psychiatric Centre,

New Consultation Request:

Name: {name}
Phone: {phone}
Concern: {concern}

Please contact me."""

    encoded = urllib.parse.quote(message)
    link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

    st.markdown(
        f"""
        <a href="{link}" target="_blank">
        <div style="
            background-color:#25D366;
            padding:16px;
            border-radius:10px;
            text-align:center;
            font-size:18px;
            font-weight:bold;
            color:white;
        ">
        💬 Book via WhatsApp
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Fill details to enable WhatsApp booking")