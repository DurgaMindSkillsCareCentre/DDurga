import streamlit as st
import requests
import urllib.parse

# =========================
# 🔐 API KEYS
# =========================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")

# =========================
# 🎨 UI
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
        return "Anxiety is caused by overactivation of the amygdala and stress hormones."
    if "sleep" in p:
        return "Sleep problems occur due to stress, overthinking, and irregular cycles."
    return "Relax, breathe slowly, and focus on one step at a time."

# =========================
# 🌐 GEMINI (FIXED)
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
# 🌍 WEB AI (NO BS4)
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

        for t in res.get("RelatedTopics", []):
            if isinstance(t, dict) and t.get("Text"):
                results.append(t["Text"])
                break
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
    sentences = combined.split(".")
    return ". ".join(sentences[:3]) + "."

# =========================
# 🧠 SMART ROUTER
# =========================
def smart_ai(prompt):

    g = gemini(prompt)
    if g:
        return g, "Gemini"

    d = deepseek(prompt)
    if d:
        return d, "DeepSeek"

    w = web_ai(prompt)
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