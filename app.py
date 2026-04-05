import streamlit as st
import requests
import urllib.parse
import random

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
MODEL = "models/gemini-2.0-flash"
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre")

st.title("🏥 DURGA PSYCHIATRIC CENTRE")
st.subheader("🧠 AI Mental Health Assistant")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False

# ================= AI =================
def offline_ai(text):
    text = text.lower()

    if "stress" in text:
        return "Break tasks into smaller steps. You don’t need to do everything at once."

    if "sleep" in text:
        return "Reduce screen time and practice slow breathing before sleep."

    if "anxiety" in text:
        return "Focus on the present moment. Try grounding techniques."

    if "anger" in text:
        return "Pause and take a deep breath before reacting."

    return "I'm here to support you. Tell me more."

def call_gemini(prompt):
    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        res = requests.post(url, json=payload, timeout=8)

        if res.status_code == 429:
            st.session_state.quota_exceeded = True
            return None

        if res.status_code != 200:
            return None

        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None

def smart_ai(user_input):

    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            response = call_gemini(user_input)

        if response:
            return response

    return offline_ai(user_input)

# ================= CHAT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append(("You", user_input))
        reply = smart_ai(user_input)
        st.session_state.messages.append(("Assistant", reply))

# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ================= CONSULTATION =================
st.markdown("---")
st.subheader("📞 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

cause = st.selectbox(
    "Select Your Concern",
    ["Stress", "Anxiety", "Depression", "Sleep Issue", "Relationship Issue", "Other"]
)

# ================= SUBMIT BUTTON =================
if st.button("Submit & Continue"):

    if name and phone:

        message = f"""Hello,
I want to book a consultation.

Name: {name}
Phone: {phone}
Concern: {cause}
"""

        link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"

        # 🔥 AUTO OPEN WHATSAPP
        st.markdown(
            f"""
            <script>
            window.open("{link}", "_blank");
            </script>
            """,
            unsafe_allow_html=True
        )

        st.success("Opening WhatsApp...")

        # ✅ BACKUP BUTTON
        st.markdown(
            f"""
            <a href="{link}" target="_blank">
                <button style="
                    background:#25D366;
                    color:white;
                    padding:16px;
                    border:none;
                    border-radius:10px;
                    font-size:18px;
                    width:100%;
                    font-weight:bold;
                ">
                💬 Click here if WhatsApp did not open
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("Please fill all fields")