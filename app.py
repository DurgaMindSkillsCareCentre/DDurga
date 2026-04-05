import streamlit as st
import requests
import urllib.parse
import time

# ================= CONFIG =================
API_KEY = st.secrets["GEMINI_API_KEY"]
WHATSAPP_NUMBER = "917395944527"

# ⚡ FAST FIRST MODEL (VERY IMPORTANT)
PRIMARY_MODEL = "models/gemini-2.0-flash"

# 🔁 FALLBACK MODELS (ONLY IF FAIL)
FALLBACK_MODELS = [
    "models/gemini-2.0-flash-001",
    "models/gemini-flash-latest",
    "models/gemini-1.5-flash"
]

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

st.markdown("# 🏥 DURGA PSYCHIATRIC CENTRE")
st.markdown("## 🧠 AI Mental Health Assistant")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= AI FUNCTION (FAST) =================
def call_model(model, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a calm psychologist. Give short helpful advice.\nUser: {prompt}"
                    }
                ]
            }
        ]
    }

    res = requests.post(url, json=payload, timeout=6)

    if res.status_code == 200:
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    return None


def ask_ai(prompt):

    # ⚡ STEP 1: FAST MODEL FIRST
    result = call_model(PRIMARY_MODEL, prompt)
    if result:
        return result

    # 🔁 STEP 2: FALLBACK ONLY IF NEEDED
    for model in FALLBACK_MODELS:
        result = call_model(model, prompt)
        if result:
            return result

    return "⚠️ AI busy. Please try again in a few seconds."


# ================= CHAT (FIXED UX) =================
with st.form(key="chat_form", clear_on_submit=True):

    user_input = st.text_area(
        "Tell me what you're feeling:",
        placeholder="Example: I feel stressed due to work pressure"
    )

    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():

        st.session_state.messages.append(("You", user_input))

        reply = ask_ai(user_input)

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

# ================= WHATSAPP MESSAGE =================
if name and phone:

    message = f"""Hello Durga Psychiatric Centre,

New Consultation Request:

Name: {name}
Phone: {phone}
Concern: {concern}

Please contact me."""

    encoded = urllib.parse.quote(message)
    url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

    st.markdown(
        f"""
        <a href="{url}" target="_blank">
        <div style="
            background-color:#25D366;
            padding:16px;
            border-radius:12px;
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