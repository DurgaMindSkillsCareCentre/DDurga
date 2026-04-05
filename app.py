import streamlit as st
import requests
import urllib.parse
import re

# =========================
# 🔐 KEYS
# =========================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", "")

# =========================
# 🎨 ULTRA PREMIUM UI
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f2027,#2c5364);
    color:white;
}
h1,h2,h3,h4,h5,p,label {
    color:white !important;
}
textarea {
    border-radius:12px !important;
}
.stButton button {
    background:#000 !important;
    color:#fff !important;
    border-radius:12px;
    padding:10px 20px;
    font-weight:bold;
}
.chat-box {
    background:#1e2a38;
    padding:12px;
    border-radius:12px;
    margin-top:10px;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 👩 PROFILE
# =========================
st.image("profile.jpg", width=150)

st.markdown("""
### D.Durga  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)  
**Founder & CEO**  
**Durga Psychiatric Centre**
""")

st.markdown("---")

# =========================
# 🧠 LOCAL AI
# =========================
def local_ai(q):
    return "Take a deep breath. Break your tasks into small steps. You are not alone."

# =========================
# 🤖 GEMINI
# =========================
def gemini_ai(q):
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents":[{"parts":[{"text":q}]}]}
        r = requests.post(url, json=payload, timeout=5)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None

# =========================
# 🤖 DEEPSEEK
# =========================
def deepseek_ai(q):
    if not DEEPSEEK_API_KEY:
        return None
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
        payload = {
            "model":"deepseek-chat",
            "messages":[{"role":"user","content":q}]
        }
        r = requests.post(url, json=payload, headers=headers, timeout=5)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return None

# =========================
# 🌐 SERPER
# =========================
def search_link(q):
    if not SERPER_API_KEY:
        return None
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        data = requests.post(url, json={"q":q}, headers=headers).json()
        return data["organic"][0]["link"]
    except:
        return None

# =========================
# 🧹 CLEAN + FILTER
# =========================
def extract_clean_text(html):
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.S)

    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)

    blacklist = [
        "menu","skip","search","privacy","terms",
        "login","about","contact","nhs","home"
    ]

    sentences = text.split(".")
    clean = []

    for s in sentences:
        if len(s) > 40 and not any(b in s.lower() for b in blacklist):
            clean.append(s.strip())

    return clean[:10]

# =========================
# 🧠 SMART SUMMARY (STRICT 3 LINES)
# =========================
def summarize(sentences, query):
    scored = []

    for s in sentences:
        score = sum(word in s.lower() for word in query.lower().split())
        if score > 0:
            scored.append((score, s))

    scored.sort(reverse=True)

    best = [s for _, s in scored[:3]]

    return ". ".join(best) + "."

# =========================
# 🌐 WEB AI (FIXED)
# =========================
def web_ai(q):
    link = search_link(q)
    if not link:
        return None

    try:
        html = requests.get(link, timeout=5).text
        clean = extract_clean_text(html)
        return summarize(clean, q)
    except:
        return None

# =========================
# 🧠 MASTER AI
# =========================
def smart_ai(q):

    r = gemini_ai(q)
    if r:
        return r[:400]

    r = deepseek_ai(q)
    if r:
        return r[:400]

    r = web_ai(q)
    if r:
        return r

    return local_ai(q)

# =========================
# 💬 CHAT
# =========================
user_input = st.text_area("Tell me what you're feeling:")

if st.button("SEND"):
    if user_input.strip():

        st.markdown(f'<div class="chat-box">You: {user_input}</div>', unsafe_allow_html=True)

        ans = smart_ai(user_input)

        st.markdown(f'<div class="chat-box">AI: {ans}</div>', unsafe_allow_html=True)

# =========================
# 📞 CONSULT FORM
# =========================
st.markdown("---")
st.markdown("## 📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Mobile")

cause = st.selectbox("Select Concern",
    ["Stress","Anxiety","Depression","Sleep Issues"]
)

if st.button("Submit"):

    msg = urllib.parse.quote(
        f"Name: {name}\nPhone: {phone}\nConcern: {cause}"
    )

    link = f"https://wa.me/917395944527?text={msg}"

    st.markdown(f"""
<a href="{link}" target="_blank">
<button style="background:#000;color:#fff;padding:12px;border-radius:12px;">
Open WhatsApp
</button>
</a>
""", unsafe_allow_html=True)