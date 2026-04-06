# -*- coding: utf-8 -*-
import streamlit as st
import requests
import urllib.parse
import re

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

WHATSAPP_NUMBER = "917395944527"
SERPER_API_KEY = "YOUR_SERPER_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_KEY"

# ================= UI =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#5f6dfc,#7b2ff7); color:white;}

.stButton button {
    background:black; color:white;
    font-size:18px; border-radius:10px;
}

.user {background:#111;padding:12px;border-radius:12px;margin:6px;text-align:right;}
.ai {background:#ffffff22;padding:12px;border-radius:12px;margin:6px;}

.dss-green {background:#00c853;padding:12px;border-radius:12px;margin:6px;color:white;}
.dss-orange {background:#ff9800;padding:12px;border-radius:12px;margin:6px;color:white;}
.dss-red {background:#e53935;padding:12px;border-radius:12px;margin:6px;color:white;}

.float-w {position:fixed;bottom:90px;right:20px;background:#25D366;width:60px;height:60px;
border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;color:white;}

.float-c {position:fixed;bottom:160px;right:20px;background:#0a84ff;width:60px;height:60px;
border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;color:white;}

.footer {position:fixed;bottom:0;width:100%;background:black;color:white;text-align:center;padding:10px;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🧠 DURGA PSYCHIATRIC CENTRE")
st.image("profile.jpg", width=120)

# ================= CLEAN =================
def clean(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text)
    return " ".join(text.split('.')[:3])

def valid(ans):
    return ans and len(ans.strip()) > 20

# ================= WEB AI =================
def serper(q):
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        res = requests.post(url, json={"q": q}, headers=headers).json()
        return clean(res.get("organic", [{}])[0].get("snippet",""))
    except:
        return ""

def duck(q):
    try:
        res = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json").json()
        return clean(res.get("AbstractText",""))
    except:
        return ""

def wiki(q):
    try:
        res = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}").json()
        return clean(res.get("extract",""))
    except:
        return ""

def gemini(q):
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data = {"contents":[{"parts":[{"text":q}]}]}
        res = requests.post(url,json=data).json()
        return clean(res["candidates"][0]["content"]["parts"][0]["text"])
    except:
        return ""

def local_ai(q):
    return "Take a slow breath. You are safe. Focus on one small step."

def smart_ai(q):
    for fn in [serper, duck, wiki, gemini]:
        ans = fn(q)
        if valid(ans):
            return ans
    return local_ai(q)

# ================= DSS =================
def dss(q):
    q=q.lower()

    if "suicide" in q:
        return "Suicidal Risk","Critical","Immediate help required","dss-red"
    if "depress" in q:
        return "Depression","Moderate","Consult psychologist","dss-orange"
    if "anxiety" in q:
        return "Anxiety","Mild","Relaxation advised","dss-green"
    return "Stress","Mild","Lifestyle care","dss-green"

# ================= STATE =================
if "chat" not in st.session_state:
    st.session_state.chat=[]

# ================= INPUT =================
st.subheader("💬 Enter your problem")

col1, col2 = st.columns([8,1])

with col1:
    query = st.text_area("Type here", height=120)

with col2:
    if st.button("❌"):
        query = ""

# ================= SEND =================
if st.button("SEND"):

    if query.strip():

        cond, sev, adv, color = dss(query)
        ai = smart_ai(query)

        st.session_state.chat.append(("user",query))
        st.session_state.chat.append(("dss",(cond,sev,adv,color)))
        st.session_state.chat.append(("ai",ai))

# ================= CHAT =================
st.subheader("💬 Conversation")

for role,msg in st.session_state.chat:

    if role=="user":
        st.markdown(f'<div class="user">👤 {msg}</div>',unsafe_allow_html=True)

    elif role=="dss":
        cond,sev,adv,color = msg
        st.markdown(f"""
        <div class="{color}">
        🧠 Condition: {cond}<br>
        ⚠ Severity: {sev}<br>
        💡 Action: {adv}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="ai">🤖 {msg}</div>',unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ================= FORM =================
st.subheader("📞 Book Consultation")

name=st.text_input("Name")
phone=st.text_input("Mobile")

cause=st.selectbox("Concern",[
"Stress","Anxiety","Depression","Panic Disorder",
"OCD","Bipolar Disorder","Sleep Disorder",
"Relationship Issues","Addiction","Sexual Issues","Other"
])

mode=st.radio("Mode",["Online","In-Person"])
time=st.selectbox("Time",["Morning","Afternoon","Evening"])
loc=st.text_input("Location")

if st.button("Submit"):

    if name and phone:

        msg=f"""I would like to request an appointment with Psychologist D.Durga.

Name: {name}
Mobile: {phone}
Concern: {cause}
Mode: {mode}
Time: {time}
Location: {loc}

Please call back.
"""

        url=f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

        st.markdown(f"""
        <a href="{url}" target="_blank">
        <div style="background:#25D366;padding:18px;text-align:center;
        color:white;font-size:20px;border-radius:10px;">
        📲 CLICK TO OPEN WHATSAPP
        </div>
        </a>
        """,unsafe_allow_html=True)

# ================= FLOAT =================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP_NUMBER}">
<div class="float-w">💬</div></a>

<a href="tel:+{WHATSAPP_NUMBER}">
<div class="float-c">📞</div></a>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP_NUMBER}">
<div class="footer">📞 Book Consultation on WhatsApp</div>
</a>
""", unsafe_allow_html=True)