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

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
    color: white;
}

/* INPUT TEXT */
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

/* LABELS WHITE */
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

/* FLOATING WHATSAPP */
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
    text-align: center;
}

/* FLOATING CALL BUTTON */
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
    text-align: center;
}

/* FOOTER BAR */
.footer-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: black;
    color: white;
    text-align: center;
    padding: 12px;
    font-size: 16px;
    z-index: 9999;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🧠 DURGA PSYCHIATRIC CENTRE")

st.image("profile.jpg", width=150)

st.markdown("""
**D.Durga**  
DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)  
Founder & CEO  
""")

# =========================
# AI INPUT
# =========================
st.subheader("Tell me what you're feeling")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_area("", key="input_box")

if st.button("SEND"):
    if user_input.strip():
        st.session_state.chat.append(("You", user_input))

        # SIMPLE LOCAL AI RESPONSE (SAFE FALLBACK)
        if "stress" in user_input.lower():
            response = "Stress is your mind under pressure. Try deep breathing and small steps."
        elif "depress" in user_input.lower():
            response = "Depression is prolonged sadness and low energy. Talking helps recovery."
        else:
            response = "Take a slow breath. You are safe. Focus on one small step."

        st.session_state.chat.append(("AI", response))

        # CLEAR INPUT
        st.session_state.input_box = ""

# =========================
# CHAT DISPLAY
# =========================
st.subheader("💬 Conversation")

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")

# =========================
# SPACING FIX (IMPORTANT)
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)

# =========================
# CONSULTATION FORM
# =========================
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
mobile = st.text_input("Mobile Number")

cause = st.selectbox("Concern", [
    "Anxiety",
    "Depression",
    "Stress",
    "Relationship Issues",
    "Sleep Disorder",
    "Sexual Issues",
    "Addiction",
    "Panic Attacks",
    "Bipolar Disorder",
    "OCD",
    "Other"
])

mode = st.radio("Session Mode", ["Online", "In-Person"])

time = st.selectbox("Preferred Time", ["Morning", "Afternoon", "Evening"])

location = st.text_input("Location / Area")

# =========================
# SUBMIT BUTTON
# =========================
if st.button("Submit Consultation"):

    message = f"""
I would like to request an appointment with Psychologist D.Durga.

Name: {name}
Mobile: {mobile}
Concern: {cause}
Session Mode: {mode}
Preferred Time: {time}
Location: {location}

Please call back to discuss further.
"""

    encoded = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/917395944527?text={encoded}"

    # AUTO OPEN WHATSAPP
    st.markdown(f"""
    <script>
    window.open("{whatsapp_url}", "_blank");
    </script>
    """, unsafe_allow_html=True)

    st.success("Redirecting to WhatsApp...")

# =========================
# NORMAL WHATSAPP BUTTON (KEEP EXISTING)
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank" class="whatsapp-btn">
📲 Click to Open WhatsApp
</a>
""", unsafe_allow_html=True)

# =========================
# FLOATING BUTTONS
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank">
<div class="float-whatsapp">💬</div>
</a>
""", unsafe_allow_html=True)

st.markdown("""
<a href="tel:+917395944527">
<div class="float-call">📞</div>
</a>
""", unsafe_allow_html=True)

# =========================
# FOOTER FIXED BAR
# =========================
st.markdown("""
<a href="https://wa.me/917395944527" target="_blank">
<div class="footer-bar">
📞 Book Consultation on WhatsApp: +91 7395944527
</div>
</a>
""", unsafe_allow_html=True)