# -*- coding: utf-8 -*-
import streamlit as st
import requests
import urllib.parse
import re

# ================= CONFIG =================
WHATSAPP_NUMBER = "917395944527"
SERPER_API_KEY = "YOUR_SERPER_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_KEY"

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#5f6dfc,#7b2ff7); color:white;}

.user {background:#111;padding:12px;border-radius:12px;margin:6px;text-align:right;}
.ai {background:#ffffff22;padding:12px;border-radius:12px;margin:6px;}

.green {background:#00c853;padding:12px;border-radius:12px;color:white;}
.orange {background:#ff9800;padding:12px;border-radius:12px;color:white;}
.red {background:#e53935;padding:12px;border-radius:12px;color:white;}

.stButton button {background:black;color:white;font-size:18px;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("##  DURGA PSYCHIATRIC CENTRE")
st.image("profile.jpg", width=130)

st.markdown("""
**D. Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW  
Founder & CEO  
Durga Psychiatric Centre
""")

# ================= CLEAN =================
def clean(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text)
    return " ".join(text.split('.')[:3])

def valid(x):
    return x and len(x.strip()) > 40

# ================= WEB AI =================
def serper(q):
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        r = requests.post(url, json={"q": q}, headers=headers, timeout=8)
        data = r.json()
        return clean(data["organic"][0]["snippet"])
    except:
        return ""

def duck(q):
    try:
        r = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json", timeout=8)
        return clean(r.json().get("AbstractText",""))
    except:
        return ""

def wiki(q):
    try:
        q = q.replace(" ","_")
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}", timeout=8)
        return clean(r.json().get("extract",""))
    except:
        return ""

def gemini(q):
    MODELS = [
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest"
    ]

    for m in MODELS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{m}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents":[{"parts":[{"text":q}]}]
            }
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                return clean(r.json()["candidates"][0]["content"]["parts"][0]["text"])
        except:
            continue
    return ""

# ================= LOCAL =================
def local_ai(q):
    return "Take a slow breath. You are safe. Focus on one small step."

# ================= MASTER =================
def smart_ai(q):

    s = serper(q)
    if valid(s): return s

    d = duck(q)
    if valid(d): return d

    w = wiki(q)
    if valid(w): return w

    g = gemini(q)
    if valid(g): return g

    return local_ai(q)

# ================= DSS =================
def dss(q):
    q=q.lower()

    if "suicide" in q:
        return "Suicidal Risk","Severe","Immediate help required","red"
    if "depress" in q:
        return "Depression","Moderate","Consult psychologist","orange"
    if "anxiety" in q:
        return "Anxiety","Mild","Relaxation advised","green"

    return "Stress","Mild","Lifestyle care","green"

# ================= STATE =================
if "chat" not in st.session_state:
    st.session_state.chat=[]

# ================= INPUT =================
st.subheader(" Enter your problem")
q = st.text_area("Type here")

# ================= SEND =================
if st.button("SEND"):
    if q.strip():

        cond, sev, adv, color = dss(q)
        ai = smart_ai(q)

        st.session_state.chat.append(("user",q))
        st.session_state.chat.append(("dss",(cond,sev,adv,color)))
        st.session_state.chat.append(("ai",ai))

# ================= CHAT =================
st.subheader(" Conversation")

for role,msg in st.session_state.chat:

    if role=="user":
        st.markdown(f'<div class="user"> {msg}</div>',unsafe_allow_html=True)

    elif role=="dss":
        c,s,a,col = msg
        st.markdown(f"""
        <div class="{col}">
         Condition: {c}<br>
         Severity: {s}<br>
         Action: {a}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="ai"> {msg}</div>',unsafe_allow_html=True)

# ================= WHATSAPP =================
st.markdown("---")

st.markdown(f"""
<a href="https://wa.me/{WHATSAPP_NUMBER}">
<div style="background:#25D366;padding:18px;text-align:center;
color:white;font-size:20px;border-radius:10px;">
 CLICK TO OPEN WHATSAPP
</div>
</a>
""", unsafe_allow_html=True)