import streamlit as st
import requests
import urllib.parse

# ================= CONFIG =================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
WHATSAPP_NUMBER = "917395944527"

# 🔥 ONLY USE THIS MODEL (CONFIRMED WORKING)
MODEL = "models/gemini-2.0-flash"

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

st.title("🏥 DURGA PSYCHIATRIC CENTRE")
st.subheader("🧠 AI Mental Health Assistant")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= OFFLINE =================
def offline_response(text):
    text = text.lower()

    if "sleep" in text:
        return "Sleep issues are often linked to stress. Try avoiding screens before bed and practice slow breathing."

    if "stress" in text:
        return "Stress can feel overwhelming. Break tasks into small steps and take mindful pauses."

    if "anxiety" in text:
        return "Try grounding yourself—focus on your breath and surroundings."

    return "I'm here for you. Tell me more."

# ================= GEMINI =================
def gemini_response(prompt):

    if not API_KEY:
        st.warning("⚠️ API KEY MISSING")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are a psychologist. Give helpful advice.\nUser: {prompt}"}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=20)

        # 🔍 DEBUG INFO (REMOVE LATER)
        st.write("Status Code:", res.status_code)

        if res.status_code != 200:
            st.write("Error:", res.text)
            return None

        data = res.json()

        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]

        st.write("Invalid response:", data)

    except Exception as e:
        st.write("Exception:", str(e))
        return None

    return None

# ================= SMART AI =================
def smart_ai(prompt):

    with st.spinner("Thinking..."):

        ai = gemini_response(prompt)

    if ai:
        return ai  # ✅ REAL AI

    return offline_response(prompt)  # ⚠ fallback

# ================= CHAT =================
with st.form("chat", clear_on_submit=True):

    user_input = st.text_area("Tell me what you're feeling:")

    send = st.form_submit_button("Send")

    if send and user_input.strip():

        st.session_state.messages.append(("You", user_input))

        reply = smart_ai(user_input)

        st.session_state.messages.append(("Assistant", reply))

# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ================= WHATSAPP =================
st.markdown("---")

name = st.text_input("Name")
phone = st.text_input("Phone Number")

if name and phone:
    msg = f"Name: {name}\nPhone: {phone}"
    link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

    st.markdown(
        f'<a href="{link}" target="_blank">'
        f'<button style="background:#25D366;color:white;padding:12px;border:none;border-radius:8px;">Chat on WhatsApp</button></a>',
        unsafe_allow_html=True
    )