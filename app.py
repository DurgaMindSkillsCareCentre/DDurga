import streamlit as st
import urllib.parse
import requests

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"
GEMINI_API_KEY = "AIzaSyCfh6C0d19D9zS2pqnuZHtV164Zhw32wD4"

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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

# ========= GEMINI API =========
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
- Keep answers short (2-3 lines)

Conversation so far:
{st.session_state.history}

User: {user_input}
"""
                        }
                    ]
                }
            ]
        }

        response = requests.post(GEMINI_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return fallback_reply(user_input)

    except:
        return fallback_reply(user_input)

# ========= FALLBACK =========
def fallback_reply(text):
    text = text.lower()

    if "stress" in text:
        return "It seems stress is affecting you. Is it more from work or personal life?"
    elif "work" in text:
        return "Work pressure can be tough. What exactly is causing stress at work?"
    elif "deadline" in text:
        return "Deadlines can feel overwhelming. Are they too frequent or too tight?"
    elif "family" in text:
        return "Family issues can be emotionally heavy. What situation is troubling you?"
    else:
        return "I'm listening. Can you tell me more?"

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