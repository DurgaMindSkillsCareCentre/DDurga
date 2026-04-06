# -*- coding: utf-8 -*-
import os, re, html, urllib.parse
import requests
import streamlit as st

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

WHATSAPP_NUMBER = "917395944527"
SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", "")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# ================= UI =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#5f6dfc,#7b2ff7);color:white;}
.block-container{padding-bottom:260px;}

.stButton>button{
background:#000;color:white;border-radius:12px;
font-weight:800;padding:10px 18px;font-size:16px;
}

textarea,input{color:black!important;}

.bubble{border-radius:18px;padding:14px;margin:10px 0;}
.user{background:#111;color:white;}
.ai{background:rgba(255,255,255,0.15);}

.dss-green{background:#12c24f;padding:14px;border-radius:16px;}
.dss-orange{background:#ff9800;padding:14px;border-radius:16px;}
.dss-red{background:#e53935;padding:14px;border-radius:16px;}

.footer-bar{
position:fixed;bottom:0;width:100%;
background:#000;padding:14px;
}
.footer-btn{
display:flex;justify-content:center;align-items:center;
gap:12px;background:#25D366;
padding:20px;font-size:20px;
font-weight:900;border-radius:16px;
color:white;text-decoration:none;
}

.float{
position:fixed;right:18px;width:60px;height:60px;
border-radius:50%;display:flex;align-items:center;justify-content:center;
z-index:999;
}
.whatsapp{bottom:90px;background:#25D366;}
.call{bottom:160px;background:#0a84ff;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🧠 DURGA PSYCHIATRIC CENTRE")

if os.path.exists("profile.jpg"):
    st.image("profile.jpg", width=150)

st.markdown("""
**D. Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW  
Founder & CEO  
Durga Psychiatric Centre
""")

# ================= AI =================
def clean(text):
    text = re.sub(r"\s+"," ",str(text))
    return text.strip()

def summary(text):
    s = re.split(r'[.!?]', text)
    return "\n".join([i.strip() for i in s if len(i)>10][:3])

def serper(q):
    if not SERPER_API_KEY: return ""
    try:
        r = requests.post("https://google.serper.dev/search",
        headers={"X-API-KEY":SERPER_API_KEY},
        json={"q":q})
        data=r.json()
        return summary(str(data))
    except: return ""

def ddg(q):
    try:
        r=requests.get(f"https://api.duckduckgo.com/?q={q}&format=json")
        return summary(r.json().get("AbstractText",""))
    except: return ""

def wiki(q):
    try:
        r=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}")
        return summary(r.json().get("extract",""))
    except: return ""

def gemini(q):
    if not GEMINI_API_KEY: return ""
    try:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        r=requests.post(url,json={"contents":[{"parts":[{"text":q}]}]})
        return summary(r.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return ""

def local(q):
    return "Take a slow breath.\nYou are safe.\nFocus on one step."

def AI(q):
    for fn in [serper,ddg,wiki,gemini]:
        res=fn(q)
        if len(res)>20:
            return res
    return local(q)

# ================= DSS =================
def dss(q):
    q=q.lower()
    if "suicide" in q: return ("Suicidal Risk","Critical","Immediate help","dss-red")
    if "depress" in q: return ("Depression","Moderate","Consult","dss-orange")
    return ("Stress","Mild","Lifestyle","dss-green")

# ================= INPUT =================
st.subheader("💬 Enter your problem")
query=st.text_area("Type here")

if st.button("SEND"):
    if query:
        cond,sev,act,css=dss(query)

        st.markdown(f'<div class="bubble user">{query}</div>',unsafe_allow_html=True)

        st.markdown(f"""
        <div class="{css}">
        Condition: {cond}<br>
        Severity: {sev}<br>
        Action: {act}
        </div>
        """,unsafe_allow_html=True)

        st.markdown(f'<div class="bubble ai">{AI(query)}</div>',unsafe_allow_html=True)

# ================= FORM =================
st.subheader("📞 Book Consultation")

name=st.text_input("Name")
phone=st.text_input("Mobile")
cause=st.selectbox("Concern",["Stress","Depression","Anxiety","Addiction","Relationship","Sexual","Other"])

if st.button("Submit Consultation"):
    msg=f"""I would like to request an appointment with Psychologist D.Durga.

Name: {name}
Mobile: {phone}
Cause: {cause}

Please call back."""
    url=f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{url}" target="_blank" class="footer-btn">CLICK TO OPEN WHATSAPP</a>',unsafe_allow_html=True)

# ================= FLOAT =================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
<div class="float whatsapp">💬</div></a>

<a href="tel:+{WHATSAPP_NUMBER}">
<div class="float call">📞</div></a>
""",unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<div class="footer-bar">
<a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" class="footer-btn">
📞 💬 BOOK CONSULTATION NOW
</a>
</div>
""",unsafe_allow_html=True)