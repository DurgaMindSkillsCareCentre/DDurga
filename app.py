import streamlit as st
import requests
import time
import urllib.parse

# =========================
# 🔐 API KEYS (Streamlit Secrets)
# =========================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "")

# =========================
# 🎨 PREMIUM UI (iPhone Style)
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
}
.stApp {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    color: white;
}
textarea, input, select {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 10px !important;
}
button {
    background: linear-gradient(135deg, #000000, #333333) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}
.whatsapp-btn {
    background: linear-gradient(135deg, #0f9d58, #25D366);
    color: white;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 👩 PROFILE SECTION
# =========================
try:
    st.image("profile.jpg", width=150)
except:
    st.warning("Upload profile.jpg in your repo")

st.markdown("""
### **D. Durga**
DPN (Nursing), DAHM, BBA, MBA(HR), MSW (Medical & Psychiatry)  
**Founder & CEO – Durga Psychiatric Centre**
""")

st.markdown("---")

# =========================
# 🧠 HEADER
# =========================
st.title("🧠 AI Mental Health Assistant")

# =========================
# 🤖 LOCAL AI (Instant)
# =========================
def local_ai(prompt):
    prompt = prompt.lower()
    if "anxiety" in prompt:
        return "Anxiety is your brain's alarm system becoming overactive. It tries to protect you but reacts too strongly."
    if "sleep" in prompt:
        return "Sleep issues often come from stress hormones staying high. Relax your body before bed."
    return "Take slow breaths, relax your body, and focus on one small step."

# =========================
# 🌐 GEMINI API
# =========================
def gemini(prompt):
    if not GEMINI_API_KEY:
        return None, None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

        res = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        }, timeout=6)

        if res.status_code != 200:
            st.warning(f"Gemini Error {res.status_code}")
            return None, None

        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"], "Gemini"

    except Exception as e:
        st.warning(f"Gemini failed: {e}")
        return None, None

# =========================
# 🔥 DEEPSEEK API (FIXED)
# =========================
def deepseek(prompt):
    if not DEEPSEEK_API_KEY:
        return None, None

    try:
        res = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a helpful mental health assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=8
        )

        if res.status_code != 200:
            st.error(f"DeepSeek Error {res.status_code}")
            st.code(res.text)
            return None, None

        data = res.json()
        return data["choices"][0]["message"]["content"], "DeepSeek"

    except Exception as e:
        st.error(f"DeepSeek Exception: {e}")
        return None, None

# =========================
# 🧠 SMART ROUTER
# =========================
def smart_ai(prompt):
    # Try Gemini first
    response, source = gemini(prompt)
    if response:
        return response, source

    # Then DeepSeek
    response, source = deepseek(prompt)
    if response:
        return response, source

    # Finally local
    return local_ai(prompt), "Local AI"

# =========================
# 💬 CHAT UI
# =========================
user_input = st.text_area("Tell me what you're feeling:")

if st.button("SEND"):
    if user_input:
        response, source = smart_ai(user_input)

        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI ({source}):** {response}")

# =========================
# 📞 CONSULTATION FORM
# =========================
st.markdown("---")
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
concern = st.selectbox("Select Concern", ["Stress", "Anxiety", "Depression", "Sleep Issue"])

if st.button("Submit & Continue"):
    if name and phone:
        message = f"""
Hello, I am {name}.
Concern: {concern}
Phone: {phone}
"""

        encoded = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/917395944527?text={encoded}"

        # AUTO OPEN WHATSAPP
        st.markdown(f"""
        <meta http-equiv="refresh" content="1;url={whatsapp_url}">
        """, unsafe_allow_html=True)

        st.success("Opening WhatsApp...")

        # BUTTON
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">
            <div class="whatsapp-btn">💬 Open WhatsApp</div>
        </a>
        """, unsafe_allow_html=True)

    else:
        st.warning("Please fill all fields")