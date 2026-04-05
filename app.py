import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")

WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #4facfe, #8e44ad);
    color: white;
}
.card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(16px);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 15px;
}
input, textarea {
    background: white !important;
    color: black !important;
    border-radius: 12px !important;
}
.stButton button {
    background: linear-gradient(135deg,#25D366,#128C7E);
    color:white;
    font-weight:bold;
    border-radius:12px;
    height:50px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 DURGA PSYCHIATRIC CENTRE")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False

# ================= QUERY CLASSIFIER =================
def classify_query(text):
    text = text.lower()

    if len(text.split()) < 5:
        return "simple"

    if any(w in text for w in ["why", "how", "explain", "reason"]):
        return "complex"

    return "medium"

# ================= LOCAL AI =================
def local_ai(text):
    text = text.lower()

    if "stress" in text:
        return "Take small steps. Breathe slowly and focus on one task."

    if "anxiety" in text:
        return "Try grounding: focus on your breath and surroundings."

    if "sleep" in text:
        return "Avoid screens before sleep and relax your mind."

    if "depression" in text:
        return "You’re not alone. Try small positive actions today."

    return "I'm here to support you. Tell me more."

# ================= GEMINI =================
def call_gemini(prompt):

    if not GEMINI_API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    try:
        res = requests.post(
            url,
            json={"contents":[{"parts":[{"text":prompt}]}]},
            timeout=8
        )

        if res.status_code == 429:
            st.session_state.quota_exceeded = True
            return None

        if res.status_code != 200:
            return None

        return res.json()["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None

# ================= DEEPSEEK =================
def call_deepseek(prompt):

    if not DEEPSEEK_API_KEY:
        return None

    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=8)

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]

    except:
        return None

    return None

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
                r = call_gemini(user_input)
            if r:
                return r

    # COMPLEX → DEEPSEEK
    if intent == "complex":
        r = call_deepseek(user_input)
        if r:
            return r

    # FALLBACK ORDER
    r = call_deepseek(user_input)
    if r:
        return r

    if not st.session_state.quota_exceeded:
        r = call_gemini(user_input)
        if r:
            return r

    return local_ai(user_input)

# ================= CHAT =================
st.markdown("### 🧠 AI Mental Health Assistant")

with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append(("You", user_input))
        reply = smart_ai(user_input)
        st.session_state.messages.append(("AI", reply))

# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ================= CONSULT =================
st.markdown("---")
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone")

cause = st.selectbox(
    "Concern",
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