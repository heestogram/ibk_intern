import streamlit as st
import requests
from PIL import Image

if st.button("🏠Home으로 돌아가기"):
    st.session_state.page = "main"

st.set_page_config(page_title="나비얌 챗봇", page_icon="🦋")



if "messages" not in st.session_state:
    st.session_state.messages = []

logo_path = "assets/logo.png"
image = Image.open(logo_path)
st.image(image, width=150)

st.markdown("<h2 style='color:#FDC100;'>🦋 나비얌 기부 챗봇</h2>", unsafe_allow_html=True)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("나비얌, 기부 시장 등에 대해 궁금한 점을 물어보세요!"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("ai"):
        with st.spinner("답변 생성 중..."):
            try:
                res = requests.post("http://localhost:8000/ask", json={"question": prompt})
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(answer)
                    
                    st.session_state.messages.append({"role": "ai", "content": answer})
                else:
                    st.error("서버 오류")
            except Exception as e:
                st.error(f"요청 실패: {e}")


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: gray;'>Powered by OpenAI + LangChain + FastAPI + Streamlit</div>", unsafe_allow_html=True)

