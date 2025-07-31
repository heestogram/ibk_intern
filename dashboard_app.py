
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("gibu_record.csv")  

df['date'] = pd.to_datetime(df['date'])

if st.button("🏠Home으로 돌아가기"):
    st.session_state.page = "main"

st.title("📊 기부 데이터 시각화 대시보드")

min_date, max_date = df['date'].min(), df['date'].max()
date_range = st.date_input("날짜 범위 선택", value=(min_date, max_date))

categories = df['category'].unique().tolist()
selected_categories = st.multiselect("카테고리 선택", categories, default=categories)

regions = df['region'].unique().tolist()
selected_regions = st.multiselect("지역 선택", regions, default=regions)


filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['category'].isin(selected_categories)) &
    (df['region'].isin(selected_regions))
]

st.subheader("카테고리별 기부 금액 총합")
fig1 = px.bar(filtered_df.groupby("category", as_index=False)['amount'].sum(),
              x='category', y='amount', text='amount')
st.plotly_chart(fig1)

st.subheader("지역별 기부 금액 총합")
fig2 = px.bar(filtered_df.groupby("region", as_index=False)['amount'].sum(),
              x='region', y='amount', text='amount')
st.plotly_chart(fig2)

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



grouped = df.groupby("region", as_index=False)["amount"].sum()

st.title("🎁 당신의 기부가 만든 변화")

for _, row in grouped.iterrows():
    region = row["region"]
    total_amount = row["amount"]

    # 해당 지역에 캠페인 정보 있는 경우만 출력
    matched = campaigns[campaigns["region"] == region]
    if not matched.empty:
        campaign_name = matched.iloc[0]["campaign_name"]
        st.markdown(f"✅ **₩{total_amount:,} 기부를 통해 {region}의 '{campaign_name}'에 기여하셨습니다.**")