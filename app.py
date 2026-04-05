import streamlit as st
import requests
import urllib.parse
import random
import time

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

    if "sleep" in text:
        return "Sleep problems are often linked to stress. Try reducing screen time before bed and practice slow breathing."

    if "stress" in text:
        return "Stress can feel overwhelming. Try breaking tasks into small steps and take short mindful breaks."

    if "anxiety" in text:
        return "Anxiety can cause racing thoughts. Try grounding yourself by focusing on your breath."

    if "anger" in text:
        return "Pause before reacting. Taking a few deep breaths can help control anger."

    return "I'm here for you. Tell me more about what you're feeling."

# ================= GEMINI =================
def gemini_response(prompt):

    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are a professional psychologist. Give helpful, slightly detailed advice.\nUser: {prompt}"}
                ]
            }
        ]
    }

    try:
        # 🔥 Give enough time to respond
        res = requests.post(url, json=payload, timeout=15)

        if res.status_code == 200:
            data = res.json()

            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None

    return None

# ================= SMART AI =================
def smart_ai(prompt):

    # ⏳ TRY GEMINI FIRST
    with st.spinner("Thinking..."):
        result = gemini_response(prompt)

    if result:
        return result  # ✅ REAL AI RESPONSE

    # ⚠️ ONLY IF FAILED → FALLBACK
    return offline_response(prompt)

# ================= CHAT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area(
        "Tell me what you're feeling:",
        placeholder="Example: I feel stressed due to work pressure"
    )

    send = st.form_submit_button("Send")

    if send and user_input.strip():

        st.session_state.messages.append(("You", user_input))

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
    ["Stress", "Anxiety", "Depression", "Sleep Issue", "Relationship Issue", "Other"]
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