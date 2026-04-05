import streamlit as st
import requests
import urllib.parse
import re
import time

# =========================
# 🔐 API KEYS (ADD IN SECRETS)
# =========================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")
SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", "")

# =========================
# 🎨 PREMIUM UI
# =========================
st.set_page_config(page_title="Durga AI", layout="wide")

st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#4e54c8,#8f94fb);
}
textarea, input {
    border-radius: 12px !important;
}
.stButton button {
    background: black !important;
    color: white !important;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 👩 PROFILE SECTION
# =========================
col1, col2 = st.columns([1,2])

with col1:
    st.image("profile.jpg", width=180)

with col2:
    st.markdown("""
### D.Durga  
**DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)**  
**Founder & CEO**  
**Durga Psychiatric Centre**
""")

st.markdown("---")

# =========================
# 🧠 LOCAL AI
# =========================
def local_ai(q):
    q = q.lower()
    if "anxiety" in q:
        return "Anxiety is when your brain's alarm system becomes overactive, even without real danger."
    if "sleep" in q:
        return "Sleep problems often occur due to stress, irregular routines, or overthinking."
    if "depression" in q:
        return "Depression is a condition causing persistent sadness, low energy, and loss of interest."
    return "Take a deep breath. Focus on one small step at a time."

# =========================
# 🤖 GEMINI
# =========================
def gemini_ai(q):
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents":[{"parts":[{"text":q}]}]}
        r = requests.post(url, json=payload, timeout=6)
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
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages":[{"role":"user","content":q}]
        }
        r = requests.post(url, json=payload, headers=headers, timeout=6)
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except:
        return None

# =========================
# 🌐 SERPER SEARCH
# =========================
def serper_search(q):
    if not SERPER_API_KEY:
        return []
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": q}
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        return [i["link"] for i in data.get("organic", [])[:3]]
    except:
        return []

# =========================
# 🧹 CLEAN TEXT
# =========================
def clean_text(html):
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)

    blacklist = ["menu","login","privacy","terms","contact"]

    sentences = text.split(".")
    good = []
    for s in sentences:
        if len(s) > 40 and not any(b in s.lower() for b in blacklist):
            good.append(s.strip())

    return ". ".join(good[:20])

# =========================
# 🧠 SUMMARY ENGINE
# =========================
def summarize(text, query):
    sents = text.split(".")
    scored = []

    for s in sents:
        score = sum(word in s.lower() for word in query.lower().split())
        if score > 0:
            scored.append((score, s))

    scored.sort(reverse=True)
    best = [s for _, s in scored[:5]]

    return ". ".join(best)

# =========================
# 🌐 WEB AI
# =========================
def web_ai(q):
    links = serper_search(q)
    combined = ""

    for link in links:
        try:
            html = requests.get(link, timeout=5).text
            combined += clean_text(html)
        except:
            continue

    if combined:
        return summarize(combined, q)

    return None

# =========================
# 🧠 MASTER AI
# =========================
def smart_ai(q):

    # 1 Gemini
    r = gemini_ai(q)
    if r:
        return "🤖 Gemini: " + r

    # 2 DeepSeek
    r = deepseek_ai(q)
    if r:
        return "🤖 DeepSeek: " + r

    # 3 Web AI
    r = web_ai(q)
    if r:
        return "🌐 Web AI: " + r

    # 4 Local fallback
    return "⚠️ Local AI: " + local_ai(q)

# =========================
# UI INPUT
# =========================
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

user_input = st.text_area("Tell me what you're feeling:", key="input_text")

if st.button("SEND"):
    if user_input.strip():
        response = smart_ai(user_input)

        st.markdown(f"### You: {user_input}")
        st.markdown(f"### {response}")

        # CLEAR INPUT
        st.session_state.input_text = ""

        # =========================
        # 📲 WHATSAPP AUTO
        # =========================
        msg = urllib.parse.quote(f"Name: User\nQuery: {user_input}")
        url = f"https://wa.me/917395944527?text={msg}"

        st.markdown(f"""
<a href="{url}" target="_blank">
<button style="background:black;color:white;padding:10px;border-radius:10px;">
Open WhatsApp
</button>
</a>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# 📞 CONSULTATION FORM
# =========================
st.markdown("## 📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

concern = st.selectbox("Select Concern",
    ["Stress","Anxiety","Depression","Sleep Issues"])

if st.button("Submit & Continue"):
    msg = urllib.parse.quote(
        f"Name:{name}\nPhone:{phone}\nConcern:{concern}"
    )
    link = f"https://wa.me/917395944527?text={msg}"
    st.markdown(f"[Click to Chat on WhatsApp]({link})")