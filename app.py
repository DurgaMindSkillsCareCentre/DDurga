import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= PREMIUM UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #5f9cff, #6a11cb);
    color: white;
}

/* Labels */
label, .stMarkdown, h1, h2, h3 {
    color: white !important;
    font-weight: 600;
}

/* Inputs */
input, textarea, select {
    background: white !important;
    color: black !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg,#00c853,#009624);
    color: white !important;
    font-size: 16px;
    font-weight: bold;
    border-radius: 12px;
    height: 50px;
}

/* Chat */
.chat-box {
    background: rgba(255,255,255,0.15);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}

.ai-label {
    font-size: 12px;
    color: #FFD700;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 DURGA PSYCHIATRIC CENTRE")
st.subheader("🧠 AI Mental Health Assistant")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False

# ================= CLASSIFIER =================
def classify_query(text):
    text = text.lower()

    if len(text.split()) < 5:
        return "simple"

    if any(w in text for w in ["why", "how", "explain"]):
        return "complex"

    return "medium"

# ================= LOCAL AI =================
def local_ai(text):
    text = text.lower()

    if "stress" in text:
        return "Take small steps. Breathe slowly and focus.", "Local AI"

    if "sleep" in text:
        return "Avoid screens before sleep and relax your mind.", "Local AI"

    if "anxiety" in text:
        return "Use grounding and slow breathing techniques.", "Local AI"

    return "I'm here to support you. Tell me more.", "Local AI"

# ================= GEMINI =================
def call_gemini(prompt):

    if not GEMINI_API_KEY:
        return None, None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    try:
        res = requests.post(
            url,
            json={"contents":[{"parts":[{"text":prompt}]}]},
            timeout=8
        )

        if res.status_code == 429:
            st.session_state.quota_exceeded = True
            return None, None

        if res.status_code != 200:
            return None, None

        text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        return text, "Gemini"

    except:
        return None, None

# ================= DEEPSEEK =================
def call_deepseek(prompt):

    if not DEEPSEEK_API_KEY:
        return None, None

    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)

        if res.status_code == 200:
            text = res.json()["choices"][0]["message"]["content"]
            return text, "DeepSeek"

    except:
        return None, None

    return None, None

# ================= SMART AI =================
def smart_ai(user_input):

    intent = classify_query(user_input)

    # SIMPLE → LOCAL
    if intent == "simple":
        return local_ai(user_input)

    # MEDIUM → GEMINI
    if intent == "medium":
        if not st.session_state.quota_exceeded:
            with st.spinner("Thinking..."):
                r, src = call_gemini(user_input)
            if r:
                return r, src

    # COMPLEX → DEEPSEEK
    r, src = call_deepseek(user_input)
    if r:
        return r, src

    # FALLBACK
    if not st.session_state.quota_exceeded:
        r, src = call_gemini(user_input)
        if r:
            return r, src

    return local_ai(user_input)

# ================= CHAT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        reply, src = smart_ai(user_input)

        st.session_state.messages.append(("You", user_input, ""))
        st.session_state.messages.append(("AI", reply, src))

# ================= DISPLAY =================
for role, msg, src in st.session_state.messages:
    if role == "AI":
        st.markdown(f"""
        <div class="chat-box">
        <div class="ai-label">🤖 {src}</div>
        <b>{role}:</b> {msg}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-box">
        <b>{role}:</b> {msg}
        </div>
        """, unsafe_allow_html=True)

# ================= CONSULT =================
st.markdown("---")
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone")

cause = st.selectbox(
    "Select Concern",
    ["Stress","Anxiety","Depression","Sleep Issue","Relationship","Other"]
)

if st.button("Submit & Continue"):

    if name and phone:

        msg = f"""Hello,
Name: {name}
Phone: {phone}
Concern: {cause}
"""

        link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

        # AUTO OPEN
        st.markdown(
            f'<script>window.open("{link}","_blank");</script>',
            unsafe_allow_html=True
        )

        st.success("Opening WhatsApp...")

        # BACKUP BUTTON
        st.markdown(
            f"""
            <a href="{link}" target="_blank">
                <button style="width:100%;padding:14px;background:#25D366;color:white;border:none;border-radius:10px;">
                💬 Open WhatsApp
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("Please fill all fields")