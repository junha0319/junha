import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ GitHub CSV 파일 불러오기 (raw 링크 사용)
csv_url = "https://raw.githubusercontent.com/junha0319/junha/main/%EC%A0%95%EB%A6%AC%EB%90%9C_%EC%9D%B8%EA%B5%AC_%ED%86%B5%EA%B3%84_%EB%8D%B0%EC%9D%B4%ED%84%B0.csv"
df = pd.read_csv(csv_url, encoding="utf-8-sig")

# Streamlit 페이지 설정
st.set_page_config(page_title="대한민국 인구 대시보드 22160027 송준하", layout="wide", page_icon="📊")
st.title("📊 대한민국 인구 대시보드 22160027 송준하")

# 사이드바 필터
years = sorted(df["연도"].unique(), reverse=True)
selected_year = st.sidebar.selectbox("연도 선택", years)
selected_gender = st.sidebar.radio("성별 선택", ["전체", "남자", "여자"])
regions = ["전국"] + sorted(df["행정구역"].unique())
selected_region = st.sidebar.selectbox("행정구역 선택", regions)

# 데이터 필터링
filtered = df[(df["연도"] == selected_year) & (df["성별"] == selected_gender)]
if selected_region != "전국":
    filtered = filtered[filtered["행정구역"] == selected_region]

# 메트릭 영역
col1, col2 = st.columns(2)
total_pop = filtered["인구수"].sum()
with col1:
    st.markdown(f"#### {selected_year} 총 인구수")
    st.subheader(f"{total_pop/1_000_000:.2f} M")

# 전년도 비교
prev_year = selected_year - 1
prev_data = df[(df["연도"] == prev_year) & (df["성별"] == selected_gender)]
if selected_region != "전국":
    prev_data = prev_data[prev_data["행정구역"] == selected_region]
prev_pop = prev_data["인구수"].sum()
delta = total_pop - prev_pop
symbol = "🔼" if delta >= 0 else "🔽"
with col2:
    st.markdown(f"#### {prev_year} 대비 증감")
    st.subheader(f"{symbol} {abs(delta)/1000:.1f} K")

# 전국 연도별 인구 변화
st.markdown("### 전국 연도별 인구 변화")
year_summary = df[(df["성별"] == "전체") & (df["행정구역"] == "전국")]
line_fig = px.line(year_summary, x="연도", y="인구수", markers=True)
st.plotly_chart(line_fig, use_container_width=True)

# 지역별 인구 막대그래프
st.markdown("### 지역별 인구수")
bar_data = df[(df["연도"] == selected_year) & (df["성별"] == selected_gender) & (df["행정구역"] != "전국")]
bar_fig = px.bar(bar_data.sort_values("인구수", ascending=True),
                 y="행정구역", x="인구수", orientation="h",
                 color="인구수", color_continuous_scale="blues")
st.plotly_chart(bar_fig, use_container_width=True)

# 테이블 출력
st.markdown("### 선택 조건 데이터 테이블")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
