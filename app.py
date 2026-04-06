# -*- coding: utf-8 -*-

import streamlit as st
import requests
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", "")

# =========================
# UI (SAFE)
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
    color: white;
}
textarea, input {
    color: black !important;
}
.whatsapp-btn {
    display:block;
    text-align:center;
    padding:15px;
    background: linear-gradient(90deg,#25D366,#128C7E);
    color:white;
    font-size:18px;
    border-radius:12px;
    text-decoration:none;
    font-weight:bold;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🧠 DURGA PSYCHIATRIC CENTRE")

# =========================
# PROFILE
# =========================
col1, col2 = st.columns([1,2])

with col1:
    st.image("profile.jpg", width=120)

with col2:
    st.markdown("""
**D.Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW  
Founder & CEO  
Durga Psychiatric Centre
""")

st.divider()

# =========================
# SESSION STATE
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "input_box" not in st.session_state:
    st.session_state.input_box = ""

# =========================
# INPUT
# =========================
st.subheader("Tell me what you're feeling")

user_input = st.text_area("", key="input_box")

# =========================
# CLINICAL AI
# =========================
def clinical_ai(q):
    q = q.lower()
    score = 0
    cond = []

    if any(w in q for w in ["sad", "depress", "hopeless"]):
        cond.append("Depressive symptoms")
        score += 3

    if any(w in q for w in ["anxiety", "worry", "panic"]):
        cond.append("Anxiety symptoms")
        score += 3

    if any(w in q for w in ["sleep", "insomnia"]):
        cond.append("Sleep disturbance")
        score += 2

    if any(w in q for w in ["daily", "severe", "cannot"]):
        score += 3

    if score >= 7:
        risk = "High"
    elif score >= 4:
        risk = "Moderate"
    else:
        risk = "Mild"

    return f"{', '.join(cond) if cond else 'Stress'}. Severity: {risk}. Seek early support."

# =========================
# WEB AI
# =========================
def serper_ai(q):
    if not SERPER_API_KEY:
        return None
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        res = requests.post(url, headers=headers, json={"q": q}, timeout=5)
        data = res.json()
        return data["organic"][0]["snippet"][:180]
    except:
        return None

def wiki_ai(q):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(q)}"
        return requests.get(url, timeout=5).json().get("extract", "")[:180]
    except:
        return None

def duck_ai(q):
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json"
        return requests.get(url, timeout=5).json().get("AbstractText", "")[:180]
    except:
        return None

def smart_ai(q):
    clinical = clinical_ai(q)

    for func in [serper_ai, wiki_ai, duck_ai]:
        res = func(q)
        if res and len(res) > 20:
            return f"{clinical}\n\n🔎 {res}"

    return clinical

# =========================
# SEND
# =========================
def handle_send():
    q = st.session_state.input_box.strip()
    if not q:
        return

    ans = smart_ai(q)

    st.session_state.chat.append(("You", q))
    st.session_state.chat.append(("AI", ans))

    st.session_state.input_box = ""

st.button("SEND", on_click=handle_send, use_container_width=True)

# =========================
# CHAT
# =========================
st.markdown("### 💬 Conversation")

with st.container():
    for role, msg in st.session_state.chat:
        st.write(f"**{role}:** {msg}")

# =========================
# SPACING
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# =========================
# FORM
# =========================
st.header("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Mobile Number")

concern = st.selectbox("Concern", [
    "Stress", "Anxiety", "Depression", "Panic Disorder",
    "OCD", "Bipolar Disorder", "PTSD", "ADHD",
    "Sleep Disorder", "Relationship Issues",
    "Addiction", "Sexual Health Issues", "Other"
])

mode = st.radio("Session Mode", ["Online", "In-Person"])

time_slot = st.selectbox("Preferred Time", ["Morning", "Afternoon", "Evening"])

location = ""
if mode == "In-Person":
    location = st.text_input("Location / Area")

# =========================
# SUBMIT
# =========================
if st.button("Submit", use_container_width=True):

    if name and phone:

        message = f"""I would like to request an appointment with Psychologist D.Durga.

Name: {name}
Mobile: {phone}
Concern: {concern}

Preferred Mode: {mode}
Preferred Time: {time_slot}
"""

        if mode == "In-Person":
            message += f"\nLocation: {location}"

        message += "\n\nPlease call back to confirm the appointment."

        encoded_msg = urllib.parse.quote(message)
        wa_url = f"https://wa.me/917395944527?text={encoded_msg}"

        st.markdown(
            f'<a class="whatsapp-btn" href="{wa_url}" target="_blank">CLICK TO OPEN WHATSAPP</a>',
            unsafe_allow_html=True
        )

    else:
        st.warning("Please fill all required details")

# =========================
# FLOATING WHATSAPP
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank">
<div style="position:fixed;bottom:90px;right:20px;background:#25D366;
color:white;padding:15px;border-radius:50%;font-size:20px;">
💬
</div>
</a>
""", unsafe_allow_html=True)

# =========================
# STICKY BAR
# =========================
st.markdown("""
<div style="position:fixed;bottom:0;width:100%;background:black;color:white;
text-align:center;padding:10px;">
📞 Book Consultation | WhatsApp: +91 7395944527
</div>
""", unsafe_allow_html=True)