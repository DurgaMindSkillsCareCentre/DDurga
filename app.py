import streamlit as st
import urllib.parse

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# =========================
# CSS (SAFE + FIXED)
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
    color: white;
}

textarea, input {
    color: black !important;
}

/* SEND BUTTON */
div.stButton > button {
    background-color: #111111;
    color: white;
    border-radius: 12px;
    font-weight: bold;
}

/* LABELS */
label {
    color: white !important;
}

/* WHATSAPP BUTTON */
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

/* FLOAT BUTTONS */
.float-whatsapp {
    position: fixed;
    bottom: 90px;
    right: 20px;
    background: #25D366;
    color: white;
    font-size: 22px;
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
    font-size: 22px;
    padding: 15px;
    border-radius: 50%;
    z-index: 9999;
}

/* FOOTER */
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

# =========================
# HEADER
# =========================
st.title(" DURGA PSYCHIATRIC CENTRE")

st.image("profile.jpg", width=150)

st.markdown("""
**D.Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW  
Founder & CEO  
""")

# =========================
# SESSION STATE
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# =========================
# INPUT
# =========================
st.subheader("Tell me what you're feeling")

user_input = st.text_area("", key="input_text")

# =========================
# DSS FUNCTION
# =========================
def analyze(text):
    text = text.lower()

    if "stress" in text:
        return ("Stress", "Mild", "Practice breathing and reduce workload.")

    elif "depress" in text:
        return ("Depression", "Moderate", "Talk to someone and seek support.")

    elif "anxiety" in text:
        return ("Anxiety", "Mild–Moderate", "Relaxation and counseling help.")

    elif "sleep" in text:
        return ("Sleep Disorder", "Mild", "Maintain routine and avoid screens.")

    else:
        return ("Emotional Distress", "Mild", "Stay calm and observe patterns.")

# =========================
# SEND BUTTON (NO ERROR)
# =========================
if st.button("SEND"):

    if st.session_state.input_text.strip():

        query = st.session_state.input_text
        st.session_state.chat.append(("You", query))

        cond, sev, adv = analyze(query)

        response = f"""
**Condition:** {cond}  
**Severity:** {sev}  
**Advice:** {adv}
"""

        st.session_state.chat.append(("AI", response))

        # SAFE CLEAR
        st.session_state.input_text = ""

# =========================
# CHAT DISPLAY
# =========================
st.subheader(" Conversation")

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:**")
    st.markdown(msg)

# =========================
# SPACING
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)

# =========================
# FORM
# =========================
st.subheader(" Book Consultation")

name = st.text_input("Name")
mobile = st.text_input("Mobile Number")

cause = st.selectbox("Concern", [
    "Anxiety","Depression","Stress","Relationship Issues",
    "Sleep Disorder","Sexual Issues","Addiction","Panic Attacks",
    "Bipolar Disorder","OCD","Other"
])

mode = st.radio("Session Mode", ["Online","In-Person"])
time = st.selectbox("Preferred Time", ["Morning","Afternoon","Evening"])
location = st.text_input("Location")

# =========================
# SUBMIT  AUTO WHATSAPP
# =========================
if st.button("Submit Consultation"):

    msg = f"""I would like to request an appointment with Psychologist D.Durga.

Name: {name}
Mobile: {mobile}
Concern: {cause}
Session Mode: {mode}
Preferred Time: {time}
Location: {location}

Please call back to discuss further.
"""

    url = "https://wa.me/917395944527?text=" + urllib.parse.quote(msg)

    st.markdown(f"""
    <script>
    window.open("{url}", "_blank");
    </script>
    """, unsafe_allow_html=True)

    st.success("Opening WhatsApp...")

# =========================
# NORMAL WHATSAPP BUTTON
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank" class="whatsapp-btn">
 Click to Open WhatsApp
</a>
""", unsafe_allow_html=True)

# =========================
# FLOAT BUTTONS
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank">
<div class="float-whatsapp"></div>
</a>
""", unsafe_allow_html=True)

st.markdown("""
<a href="tel:+917395944527">
<div class="float-call"></div>
</a>
""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank">
<div class="footer-bar">
 Book Consultation on WhatsApp: +91 7395944527
</div>
</a>
""", unsafe_allow_html=True)