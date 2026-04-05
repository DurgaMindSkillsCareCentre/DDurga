import streamlit as st
import requests
import urllib.parse

# =========================
# 🔐 API KEYS
# =========================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")

# =========================
# 🎨 UI DESIGN
# =========================
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

# =========================
# 🏥 HEADER
# =========================
st.title("🏥 DURGA PSYCHIATRIC CENTRE")
st.subheader("🧠 AI Mental Health Assistant")

# =========================
# 🧠 LOCAL AI (LAST RESORT)
# =========================
def local_ai(prompt):
    p = prompt.lower()
    if "mood swing" in p:
        return "Mood swings are like your feelings changing quickly, like sunny to rainy."
    if "anxiety" in p:
        return "Anxiety is when your brain feels too worried even when there is no danger."
    return "Take a deep breath and relax your mind step by step."

# =========================
# 🌐 GEMINI
# =========================
def gemini(prompt):
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        res = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
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
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=5
        )

        if res.status_code != 200:
            return None

        return res.json()["choices"][0]["message"]["content"]
    except:
        return None

# =========================
# 🌍 ADVANCED WEB AI
# =========================
def web_ai(prompt):
    results = []

    # DuckDuckGo
    try:
        res = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": prompt, "format": "json"},
            timeout=4
        ).json()

        if res.get("AbstractText"):
            results.append(res["AbstractText"])

        for topic in res.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(topic["Text"])
    except:
        pass

    # Wikipedia
    try:
        res = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{prompt}",
            timeout=4
        ).json()

        if res.get("extract"):
            results.append(res["extract"])
    except:
        pass

    return summarize(results)

# =========================
# 🧠 SUMMARIZER
# =========================
def summarize(texts):
    if not texts:
        return None

    combined = " ".join(texts)

    # Clean summary
    sentences = combined.split(".")
    summary = ". ".join(sentences[:4])

    return summary.strip() + "."

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

    # 3️⃣ Web AI (MAIN FALLBACK)
    w = web_ai(prompt)
    if w:
        return w, "Web AI"

    # 4️⃣ Local AI (LAST)
    return local_ai(prompt), "Local AI"

# =========================
# 💬 CHAT UI
# =========================
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

user_input = st.text_area(
    "Tell me what you're feeling:",
    key="input_text"
)

if st.button("SEND"):
    if user_input.strip():

        response, source = smart_ai(user_input)

        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI ({source}):** {response}")

        # 🔥 CLEAR INPUT BOX
        st.session_state.input_text = ""

# =========================
# 📞 CONSULTATION
# =========================
st.markdown("---")
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
concern = st.selectbox("Concern", ["Stress", "Anxiety", "Depression", "Sleep"])

if st.button("Submit & Continue"):
    if name and phone:
        msg = f"Hello, I am {name}. Concern: {concern}. Phone: {phone}"
        encoded = urllib.parse.quote(msg)

        url = f"https://wa.me/917395944527?text={encoded}"

        st.markdown(f'<meta http-equiv="refresh" content="1;url={url}">', unsafe_allow_html=True)
        st.success("Opening WhatsApp...")

    else:
        st.warning("Fill all fields")