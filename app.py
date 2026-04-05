import streamlit as st
import requests
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

# =========================
# SAFE GRADIENT UI
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    color: white;
}

textarea, input {
    background-color: #ffffff !important;
    color: black !important;
    border-radius: 10px !important;
}

.stButton>button {
    background: #000000;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

h1, h2, h3 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("DURGA PSYCHIATRIC CENTRE")

# =========================
# PROFILE
# =========================
try:
    st.image("profile.jpg", width=180)
except:
    st.warning("Upload profile.jpg")

st.markdown("""
D.Durga  
DPN Nursing, DAHM, BBA, MBA HR, MSW Medical Psychiatry  

Founder and CEO  
Durga Psychiatric Centre
""")

st.divider()

# =========================
# AI FUNCTIONS
# =========================
def local_ai(q):
    return "Slow down. Breathe gently. Take one step at a time."

def gemini_ai(q):
    key = st.secrets.get("GEMINI_API_KEY", "")
    if not key:
        return None
    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + key
        data = {"contents":[{"parts":[{"text":q}]}]}
        r = requests.post(url, json=data, timeout=5)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None

def deepseek_ai(q):
    key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if not key:
        return None
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": "Bearer " + key}
        data = {
            "model": "deepseek-chat",
            "messages":[{"role":"user","content":q}]
        }
        r = requests.post(url, json=data, headers=headers, timeout=5)
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

        return None
    except:
        return None

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
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# =========================
# CHAT UI
# =========================
st.subheader("AI Mental Health Assistant")

user_input = st.text_area("Tell me what you are feeling", key="input_text")

if st.button("SEND"):
    if user_input.strip():

        answer = smart_ai(user_input)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("AI", answer))

        st.session_state.input_text = ""
        st.rerun()

# =========================
# DISPLAY CHAT
# =========================
for role, msg in st.session_state.history:
    if role == "You":
        st.write("You:", msg)
    else:
        st.write("AI:", msg)

# =========================
# CONSULT FORM
# =========================
st.divider()
st.subheader("Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Mobile Number")
concern = st.selectbox(
    "Select Concern",
    ["Stress", "Anxiety", "Depression", "Sleep Issues"]
)

if st.button("Submit"):
    if name and phone:
        message = urllib.parse.quote(
            "Name: " + name + "\nPhone: " + phone + "\nConcern: " + concern
        )

        whatsapp_url = "https://wa.me/917395944527?text=" + message

        st.success("Click below to open WhatsApp")
        st.markdown("[Open WhatsApp](" + whatsapp_url + ")")
    else:
        st.warning("Please fill all details")