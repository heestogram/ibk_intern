import streamlit as st
from PIL import Image


st.set_page_config(page_title="나비얌 앱 기능 추가 실험실", page_icon="🦋", layout="centered")


if "page" not in st.session_state:
    st.session_state.page = "main"

# 사이드바
with st.sidebar:
    st.markdown("<h2 style='font-weight:bold;'>MENU</h2>", unsafe_allow_html=True)
    if st.button("💬 기부 QnA 챗봇"):
        st.session_state.page = "chatbot"
    if st.button("📊 기부 임팩트 대시보드"):
        st.session_state.page = "dashboard"


if st.session_state.page == "main":
    st.image("assets/logo.png", width=200)
    st.title("나비얌 앱 기능 추가 실험실")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🖱️ 체험할 기능을 선택하세요!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 기부 QnA 챗봇"):
            st.session_state.page = "chatbot"
    with col2:
        if st.button("📊 기부 임팩트 대시보드"):
            st.session_state.page = "dashboard"



elif st.session_state.page == "chatbot":
    exec(open("chatbot_app.py").read())

elif st.session_state.page == "dashboard":
    exec(open("dashboard_app.py").read())

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: gray;'>By IBK 창공 Team 12</div>", unsafe_allow_html=True)
