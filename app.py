import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
MODEL = "models/gemini-2.0-flash"
WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

# ================= CUSTOM STYLE =================
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.main {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #2c3e50;
}
.stButton button {
    background-color: #25D366;
    color: white;
    border-radius: 8px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🏥 DURGA PSYCHIATRIC CENTRE")

# ================= PROFILE =================
col1, col2 = st.columns([1,2])

with col1:
    st.image("uploaded_image.jpg", width=150)

with col2:
    st.markdown("""
    ### 👩‍⚕️ D. DURGA  
    **DPN (Nursing), DAHM, BBA, MBA (HR), MSW (Medical & Psychiatry)**  

    **Founder & CEO**  
    Durga Psychiatric Centre
    """)

st.markdown("---")

# ================= AI SECTION =================
st.subheader("🧠 AI Mental Health Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quota_exceeded" not in st.session_state:
    st.session_state.quota_exceeded = False


def offline_ai(text):
    text = text.lower()

    if "stress" in text:
        return "Break your workload into smaller steps. Take short mindful breaks."

    if "sleep" in text:
        return "Reduce screen time before bed. Practice slow breathing."

    if "anxiety" in text:
        return "Focus on breathing and grounding techniques."

    if "anger" in text:
        return "Pause before reacting. Deep breathing helps control anger."

    return "I'm here to support you. Tell me more."


def call_gemini(prompt):
    if not API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        res = requests.post(url, json=payload, timeout=8)

        if res.status_code == 429:
            st.session_state.quota_exceeded = True
            return None

        if res.status_code != 200:
            return None

        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None


def smart_ai(user_input):

    if not st.session_state.quota_exceeded:
        with st.spinner("Thinking..."):
            response = call_gemini(user_input)

        if response:
            return response

    return offline_ai(user_input)


# ================= CHAT INPUT =================
with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append(("You", user_input))
        reply = smart_ai(user_input)
        st.session_state.messages.append(("Assistant", reply))


# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ================= CONSULTATION =================
st.markdown("---")
st.subheader("📞 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

cause = st.selectbox(
    "Select Your Concern",
    ["Stress", "Anxiety", "Depression", "Sleep Issue", "Relationship Issue", "Other"]
)

# ================= SUBMIT =================
if st.button("Submit & Continue"):

    if name and phone:

        message = f"""Hello,
I want to book a consultation.

Name: {name}
Phone: {phone}
Concern: {cause}
"""

        link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"

        # AUTO OPEN WHATSAPP
        st.markdown(
            f"""
            <script>
            window.open("{link}", "_blank");
            </script>
            """,
            unsafe_allow_html=True
        )

        st.success("Opening WhatsApp...")

        # BACKUP BUTTON
        st.markdown(
            f"""
            <a href="{link}" target="_blank">
                <button style="
                    background:#25D366;
                    color:white;
                    padding:16px;
                    border:none;
                    border-radius:10px;
                    font-size:18px;
                    width:100%;
                ">
                💬 Open WhatsApp
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("Please fill all fields")