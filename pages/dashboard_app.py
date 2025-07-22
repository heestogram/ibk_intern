# import streamlit as st
# import plotly.graph_objects as go

# # 기부 요약
# st.title("🎁 당신의 기부가 만든 변화")

# st.metric("이번 기부로 지원된 결식 아동 수", "3명")
# st.metric("누적 기부 금액", "₩42,000")

# # 기부 영향력 차트
# labels = ["도시락 지원", "보육 후원", "운영비"]
# values = [30000, 10000, 2000]

# fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
# st.plotly_chart(fig)

# st.success("이번 기부로 강남구청의 복지 사각지대 캠페인이 더욱 확대되었습니다!")

import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 또는 생성한 DataFrame을 불러옵니다
df = pd.read_csv("gibu_record.csv")  # 또는 직접 생성한 df

# 날짜 컬럼 문자열을 datetime으로 변환
df['date'] = pd.to_datetime(df['date'])

# 제목
st.title("📊 기부 데이터 시각화 대시보드")

# 날짜 필터
min_date, max_date = df['date'].min(), df['date'].max()
date_range = st.date_input("날짜 범위 선택", value=(min_date, max_date))

# 카테고리 필터
categories = df['category'].unique().tolist()
selected_categories = st.multiselect("카테고리 선택", categories, default=categories)

# 지역 필터
regions = df['region'].unique().tolist()
selected_regions = st.multiselect("지역 선택", regions, default=regions)

# 필터 적용
filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['category'].isin(selected_categories)) &
    (df['region'].isin(selected_regions))
]

# 카테고리별 총 금액
st.subheader("카테고리별 기부 금액 총합")
fig1 = px.bar(filtered_df.groupby("category", as_index=False)['amount'].sum(),
              x='category', y='amount', text='amount')
st.plotly_chart(fig1)

# 지역별 총 금액
st.subheader("지역별 기부 금액 총합")
fig2 = px.bar(filtered_df.groupby("region", as_index=False)['amount'].sum(),
              x='region', y='amount', text='amount')
st.plotly_chart(fig2)

# 날짜별 추이
st.subheader("날짜별 기부 금액 추이")
fig3 = px.line(filtered_df.groupby('date', as_index=False)['amount'].sum(),
               x='date', y='amount', markers=True)
st.plotly_chart(fig3)


campaigns = pd.DataFrame([
    {"region":"서울","detail_region": "강남구", "campaign_name": "복지 사각지대 캠페인", "base_support": 100000,
     "comment_text": "복지 사각지대 캠페인이 더욱 확대되었습니다!"},
    {"region":"인천","detail_region": "송도", "campaign_name": "반찬 나눔 프로젝트", "base_support": 50000,
     "comment_text": "더 많은 독거노인에게 반찬을 배달할 수 있게 되었어요!"}
])



# UI
grouped = df.groupby("region", as_index=False)["amount"].sum()

# 제목
st.title("🎁 당신의 기부가 만든 변화")

# 누적 기부 정보를 기반으로 문장 출력
for _, row in grouped.iterrows():
    region = row["region"]
    total_amount = row["amount"]

    # 해당 지역에 캠페인 정보 있는 경우만 출력
    matched = campaigns[campaigns["region"] == region]
    if not matched.empty:
        campaign_name = matched.iloc[0]["campaign_name"]
        st.markdown(f"✅ **₩{total_amount:,} 기부를 통해 {region}의 '{campaign_name}'에 기여하셨습니다.**")