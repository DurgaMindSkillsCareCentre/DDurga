import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
MODEL = "models/gemini-2.0-flash"
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= PREMIUM UI =================
st.markdown("""
<style>

/* BACKGROUND GRADIENT */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

/* MAIN CARD */
.main-card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* PROFILE CARD */
.profile-card {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4);
    padding: 15px;
    border-radius: 15px;
    color: black;
}

/* BUTTON */
.stButton button {
    background: linear-gradient(135deg, #25D366, #128C7E);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

/* INPUT BOX */
input, textarea {
    border-radius: 10px !important;
}

/* HEADINGS */
h1 {
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>🏥 DURGA PSYCHIATRIC CENTRE</h1>", unsafe_allow_html=True)

# ================= PROFILE =================
st.markdown('<div class="main-card">', unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    st.image("uploaded_image.jpg", width=140)

with col2:
    st.markdown("""
    <div class="profile-card">
    <h3>👩‍⚕️ D. DURGA</h3>
    <b>DPN (Nursing), DAHM, BBA, MBA (HR), MSW</b><br><br>
    Founder & CEO<br>
    Durga Psychiatric Centre
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= AI =================
st.markdown('<div class="main-card">', unsafe_allow_html=True)

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
        return "Reduce screen time and practice breathing before sleep."

    if "anxiety" in text:
        return "Try grounding techniques and slow breathing."

    if "anger" in text:
        return "Pause. Take deep breaths before reacting."

    return "I'm here to support you."


def call_gemini(prompt):
    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
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


def smart_ai(user_input):
    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            response = call_gemini(user_input)
        if response:
            return response

    return offline_ai(user_input)


# ================= CHAT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append(("You", user_input))
        reply = smart_ai(user_input)
        st.session_state.messages.append(("Assistant", reply))


for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

st.markdown('</div>', unsafe_allow_html=True)

# ================= CONSULT =================
st.markdown('<div class="main-card">', unsafe_allow_html=True)

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

        st.markdown(
            f'<script>window.open("{link}","_blank");</script>',
            unsafe_allow_html=True
        )

        st.success("Opening WhatsApp...")

        st.markdown(
            f"""
            <a href="{link}" target="_blank">
                <button style="
                    background:linear-gradient(135deg,#25D366,#128C7E);
                    color:white;
                    padding:16px;
                    border:none;
                    border-radius:12px;
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
        st.error("Fill all fields")

st.markdown('</div>', unsafe_allow_html=True)