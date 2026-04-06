# -*- coding: utf-8 -*-
import streamlit as st
import requests
import urllib.parse
import re
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ================= CONFIG =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

WHATSAPP_NUMBER = "917395944527"
SERPER_API_KEY = "YOUR_SERPER_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_KEY"

# ================= UI =================
st.markdown("""
<style>
html, body, [class*="css"] {
 font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Emoji",
 "Apple Color Emoji", "Noto Color Emoji", sans-serif !important;
}

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
st.title(" DURGA PSYCHIATRIC CENTRE")
st.image("profile.jpg", width=120)

st.markdown("""
**D. Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)  
Founder & CEO  
Durga Psychiatric Centre  
 +91 7395944527
""")

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
        res = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY},
            json={"q": q}, timeout=5).json()
        return clean(res.get("organic",[{}])[0].get("snippet",""))
    except:
        return ""

def duck(q):
    try:
        res = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json", timeout=5).json()
        return clean(res.get("AbstractText",""))
    except:
        return ""

def wiki(q):
    try:
        res = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}", timeout=5).json()
        return clean(res.get("extract",""))
    except:
        return ""

def gemini(q):
    try:
        url=f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data={"contents":[{"parts":[{"text":q}]}]}
        res=requests.post(url,json=data,timeout=5).json()
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

# ================= PDF =================
def generate_pdf(query, cond, sev, adv, ai_text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Durga Psychiatric Centre</b>", styles["Title"]))
    story.append(Spacer(1,10))

    try:
        story.append(Image("profile.jpg", width=1.5*inch, height=1.5*inch))
        story.append(Spacer(1,10))
    except:
        pass

    story.append(Paragraph("<b>D. Durga</b>", styles["Heading2"]))
    story.append(Paragraph("DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)", styles["Normal"]))
    story.append(Paragraph("Founder & CEO", styles["Normal"]))
    story.append(Paragraph(" +91 7395944527", styles["Normal"]))
    story.append(Spacer(1,10))

    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1,10))

    story.append(Paragraph(f"<b>Query:</b> {query}", styles["Normal"]))
    story.append(Spacer(1,10))

    story.append(Paragraph(f"Condition: {cond}", styles["Normal"]))
    story.append(Paragraph(f"Severity: {sev}", styles["Normal"]))
    story.append(Paragraph(f"Advice: {adv}", styles["Normal"]))
    story.append(Spacer(1,10))

    story.append(Paragraph(f"AI Summary: {ai_text}", styles["Normal"]))

    doc.build(story)

# ================= STATE =================
if "chat" not in st.session_state:
    st.session_state.chat=[]

# ================= INPUT =================
st.subheader(" Enter your problem")

col1,col2=st.columns([8,1])

with col1:
    query=st.text_area("Type here", height=120)

with col2:
    if st.button(""):
        query=""

# ================= SEND =================
if st.button("SEND"):
    if query.strip():
        cond,sev,adv,color=dss(query)
        ai=smart_ai(query)

        st.session_state.chat.append(("user",query))
        st.session_state.chat.append(("dss",(cond,sev,adv,color)))
        st.session_state.chat.append(("ai",ai))

        generate_pdf(query, cond, sev, adv, ai)

# ================= CHAT =================
st.subheader(" Conversation")

for role,msg in st.session_state.chat:

    if role=="user":
        st.markdown(f'<div class="user"> {msg}</div>',unsafe_allow_html=True)

    elif role=="dss":
        cond,sev,adv,color=msg
        st.markdown(f"""
        <div class="{color}">
         Condition: {cond}<br>
         Severity: {sev}<br>
         Action: {adv}
        </div>
        """,unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="ai"> {msg}</div>',unsafe_allow_html=True)

# ================= PDF DOWNLOAD =================
try:
    with open("report.pdf","rb") as f:
        st.download_button(" Download Report PDF", f, file_name="report.pdf")
except:
    pass

# ================= WHATSAPP =================
st.subheader(" Book Consultation")

name=st.text_input("Name")
phone=st.text_input("Mobile")

if st.button("Submit"):
    if name and phone:
        msg=f"Appointment Request\nName:{name}\nMobile:{phone}"
        url=f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

        st.markdown(f"""
        <a href="{url}" target="_blank">
        <div style="background:#25D366;padding:18px;text-align:center;
        color:white;font-size:20px;border-radius:10px;">
         CLICK TO OPEN WHATSAPP
        </div>
        </a>
        """,unsafe_allow_html=True)