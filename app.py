import streamlit as st
import requests
import urllib.parse

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

# =========================
# SAFE GRADIENT UI (NO BREAK)
# =========================
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    color: white;
}

/* Text inputs */
textarea, input {
    background-color: #ffffff !important;
    color: black !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #000000, #434343);
    color: white;
    border-radius: 12px;
    font-weight: bold;
    padding: 10px 20px;
}

/* Cards look */
.block-container {
    padding-top: 2rem;
}

/* Section titles */
h1, h2, h3 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🧠 DURGA PSYCHIATRIC CENTRE")

# =========================
# PROFILE
# =========================
try:
    st.image("profile.jpg", width=180)
except:
    st.warning("Profile image not found")

st.markdown("""
**D.Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)  

**Founder & CEO**  
Durga Psychiatric Centre
""")

st.divider()

# =========================
# AI BACKENDS
# =========================

def local_ai(q):
    return "Your mind is overwhelmed. Slow down, breathe deeply, and take one small step at a time."

def gemini_ai(q):
    key = st.secrets.get("GEMINI_API_KEY", "")
    if not key:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
        data = {"contents":[{"parts":[{"text":q}]}]}
        r = requests.post(url, json=data, timeout=6)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None

def deepseek_ai(q):
    key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if not key:
        return None
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}"}
        data = {
            "model": "deepseek-chat",
            "messages":[{"role":"user","content":q}]
        }
        r = requests.post(url, json=data, headers=headers, timeout=6)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return None

def web_ai(q):
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": q, "format": "json"}
        res = requests.get(url, params=params, timeout=5).json()

        if res.get("AbstractText"):
            return res["AbstractText"]

        return "Try relaxation, breathing exercises, and talking to someone you trust."
    except:
        return None

# =========================
# SMART AI ROUTER
# =========================
def smart_ai(q):

    r = gemini_ai(q)
    if r:
        return r[:300]

    r = deepseek_ai(q)
    if r:
        return r[:300]

    r = web_ai(q)
    if r:
        return r[:300]

    return local_ai(q)

# =========================
# CHAT
# =========================
st.subheader("AI Mental Health Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("Tell me what you're feeling:")

if st.button("SEND"):
    if user_input.strip():

        answer = smart_ai(user_input)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("AI", answer))

        # CLEAR INPUT (IMPORTANT FIX)
        st.session_state["clear_input"] = True
        st.rerun()

# CLEAR TEXT BOX AFTER SEND
if st.session_state.get("clear_input"):
    st.session_state["clear_input"] = False
    st.text_area("Tell me what you're feeling:", value="")

# DISPLAY CHAT
for role, msg in st.session_state.history:
    if role == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI:** {msg}")

# =========================
# CONSULT FORM
# =========================
st.divider()
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Mobile Number")
concern = st.selectbox(
    "Select Concern",
    ["Stress", "Anxiety", "Depression", "Sleep Issues"]
)

if st.button("Submit"):

    if name and phone:
        message = urllib.parse.quote(
            f"Name: {name}\nPhone: {phone}\nConcern: {concern}"
        )

        whatsapp_url = f"https://wa.me/917395944527?text={message}"

        st.success("Click below to continue")

        st.markdown(f"[👉 Open WhatsApp]( {whatsapp_url} )")
    else:
        st.warning("Please fill all fields")