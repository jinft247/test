import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="점심 메뉴 룰렛", layout="wide")

# 2. 데이터 정의
MENU_DATA = {
    "한식": ["김치찌개", "비빔밥", "제육볶음", "불고기", "된장찌개", "국밥"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부", "양장피"],
    "일식": ["돈카츠", "초밥", "라멘", "규동", "소바", "텐동"],
    "양식": ["파스타", "피자", "스테이크", "햄버거", "샐러드"],
    "분식": ["떡볶이", "튀김", "순대", "라면", "김밥"]
}

# 3. 사이드바 구성
st.sidebar.header("🍱 카테고리별 메뉴 선택")
selected_menus = []

for category, menus in MENU_DATA.items():
    with st.sidebar.expander(f"{category} 메뉴"):
        # 기본적으로 모든 메뉴가 선택되어 있도록 설정
        choice = st.multiselect(f"{category} 목록", menus, default=menus[:3], key=category)
        selected_menus.extend(choice)

# 4. 본문 구성
st.title("🎡 오늘의 점심 메뉴 룰렛")
st.markdown("사이드바에서 원하는 메뉴를 선택한 후, 아래 버튼을 눌러보세요!")

if len(selected_menus) < 2:
    st.warning("룰렛을 돌리려면 최소 2개 이상의 메뉴를 선택해주세요.")
else:
    # 룰렛 차트(Plotly) 생성
    fig = go.Figure(data=[go.Pie(
        labels=selected_menus,
        values=[1] * len(selected_menus),
        hole=.4,
        textinfo='label',
        showlegend=False,
        marker=dict(colors=random.sample(['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#FF6666'] * 5, len(selected_menus)))
    )])
    
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=500)
    
    # 룰렛 출력
    roulette_placeholder = st.empty()
    roulette_placeholder.plotly_chart(fig, use_container_width=True)

    # 돌리기 버튼
    if st.button("🚀 룰렛 돌리기!", use_container_width=True):
        # 애니메이션 효과 시뮬레이션
        with st.spinner("메뉴 고르는 중..."):
            for i in range(10):
                # 회전하는 느낌을 주기 위해 rotation 값을 변경하며 업데이트
                fig.update_layout(rotation=random.randint(0, 360))
                roulette_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(0.1)
        
        # 결과 선정
        winner = random.choice(selected_menus)
        st.balloons()
        st.success(f"🎉 오늘 점심은 **{winner}** 어떠세요?")
        st.markdown(f"### 오늘의 추천: {winner}")