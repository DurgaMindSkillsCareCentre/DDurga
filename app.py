import streamlit as st
import urllib.parse
import google.generativeai as genai

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"
GEMINI_API_KEY = "AIzaSyC_3bp0o5I46PGNl_cYer4A5o-kEZVKOx0"  # 🔴 Use fresh key

genai.configure(api_key=GEMINI_API_KEY)

# ✅ BEST WORKING METHOD (IMPORTANT)
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])
    GEMINI_OK = True
except:
    GEMINI_OK = False

st.set_page_config(page_title="Durga Psychiatric Centre")

# ========= SESSION =========
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    if GEMINI_OK:
        st.session_state.chat = model.start_chat(history=[])
    else:
        st.session_state.chat = None

# ========= HEADER =========
st.title("Durga Psychiatric Centre")
st.write("AI Mental Health Assistant")

st.markdown("---")

# ========= FALLBACK =========
def fallback_reply(text):
    text = text.lower()

    if "stress" in text:
        return "Stress can feel heavy. Is it mainly from studies, work, or personal life?"
    elif "work" in text:
        return "Work pressure can be exhausting. What part of work is affecting you most?"
    elif "family" in text:
        return "Family issues can be emotionally difficult. What situation is troubling you?"
    elif "anxiety" in text:
        return "Anxiety can feel intense. When do you experience it most?"
    else:
        return "I understand. Can you explain a little more about what you're going through?"

# ========= AI FUNCTION =========
def get_ai_reply(user_input):

    if not GEMINI_OK or st.session_state.chat is None:
        return fallback_reply(user_input)

    try:
        response = st.session_state.chat.send_message(user_input)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return fallback_reply(user_input)

    except Exception as e:
        return fallback_reply(user_input)

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

# ========= FORM =========
st.markdown("---")
st.subheader("Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox(
    "Concern",
    ["Stress", "Anxiety", "Depression", "Relationship", "Addiction", "Other"]
)

message = f"""Hello, I need consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"

st.link_button("Open WhatsApp", wa_link)

st.caption("Your information is confidential.")