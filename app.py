import streamlit as st
import requests
import urllib.parse
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

PRIMARY_MODEL = "models/gemini-2.0-flash"
FALLBACK_MODELS = [
    "models/gemini-2.0-flash-001",
    "models/gemini-flash-latest",
    "models/gemini-1.5-flash"
]

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

st.markdown("# 🏥 DURGA PSYCHIATRIC CENTRE")
st.markdown("## 🧠 AI Mental Health Assistant")

# ================= SAFE SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= HTTP SESSION WITH RETRY =================
def build_session():
    session = requests.Session()
    retries = Retry(
        total=2,                # small retry to avoid delays
        backoff_factor=0.5,     # quick retry
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

HTTP = build_session()

# ================= CORE CALL =================
def call_model(model, prompt):
    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are a calm psychologist. Give short helpful advice.\nUser: {prompt}"}
                ]
            }
        ]
    }

    try:
        # 🔥 split timeout (connect, read)
        res = HTTP.post(url, json=payload, timeout=(3, 10))

        if res.status_code != 200:
            return None

        data = res.json()

        # 🛡️ SAFE PARSING
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        return None

    return None


# ================= AI ENGINE =================
def ask_ai(prompt):

    # ⚡ primary (fast)
    result = call_model(PRIMARY_MODEL, prompt)
    if result:
        return result

    # 🔁 quick retry same model
    result = call_model(PRIMARY_MODEL, prompt)
    if result:
        return result

    # 🔁 fallback models
    for model in FALLBACK_MODELS:
        result = call_model(model, prompt)
        if result:
            return result

    return "⚠️ AI is busy right now. Please try again in a few seconds."


# ================= CHAT =================
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Tell me what you're feeling:",
        placeholder="Example: I feel stressed due to work pressure"
    )

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append(("You", user_input))

        try:
            with st.spinner("Thinking..."):
                reply = ask_ai(user_input)
        except Exception:
            reply = "⚠️ Temporary issue. Please try again."

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
            margin-top:10px;
        ">
        💬 Book via WhatsApp
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Fill details to enable WhatsApp booking")