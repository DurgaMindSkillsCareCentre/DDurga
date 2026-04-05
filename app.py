import streamlit as st
import requests
import urllib.parse
import re

# =========================
# 🔐 API KEYS
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
.stApp {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    color: white;
}
textarea, input {
    background: white !important;
    color: black !important;
    border-radius: 12px !important;
}
button {
    background: #111 !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 DURGA PSYCHIATRIC CENTRE")
st.subheader("🧠 AI Mental Health Assistant")

# =========================
# 🧠 LOCAL AI
# =========================
def local_ai(prompt):
    return "Take a deep breath. Relax your mind step by step."

# =========================
# 🌐 GEMINI
# =========================
def gemini(prompt):
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        res = requests.post(url, json={
            "contents":[{"parts":[{"text":prompt}]}]
        }, timeout=5)

        if res.status_code != 200:
            return None

        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None

# =========================
# 🔥 DEEPSEEK
# =========================
def deepseek(prompt):
    if not DEEPSEEK_API_KEY:
        return None
    try:
        res = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model":"deepseek-chat",
                "messages":[{"role":"user","content":prompt}]
            },
            timeout=5
        )

        if res.status_code != 200:
            return None

        return res.json()["choices"][0]["message"]["content"]
    except:
        return None

# =========================
# 🔍 SERPER SEARCH
# =========================
def serper_links(query):
    if not SERPER_API_KEY:
        return []

    try:
        res = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY},
            json={"q": query},
            timeout=6
        ).json()

        links = []
        for item in res.get("organic", [])[:3]:
            if item.get("link"):
                links.append(item["link"])

        return links
    except:
        return []

# =========================
# 🌍 SCRAPE WEB CONTENT
# =========================
def scrape_text(url):
    try:
        html = requests.get(url, timeout=5).text

        # remove scripts/styles
        html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.S)
        html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.S)

        # remove tags
        text = re.sub(r'<[^>]+>', ' ', html)

        # clean spaces
        text = re.sub(r'\s+', ' ', text)

        return text[:2000]  # limit size
    except:
        return ""

# =========================
# 🧠 SUMMARIZER
# =========================
def summarize(text):
    sentences = text.split(".")
    return ". ".join(sentences[:5]).strip() + "."

# =========================
# 🔥 MULTI-PAGE WEB AI
# =========================
def multi_web_ai(query):

    links = serper_links(query)

    if not links:
        return None

    combined = ""

    for link in links:
        combined += scrape_text(link) + " "

    if not combined.strip():
        return None

    return summarize(combined)

# =========================
# 🧠 SMART ROUTER
# =========================
def smart_ai(prompt):

    # 1️⃣ Gemini
    g = gemini(prompt)
    if g:
        return g, "Gemini"

    # 2️⃣ DeepSeek
    d = deepseek(prompt)
    if d:
        return d, "DeepSeek"

    # 3️⃣ 🔥 Multi-page Web AI
    w = multi_web_ai(prompt)
    if w:
        return w, "Web AI (Multi)"

    # 4️⃣ Local fallback
    return local_ai(prompt), "Local AI"

# =========================
# 💬 CHAT
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling:")
    submitted = st.form_submit_button("SEND")

if submitted and user_input.strip():

    response, source = smart_ai(user_input)

    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append((f"AI ({source})", response))

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")

# =========================
# 📞 CONSULT
# =========================
st.markdown("---")
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone")

if st.button("Submit & Continue"):
    if name and phone:
        msg = f"Hello, I am {name}. Phone: {phone}"
        link = f"https://wa.me/917395944527?text={urllib.parse.quote(msg)}"

        st.markdown(f'<meta http-equiv="refresh" content="1;url={link}">', unsafe_allow_html=True)
        st.success("Opening WhatsApp...")