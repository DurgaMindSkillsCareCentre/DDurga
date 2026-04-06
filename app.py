# -*- coding: utf-8 -*-
import os
import re
import html as html_lib
import urllib.parse

import requests
import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")
st.markdown("""
<style>

/* 🔴 Hide Streamlit top header (Fork / Menu / Deploy icons) */
header[data-testid="stHeader"] {
    display: none !important;
}

/* 🔴 Remove top spacing created by header */
.block-container {
    padding-top: 0rem !important;
}

/* 🔴 Hide hamburger menu (⋮) */
#MainMenu {
    visibility: hidden;
}

/* 🔴 Hide footer */
footer {
    visibility: hidden;
}

/* 🔴 Hide "Made with Streamlit" */
[data-testid="stToolbar"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)
WHATSAPP_NUMBER = "917395944527"   # wa.me format, no plus sign
DISPLAY_NUMBER = "+91 7395944527"  # display format

SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", os.getenv("SERPER_API_KEY", ""))
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

# =========================
# SVG ICONS
# =========================
def icon_brain():
    return """
    <svg width="36" height="36" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ff7a59"/>
          <stop offset="45%" stop-color="#7b2ff7"/>
          <stop offset="100%" stop-color="#00c2ff"/>
        </linearGradient>
        <linearGradient id="g2" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffd166"/>
          <stop offset="100%" stop-color="#ff4d8d"/>
        </linearGradient>
      </defs>
      <circle cx="23" cy="23" r="12" fill="url(#g2)"/>
      <circle cx="41" cy="23" r="12" fill="url(#g1)"/>
      <rect x="14" y="25" width="36" height="22" rx="11" fill="white"/>
      <path d="M24 16v32M40 16v32M32 14v36" stroke="#7b2ff7" stroke-width="3" stroke-linecap="round"/>
      <path d="M18 28c2 0 4-2 5-4M46 28c-2 0-4-2-5-4" stroke="#ff4d8d" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    """

def icon_chat():
    return """
    <svg width="30" height="30" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M10 14h44a8 8 0 0 1 8 8v18a8 8 0 0 1-8 8H28l-10 8v-8H10a8 8 0 0 1-8-8V22a8 8 0 0 1 8-8z" fill="white"/>
    </svg>
    """

def icon_mobile():
    return """
    <svg width="30" height="30" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="phoneg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#00c2ff"/>
          <stop offset="100%" stop-color="#7b2ff7"/>
        </linearGradient>
      </defs>
      <rect x="20" y="8" width="24" height="48" rx="6" fill="url(#phoneg)"/>
      <rect x="23" y="13" width="18" height="32" rx="3" fill="white"/>
      <circle cx="32" cy="51" r="3" fill="white"/>
    </svg>
    """

def icon_user():
    return """
    <svg width="28" height="28" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="ug" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#7b2ff7"/>
          <stop offset="100%" stop-color="#00c2ff"/>
        </linearGradient>
      </defs>
      <circle cx="32" cy="22" r="11" fill="url(#ug)"/>
      <path d="M14 54c2-11 10-16 18-16s16 5 18 16" fill="url(#ug)"/>
    </svg>
    """

def icon_bot():
    return """
    <svg width="28" height="28" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ff7a59"/>
          <stop offset="50%" stop-color="#7b2ff7"/>
          <stop offset="100%" stop-color="#00c2ff"/>
        </linearGradient>
      </defs>
      <rect x="14" y="16" width="36" height="28" rx="10" fill="url(#bg)"/>
      <circle cx="26" cy="29" r="3" fill="white"/>
      <circle cx="38" cy="29" r="3" fill="white"/>
      <rect x="30" y="8" width="4" height="8" rx="2" fill="url(#bg)"/>
      <circle cx="32" cy="6" r="3" fill="url(#bg)"/>
    </svg>
    """

def icon_whatsapp():
    return """
    <svg width="28" height="28" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M32 6C18.8 6 8 16.3 8 29.1c0 4.6 1.4 9 3.9 12.7L8 58l16.8-3.7c3.5 2 7.5 3.1 12.1 3.1 13.2 0 24-10.3 24-23.1S45.2 6 32 6z" fill="white"/>
      <path d="M26 20c1.2-1.2 2.4-1.1 3.4.1l2.8 3.6c.7.9.7 2-.1 2.8l-1.7 1.8c-.4.4-.5 1-.2 1.5 1.4 2.6 3.4 4.8 6 6.3.5.3 1.1.2 1.5-.2l1.8-1.7c.8-.8 1.9-.8 2.8-.1l3.6 2.8c1.2 1 1.3 2.2.1 3.4l-1.1 1.1c-1.1 1.1-2.6 1.7-4.1 1.5-4-.5-8.1-2.9-11.6-6.4-3.5-3.5-5.9-7.6-6.4-11.6-.2-1.5.4-3 1.5-4.1l1.1-1.1z" fill="#25D366"/>
    </svg>
    """

# =========================
# STYLE
# =========================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #5f6dfc, #7b2ff7);
        color: white;
    }

    .block-container {
        padding-top: 2.4rem !important;
        padding-bottom: 430px;
    }

    .hero-wrap {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 14px;
    }

    .hero-icon {
        width: 38px;
        height: 38px;
        flex: 0 0 38px;
        margin-top: 4px;
    }

    .hero-title {
        font-size: clamp(1.9rem, 5vw, 3rem);
        font-weight: 900;
        line-height: 1.05;
        color: white;
        letter-spacing: 0.02em;
    }

    .profile-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: white;
        margin-bottom: 6px;
    }

    .profile-meta {
        font-size: 1rem;
        line-height: 1.55;
        color: white;
        opacity: 0.98;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 18px 0 14px 0;
    }

    .section-icon {
        width: 34px;
        height: 34px;
        flex: 0 0 34px;
    }

    .section-title {
        font-size: clamp(1.5rem, 4.5vw, 2.2rem);
        font-weight: 900;
        line-height: 1.1;
        color: white;
    }

    .stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        background: #111111 !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        padding: 1rem 1.4rem !important;
        font-size: 1.05rem !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        width: 100% !important;
    }

    .stTextArea textarea,
    .stTextInput input,
    .stSelectbox div,
    .stRadio div {
        color: #111 !important;
    }

    .bubble {
        border-radius: 18px;
        padding: 14px 16px;
        margin: 10px 0 14px 0;
        word-break: break-word;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }

    .bubble-head {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
        font-weight: 800;
    }

    .bubble-body {
        font-size: 1.02rem;
        line-height: 1.6;
        white-space: normal;
    }

    .user-bubble {
        background: #111111;
        color: white;
    }

    .ai-bubble {
        background: rgba(255, 255, 255, 0.16);
        color: white;
    }

    .dss-card {
        border-radius: 18px;
        padding: 14px 16px;
        margin: 10px 0 14px 0;
        line-height: 1.65;
        font-size: 1.02rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }

    .dss-green { background: #12c24f; color: white; }
    .dss-orange { background: #ff9800; color: white; }
    .dss-red { background: #e53935; color: white; }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.16);
        font-size: 0.92rem;
        font-weight: 800;
    }

    .whatsapp-cta-wrap {
        margin-top: 12px;
    }

    .whatsapp-cta {
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
    }

    .float-btn {
        position: fixed;
        right: 18px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        box-shadow: 0 10px 20px rgba(0,0,0,0.22);
    }
    .float-wa { bottom: 92px; background: #25D366; }
    .float-call { bottom: 164px; background: #0a84ff; }

    .footer-bar {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        z-index: 9998;
        background: linear-gradient(90deg, #000000, #1a1a1a);
        padding: 16px 12px;
        box-shadow: 0 -8px 25px rgba(0,0,0,0.35);
    }

    .footer-btn {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        background: linear-gradient(90deg, #25D366, #1ebe5d);
        color: white !important;
        font-size: 1.2rem;
        font-weight: 900;
        padding: 18px 20px;
        border-radius: 16px;
        text-decoration: none !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        letter-spacing: 0.5px;
    }

    .footer-icon { display: flex; align-items: center; }
    .footer-bar a { color: white !important; text-decoration: none !important; display: block; }

    .screening-card {
        background: rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 16px;
        margin: 12px 0 18px 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
        border: 1px solid rgba(255,255,255,0.16);
    }

    .mini-note {
        color: white;
        font-weight: 600;
        margin-top: 6px;
        margin-bottom: 8px;
    }

    .screening-result {
        border-radius: 16px;
        padding: 14px 16px;
        margin-top: 12px;
        line-height: 1.6;
        font-size: 1.02rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
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
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
NOISE_PHRASES = [
    "skip to main content",
    "skip to content",
    "search the website",
    "search the",
    "menu",
    "home",
    "contact us",
    "about us",
    "log in",
    "login",
    "sign in",
    "privacy policy",
    "terms of use",
]

def normalize_text(text):
    if not text:
        return ""
    text = html_lib.unescape(str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def strip_noise(text):
    text = normalize_text(text)
    for phrase in NOISE_PHRASES:
        text = re.sub(re.escape(phrase), " ", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" -|:;,.")
    return text

def looks_noisy(fragment):
    low = fragment.lower()
    if any(p in low for p in NOISE_PHRASES):
        return True
    if low.startswith(("home ", "menu ", "search ")):
        return True
    return False

def make_three_to_five_lines(text):
    text = strip_noise(text)
    if not text:
        return ""

    parts = re.split(r"(?<=[.!?])\s+|\n+|[•|]+", text)
    lines = []

    for part in parts:
        part = part.strip(" -–—:;,.")
        if not part or looks_noisy(part):
            continue
        if len(part.split()) >= 4:
            lines.append(part)
        if len(lines) == 5:
            break

    if len(lines) < 3:
        clauses = re.split(r"\s-\s|;\s*|:\s*|\s\|\s*", text)
        for clause in clauses:
            clause = clause.strip(" -–—:;,.")
            if not clause or looks_noisy(clause):
                continue
            if len(clause.split()) >= 4 and clause not in lines:
                lines.append(clause)
            if len(lines) == 5:
                break

    if len(lines) < 3:
        words = text.split()
        if words:
            step = max(10, len(words) // 3 or 10)
            for i in range(0, min(len(words), step * 5), step):
                chunk = " ".join(words[i : i + step]).strip()
                if chunk and chunk not in lines:
                    lines.append(chunk)
                if len(lines) == 5:
                    break

    return "\n".join(lines[:5]).strip()

def valid_answer(text):
    return bool(text and len(text.strip()) >= 25)

# =========================
# WEB AI SOURCES
# =========================
def serper_search(query):
    if not SERPER_API_KEY:
        return ""
    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        res = requests.post(url, json={"q": query}, headers=headers, timeout=8)
        if res.status_code != 200:
            return ""

        data = res.json()
        pieces = []

        answer_box = data.get("answerBox") or {}
        if isinstance(answer_box, dict):
            for key in ("answer", "snippet"):
                if answer_box.get(key):
                    pieces.append(answer_box.get(key))

        knowledge = data.get("knowledgeGraph") or {}
        if isinstance(knowledge, dict) and knowledge.get("description"):
            pieces.append(knowledge.get("description"))

        organic = data.get("organic") or []
        for item in organic[:3]:
            if not isinstance(item, dict):
                continue
            if item.get("snippet"):
                pieces.append(item.get("snippet"))

        return make_three_to_five_lines(" ".join(str(x) for x in pieces if x))
    except:
        return ""

def duckduckgo_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_redirect=1&no_html=1&skip_disambig=1"
        res = requests.get(url, timeout=8)
        if res.status_code != 200:
            return ""

        data = res.json()
        pieces = []

        if data.get("AbstractText"):
            pieces.append(data.get("AbstractText"))

        if data.get("Answer"):
            pieces.append(data.get("Answer"))

        related = data.get("RelatedTopics") or []
        for item in related:
            if len(pieces) >= 3:
                break
            if isinstance(item, dict):
                if item.get("Text"):
                    pieces.append(item.get("Text"))
                else:
                    topics = item.get("Topics") or []
                    for sub in topics:
                        if sub.get("Text"):
                            pieces.append(sub.get("Text"))
                            break

        return make_three_to_five_lines(" ".join(str(x) for x in pieces if x))
    except:
        return ""

def wikipedia_search(query):
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": 1,
        }
        search_res = requests.get(search_url, params=params, timeout=8)
        if search_res.status_code != 200:
            return ""

        search_json = search_res.json()
        items = search_json.get("query", {}).get("search", [])
        if not items:
            return ""

        title = items[0].get("title", "").strip()
        if not title:
            return ""

        summary_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title)
        summary_res = requests.get(summary_url, timeout=8)
        if summary_res.status_code != 200:
            return ""

        summary_json = summary_res.json()
        text = summary_json.get("extract") or summary_json.get("description") or ""
        return make_three_to_five_lines(text)
    except:
        return ""

def gemini_search(query):
    if not GEMINI_API_KEY:
        return ""

    models = [
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-001",
        "models/gemini-2.0-flash-lite",
        "models/gemini-flash-latest",
    ]

    prompt = (
        "Answer in 3 to 5 short lines only. "
        "No bullets. No headings. No navigation text. No citations. "
        "Be clear, concise, and medically cautious.\n\n"
        f"User query: {query}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={GEMINI_API_KEY}"
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code != 200:
                continue

            data = res.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return make_three_to_five_lines(text)
        except:
            continue

    return ""

def local_smart_ai(query):
    q = query.lower()

    if any(k in q for k in ["suicide", "kill myself", "end my life", "self harm", "harm myself"]):
        return make_three_to_five_lines(
            "This sounds urgent and needs immediate human support. Please contact emergency help or a trusted person now. Do not stay alone."
        )

    if any(k in q for k in ["depress", "sad", "hopeless", "low mood", "no interest", "worthless"]):
        return make_three_to_five_lines(
            "Depression can feel heavy and draining. Small routine steps and talking to a professional can help. Please seek support early."
        )

    if any(k in q for k in ["anxiety", "panic", "worry", "fear", "nervous"]):
        return make_three_to_five_lines(
            "Anxiety often makes the body feel tense and restless. Slow breathing and grounding can help. Counseling may improve control."
        )

    if any(k in q for k in ["sleep", "insomnia", "wake up", "sleepless"]):
        return make_three_to_five_lines(
            "Sleep problems often come from stress or irregular habits. Keep a fixed sleep routine and avoid screens before bed. Seek help if it continues."
        )

    if any(k in q for k in ["premature ejaculation", "ejaculation", "sexual", "sexual issues", "erection", "erectile"]):
        return make_three_to_five_lines(
            "Sexual health concerns are common and treatable. Stress, anxiety, and habit patterns can play a role. A clinician can guide proper care."
        )

    if any(k in q for k in ["addiction", "porn", "masturbation", "craving", "habit"]):
        return make_three_to_five_lines(
            "Addictive habits can become repetitive and hard to control. Structure, support, and counseling can help. Start with one small change today."
        )

    if any(k in q for k in ["relationship", "marriage", "partner", "couple"]):
        return make_three_to_five_lines(
            "Relationship stress can affect mood and thinking. Calm communication and clarity help reduce conflict. Counseling can support both sides."
        )

    return make_three_to_five_lines(
        "Take a slow breath and focus on one small step. Your concern matters and support can help. If symptoms persist, meet a professional."
    )

def smart_ai(query):
    chain = [
        ("Web AI (Serper)", serper_search(query)),
        ("Web AI (DuckDuckGo)", duckduckgo_search(query)),
        ("Web AI (Wikipedia)", wikipedia_search(query)),
        ("Gemini AI", gemini_search(query)),
    ]

    for source, raw in chain:
        if valid_answer(raw):
            return source, raw

    return "Local Smart AI", local_smart_ai(query)

# =========================
# DSS
# =========================
def dss_score(query):
    q = query.lower()

    if any(k in q for k in ["suicide", "kill myself", "end my life", "self harm", "harm myself"]):
        return "Suicidal Risk", "Critical", "Immediate help required", "dss-red"

    if any(k in q for k in ["hopeless", "worthless", "no energy", "cant get out of bed", "can't get out of bed"]):
        return "Depression", "Severe", "Consult psychologist urgently", "dss-red"

    if any(k in q for k in ["depress", "sad", "low mood", "loss of interest"]):
        return "Depression", "Moderate", "Consult psychologist", "dss-orange"

    if any(k in q for k in ["panic", "anxiety", "worry", "fear", "nervous"]):
        if any(k in q for k in ["can t breathe", "can't breathe", "shaking", "faint", "severe"]):
            return "Anxiety", "Severe", "Seek prompt evaluation", "dss-red"
        return "Anxiety", "Mild", "Relaxation advised", "dss-green"

    if any(k in q for k in ["sleep", "insomnia", "wake up", "sleepless"]):
        return "Sleep Disorder", "Mild", "Improve sleep routine", "dss-green"

    if any(k in q for k in ["premature ejaculation", "ejaculation", "sexual", "erection", "erectile"]):
        return "Sexual Health Concern", "Moderate", "Consult psychologist", "dss-orange"

    if any(k in q for k in ["addiction", "porn", "masturbation", "habit"]):
        return "Behavioral Addiction", "Moderate", "Counseling advised", "dss-orange"

    if any(k in q for k in ["relationship", "marriage", "partner", "couple"]):
        return "Relationship Stress", "Mild", "Communication support helps", "dss-green"

    return "Stress", "Mild", "Lifestyle care", "dss-green"

# =========================
# SCREENING MODULE
# =========================
def level_from_score(score):
    if score <= 4:
        return "Mild", "dss-green", "Self-care and monitor"
    if score <= 9:
        return "Moderate", "dss-orange", "Consultation advised"
    return "Severe", "dss-red", "Please book consultation soon"

def render_screening_result(title, score, max_score):
    level, css_class, action = level_from_score(score)
    pct = round((score / max_score) * 100)

    st.markdown(
        f"""
        <div class="screening-result {css_class}">
            <div class="bubble-head">
                <span class="pill">{icon_brain()}<span>{html_lib.escape(title)}</span></span>
            </div>
            <div class="bubble-body">
                <strong>Score:</strong> {score}/{max_score} ({pct}%)<br>
                <strong>Level:</strong> {level}<br>
                <strong>Action:</strong> {action}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='color:white;font-weight:700;'>This is a screening tool, not a diagnosis.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="whatsapp-cta-wrap">
            <a class="whatsapp-cta" href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" rel="noopener noreferrer">
                📲 BOOK CONSULTATION ON WHATSAPP
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

def run_screening(test_name, questions, prefix):
    options = [
        "0 - Not at all",
        "1 - Several days",
        "2 - More than half the days",
        "3 - Nearly every day",
    ]

    with st.form(f"{prefix}_form", clear_on_submit=False):
        st.markdown(
            "<div class='mini-note'>Rate how often you experienced each item in the last 2 weeks.</div>",
            unsafe_allow_html=True,
        )

        answers = []
        for i, q in enumerate(questions):
            ans = st.radio(
                q,
                options=options,
                index=0,
                key=f"{prefix}_q_{i}",
                horizontal=False,
            )
            answers.append(options.index(ans))

        submitted = st.form_submit_button(f"Calculate {test_name} Score")

    if submitted:
        score = sum(answers)
        st.session_state[f"screen_{prefix}"] = {"score": score, "max_score": len(questions) * 3}

    result = st.session_state.get(f"screen_{prefix}")
    if result:
        render_screening_result(test_name, result["score"], result["max_score"])

# =========================
# RENDERERS
# =========================
def render_message_user(text):
    safe = html_lib.escape(text).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="bubble user-bubble">
            <div class="bubble-head">
                <span class="pill">{icon_user()}<span>You</span></span>
            </div>
            <div class="bubble-body">{safe}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_message_dss(condition, severity, action, css_class):
    st.markdown(
        f"""
        <div class="dss-card {css_class}">
            <div class="bubble-head">
                <span class="pill">{icon_brain()}<span>Medical DSS</span></span>
            </div>
            <div class="bubble-body">
                <strong>Condition:</strong> {html_lib.escape(condition)}<br>
                <strong>Severity:</strong> {html_lib.escape(severity)}<br>
                <strong>Action:</strong> {html_lib.escape(action)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_message_ai(source, summary_text):
    safe_summary = html_lib.escape(summary_text).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="bubble ai-bubble">
            <div class="bubble-head">
                <span class="pill">{icon_bot()}<span>{html_lib.escape(source)}</span></span>
            </div>
            <div class="bubble-body">{safe_summary}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_section_header(icon_html, title_text):
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-icon">{icon_html}</div>
            <div class="section-title">{html_lib.escape(title_text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_whatsapp_url" not in st.session_state:
    st.session_state.last_whatsapp_url = ""

# =========================
# HEADER / PROFILE
# =========================
st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-icon">{icon_brain()}</div>
        <div class="hero-title">DURGA PSYCHIATRIC CENTRE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_pic, col_text = st.columns([1, 2])

with col_pic:
    if os.path.exists("profile.jpg"):
        st.image("profile.jpg", width=150)
    else:
        st.warning("profile.jpg not found")

with col_text:
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

st.divider()

# =========================
# SCREENING TESTS (ABOVE AI QUERY)
# =========================
render_section_header(icon_brain(), "Screening Tests")
st.markdown(
    "<div class='mini-note'>Choose one tab below. The tabs use icons and stay visible on mobile.</div>",
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

with tab_stress:
    st.markdown("<div class='screening-card'>", unsafe_allow_html=True)
    run_screening("Stress Test", stress_questions, "stress")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_anxiety:
    st.markdown("<div class='screening-card'>", unsafe_allow_html=True)
    run_screening("Anxiety Test", anxiety_questions, "anxiety")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_depression:
    st.markdown("<div class='screening-card'>", unsafe_allow_html=True)
    run_screening("Depression Test", depression_questions, "depression")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# =========================
# INPUT SECTION
# =========================
render_section_header(icon_chat(), "Enter your problem")

query = st.text_area(
    "Type here",
    key="query_text",
    height=140,
    placeholder="Explain your concern clearly",
)

if st.button("SEND", key="send_query_btn"):
    if query.strip():
        condition, severity, action, css_class = dss_score(query)
        source, answer = smart_ai(query)

        st.session_state.messages.append({"type": "user", "text": query})
        st.session_state.messages.append(
            {
                "type": "dss",
                "condition": condition,
                "severity": severity,
                "action": action,
                "css_class": css_class,
            }
        )
        st.session_state.messages.append({"type": "ai", "source": source, "text": answer})

# =========================
# CONVERSATION
# =========================
render_section_header(icon_chat(), "Conversation")

for msg in st.session_state.messages:
    if msg["type"] == "user":
        render_message_user(msg["text"])
    elif msg["type"] == "dss":
        render_message_dss(
            msg["condition"],
            msg["severity"],
            msg["action"],
            msg["css_class"],
        )
    else:
        render_message_ai(msg["source"], msg["text"])

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# =========================
# CONSULTATION FORM
# =========================
render_section_header(icon_mobile(), "Book Consultation")

with st.form("consultation_form", clear_on_submit=False):
    name = st.text_input("Name")
    phone = st.text_input("Mobile Number")

    cause = st.selectbox(
        "Concern",
        [
            "Stress",
            "Anxiety",
            "Depression",
            "Panic Disorder",
            "OCD",
            "Bipolar Disorder",
            "Sleep Disorder",
            "Relationship Issues",
            "Addiction",
            "Sexual Health Issues",
            "Other",
        ],
    )

    mode = st.radio("Session Mode", ["Online", "In-Person"])
    time_slot = st.selectbox("Preferred Time", ["Morning", "Afternoon", "Evening"])
    location = st.text_input("Location")

    submitted = st.form_submit_button("Submit Consultation")

if submitted:
    if name.strip() and phone.strip():
        message = (
            "I would like to request an appointment with Psychologist D.Durga.\n\n"
            f"Name: {name}\n"
            f"Mobile: {phone}\n"
            f"Concern: {cause}\n"
            f"Session Mode: {mode}\n"
            f"Preferred Time: {time_slot}\n"
            f"Location: {location}\n\n"
            "Please call back to discuss further."
        )

        whatsapp_url = "https://wa.me/{num}?text={text}".format(
            num=WHATSAPP_NUMBER,
            text=urllib.parse.quote(message),
        )

        st.session_state.last_whatsapp_url = whatsapp_url
        st.markdown(
            "<div style='color:white; font-weight:600;'>Click below to open WhatsApp and send the message.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.warning("Please enter both Name and Mobile Number.")

if st.session_state.last_whatsapp_url:
    st.markdown(
        f"""
        <div class="whatsapp-cta-wrap">
            <a class="whatsapp-cta" href="{st.session_state.last_whatsapp_url}" target="_blank" rel="noopener noreferrer">
                📲 CLICK TO OPEN WHATSAPP
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# FLOATING BUTTONS
# =========================
st.markdown(
    f"""
    <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" aria-label="WhatsApp">
        <div class="float-btn float-wa">{icon_whatsapp()}</div>
    </a>

    <a href="tel:{DISPLAY_NUMBER}" aria-label="Call">
        <div class="float-btn float-call">{icon_mobile()}</div>
    </a>
    """,
    unsafe_allow_html=True,
)

# =========================
# FIXED BOTTOM BOOK APPOINTMENT BUTTON
# =========================
st.markdown(
    f"""
    <div class="footer-bar">
        <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
            <div class="footer-btn">
                <span class="footer-icon">{icon_mobile()}</span>
                <span class="footer-icon">{icon_whatsapp()}</span>
                <span>BOOK CONSULTATION NOW</span>
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)