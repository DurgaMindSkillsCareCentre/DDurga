import streamlit as st
import requests
import urllib.parse
from PIL import Image
import time

# ================= CONFIG =================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= UI (SAFE PREMIUM) =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #5f9cff, #7b2ff7);
}
h1,h2,h3,p,label {
    color: white !important;
}
textarea,input,select {
    background: white !important;
    color: black !important;
    border-radius: 10px !important;
}
div.stButton > button {
    background: linear-gradient(135deg,#111,#333) !important;
    color: white !important;
    border-radius: 12px;
    height: 48px;
    font-weight: bold;
}
.badge {
    padding:4px 10px;
    border-radius:8px;
    font-size:12px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🏥 DURGA PSYCHIATRIC CENTRE")

# ================= PROFILE =================
col1, col2 = st.columns([1,2])
with col1:
    try:
        img = Image.open("profile.jpg")
        st.image(img, width=120)
    except:
        st.warning("Upload profile.jpg")

with col2:
    st.markdown("""
    **D. Durga**  
    DPN (Nursing), DAHM, BBA, MBA(HR), MSW  

    **Founder & CEO**  
    Durga Psychiatric Centre
    """)

st.divider()

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ai_status" not in st.session_state:
    st.session_state.ai_status = "Local"

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False

# ================= LOCAL AI =================
def local_ai(text):
    return "Try grounding, slow breathing, and reducing overload step by step.", "Local"

# ================= GEMINI =================
def gemini(prompt):
    if not GEMINI_API_KEY:
        return None, None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        r = requests.post(url, json={
            "contents":[{"parts":[{"text":prompt}]}]
        }, timeout=5)

        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"], "Gemini"

        elif r.status_code == 429:
            st.session_state.quota_exceeded = True

    except:
        pass

    return None, None

# ================= DEEPSEEK =================
def deepseek(prompt):
    if not DEEPSEEK_API_KEY:
        return None, None

    try:
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model":"deepseek-chat",
                "messages":[{"role":"user","content":prompt}]
            },
            timeout=6
        )

        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], "DeepSeek"

        else:
            st.warning("DeepSeek error")

    except:
        pass

    return None, None

# ================= SMART ROUTER =================
def get_ai(user):

    # Try Gemini
    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            r, src = gemini(user)
        if r:
            st.session_state.ai_status = "Gemini"
            return r, src

    # Try DeepSeek
    r, src = deepseek(user)
    if r:
        st.session_state.ai_status = "DeepSeek"
        return r, src

    # Fallback
    st.session_state.ai_status = "Local"
    return local_ai(user)

# ================= STATUS BADGE =================
status = st.session_state.ai_status

color = {
    "Gemini":"#00c853",
    "DeepSeek":"#ff9800",
    "Local":"#9e9e9e"
}

st.markdown(f"""
<span class="badge" style="background:{color.get(status)}">
AI: {status}
</span>
""", unsafe_allow_html=True)

# ================= CHAT =================
st.subheader("🧠 AI Mental Health Assistant")

user_input = st.text_area("Tell me what you're feeling")

if st.button("SEND"):
    if user_input.strip():
        reply, src = get_ai(user_input)

        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append((f"AI ({src})", reply))

# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")

# ================= CONSULT =================
st.divider()
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

issue = st.selectbox("Concern",
    ["Stress","Anxiety","Depression","Sleep Issues","Relationship","Other"]
)

if st.button("Submit & Continue"):

    if name and phone:
        msg = f"Name: {name}\nPhone: {phone}\nIssue: {issue}"
        link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

        st.success("Click below to open WhatsApp")

        st.markdown(f"""
        <a href="{link}" target="_blank">
        <div style="
            background: linear-gradient(135deg,#075e54,#25D366);
            color:white;
            padding:16px;
            text-align:center;
            border-radius:12px;
            font-weight:bold;
            font-size:18px;">
            💬 OPEN WHATSAPP
        </div>
        </a>
        """, unsafe_allow_html=True)

    else:
        st.error("Fill all details")