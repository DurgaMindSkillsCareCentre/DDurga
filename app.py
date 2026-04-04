import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
API_KEY = st.secrets["GEMINI_API_KEY"]
WHATSAPP_NUMBER = "917395944527"

MODEL = "models/gemini-2.0-flash"  # stable

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

st.markdown("# 🏥 DURGA PSYCHIATRIC CENTRE")
st.markdown("### 🧠 AI Mental Health Assistant")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ================= AI FUNCTION =================
def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"You are a compassionate psychologist. Give clear helpful response.\nUser: {prompt}"
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "⚠️ AI busy. Please try again."

    except:
        return "⚠️ AI temporarily unavailable. Please try again."

# ================= CHAT =================
def send_message():
    text = st.session_state.user_input.strip()

    if text:
        st.session_state.messages.append(("You", text))
        reply = ask_gemini(text)
        st.session_state.messages.append(("Assistant", reply))
        st.session_state.user_input = ""  # clear input

st.text_area(
    "Tell me what you're feeling:",
    key="user_input",
    placeholder="Example: I feel stressed due to work pressure"
)

st.button("Send", on_click=send_message)

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

# ================= WHATSAPP BUTTON =================
if name and phone:

    message = f"""
Hello Durga Psychiatric Centre,

New Consultation Request:

Name: {name}
Phone: {phone}
Concern: {concern}

Please contact me.
"""

    encoded = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

    st.markdown(
        f"""
        <a href="{whatsapp_url}" target="_blank">
        <button style="
            background-color:#25D366;
            color:white;
            padding:14px;
            width:100%;
            border:none;
            border-radius:10px;
            font-size:18px;
        ">
        💬 Submit & Chat on WhatsApp
        </button>
        </a>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Fill details to enable WhatsApp booking")