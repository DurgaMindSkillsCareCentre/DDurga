import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
API_KEY = st.secrets["GEMINI_API_KEY"]
WHATSAPP_NUMBER = "917395944527"

MODEL_PRIORITY = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite"
]

# ================= PAGE =================
st.set_page_config(page_title="Durga AI Therapist", layout="centered")

st.title("🧠 AI Mental Health Assistant")

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ================= AI FUNCTION =================
def ask_gemini(prompt):
    for model in MODEL_PRIORITY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"You are a compassionate psychologist. Give helpful, human-like responses.\nUser: {prompt}"
                            }
                        ]
                    }
                ]
            }

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

        except:
            continue

    return "⚠️ AI temporarily unavailable. Please try again."

# ================= CHAT INPUT =================
def send_message():
    user_text = st.session_state.user_input.strip()

    if user_text:
        st.session_state.messages.append(("You", user_text))

        reply = ask_gemini(user_text)

        st.session_state.messages.append(("Assistant", reply))

        # ✅ CLEAR INPUT AFTER SEND
        st.session_state.user_input = ""

st.text_area(
    "Tell me what you're feeling:",
    key="user_input",
    placeholder="Example: I feel stressed due to work pressure"
)

st.button("Send", on_click=send_message)

# ================= DISPLAY CHAT =================
for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")

# ================= WHATSAPP DIRECT BUTTON =================
st.markdown("---")

st.markdown(
    f"""
    <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
        <button style="background-color:#25D366;color:white;padding:12px 20px;
        border:none;border-radius:8px;font-size:16px;">
        💬 Chat on WhatsApp
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

# ================= BOOK CONSULTATION =================
st.markdown("---")
st.subheader("📅 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

concern = st.selectbox(
    "Select Your Concern",
    ["Stress", "Anxiety", "Depression", "Relationship Issue", "Addiction", "Other"]
)

if st.button("Submit & Chat on WhatsApp"):

    if name and phone:

        message = f"""
Hello Durga Psychiatric Centre,

New Consultation Request:

👤 Name: {name}
📞 Phone: {phone}
🧠 Concern: {concern}

Please contact me.
"""

        encoded_message = urllib.parse.quote(message)

        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"

        # ✅ AUTO REDIRECT
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={whatsapp_url}">',
            unsafe_allow_html=True
        )

    else:
        st.warning("Please fill all details")