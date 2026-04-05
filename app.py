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

# ================= SMART NLP ENGINE =================
def detect_emotion(text):
    text = text.lower()

    if any(w in text for w in ["stress", "pressure", "deadline"]):
        return "stress"

    if any(w in text for w in ["sleep", "insomnia", "night"]):
        return "sleep"

    if any(w in text for w in ["anxiety", "fear", "worry"]):
        return "anxiety"

    if any(w in text for w in ["anger", "angry", "irritated"]):
        return "anger"

    if any(w in text for w in ["sad", "depressed", "lonely"]):
        return "depression"

    return "general"

# ================= DYNAMIC RESPONSES =================
responses = {
    "stress": [
        "You're under pressure. Let's slow things down—focus on one small task at a time.",
        "Stress can build quickly. Try deep breathing for 2 minutes and reset your focus.",
        "Break your workload into smaller steps. You don’t need to do everything at once."
    ],
    "sleep": [
        "Sleep issues often come from mental overload. Reduce screen time before bed.",
        "Try slow breathing: inhale 4 sec, hold 4 sec, exhale 6 sec.",
        "Keep your phone away at night and relax your mind before sleep."
    ],
    "anxiety": [
        "Anxiety comes from future thinking. Bring your focus to the present moment.",
        "Try grounding: name 5 things you see, 4 things you feel.",
        "Slow breathing can reduce anxiety significantly."
    ],
    "anger": [
        "Pause before reacting. Take a deep breath.",
        "Anger is intense but temporary. Give yourself space before responding.",
        "Step away for a moment—this reduces emotional intensity."
    ],
    "depression": [
        "You're not alone. Even small steps matter.",
        "Try doing one simple positive activity today.",
        "Talk to someone you trust. Sharing helps."
    ],
    "general": [
        "I'm here to support you. Tell me more.",
        "You're safe to express your thoughts here.",
        "Let's work through this together."
    ]
}

def smart_offline_ai(user_input):
    emotion = detect_emotion(user_input)
    return random.choice(responses[emotion])

# ================= GEMINI CALL =================
def call_gemini(prompt):

    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
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

# ================= SMART AI CORE =================
def smart_ai(user_input):

    # Build context (last 3 messages)
    history = ""
    for role, msg in st.session_state.messages[-6:]:
        history += f"{role}: {msg}\n"

    prompt = f"""
You are a calm, supportive mental health assistant.

Conversation:
{history}

User: {user_input}

Give a helpful, short, empathetic response.
"""

    # 🚀 Try Gemini only if available
    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            response = call_gemini(prompt)

        if response:
            return response

    # ⚡ Instant fallback
    return smart_offline_ai(user_input)

# ================= CHAT UI =================
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

# ================= WHATSAPP =================
st.markdown("---")
st.subheader("📞 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

if name and phone:
    message = f"Name: {name}\nPhone: {phone}"
    link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"

    st.markdown(
        f'<a href="{link}" target="_blank">'
        f'<button style="background:#25D366;color:white;padding:14px;border:none;border-radius:10px;font-size:16px;">Chat on WhatsApp</button></a>',
        unsafe_allow_html=True
    )