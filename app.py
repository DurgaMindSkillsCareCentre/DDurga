# -*- coding: utf-8 -*-
import streamlit as st
import requests
import urllib.parse
import re
import json

# ===================== CONFIG =====================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

WHATSAPP_NUMBER = "917395944527"
SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", "")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# ===================== CSS =====================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
    color: white;
}
textarea, input { color: black !important; }
div.stButton > button {
    background: #111111; color: white; border-radius: 12px; font-weight: bold;
}
label { color: white !important; }

/* Floating buttons */
.float-w {
 position: fixed; bottom: 90px; right: 20px;
 background:#25D366; width:60px; height:60px;
 border-radius:50%; display:flex; align-items:center; justify-content:center;
 font-size:28px; color:white; z-index:9999;
}
.float-c {
 position: fixed; bottom: 160px; right: 20px;
 background:#0a84ff; width:60px; height:60px;
 border-radius:50%; display:flex; align-items:center; justify-content:center;
 font-size:28px; color:white; z-index:9999;
}

/* Sticky footer */
.footer {
 position: fixed; bottom:0; left:0; width:100%;
 background:black; color:white; text-align:center; padding:12px; z-index:9999;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.title("Durga Psychiatric Centre")
st.image("profile.jpg", width=150)

# ===================== SESSION =====================
if "chat" not in st.session_state:
    st.session_state.chat = []

# ===================== TEXT CLEAN =====================
def clean_summary(text):
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\xa0", " ")

    junk = ["skip to", "menu", "home", "login", "contact"]
    for j in junk:
        text = re.sub(j + r".*?\.", "", text, flags=re.IGNORECASE)

    sentences = re.split(r'(?<=[.!?]) +', text)

    clean = []
    for s in sentences:
        if len(s.split()) > 5:
            clean.append(s.strip())
        if len(clean) == 3:
            break

    return " ".join(clean)

# ===================== WEB AI =====================
def serper_search(q):
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        r = requests.post(url, headers=headers, json={"q": q}, timeout=8)
        data = r.json()
        return " ".join([x.get("snippet","") for x in data.get("organic",[])[:3]])
    except:
        return ""

def duck(q):
    try:
        url = f"https://api.duckduckgo.com/?q={q}&format=json"
        return requests.get(url).json().get("AbstractText","")
    except:
        return ""

def wiki(q):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        return requests.get(url).json().get("extract","")
    except:
        return ""

def gemini(q):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data = {"contents":[{"parts":[{"text":"Explain in 3 lines: "+q}]}]}
        r = requests.post(url,json=data)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return ""

# ===================== LOCAL DSS =====================
def dss(text):
    t = text.lower()

    suicide_words = ["suicide","kill myself","end my life","die"]
    if any(w in t for w in suicide_words):
        return ("Suicidal Risk", "Critical", "Immediate help required")

    if "depress" in t:
        return ("Depression","Moderate","Seek professional help")

    if "anxiety" in t or "panic" in t:
        return ("Anxiety","Mild-Moderate","Relaxation and therapy helpful")

    if "sleep" in t:
        return ("Sleep Issue","Mild","Fix sleep routine")

    return ("Stress","Mild","Manage workload and rest")

# ===================== LOCAL AI =====================
def local_ai(q):
    return "You may be experiencing emotional stress. Small steps and support help recovery."

# ===================== FINAL AI =====================
def smart_ai(q):
    text = serper_search(q)
    if not text or len(text)<30:
        text = duck(q)
    if not text or len(text)<30:
        text = wiki(q)
    if not text or len(text)<30:
        text = gemini(q)
    if not text or len(text)<20:
        return local_ai(q)

    return clean_summary(text)

# ===================== VOICE INPUT =====================
st.markdown("### Voice Input")
voice = st.text_input("Speak (type here for now)")

# ===================== INPUT =====================
user_input = st.text_area("Tell me what you are feeling")

if st.button("SEND"):
    if user_input.strip():

        st.session_state.chat.append(("You", user_input))

        cond, sev, adv = dss(user_input)

        ai_text = smart_ai(user_input)

        response = f"""
Condition: {cond}

Severity: {sev}

Advice: {adv}

Summary:
{ai_text}
"""

        st.session_state.chat.append(("AI", response))

        # EMERGENCY ALERT
        if sev == "Critical":
            st.error("Emergency detected. Contact immediately.")
            call_link = f"tel:+{WHATSAPP_NUMBER}"
            st.markdown(f'<a href="{call_link}">Call Now</a>', unsafe_allow_html=True)

# ===================== CHAT =====================
st.subheader("Conversation")
for r,m in st.session_state.chat:
    st.write(r+":")
    st.write(m)

# ===================== FORM =====================
st.subheader("Book Consultation")

name = st.text_input("Name")
mobile = st.text_input("Mobile")
cause = st.selectbox("Concern",["Stress","Anxiety","Depression","Sleep","Other"])
mode = st.radio("Mode",["Online","In Person"])
time = st.selectbox("Time",["Morning","Afternoon","Evening"])
loc = st.text_input("Location")

if st.button("Submit"):
    msg = f"""I would like to request an appointment.

Name: {name}
Mobile: {mobile}
Concern: {cause}
Mode: {mode}
Time: {time}
Location: {loc}
"""

    link = "https://wa.me/"+WHATSAPP_NUMBER+"?text="+urllib.parse.quote(msg)
    st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

# ===================== FLOATING =====================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
<div class="float-w">💬</div></a>

<a href="tel:+{WHATSAPP_NUMBER}">
<div class="float-c">📞</div></a>
""", unsafe_allow_html=True)

# ===================== FOOTER =====================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP_NUMBER}">
<div class="footer">Book Consultation on WhatsApp</div>
</a>
""", unsafe_allow_html=True)