import streamlit as st
from PIL import Image


st.set_page_config(page_title="나비얌", page_icon="🦋", layout="centered")
st.image("assets/logo.png", width=300)
st.title("나비얌 기능 추가 실험실")

st.markdown("### 🖱️ 체험할 기능을 선택하세요!")


col1, col2 = st.columns(2)
with col1:
    if st.button("💬 기부 QnA 챗봇"):
        st.switch_page("pages/chatbot_app.py")

with col2:
    if st.button("📊 기부 임팩트 대시보드"):
        st.switch_page("pages/dashboard_app.py")