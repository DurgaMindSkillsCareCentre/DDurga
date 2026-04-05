import streamlit as st
import requests
import urllib.parse
from bs4 import BeautifulSoup

# =========================
# 🔐 API KEYS
# =========================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")

# =========================
# 🎨 PREMIUM UI
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    color: white;
}
textarea, input, select {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
}
button {
    background: #111 !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}
.whatsapp-btn {
    background: #0f9d58;
    color: white;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏥 HEADER
# =========================
st.title("🏥 DURGA PSYCHIATRIC CENTRE")
st.subheader("🧠 AI Mental Health Assistant")

# =========================
# 👩 PROFILE
# =========================
try:
    st.image("profile.jpg", width=140)
except:
    pass

st.markdown("""
**D. Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW  
(Medical & Psychiatry)  
Founder & CEO
""")

st.markdown("---")

# =========================
# 🧠 LOCAL AI
# =========================
def local_ai(prompt):
    p = prompt.lower()
    if "anxiety" in p:
        return "Anxiety is caused by overactivation of the brain’s fear center (amygdala) and stress hormones."
    if "sleep" in p:
        return "Sleep problems occur due to high stress, overthinking, and irregular sleep cycles."
    return "Relax your body, slow your breathing, and take one step at a time."

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
# 🌍 WEB SEARCH (MULTI SOURCE)
# =========================
def web_search_ai(query):
    results = []

    # 1️⃣ DuckDuckGo
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json"}
        res = requests.get(url, params=params, timeout=4).json()

        if res.get("AbstractText"):
            results.append(res["AbstractText"])

        for t in res.get("RelatedTopics", []):
            if isinstance(t, dict) and t.get("Text"):
                results.append(t["Text"])
                break
    except:
        pass

    # 2️⃣ Wikipedia
    try:
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        res = requests.get(wiki_url, timeout=4).json()
        if res.get("extract"):
            results.append(res["extract"])
    except:
        pass

    # 3️⃣ Basic scraping (fallback)
    try:
        search_url = f"https://duckduckgo.com/html/?q={query}"
        html = requests.get(search_url, timeout=4).text
        soup = BeautifulSoup(html, "html.parser")
        snippets = soup.find_all("a", class_="result__a", limit=2)
        for s in snippets:
            results.append(s.text)
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

    # simple compression logic
    sentences = combined.split(".")
    summary = ". ".join(sentences[:3])

    return summary.strip() + "."

# =========================
# 🧠 SMART ROUTER V5
# =========================
def smart_ai(prompt):

    g = gemini(prompt)
    if g:
        return g, "Gemini"

    d = deepseek(prompt)
    if d:
        return d, "DeepSeek"

    w = web_search_ai(prompt)
    if w:
        return w, "Web AI"

    return local_ai(prompt), "Local AI"

# =========================
# 💬 CHAT
# =========================
user_input = st.text_area("Tell me what you're feeling:")

if st.button("SEND"):
    if user_input.strip():
        response, source = smart_ai(user_input)

        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI ({source}):** {response}")

# =========================
# 📞 CONSULTATION
# =========================
st.markdown("---")
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
concern = st.selectbox("Select Concern", ["Stress", "Anxiety", "Depression", "Sleep Issue"])

if st.button("Submit & Continue"):
    if name and phone:

        msg = f"Hello, I am {name}. Concern: {concern}. Phone: {phone}"
        encoded = urllib.parse.quote(msg)
        url = f"https://wa.me/917395944527?text={encoded}"

        st.markdown(f'<meta http-equiv="refresh" content="1;url={url}">', unsafe_allow_html=True)
        st.success("Opening WhatsApp...")

        st.markdown(f"""
        <a href="{url}" target="_blank">
            <div class="whatsapp-btn">💬 Open WhatsApp</div>
        </a>
        """, unsafe_allow_html=True)

    else:
        st.warning("Please fill all fields")