import streamlit as st
import plotly.graph_objects as go

# 기부 요약
st.title("🎁 당신의 기부가 만든 변화")

st.metric("이번 기부로 지원된 결식 아동 수", "3명")
st.metric("누적 기부 금액", "₩42,000")

# 기부 영향력 차트
labels = ["도시락 지원", "보육 후원", "운영비"]
values = [30000, 10000, 2000]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig)

st.success("이번 기부로 강남구청의 복지 사각지대 캠페인이 더욱 확대되었습니다!")