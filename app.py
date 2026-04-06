import streamlit as st
import urllib.parse

# PAGE CONFIG
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# SAFE CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
    color: white;
}
textarea, input {
    color: black !important;
}
div.stButton > button {
    background-color: #111111;
    color: white;
    border-radius: 10px;
}
label {
    color: white !important;
}
.float-whatsapp {
    position: fixed;
    bottom: 90px;
    right: 20px;
    background: #25D366;
    color: white;
    padding: 15px;
    border-radius: 50%;
    z-index: 9999;
}
.float-call {
    position: fixed;
    bottom: 160px;
    right: 20px;
    background: #0a84ff;
    color: white;
    padding: 15px;
    border-radius: 50%;
    z-index: 9999;
}
.footer-bar {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: black;
    color: white;
    text-align: center;
    padding: 12px;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("DURGA PSYCHIATRIC CENTRE")

st.image("profile.jpg", width=150)

st.write("D Durga")
st.write("DPN Nursing, DAHM, BBA, MBA HR, MSW")
st.write("Founder and CEO")

# SESSION
if "chat" not in st.session_state:
    st.session_state.chat = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# INPUT
st.subheader("Tell me what you are feeling")

st.text_area("", key="input_text")

# SIMPLE DSS
def analyze(text):
    text = text.lower()
    if "stress" in text:
        return "Stress", "Mild", "Relax and reduce workload"
    elif "depress" in text:
        return "Depression", "Moderate", "Talk to someone and seek help"
    elif "sleep" in text:
        return "Sleep issue", "Mild", "Maintain sleep routine"
    else:
        return "Emotional issue", "Mild", "Stay calm and observe"

# SEND
if st.button("SEND"):
    if st.session_state.input_text.strip():

        q = st.session_state.input_text
        st.session_state.chat.append(("You", q))

        c, s, a = analyze(q)

        res = "Condition: " + c + "\n\nSeverity: " + s + "\n\nAdvice: " + a

        st.session_state.chat.append(("AI", res))

        st.session_state.input_text = ""

# CHAT
st.subheader("Conversation")

for r, m in st.session_state.chat:
    st.write(r + ":")
    st.write(m)

st.write("")

# FORM
st.subheader("Book Consultation")

name = st.text_input("Name")
mobile = st.text_input("Mobile")

cause = st.selectbox("Concern", [
    "Stress","Depression","Anxiety","Sleep","Relationship","Other"
])

mode = st.radio("Mode", ["Online","In Person"])
time = st.selectbox("Time", ["Morning","Afternoon","Evening"])
loc = st.text_input("Location")

# SUBMIT
if st.button("Submit Consultation"):

    msg = "I would like to book appointment with D Durga.\n"
    msg += "Name: " + name + "\n"
    msg += "Mobile: " + mobile + "\n"
    msg += "Concern: " + cause + "\n"
    msg += "Mode: " + mode + "\n"
    msg += "Time: " + time + "\n"
    msg += "Location: " + loc

    url = "https://wa.me/917395944527?text=" + urllib.parse.quote(msg)

    st.markdown(f'<script>window.open("{url}")</script>', unsafe_allow_html=True)

# FLOAT BUTTONS
st.markdown('<a href="https://wa.me/917395944527"><div class="float-whatsapp">W</div></a>', unsafe_allow_html=True)
st.markdown('<a href="tel:+917395944527"><div class="float-call">C</div></a>', unsafe_allow_html=True)

# FOOTER
st.markdown('<a href="https://wa.me/917395944527"><div class="footer-bar">Book on WhatsApp 7395944527</div></a>', unsafe_allow_html=True)