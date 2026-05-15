import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# --- [수정 1] 파일 저장 및 불러오기 함수 정의 ---
def load_data():
    if os.path.exists('events.csv'):
        return pd.read_csv('events.csv')
    else:
        # 파일이 없을 때 사용할 초기 데이터
        return pd.DataFrame([
            {"행사명": "부모님 결혼기념일", "날짜": "2000-02-12", "반복": True, "메모": "직접 만든 감사 카드 준비"},
            {"행사명": "어버이날", "날짜": "2026-05-08", "반복": True, "메모": "직접 만든 감사 카드 준비"},
            {"행사명": "사촌동생 중학교 졸업식", "날짜": "2026-01-08", "반복": False, "메모": "축하 이미지 생성해서 보내줌"}
        ])

def save_data(df):
    df.to_csv('events.csv', index=False)

# 페이지 기본 설정
st.set_page_config(page_title="패밀리 플래너", page_icon="🎁", layout="wide")

st.title("🎁 우리 가족 기념일 & 기프트 플래너")

# --- [수정 2] 세션 상태 초기화 (파일에서 불러오기) ---
if 'events' not in st.session_state:
    st.session_state.events = load_data()

if 'profiles' not in st.session_state:
    st.session_state.profiles = {
        "나": {"상의 사이즈": "95(M)", "선호 스타일": "헤리티지 사파리 자켓"},
        "언니": {"상의 사이즈": "100(L)", "선호 스타일": "꽃무늬 블라우스"},
        "엄마": {"상의 사이즈": "90(S)", "선호 스타일": "버버리 자켓"},
        "아빠": {"상의 사이즈": "105(XL)", "선호 스타일": "POLO 카라 티셔츠"}
    }

# 탭 구성하기
tab1, tab2 = st.tabs(["🗓️ 다가오는 기념일 (D-Day)", "🛍️ 가족 프로필 & 선물 아이디어"])

with tab1:
    st.subheader("다가오는 일정")
    
    # D-Day 계산 로직
    today = date.today()
    
    # 일정 표시 루프
    for index, row in st.session_state.events.iterrows():
        event_date = datetime.strptime(row["날짜"], "%Y-%m-%d").date()
        
        if row["반복"]:
            next_date = event_date.replace(year=today.year)
            if next_date < today:
                next_date = next_date.replace(year=today.year + 1)
        else:
            next_date = event_date

        # 0(월요일)부터 6(일요일)까지의 한글 요일 리스트
        weekday_list = ['월', '화', '수', '목', '금', '토', '일']
        korean_weekday = weekday_list[next_date.weekday()]

        d_day = (next_date - today).days
        
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['행사명']}** ({next_date.strftime('%Y년 %m월 %d일')} {korean_weekday}요일)")
                st.caption(f"메모: {row['메모']}")
            with col2:
                if d_day > 0:
                    st.metric(label="D-Day", value=f"D-{d_day}")
                elif d_day == 0:
                    st.metric(label="D-Day", value="D-Day! 🎉")
                else:
                    st.metric(label="D-Day", value=f"D+{-d_day}")

    st.divider()
    
    # 레이아웃을 위해 컬럼 나누기 (추가와 삭제)
    col_add, col_del = st.columns(2)

    with col_add:
        st.write("➕ **새로운 일정 추가**")
        with st.form("add_event_form", clear_on_submit=True):
            new_name = st.text_input("행사명")
            new_date = st.date_input("날짜 선택")
            is_repeat = st.checkbox("매년 반복 (생일, 결혼기념일 등)")
            new_memo = st.text_area("메모 (선물 아이디어 등)")
            submit_btn = st.form_submit_button("추가하기")
            
            if submit_btn and new_name:
    # new_memo 변수를 추가합니다.
                new_row = {
                "행사명": new_name, 
                "날짜": new_date.strftime("%Y-%m-%d"), 
                "반복": is_repeat, 
                "메모": new_memo  # 기존 "" 에서 new_memo로 수정
                }
                st.session_state.events = pd.concat([st.session_state.events, pd.DataFrame([new_row])], ignore_index=True)
                save_data(st.session_state.events)
                st.rerun()

    with col_del:
        st.write("⚙️ **일정 관리 (수정 및 삭제)**")
        if not st.session_state.events.empty:
            # 1. 수정/삭제할 일정 선택
            event_names = st.session_state.events["행사명"].tolist()
            selected_event_name = st.selectbox("관리할 일정을 선택하세요", event_names)
            
            # 선택된 일정의 기존 데이터 가져오기
            event_to_edit = st.session_state.events[st.session_state.events["행사명"] == selected_event_name].iloc[0]
            
            # 2. 수정용 입력 창 (기존 값을 value/index로 넣어줌)
            with st.expander(f"'{selected_event_name}' 내용 수정"):
                edit_name = st.text_input("행사명 수정", value=event_to_edit["행사명"])
                edit_date = st.date_input("날짜 수정", value=datetime.strptime(event_to_edit["날짜"], "%Y-%m-%d").date())
                edit_repeat = st.checkbox("매년 반복 수정", value=bool(event_to_edit["반복"]), key="edit_rep")
                edit_memo = st.text_area("메모 수정", value=event_to_edit["메모"] if pd.notna(event_to_edit["메모"]) else "")
                
                col_edit_btn, col_del_btn = st.columns(2)
                
                with col_edit_btn:
                    if st.button("수정 완료"):
                        # 데이터 업데이트
                        idx = st.session_state.events[st.session_state.events["행사명"] == selected_event_name].index[0]
                        st.session_state.events.at[idx, "행사명"] = edit_name
                        st.session_state.events.at[idx, "날짜"] = edit_date.strftime("%Y-%m-%d")
                        st.session_state.events.at[idx, "반복"] = edit_repeat
                        st.session_state.events.at[idx, "메모"] = edit_memo
                        
                        save_data(st.session_state.events)
                        st.success("수정되었습니다!")
                        st.rerun()
                
                with col_del_btn:
                    if st.button("일정 삭제", type="primary"): # 삭제 버튼은 강조색으로
                        st.session_state.events = st.session_state.events[st.session_state.events["행사명"] != selected_event_name]
                        save_data(st.session_state.events)
                        st.warning("일정이 삭제되었습니다.")
                        st.rerun()
        else:
            st.info("관리할 일정이 없습니다.")

with tab2:
    st.subheader("가족 프로필 관리")
    st.write("옷이나 신발 사이즈를 미리 적어두면 선물 고를 때 편해요!")
    
    for member, info in st.session_state.profiles.items():
        with st.expander(f"👤 {member}의 프로필"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input(f"{member} 상의 사이즈", value=info["상의 사이즈"], key=f"size_{member}")
            with col_b:
                st.text_input(f"{member} 선호 스타일", value=info["선호 스타일"], key=f"style_{member}")