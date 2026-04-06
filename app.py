# -*- coding: utf-8 -*-
import streamlit as st
import requests
import urllib.parse
import re

# ================= CONFIG =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

SERPER_API = st.secrets.get("SERPER_API_KEY", "")
GEMINI_API = st.secrets.get("GEMINI_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

# ================= CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#5f6dfc,#7b2ff7);
    color:white;
}
.block-container { padding-bottom:120px; }
label { color:white !important; }

.mic-btn {
 width:110px;height:110px;border-radius:50%;
 background:#25D366;
 display:flex;align-items:center;justify-content:center;
 font-size:40px;color:white;margin:auto;
}

.footer {
 position:fixed;bottom:0;width:100%;
 background:black;color:white;text-align:center;
 padding:10px;z-index:9999;
}

.float-w {
 position:fixed;bottom:90px;right:20px;
 background:#25D366;width:60px;height:60px;
 border-radius:50%;display:flex;
 align-items:center;justify-content:center;
 font-size:26px;color:white;z-index:9999;
}
.float-c {
 position:fixed;bottom:160px;right:20px;
 background:#0a84ff;width:60px;height:60px;
 border-radius:50%;display:flex;
 align-items:center;justify-content:center;
 font-size:26px;color:white;z-index:9999;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🧠 DURGA PSYCHIATRIC CENTRE")

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

# ================= CLEAN =================
def clean_text(t):
    if not isinstance(t, str):
        return ""
    t = re.sub(r'\s+', ' ', t)
    s = re.split(r'(?<=[.!?]) +', t)
    return " ".join(s[:3])

# ================= WEB AI =================
def serper(q):
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API},
            json={"q": q}, timeout=5)
        return r.json()["organic"][0]["snippet"]
    except:
        return ""

def duck(q):
    try:
        return requests.get(
            f"https://api.duckduckgo.com/?q={q}&format=json"
        ).json().get("AbstractText","")
    except:
        return ""

def wiki(q):
    try:
        return requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        ).json().get("extract","")
    except:
        return ""

def gemini(q):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API}"
        data = {"contents":[{"parts":[{"text":"Explain in 3 lines: "+q}]}]}
        r = requests.post(url,json=data)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return ""

def local_ai(q):
    return "You may be experiencing stress. Small steps and support help recovery."

def smart_ai(q):
    if not isinstance(q, str) or not q.strip():
        return ""
    text = serper(q) or duck(q) or wiki(q) or gemini(q) or local_ai(q)
    return clean_text(text)

# ================= DSS =================
def dss(q):
    if not isinstance(q, str):
        return "Unknown", "Low", "Provide valid input"

    q = q.lower()

    if "suicide" in q:
        return "Suicidal Risk", "Critical", "Immediate help required"

    if "depress" in q:
        return "Depression", "Moderate", "Consult psychologist"

    if "anxiety" in q:
        return "Anxiety", "Mild-Moderate", "Therapy helps"

    return "Stress", "Mild", "Relax and manage routine"

# ================= VOICE =================
st.subheader("🎤 Voice Input")

voice_html = """
<div style="text-align:center;">
<div class="mic-btn" onclick="start()">🎤</div>
<p>Tap and Speak</p>
</div>

<script>
function start(){
 var r=new webkitSpeechRecognition();
 r.lang="en-US";
 r.start();
 r.onresult=function(e){
  let t=e.results[0][0].transcript;
  window.parent.postMessage(
   {type:"streamlit:setComponentValue",value:t},"*"
  );
 }
}
</script>
"""

voice = st.components.v1.html(voice_html, height=200)

# ================= RESULT =================
if isinstance(voice, str) and voice.strip():

    cond, sev, adv = dss(voice)
    ai = smart_ai(voice)

    st.markdown("### 🧠 Analysis")
    st.write(f"Condition: {cond}")
    st.write(f"Severity: {sev}")
    st.write(f"Advice: {adv}")

    st.markdown("### 🌐 AI Summary")
    st.write(ai)

st.markdown("<br>", unsafe_allow_html=True)

# ================= FORM =================
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Mobile")

cause = st.selectbox("Concern", [
"Stress","Anxiety","Depression","Panic Disorder",
"OCD","Bipolar Disorder","PTSD","ADHD",
"Sleep Disorder","Relationship Issues",
"Addiction","Sexual Health Issues","Other"
])

mode = st.radio("Mode", ["Online","In-Person"])
time = st.selectbox("Time", ["Morning","Afternoon","Evening"])
loc = st.text_input("Location")

if st.button("Submit"):

    if name and phone:

        msg = f"""I would like to request an appointment.

Name: {name}
Mobile: {phone}
Concern: {cause}
Mode: {mode}
Time: {time}
Location: {loc}
"""

        url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

        st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)

        st.markdown(f'<a href="{url}" target="_blank">CLICK TO OPEN WHATSAPP</a>', unsafe_allow_html=True)

    else:
        st.warning("Enter Name and Mobile")

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