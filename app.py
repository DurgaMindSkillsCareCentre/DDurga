import streamlit as st
import requests
import urllib.parse
from PIL import Image

# ================= CONFIG =================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= PREMIUM UI =================
st.markdown("""
<style>

/* Background */
html, body, [class*="css"] {
    background: linear-gradient(180deg,#5f9cff,#7b2ff7) !important;
    color: white !important;
    font-family: -apple-system, sans-serif;
}

/* Text */
h1, h2, h3, label, p {
    color: white !important;
}

/* Inputs */
textarea, input, select {
    background: white !important;
    color: black !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

/* SEND Button */
button[kind="primary"] {
    background: linear-gradient(135deg,#000000,#333333) !important;
    color: white !important;
    border-radius: 14px !important;
    height: 50px !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

/* Chat bubble */
.chat {
    background: rgba(255,255,255,0.15);
    padding: 12px;
    border-radius: 16px;
    margin-bottom: 10px;
}

/* AI label */
.ai {
    color: gold;
    font-size: 12px;
}

/* Profile card */
.profile {
    background: rgba(255,255,255,0.2);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("## 🏥 DURGA PSYCHIATRIC CENTRE")

# ================= PROFILE =================
try:
    img = Image.open("profile.jpg")
    st.image(img, width=120)
except:
    st.warning("Upload profile.jpg in repo root")

st.markdown("""
<div class="profile">
<b>D. Durga</b><br>
DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)<br><br>

<b>Founder & CEO</b><br>
Durga Psychiatric Centre
</div>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False

# ================= LOCAL AI =================
def local_ai(text):
    t = text.lower()

    if "stress" in t:
        return "Take small steps. Focus on breathing and relaxation.", "Local AI"

    if "sleep" in t:
        return "Avoid screens before bed. Try deep breathing and calm music.", "Local AI"

    if "anxiety" in t:
        return "Anxiety happens when the brain senses danger. Practice grounding.", "Local AI"

    return "I'm here to support you. Tell me more.", "Local AI"

# ================= GEMINI =================
def gemini(prompt):
    if not GEMINI_API_KEY:
        return None, None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    try:
        res = requests.post(url, json={
            "contents":[{"parts":[{"text":prompt}]}]
        }, timeout=5)

        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"], "Gemini"

        elif res.status_code == 429:
            st.session_state.quota_exceeded = True

    except:
        pass

    return None, None

# ================= DEEPSEEK =================
def deepseek(prompt):
    if not DEEPSEEK_API_KEY:
        return None, None

    try:
        res = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a helpful mental health assistant."},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=6
        )

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"], "DeepSeek"

    except:
        pass

    return None, None

# ================= AI ROUTER =================
def ai(user):
    # 1️⃣ Gemini first
    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            r, src = gemini(user)
        if r:
            return r, src

    # 2️⃣ DeepSeek
    r, src = deepseek(user)
    if r:
        return r, src

    # 3️⃣ Local fallback
    return local_ai(user)

# ================= CHAT =================
st.markdown("### 🧠 AI Mental Health Assistant")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling")
    send = st.form_submit_button("SEND")

    if send and user_input.strip():
        reply, source = ai(user_input)

        st.session_state.messages.append(("You", user_input, ""))
        st.session_state.messages.append(("AI", reply, source))

# ================= DISPLAY =================
for role, msg, src in st.session_state.messages:
    if role == "AI":
        st.markdown(f"""
        <div class="chat">
        <div class="ai">🤖 {src}</div>
        <b>{msg}</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat">
        <b>You:</b> {msg}
        </div>
        """, unsafe_allow_html=True)

# ================= CONSULT =================
st.markdown("---")
st.markdown("### 📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

issue = st.selectbox("Select Concern",
    ["Stress","Anxiety","Depression","Sleep Issues","Relationship","Other"]
)

if st.button("Submit & Continue"):

    if name and phone:
        msg = f"Name: {name}\nPhone: {phone}\nIssue: {issue}"

        link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

        st.success("Opening WhatsApp...")

        st.markdown(f"""
        <a href="{link}" target="_blank">
        <button style="width:100%;background:#25D366;color:white;padding:14px;border:none;border-radius:12px;">
        💬 Open WhatsApp
        </button>
        </a>
        """, unsafe_allow_html=True)

    else:
        st.error("Please fill all fields")