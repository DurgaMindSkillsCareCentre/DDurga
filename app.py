import streamlit as st
import urllib.parse
import requests

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("API key not found in secrets")
    st.stop()

URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Durga Psychiatric Centre")

# ========= SESSION =========
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = ""

# ========= HEADER =========
st.title("Durga Psychiatric Centre")
st.write("AI Mental Health Assistant")

st.markdown("---")

# ========= GEMINI FUNCTION =========
def get_ai_reply(user_input):
    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
You are a compassionate mental health assistant.

- Be empathetic
- Ask specific follow-up questions
- Avoid repeating sentences
- Keep answers short

Conversation:
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
            return f"❌ API ERROR: {response.status_code}"

    except Exception as e:
        return f"❌ ERROR: {e}"

# ========= INPUT =========
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling:")
    submit = st.form_submit_button("Send")

if submit and user_input:
    reply = get_ai_reply(user_input)

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Assistant", reply))

    st.session_state.history += f"\nUser: {user_input}\nAssistant: {reply}"

    st.rerun()

# ========= DISPLAY =========
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ========= FORM =========
st.markdown("---")
st.subheader("Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox("Concern", ["Stress","Anxiety","Depression","Other"])

message = f"""Hello, I need consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"

st.link_button("Open WhatsApp", wa_link)

st.caption("Your information is confidential.")