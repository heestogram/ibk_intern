import streamlit as st
import requests


st.set_page_config(page_title="나비얌 챗봇", page_icon="💛")



# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

st.image("logo.png", width=150)
st.markdown("<h2 style='color:#FDC100;'>💛 나비얌 기부 챗봇</h2>", unsafe_allow_html=True)

# 이전 대화 렌더링
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if prompt := st.chat_input("궁금한 점을 입력해 주세요!"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # FastAPI 서버로 요청
    with st.chat_message("ai"):
        with st.spinner("답변 생성 중..."):
            try:
                res = requests.post("http://localhost:8000/ask", json={"question": prompt})
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(answer)
                    # 챗봇 응답 저장
                    st.session_state.messages.append({"role": "ai", "content": answer})
                else:
                    st.error("서버 오류")
            except Exception as e:
                st.error(f"요청 실패: {e}")


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: gray;'>Powered by OpenAI + LangChain + FastAPI + Streamlit</div>", unsafe_allow_html=True)
