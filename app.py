import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
MODEL = "models/gemini-2.0-flash"
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= ULTRA PREMIUM UI =================
st.markdown("""
<style>

/* ===== BACKGROUND (iOS Gradient) ===== */
.stApp {
    background: linear-gradient(180deg, #4facfe 0%, #8e44ad 100%);
    color: white;
}

/* ===== GLASS CARD ===== */
.card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(18px);
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
}

/* ===== HEADINGS ===== */
h1, h2, h3 {
    color: white !important;
    font-weight: 700;
}

/* ===== LABEL TEXT ===== */
label, p {
    color: #f2f2f2 !important;
}

/* ===== INPUT ===== */
input, textarea {
    background: white !important;
    color: black !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 12px !important;
}

/* ===== DROPDOWN ===== */
.stSelectbox div {
    background: white !important;
    color: black !important;
    border-radius: 14px !important;
}

/* ===== SEND BUTTON ===== */
.stForm button {
    background: linear-gradient(135deg, #ff7a18, #ff3d00) !important;
    color: white !important;
    border-radius: 14px !important;
    height: 48px;
    font-weight: bold;
}

/* ===== WHATSAPP BUTTON ===== */
.stButton button {
    background: linear-gradient(135deg, #25D366, #128C7E) !important;
    color: white !important;
    border-radius: 16px !important;
    height: 52px;
    font-size: 18px;
    font-weight: bold;
}

/* ===== CHAT BUBBLES ===== */
.chat-user {
    background: #ffffff;
    color: black;
    padding: 12px;
    border-radius: 18px;
    margin: 8px 0;
    text-align: right;
}

.chat-ai {
    background: rgba(255,255,255,0.2);
    padding: 12px;
    border-radius: 18px;
    margin: 8px 0;
}

/* ===== PROFILE CARD ===== */
.profile {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4);
    padding: 15px;
    border-radius: 16px;
    color: black;
}

/* ===== SUCCESS ===== */
.stAlert {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>🏥 DURGA PSYCHIATRIC CENTRE</h1>", unsafe_allow_html=True)

# ================= PROFILE =================
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    st.image("uploaded_image.jpg", width=130)

with col2:
    st.markdown("""
    <div class="profile">
    <b>👩‍⚕️ D. DURGA</b><br>
    DPN (Nursing), DAHM, BBA, MBA (HR), MSW<br><br>
    Founder & CEO<br>
    Durga Psychiatric Centre
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= AI =================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🧠 AI Mental Health Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False


def offline_ai(text):
    text = text.lower()
    if "stress" in text:
        return "Break work into small steps. Take mindful pauses."
    if "sleep" in text:
        return "Reduce screen time. Try slow breathing before sleep."
    if "anxiety" in text:
        return "Focus on breathing and grounding."
    if "anger" in text:
        return "Pause. Take deep breaths before reacting."
    return "I'm here to support you."


def call_gemini(prompt):
    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    try:
        res = requests.post(
            url,
            json={"contents":[{"parts":[{"text":prompt}]}]},
            timeout=6
        )

        if res.status_code == 429:
            st.session_state.quota_exceeded = True
            return None

        if res.status_code != 200:
            return None

        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None


def smart_ai(user_input):
    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            r = call_gemini(user_input)
        if r:
            return r
    return offline_ai(user_input)


# ================= CHAT INPUT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append(("user", user_input))
        reply = smart_ai(user_input)
        st.session_state.messages.append(("ai", reply))


# ================= CHAT DISPLAY =================
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai">{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= CONSULT =================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

cause = st.selectbox(
    "Select Concern",
    ["Stress", "Anxiety", "Depression", "Sleep Issue", "Relationship", "Other"]
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
                <button style="
                    background:linear-gradient(135deg,#25D366,#128C7E);
                    color:white;
                    padding:16px;
                    border:none;
                    border-radius:16px;
                    font-size:18px;
                    width:100%;
                ">
                💬 Open WhatsApp
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("Please fill all fields")

st.markdown('</div>', unsafe_allow_html=True)