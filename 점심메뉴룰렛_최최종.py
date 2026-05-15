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
        # 기본값 설정 및 선택
        choice = st.multiselect(f"{category} 목록", menus, default=menus[:3], key=f"select_{category}")
        selected_menus.extend(choice)

# 4. 본문 구성
st.title("🎡 오늘의 점심 메뉴 룰렛")
st.markdown("사이드바에서 원하는 메뉴를 선택한 후, 아래 버튼을 눌러보세요!")

if len(selected_menus) < 2:
    st.warning("룰렛을 돌리려면 최소 2개 이상의 메뉴를 선택해주세요.")
else:
    # 초기 룰렛 차트 생성
    fig = go.Figure(data=[go.Pie(
        labels=selected_menus,
        values=[1] * len(selected_menus),
        hole=.4,
        textinfo='label',
        showlegend=False,
        marker=dict(colors=random.sample(['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#FF6666'] * 5, len(selected_menus)))
    )])
    
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=500)
    
    # 룰렛 출력 공간 확보
    roulette_placeholder = st.empty()
    # 처음 화면 로드 시 차트 표시 (중복 방지를 위해 고유 key 할당)
    roulette_placeholder.plotly_chart(fig, use_container_width=True, key="initial_chart")

    # 돌리기 버튼
    if st.button("🚀 룰렛 돌리기!", use_container_width=True):
        with st.spinner("메뉴 고르는 중..."):
            # 애니메이션: 회전 각도를 바꿔가며 다시 그리기
            for i in range(20):
                new_rotation = random.randint(0, 360)
                # update_layout이 아닌 update_traces 사용 (중요!)
                fig.update_traces(rotation=new_rotation)
                
                # 에러 해결 핵심: 매번 다른 key를 부여하여 중복 ID 에러 방지
                roulette_placeholder.plotly_chart(
                    fig, 
                    use_container_width=True, 
                    key=f"spin_{i}"
                )
                time.sleep(0.05)
        
        # 애니메이션 완료 후 최종 결과 차트 고정
        roulette_placeholder.plotly_chart(fig, use_container_width=True, key="final_chart")

        # 결과 선정 및 축하 효과
        winner = random.choice(selected_menus)
        st.balloons()
        st.success(f"🎉 오늘 점심은 **{winner}** 어떠세요?")
        st.markdown(f"### 오늘의 추천 메뉴: {winner}")