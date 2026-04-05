import streamlit as st
import requests
import urllib.parse
import re

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga AI", layout="centered")

# =========================
# PREMIUM UI
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
    border-radius: 12px;
    font-weight: bold;
    padding: 10px 20px;
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

# =========================
# PROFILE
# =========================
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
# SMART AI
# =========================

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def web_scrape_ai(query):
    try:
        search_url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        html = requests.get(search_url, timeout=5).text

        links = re.findall(r'nofollow" class="result__a" href="(.*?)"', html)

        if not links:
            return None

        first_link = links[0]
        page = requests.get(first_link, timeout=5).text

        paragraphs = re.findall(r'<p>(.*?)</p>', page)

        text = " ".join(paragraphs[:5])
        text = re.sub('<.*?>', '', text)

        text = clean_text(text)

        if len(text) < 50:
            return None

        return text[:300]

    except:
        return None


def local_ai(q):
    if "sleep" in q.lower():
        return "Sleep problems happen due to stress, overthinking, or irregular routine. Try fixed sleep time and avoid screens before bed."
    if "depress" in q.lower():
        return "Depression is prolonged sadness, low energy, and loss of interest. Talking to someone and small daily actions help recovery."
    if "stress" in q.lower():
        return "Stress is your body's response to pressure. Slow breathing, rest, and breaking tasks into small steps helps."
    return "Take a slow breath. You are safe. Focus on one step at a time."


def smart_ai(q):
    # 1️⃣ WEB AI
    result = web_scrape_ai(q)
    if result:
        return result

    # 2️⃣ LOCAL FALLBACK
    return local_ai(q)

# =========================
# STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# =========================
# SEND HANDLER
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

st.text_area(
    "Tell me what you're feeling",
    key="user_input"
)

st.button("SEND", on_click=handle_send)

# =========================
# CHAT
# =========================
for role, msg in st.session_state.history:
    st.write(f"**{role}:** {msg}")

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
            f"Name: {name}\nPhone: {phone}\nConcern: {concern}"
        )

        wa_url = f"https://wa.me/917395944527?text={msg}"

        st.markdown(
            f'<a class="whatsapp-btn" href="{wa_url}" target="_blank">CLICK TO OPEN WHATSAPP</a>',
            unsafe_allow_html=True
        )
    else:
        st.warning("Fill all details")