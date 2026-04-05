import streamlit as st
import requests
import urllib.parse

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

SERPER_API_KEY = "YOUR_SERPER_API_KEY_HERE"

# =========================
# SAFE PREMIUM UI
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

/* WhatsApp Button */
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
    margin-top:10px;
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
# AI FUNCTIONS
# =========================
def summarize(text):
    sentences = text.split(".")
    clean = [s.strip() for s in sentences if len(s.strip()) > 20]
    return ". ".join(clean[:3]) + "."

def serper_search(query):
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query}

        res = requests.post(url, headers=headers, json=payload, timeout=8)
        data = res.json()

        if "organic" not in data:
            return None

        snippets = []
        for item in data["organic"][:3]:
            if "snippet" in item:
                snippets.append(item["snippet"])

        if not snippets:
            return None

        combined = " ".join(snippets)
        return summarize(combined)

    except:
        return None

def local_ai(q):
    q = q.lower()

    if "sleep" in q or "insomnia" in q:
        return "Insomnia is difficulty sleeping due to stress or irregular routine. Maintain fixed sleep time and reduce screen use before bed."
    
    if "anxiety" in q:
        return "Anxiety is excessive worry without real danger. It activates the body stress response. Breathing and relaxation help control it."
    
    if "depress" in q:
        return "Depression is persistent sadness, low energy, and loss of interest. Early support, routine, and professional help improve recovery."

    return "Take a slow breath. Focus on one step at a time. You are safe."

def smart_ai(q):
    result = serper_search(q)
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
# SEND FUNCTION
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
# CHAT DISPLAY (ISOLATED)
# =========================
with st.container():
    for role, msg in st.session_state.history:
        st.write(f"**{role}:** {msg}")

# =========================
# SPACE FIX (IMPORTANT)
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