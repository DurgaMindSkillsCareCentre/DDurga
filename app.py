import streamlit as st
import requests
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

SERPER_API_KEY = "YOUR_SERPER_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_KEY"

# =========================
# UI
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    color: white;
}

textarea, input {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
}

.stButton>button {
    background: black;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

/* WhatsApp */
.whatsapp-btn {
    display:block;
    text-align:center;
    padding:15px;
    background: linear-gradient(90deg,#25D366,#128C7E);
    color:white;
    font-size:18px;
    border-radius:12px;
    text-decoration:none;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("DURGA PSYCHIATRIC CENTRE")

try:
    st.image("profile.jpg", width=180)
except:
    st.warning("Upload profile.jpg")

st.markdown("""
**D.Durga**  
DPN Nursing, DAHM, BBA, MBA HR, MSW Medical Psychiatry  

Founder and CEO  
Durga Psychiatric Centre
""")

st.divider()

# =========================
# UTILS
# =========================
def summarize(text):
    parts = text.split(".")
    clean = [p.strip() for p in parts if len(p.strip()) > 25]
    return ". ".join(clean[:3]) + "." if clean else None

# =========================
# SERPER (GOOGLE)
# =========================
def serper_ai(q):
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        res = requests.post(url, headers=headers, json={"q": q}, timeout=8)

        if res.status_code != 200:
            return None

        data = res.json()

        snippets = []
        for item in data.get("organic", [])[:3]:
            if "snippet" in item:
                snippets.append(item["snippet"])

        if not snippets:
            return None

        return summarize(" ".join(snippets))

    except:
        return None

# =========================
# WIKIPEDIA (VERY RELIABLE)
# =========================
def wiki_ai(q):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(q)}"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()

        return summarize(data.get("extract", ""))

    except:
        return None

# =========================
# DUCKDUCKGO
# =========================
def duck_ai(q):
    try:
        url = "https://api.duckduckgo.com/"
        res = requests.get(url, params={"q": q, "format": "json"}, timeout=5)

        data = res.json()

        return summarize(data.get("AbstractText", ""))

    except:
        return None

# =========================
# GEMINI
# =========================
def gemini_ai(q):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [{"parts": [{"text": q}]}]
        }

        res = requests.post(url, json=payload, timeout=8)

        data = res.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        return summarize(text)

    except:
        return None

# =========================
# LOCAL AI
# =========================
def local_ai(q):
    q = q.lower()

    if "sleep" in q or "insomnia" in q:
        return "Insomnia is difficulty sleeping due to stress or irregular routine. Maintain consistent sleep schedule and avoid screens."

    if "anxiety" in q:
        return "Anxiety is excessive worry without danger. It triggers stress response. Breathing and relaxation techniques help control it."

    if "depress" in q:
        return "Depression is persistent sadness and low energy. Early support, routine, and therapy help recovery."

    return "Take a slow breath. Focus on one step at a time. You are safe."

# =========================
# SMART ROUTER
# =========================
def smart_ai(q):

    for func in [serper_ai, wiki_ai, duck_ai, gemini_ai]:
        result = func(q)
        if result:
            return result

    return local_ai(q)

# =========================
# STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# =========================
# SEND
# =========================
def handle_send():
    q = st.session_state.user_input.strip()
    if not q:
        return

    ans = smart_ai(q)

    st.session_state.history.append(("You", q))
    st.session_state.history.append(("AI", ans))

    st.session_state.user_input = ""

# =========================
# INPUT
# =========================
st.subheader("AI Mental Health Assistant")

st.text_area("Tell me what you're feeling", key="user_input")

st.button("SEND", on_click=handle_send)

# =========================
# CHAT
# =========================
with st.container():
    for role, msg in st.session_state.history:
        st.write(f"**{role}:** {msg}")

# =========================
# SPACE FIX
# =========================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.divider()

# =========================
# CONSULT FORM
# =========================
with st.container():
    st.subheader("Book Consultation")

    name = st.text_input("Name")
    phone = st.text_input("Mobile Number")
    concern = st.selectbox(
        "Concern",
        ["Stress", "Anxiety", "Depression", "Sleep Issues"]
    )

    if st.button("Submit"):
        if name and phone:
            msg = urllib.parse.quote(
                f"Name: {name}\nPhone: {phone}\nConcern: {concern}"
            )

            wa_url = f"https://wa.me/917395944527?text={msg}"

            st.markdown(
                f'<a class="whatsapp-btn" href="{wa_url}" target="_blank">CLICK TO OPEN WHATSAPP</a>',
                unsafe_allow_html=True
            )
        else:
            st.warning("Fill all details")