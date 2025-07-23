import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def get_image_base64(path, fixed_height=20):
    img = Image.open(path)

    # 비율 유지하며 높이에 맞게 리사이즈
    w, h = img.size
    new_height = fixed_height
    new_width = int((w / h) * new_height)
    img = img.resize((new_width, new_height))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    base64_str = base64.b64encode(img_bytes).decode()
    return base64_str, new_width, new_height

logo_base64, logo_width, logo_height = get_image_base64("assets/ibk_logo2.png")


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

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; margin-top: -5px;'>
        <img src='data:image/png;base64,{logo_base64}' width='{logo_width}' height='{logo_height}' style='margin-right: 8px;'/>
        <span style='color: gray; font-size: 18px; font-weight: 500;'>BY IBK창공 12조</span>
    </div>
    """, unsafe_allow_html=True)



elif st.session_state.page == "chatbot":
    exec(open("chatbot_app.py").read())

elif st.session_state.page == "dashboard":
    exec(open("dashboard_app.py").read())

