import streamlit as st
import urllib.parse
import google.generativeai as genai

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"

# 🔐 API KEY FROM SECRETS (NOT IN CODE)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ Stable model + chat session
model = genai.GenerativeModel("gemini-1.5-flash")

# ========= PAGE =========
st.set_page_config(page_title="Durga Psychiatric Centre")

# ========= SESSION =========
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========= HEADER =========
st.title("Durga Psychiatric Centre")
st.write("AI Mental Health Assistant")

st.markdown("---")

# ========= CHAT =========
st.subheader("Talk to our AI Assistant")

def get_ai_reply(user_input):
    try:
        prompt = f"""
You are a compassionate mental health assistant.

Rules:
- Be empathetic
- Ask meaningful follow-up questions
- Avoid repeating same sentences
- Keep responses short (2-3 lines)
- Encourage seeking professional help if needed

User: {user_input}
"""
        response = st.session_state.chat.send_message(prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "I'm here to listen. Can you tell me more?"

    except Exception as e:
        return "⚠️ AI service temporarily unavailable. Please try again."

# ========= INPUT =========
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling:")
    submit = st.form_submit_button("Send")

if submit and user_input:
    st.session_state.messages.append(("You", user_input))
    reply = get_ai_reply(user_input)
    st.session_state.messages.append(("Assistant", reply))
    st.rerun()

# ========= DISPLAY =========
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ========= CONSULTATION =========
st.markdown("---")
st.subheader("Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox(
    "Concern",
    ["Stress", "Anxiety", "Depression", "Relationship", "Addiction", "Other"]
)

# ========= WHATSAPP =========
message = f"""Hello, I would like to book a consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

encoded = urllib.parse.quote(message)
wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

st.link_button("Open WhatsApp", wa_link)

# ========= FOOTER =========
st.caption("Your information is confidential.")