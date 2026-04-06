# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse

st.set_page_config(page_title="Durga Psychiatric Centre", layout="centered")

WHATSAPP = "917395944527"

# ================= UI =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#5f6dfc,#7b2ff7); color:white;}
textarea,input{color:black!important;}
button{background:black!important;color:white!important;border-radius:12px!important;font-size:16px!important;padding:10px!important;}
label{color:white!important;}
.whatsapp-btn{
display:block;text-align:center;padding:16px;
background:linear-gradient(90deg,#25D366,#128C7E);
color:white;font-size:18px;border-radius:12px;text-decoration:none;margin-top:10px;
}
.float-w{position:fixed;bottom:90px;right:20px;background:#25D366;width:60px;height:60px;border-radius:50%;
display:flex;align-items:center;justify-content:center;font-size:26px;color:white;z-index:9999;}
.float-c{position:fixed;bottom:160px;right:20px;background:#0a84ff;width:60px;height:60px;border-radius:50%;
display:flex;align-items:center;justify-content:center;font-size:26px;color:white;z-index:9999;}
.footer{position:fixed;bottom:0;width:100%;background:black;color:white;text-align:center;padding:12px;z-index:9999;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("DURGA PSYCHIATRIC CENTRE")

# ================= VOICE =================
st.subheader("🎤 Voice Input")

voice_text = st.text_input("Tap mic and speak (mobile browser will open voice keyboard)")

if st.button("Send Voice Query"):
    if voice_text:
        st.success("Voice Query Received")
        st.write("AI:", "You may be experiencing emotional stress. Please take support.")

# ================= TEXT =================
st.subheader("💬 Your Query")

query = st.text_area("Type your concern here")

if st.button("SEND"):
    if query:
        st.write("AI Response:")
        st.write("Condition: Stress")
        st.write("Severity: Mild")
        st.write("Advice: Relax, take breaks, seek support if needed.")

# ================= FORM =================
st.subheader("📞 Book Consultation")

name = st.text_input("Name")
mobile = st.text_input("Mobile Number")

cause = st.selectbox("Concern", [
"Stress","Anxiety","Depression","Panic Disorder","OCD","Bipolar Disorder",
"PTSD","ADHD","Sleep Disorder","Relationship Issues","Addiction",
"Sexual Health Issues","Phobia","Anger Issues","Other"
])

mode = st.radio("Session Mode", ["Online","In-Person"])
time = st.selectbox("Preferred Time", ["Morning","Afternoon","Evening"])
location = st.text_input("Location")

# ================= SUBMIT =================
if st.button("Submit Consultation"):

    msg = f"""I would like to request an appointment with Psychologist D.Durga.

Name: {name}
Mobile: {mobile}
Concern: {cause}
Mode: {mode}
Preferred Time: {time}
Location: {location}

Please call back to discuss further.
"""

    url = "https://wa.me/" + WHATSAPP + "?text=" + urllib.parse.quote(msg)

    st.success("Opening WhatsApp...")

    # AUTO REDIRECT (SAFE)
    st.markdown(f"""
    <meta http-equiv="refresh" content="1; url={url}">
    """, unsafe_allow_html=True)

    # FALLBACK BUTTON (IMPORTANT)
    st.markdown(f"""
    <a href="{url}" target="_blank" class="whatsapp-btn">
    CLICK TO OPEN WHATSAPP
    </a>
    """, unsafe_allow_html=True)

# ================= FLOAT =================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP}">
<div class="float-w">💬</div></a>

<a href="tel:+{WHATSAPP}">
<div class="float-c">📞</div></a>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<a href="https://wa.me/{WHATSAPP}">
<div class="footer">📞 Book Consultation on WhatsApp</div>
</a>
""", unsafe_allow_html=True)