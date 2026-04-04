import streamlit as st
import requests
import urllib.parse
import time

# ================= CONFIG =================
API_KEY = st.secrets["GEMINI_API_KEY"]
WHATSAPP_NUMBER = "917395944527"

MODEL = "models/gemini-2.0-flash"  # confirmed stable

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

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a compassionate psychologist. Help clearly.\nUser: {prompt}"
                    }
                ]
            }
        ]
    }

    # 🔁 Retry logic
    for _ in range(3):
        try:
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if "candidates" in data:
                    return data["candidates"][0]["content"]["parts"][0]["text"]

            time.sleep(1)

        except:
            time.sleep(1)

    return "⚠️ AI is temporarily busy. Please try again in a few seconds."

# ================= CHAT =================
def send_message():
    text = st.session_state.user_input.strip()

    if text:
        st.session_state.messages.append(("You", text))

        reply = ask_gemini(text)

        st.session_state.messages.append(("Assistant", reply))

        st.session_state.user_input = ""  # clear box

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

# ================= WHATSAPP CTA =================
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
            cursor:pointer;
        ">
        💬 Book via WhatsApp
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Fill details to enable booking")