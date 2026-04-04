import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
WHATSAPP_NUMBER = "917395944527"

# Get API key securely
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

# ✅ FINAL WORKING MODEL + ENDPOINT
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

st.set_page_config(page_title="Durga Psychiatric Centre")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = ""

# ================= HEADER =================
st.title("🧠 Durga Psychiatric Centre")
st.write("AI Mental Health Assistant")

st.markdown("---")

# ================= GEMINI FUNCTION =================
def get_ai_reply(user_input):
    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
You are a compassionate and professional mental health assistant.

Guidelines:
- Be empathetic and supportive
- Ask meaningful follow-up questions
- Avoid repeating the same sentence
- Keep responses short and natural

Conversation history:
{st.session_state.history}

User: {user_input}
"""
                        }
                    ]
                }
            ]
        }

        response = requests.post(URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ API ERROR {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# ================= CHAT INPUT =================
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Tell me what you're feeling:",
        placeholder="Example: I feel stressed due to work pressure"
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    reply = get_ai_reply(user_input)

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Assistant", reply))

    # Store history for better AI responses
    st.session_state.history += f"\nUser: {user_input}\nAssistant: {reply}"

    st.rerun()

# ================= DISPLAY CHAT =================
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ================= CONSULTATION FORM =================
st.markdown("---")
st.subheader("📅 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
concern = st.selectbox("Concern", ["Stress", "Anxiety", "Depression", "Other"])

# WhatsApp message
message = f"""Hello, I need consultation.

Name: {name}
Phone: {phone}
Concern: {concern}
"""

encoded_msg = urllib.parse.quote(message)
wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"

# ✅ SINGLE BUTTON (FIXED)
st.link_button("💬 Chat on WhatsApp", wa_link)

st.caption("🔒 Your information is confidential.")