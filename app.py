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
# 🎨 UI
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#4e54c8,#8f94fb);
}
.stButton button {
    background:black !important;
    color:white !important;
    border-radius:12px;
    font-weight:bold;
}
textarea {
    border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 👩 PROFILE
# =========================
st.image("profile.jpg", width=180)

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
    return "Take a deep breath. Break things into small steps. You are not alone."

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
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
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
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except:
        return None

# =========================
# 🌐 SERPER SEARCH
# =========================
def serper_links(q):
    if not SERPER_API_KEY:
        return []
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        r = requests.post(url, json={"q": q}, headers=headers)
        data = r.json()
        return [i["link"] for i in data.get("organic", [])[:3]]
    except:
        return []

# =========================
# 🧹 CLEAN CONTENT
# =========================
def clean_text(html):
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.S)

    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)

    blacklist = ["menu","login","privacy","terms","contact","about"]

    sentences = text.split(".")
    good = []

    for s in sentences:
        if len(s) > 40 and not any(b in s.lower() for b in blacklist):
            good.append(s.strip())

    return good[:15]

# =========================
# 🧠 SMART SUMMARY (CORE FIX)
# =========================
def smart_summary(sentences, query):
    scored = []

    for s in sentences:
        score = sum(word in s.lower() for word in query.lower().split())
        if score > 0:
            scored.append((score, s))

    scored.sort(reverse=True)

    best = [s for _, s in scored[:4]]

    if not best:
        return None

    return ". ".join(best) + "."

# =========================
# 🌐 WEB AI (FIXED)
# =========================
def web_ai(q):
    links = serper_links(q)

    all_sentences = []

    for link in links:
        try:
            html = requests.get(link, timeout=5).text
            cleaned = clean_text(html)
            all_sentences.extend(cleaned)
        except:
            continue

    return smart_summary(all_sentences, q)

# =========================
# 🧠 MASTER AI
# =========================
def smart_ai(q):

    r = gemini_ai(q)
    if r:
        return "Gemini: " + r[:500]

    r = deepseek_ai(q)
    if r:
        return "DeepSeek: " + r[:500]

    r = web_ai(q)
    if r:
        return "Web AI: " + r

    return "Local AI: " + local_ai(q)

# =========================
# INPUT
# =========================
user_input = st.text_area("Tell me what you're feeling:")

if st.button("SEND"):
    if user_input.strip():

        st.markdown(f"### You: {user_input}")

        answer = smart_ai(user_input)

        st.markdown(f"### {answer}")

        # WhatsApp
        msg = urllib.parse.quote(user_input)
        wa = f"https://wa.me/917395944527?text={msg}"

        st.markdown(f"""
<a href="{wa}" target="_blank">
<button style="background:black;color:white;padding:10px;border-radius:10px;">
Open WhatsApp
</button>
</a>
""", unsafe_allow_html=True)