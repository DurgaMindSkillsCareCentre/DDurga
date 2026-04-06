# -*- coding: utf-8 -*-
import base64
import os
import time
import urllib.parse

import requests
import streamlit as st
import streamlit.components.v1 as components

# ================= CONFIG =================
API_KEY = st.secrets["GEMINI_API_KEY"]
WHATSAPP_NUMBER = "917395944527"
PROFILE_IMAGE = "profile.jpg"

MODEL_PRIORITY = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-flash-latest",
]

# ================= PAGE =================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

def get_base64_image(image_path: str) -> str | None:
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

PROFILE_B64 = get_base64_image(PROFILE_IMAGE)

# ================= GLOBAL CSS =================
st.markdown(
    """
    <style>
    header[data-testid="stHeader"],
    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"] {
        display: none !important;
    }

    .block-container {
        padding-top: 0.9rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 920px;
    }

    .app-shell {
        background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
        color: white;
        border-radius: 0;
    }

    .hero {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin-bottom: 12px;
    }

    .hero-badge {
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        margin-top: 2px;
    }

    .hero-title {
        font-size: clamp(1.8rem, 4.8vw, 2.8rem);
        font-weight: 900;
        line-height: 1.06;
        color: white;
    }

    .profile-row {
        display: flex;
        gap: 14px;
        align-items: flex-start;
        margin: 10px 0 8px 0;
    }

    .profile-img {
        width: 132px;
        height: 132px;
        border-radius: 18px;
        object-fit: cover;
        box-shadow: 0 12px 30px rgba(0,0,0,0.28);
        border: 3px solid rgba(255,255,255,0.65);
        background: rgba(255,255,255,0.15);
    }

    .profile-placeholder {
        width: 132px;
        height: 132px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.16);
        box-shadow: 0 12px 30px rgba(0,0,0,0.28);
        border: 3px solid rgba(255,255,255,0.28);
        font-size: 54px;
    }

    .profile-name {
        font-size: 1.18rem;
        font-weight: 900;
        color: white;
        margin-bottom: 6px;
    }

    .profile-meta {
        font-size: 1rem;
        line-height: 1.55;
        color: white;
        opacity: 0.98;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 18px 0 12px 0;
        font-size: clamp(1.35rem, 3.8vw, 2rem);
        font-weight: 900;
        color: white;
    }

    .cardish {
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.10);
        padding: 16px;
    }

    .stButton > button {
        background: #111111 !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        padding: 0.9rem 1.1rem !important;
        font-size: 1.02rem !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        width: 100% !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        color: #111 !important;
        border-radius: 12px !important;
    }

    .msg {
        border-radius: 16px;
        padding: 14px 16px;
        margin: 10px 0 12px 0;
        box-shadow: 0 8px 18px rgba(0,0,0,0.10);
        word-break: break-word;
    }

    .msg-user {
        background: #111111;
        color: white;
    }

    .msg-ai {
        background: rgba(255,255,255,0.15);
        color: white;
    }

    .cta-wa {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        padding: 14px 16px;
        border-radius: 14px;
        background: linear-gradient(90deg, #25D366, #1ebe5d);
        color: #ffffff !important;
        text-decoration: none !important;
        font-size: 1.02rem;
        font-weight: 900;
        box-shadow: 0 8px 22px rgba(0,0,0,0.18);
        margin-top: 10px;
    }

    .bottom-bar {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, #000000, #1a1a1a);
        padding: 12px;
        box-shadow: 0 -8px 25px rgba(0,0,0,0.35);
        z-index: 9998;
    }

    .bottom-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(90deg, #25D366, #1ebe5d);
        color: white !important;
        font-size: 1.08rem;
        font-weight: 900;
        padding: 16px 18px;
        border-radius: 16px;
        text-decoration: none !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    .float-btn {
        position: fixed;
        right: 18px;
        width: 58px;
        height: 58px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        box-shadow: 0 10px 20px rgba(0,0,0,0.22);
    }

    .float-wa { bottom: 84px; background: #25D366; }
    .float-call { bottom: 156px; background: #0a84ff; }

    .small-note {
        color: white;
        font-weight: 600;
        opacity: 0.96;
    }

    .screening-tabs {
        margin-top: 8px;
        margin-bottom: 12px;
    }

    div[data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }

    div[data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.10));
        color: white;
        border-radius: 14px;
        padding: 10px 14px;
        font-weight: 900;
        border: 1px solid rgba(255,255,255,0.18);
    }

    div[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #25D366, #1ebe5d);
        color: white;
        border: none;
        box-shadow: 0 8px 18px rgba(0,0,0,0.20);
    }

    .screening-result {
        border-radius: 16px;
        padding: 14px 16px;
        margin-top: 12px;
        line-height: 1.6;
        font-size: 1.02rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }
    .dss-green { background: #12c24f; color: white; }
    .dss-orange { background: #ff9800; color: white; }
    .dss-red { background: #e53935; color: white; }

    .splash-wrap{
        position: fixed;
        inset: 0;
        z-index: 99999;
        background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        color: white;
        animation: splashFadeIn 0.45s ease;
    }
    .splash-logo{
        width: 92px;
        height: 92px;
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.16);
        box-shadow: 0 14px 30px rgba(0,0,0,0.22);
        font-size: 44px;
        margin-bottom: 18px;
        animation: popIn 0.7s ease-out;
    }
    .splash-profile{
        width: 96px;
        height: 96px;
        border-radius: 18px;
        margin: 12px 0 10px 0;
        box-shadow: 0 12px 28px rgba(0,0,0,0.35);
        border: 3px solid rgba(255,255,255,0.6);
        background: rgba(255,255,255,0.15) center center / cover no-repeat;
        animation: profileIn 0.8s ease;
    }
    .splash-title{
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        line-height: 1.1;
        letter-spacing: 0.02em;
    }
    .splash-sub{
        margin-top: 10px;
        font-size: 1rem;
        opacity: 0.95;
        text-align: center;
    }
    .loader{
        margin-top: 22px;
        width: 54px;
        height: 54px;
        border-radius: 50%;
        border: 5px solid rgba(255,255,255,0.25);
        border-top-color: white;
        animation: spin 0.9s linear infinite;
    }
    .splash-voice{
        margin-top: 18px;
        padding: 12px 18px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.25);
        background: rgba(255,255,255,0.12);
        color: white;
        font-weight: 800;
        cursor: pointer;
        animation: pulse 1.5s infinite;
    }
    @keyframes spin{ to{transform: rotate(360deg);} }
    @keyframes popIn{ from{transform: scale(0.75); opacity: 0;} to{transform: scale(1); opacity: 1;} }
    @keyframes profileIn{ from{transform: translateY(12px); opacity: 0;} to{transform: translateY(0); opacity: 1;} }
    @keyframes splashFadeIn{ from{opacity: 0;} to{opacity: 1;} }
    @keyframes pulse{ 0%{opacity: .7} 50%{opacity: 1} 100%{opacity: .7} }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= SPLASH =================
splash = st.empty()

splash_profile_style = ""
if PROFILE_B64:
    splash_profile_style = f'background-image: url("data:image/jpeg;base64,{PROFILE_B64}");'

with splash.container():
    splash_html = f"""
    <div class="splash-wrap" id="splashWrap">
        <div class="splash-logo">🧠</div>
        <div class="splash-profile" style="{splash_profile_style}"></div>
        <div class="splash-title">Durga Psychiatric Centre</div>
        <div class="splash-sub">Loading your clinic assistant...</div>
        <div class="loader"></div>
        <button class="splash-voice" onclick="speakWelcome()">🔊 Tap to hear welcome</button>
    </div>
    """
    st.markdown(splash_html, unsafe_allow_html=True)

components.html(
    """
    <script>
    (function () {
        let spoken = false;

        function sayWelcome() {
            if (spoken) return;
            try {
                spoken = true;
                const msg = new SpeechSynthesisUtterance(
                    "Welcome to Durga Psychiatric Centre. Your mental wellness matters. How can I help you today?"
                );
                msg.rate = 0.95;
                msg.pitch = 1.0;
                msg.volume = 1.0;

                const voices = window.speechSynthesis.getVoices();
                if (voices && voices.length) {
                    msg.voice = voices.find(v => /female/i.test(v.name)) || voices[0];
                }

                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(msg);
            } catch (e) {
                console.log("Voice welcome not available:", e);
            }
        }

        window.speakWelcome = sayWelcome;

        // Mobile browsers usually require a user tap, so we attempt once and then
        // also listen for the first interaction.
        setTimeout(() => {
            try { sayWelcome(); } catch (e) {}
        }, 700);

        const once = () => { sayWelcome(); document.removeEventListener("click", once); document.removeEventListener("touchend", once); };
        document.addEventListener("click", once);
        document.addEventListener("touchend", once);
    })();
    </script>
    """,
    height=0,
)

time.sleep(2.5)
splash.empty()

# ================= CHAT STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "screening_choice" not in st.session_state:
    st.session_state.screening_choice = "Stress"

if "last_whatsapp_url" not in st.session_state:
    st.session_state.last_whatsapp_url = ""

# ================= AI FUNCTION =================
def ask_gemini(prompt):
    for model in MODEL_PRIORITY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "You are a professional therapist. Respond empathetically in 3 to 5 short lines.\n"
                                    f"User: {prompt}"
                                )
                            }
                        ]
                    }
                ]
            }

            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue

    return "⚠️ AI temporarily unavailable. Please try again."

# ================= SIMPLE SCREENING =================
def screening_score(kind: str, answers: list[int]) -> tuple[int, int, str, str]:
    score = sum(answers)
    max_score = len(answers) * 3
    if score <= 4:
        level, css = "Mild", "dss-green"
    elif score <= 9:
        level, css = "Moderate", "dss-orange"
    else:
        level, css = "Severe", "dss-red"
    return score, max_score, level, css

# ================= HEADER =================
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">🧠</div>
        <div class="hero-title">Durga Psychiatric Centre</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_img, col_info = st.columns([1, 2])

with col_img:
    if PROFILE_B64:
        st.markdown(
            f'<img class="profile-img" src="data:image/jpeg;base64,{PROFILE_B64}" alt="Profile">',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="profile-placeholder">🧑‍⚕️</div>', unsafe_allow_html=True)

with col_info:
    st.markdown(
        """
        <div class="profile-name">D. Durga</div>
        <div class="profile-meta">
            DPN (Nursing), DAHM, BBA, MBA(HR), MSW<br>
            Founder & CEO<br>
            Durga Psychiatric Centre
        </div>
        """,
        unsafe_allow_html=True,
    )

# ================= SCREENING FIRST (OPTION 2) =================
st.markdown('<div class="section-title">🧪 Screening Tests</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">Choose one tab below. The result can guide consultation.</div>',
    unsafe_allow_html=True,
)

tab_stress, tab_anxiety, tab_depression = st.tabs(["🧠 Stress", "😰 Anxiety", "😔 Depression"])

stress_questions = [
    "I feel overwhelmed by my workload.",
    "I find it hard to relax.",
    "I feel irritable or easily annoyed.",
    "I have trouble sleeping because of stress.",
    "I find it hard to concentrate.",
]

anxiety_questions = [
    "I feel nervous or anxious.",
    "I cannot stop worrying.",
    "I worry too much about different things.",
    "I find it hard to relax.",
    "I feel afraid that something bad may happen.",
]

depression_questions = [
    "I feel down, depressed, or hopeless.",
    "I have little interest or pleasure in doing things.",
    "I feel tired or have little energy.",
    "I feel bad about myself or feel like a failure.",
    "I have trouble concentrating on tasks.",
]

def render_screen_form(prefix: str, title: str, questions: list[str]):
    options = [
        "0 - Not at all",
        "1 - Several days",
        "2 - More than half the days",
        "3 - Nearly every day",
    ]
    with st.form(f"{prefix}_form", clear_on_submit=False):
        st.markdown('<div class="cardish">', unsafe_allow_html=True)
        st.markdown(
            '<div class="small-note">Rate how often you experienced each item in the last 2 weeks.</div>',
            unsafe_allow_html=True,
        )
        answers = []
        for i, q in enumerate(questions):
            ans = st.radio(q, options=options, index=0, key=f"{prefix}_q_{i}", horizontal=False)
            answers.append(options.index(ans))

        submitted = st.form_submit_button(f"Calculate {title} Score")
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        score, max_score, level, css = screening_score(prefix, answers)
        st.markdown(
            f"""
            <div class="screening-result {css}">
                <strong>{title} Score:</strong> {score}/{max_score}<br>
                <strong>Level:</strong> {level}<br>
                <strong>Action:</strong> {"Self-care and monitor" if level=="Mild" else "Consultation advised" if level=="Moderate" else "Please book consultation soon"}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="small-note">This is a screening tool, not a diagnosis.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <a class="cta-wa" href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" rel="noopener noreferrer">
                📲 BOOK CONSULTATION ON WHATSAPP
            </a>
            """,
            unsafe_allow_html=True,
        )

with tab_stress:
    render_screen_form("Stress", "Stress", stress_questions)

with tab_anxiety:
    render_screen_form("Anxiety", "Anxiety", anxiety_questions)

with tab_depression:
    render_screen_form("Depression", "Depression", depression_questions)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ================= INPUT =================
st.markdown('<div class="section-title">💬 Enter your problem</div>', unsafe_allow_html=True)

user_input = st.text_area("Tell me what you're feeling:")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append(("You", user_input))
        reply = ask_gemini(user_input)
        st.session_state.messages.append(("Assistant", reply))

# ================= DISPLAY =================
for role, msg in st.session_state.messages:
    css = "msg-user" if role == "You" else "msg-ai"
    st.markdown(f'<div class="msg {css}"><strong>{role}:</strong> {msg}</div>', unsafe_allow_html=True)

# ================= WHATSAPP =================
st.markdown("---")
st.markdown(
    f"""
    <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" class="cta-wa">
        💬 Chat on WhatsApp
    </a>
    """,
    unsafe_allow_html=True,
)

# ================= BOOKING =================
st.markdown("---")
st.markdown('<div class="section-title">📅 Book a Consultation</div>', unsafe_allow_html=True)

name = st.text_input("Name")
phone = st.text_input("Phone Number")

if st.button("Submit"):
    msg = f"I would like to request an appointment.\n\nName: {name}\nMobile: {phone}"
    st.session_state.last_whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
    st.success("Click below to open WhatsApp and send the message.")

if st.session_state.last_whatsapp_url:
    st.markdown(
        f"""
        <a href="{st.session_state.last_whatsapp_url}" target="_blank" class="cta-wa">
            📲 CLICK TO OPEN WHATSAPP
        </a>
        """,
        unsafe_allow_html=True,
    )

# ================= FLOATING BUTTONS =================
st.markdown(
    f"""
    <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
        <div class="float-btn float-wa">{'<svg width="28" height="28" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 6C18.8 6 8 16.3 8 29.1c0 4.6 1.4 9 3.9 12.7L8 58l16.8-3.7c3.5 2 7.5 3.1 12.1 3.1 13.2 0 24-10.3 24-23.1S45.2 6 32 6z" fill="white"/><path d="M26 20c1.2-1.2 2.4-1.1 3.4.1l2.8 3.6c.7.9.7 2-.1 2.8l-1.7 1.8c-.4.4-.5 1-.2 1.5 1.4 2.6 3.4 4.8 6 6.3.5.3 1.1.2 1.5-.2l1.8-1.7c.8-.8 1.9-.8 2.8-.1l3.6 2.8c1.2 1 1.3 2.2.1 3.4l-1.1 1.1c-1.1 1.1-2.6 1.7-4.1 1.5-4-.5-8.1-2.9-11.6-6.4-3.5-3.5-5.9-7.6-6.4-11.6-.2-1.5.4-3 1.5-4.1l1.1-1.1z" fill="#25D366"/></svg>'}</div>
    </a>

    <a href="tel:{DISPLAY_NUMBER}" target="_blank">
        <div class="float-btn float-call">{'<svg width="28" height="28" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="8" width="24" height="48" rx="6" fill="white"/><circle cx="32" cy="51" r="3" fill="white"/></svg>'}</div>
    </a>
    """,
    unsafe_allow_html=True,
)

# ================= BOTTOM BAR =================
st.markdown(
    f"""
    <div class="bottom-bar">
        <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" class="bottom-btn">
            📞 💬 BOOK CONSULTATION NOW
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
