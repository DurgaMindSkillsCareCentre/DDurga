import streamlit as st
import requests

# ================= CONFIG =================
API_KEY = st.secrets["GEMINI_API_KEY"]
WHATSAPP_NUMBER = "917395944527"

MODEL_PRIORITY = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-flash-latest"
]

# ================= PAGE =================
st.set_page_config(page_title="Durga AI Therapist", layout="centered")

st.title("🧠 AI Mental Health Assistant")

# ================= CHAT STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= INPUT =================
user_input = st.text_area("Tell me what you're feeling:")

# ================= AI FUNCTION =================
def ask_gemini(prompt):
    for model in MODEL_PRIORITY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"You are a professional therapist. Respond empathetically.\nUser: {prompt}"}
                        ]
                    }
                ]
            }

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

        except:
            continue

    return "⚠️ AI temporarily unavailable. Please try again."

# ================= SEND BUTTON =================
if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append(("You", user_input))

        reply = ask_gemini(user_input)

        st.session_state.messages.append(("Assistant", reply))

# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")

# ================= WHATSAPP =================
st.markdown("---")

st.markdown(
    f"""
    <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
        <button style="background-color:#25D366;color:white;padding:12px 20px;
        border:none;border-radius:8px;font-size:16px;">
        💬 Chat on WhatsApp
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

# ================= BOOKING =================
st.markdown("---")
st.subheader("📅 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

if st.button("Submit"):
    st.success("We will contact you shortly!")