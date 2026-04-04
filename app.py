import streamlit as st
import urllib.parse
import random

WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", page_icon="")

# ========= SESSION =========
if "history" not in st.session_state:
    st.session_state.history = []

# ========= HEADER =========
st.title(" Durga Psychiatric Centre")
st.write("Confidential Mental Health Support")

st.markdown("---")

# ========= CHATBOT =========
st.subheader(" Talk to our Assistant")

def bot_reply(text):
    text = text.lower()

    if "stress" in text:
        return random.choice([
            "I understand you're feeling stressed. Is it work-related or personal?",
            "Stress can feel overwhelming. What seems to be causing it?",
            "Can you tell me more about your stress?"
        ])

    elif "anxiety" in text:
        return random.choice([
            "Anxiety can feel intense. When do you feel it the most?",
            "You're not alone. Can you describe your anxiety?",
        ])

    elif "depression" in text:
        return "I'm sorry you're feeling this way. How long have you been experiencing this?"

    else:
        return "I'm here to listen. Can you tell me more?"

# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling:")
    submit = st.form_submit_button("Send")

if submit and user_input:
    st.session_state.history.append(("You", user_input))
    reply = bot_reply(user_input)
    st.session_state.history.append(("Assistant", reply))
    st.rerun()

# Display chat
for role, msg in st.session_state.history:
    st.write(f"**{role}:** {msg}")

# ========= FORM =========
st.markdown("---")
st.subheader(" Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox("Concern", ["Stress", "Anxiety", "Depression", "Relationship", "Addiction", "Other"])

# ========= WHATSAPP FLOW =========
if st.button(" Open WhatsApp"):

    if not name or not phone:
        st.error("Please fill all details")
    else:
        message = f"""Hello, I would like to book a consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

        encoded = urllib.parse.quote(message)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

        st.success("Tap below to open WhatsApp")
        st.link_button(" Open WhatsApp Chat", wa_link)

# ========= FOOTER =========
st.caption("Your information is confidential.")