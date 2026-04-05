import streamlit as st
import requests
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

# =========================
# UI (SAFE GRADIENT)
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
    background: black;
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
# AI LOGIC
# =========================
def local_ai(q):
    return "Take a slow breath. You are safe. Focus on one small step."

def web_ai(q):
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": q, "format": "json"}
        data = requests.get(url, params=params, timeout=5).json()

        if data.get("AbstractText"):
            return data["AbstractText"][:200]

        return None
    except:
        return None

def smart_ai(q):
    r = web_ai(q)
    if r:
        return r
    return local_ai(q)

# =========================
# SESSION STATE INIT
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# =========================
# SEND FUNCTION (FIXED)
# =========================
def handle_send():
    q = st.session_state.user_input.strip()
    if not q:
        return

    answer = smart_ai(q)

    st.session_state.history.append(("You", q))
    st.session_state.history.append(("AI", answer))

    # CLEAR INPUT SAFELY
    st.session_state.user_input = ""

# =========================
# INPUT UI (IMPORTANT KEY)
# =========================
st.subheader("AI Mental Health Assistant")

st.text_area(
    "Tell me what you are feeling",
    key="user_input"
)

st.button("SEND", on_click=handle_send)

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
    "Concern",
    ["Stress", "Anxiety", "Depression", "Sleep Issues"]
)

if st.button("Submit"):
    if name and phone:
        msg = urllib.parse.quote(
            "Name: " + name + "\nPhone: " + phone + "\nConcern: " + concern
        )
        url = "https://wa.me/917395944527?text=" + msg

        st.success("Click below to open WhatsApp")
        st.markdown("[Open WhatsApp](" + url + ")")
    else:
        st.warning("Fill all details")