import streamlit as st
import requests
import urllib.parse
from PIL import Image

# ================= CONFIG =================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= SIMPLE PREMIUM UI =================
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #5f9cff, #7b2ff7);
}
.stApp {
    background: linear-gradient(to bottom, #5f9cff, #7b2ff7);
}
h1, h2, h3, p, label {
    color: white !important;
}
textarea, input, select {
    background: white !important;
    color: black !important;
    border-radius: 10px !important;
}
div.stButton > button {
    background: #111 !important;
    color: white !important;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
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
        st.image(img, width=130)
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

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False

# ================= LOCAL AI =================
def local_ai(text):
    t = text.lower()

    if "stress" in t:
        return "Take small steps and practice slow breathing.", "Local AI"

    if "sleep" in t:
        return "Reduce screen time and relax your mind before bed.", "Local AI"

    if "anxiety" in t:
        return "Anxiety is your brain reacting to stress. Stay grounded.", "Local AI"

    return "I'm here to support you.", "Local AI"

# ================= GEMINI =================
def gemini(prompt):
    if not GEMINI_API_KEY:
        return None, None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

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
                "messages":[{"role":"user","content":prompt}]
            },
            timeout=6
        )

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"], "DeepSeek"

    except:
        pass

    return None, None

# ================= AI ROUTER =================
def get_ai_response(user_input):

    # Gemini first
    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            r, src = gemini(user_input)
        if r:
            return r, src

    # DeepSeek next
    r, src = deepseek(user_input)
    if r:
        return r, src

    # Fallback
    return local_ai(user_input)

# ================= CHAT =================
st.subheader("🧠 AI Mental Health Assistant")

user_input = st.text_area("Tell me what you're feeling")

if st.button("SEND"):
    if user_input.strip():
        reply, source = get_ai_response(user_input)

        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append((f"AI ({source})", reply))

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

        st.success("Opening WhatsApp...")

        st.markdown(f"[👉 Click here to open WhatsApp]({link})")

    else:
        st.error("Please fill all fields")