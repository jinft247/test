import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Todo List App", layout="centered")

st.title("📝 My Todo List")

# 세션 상태 초기화 (할 일을 저장할 리스트)
if 'todos' not in st.session_state:
    st.session_state.todos = []

# 1. 상단 입력창과 추가 버튼
col1, col2 = st.columns([4, 1])
with col1:
    new_todo = st.text_input("할 일을 입력하세요", placeholder="예: 운동하기", key="todo_input")
with col2:
    if st.button("추가", use_container_width=True):
        if new_todo:
            st.session_state.todos.append({"task": new_todo, "completed": False})
            st.rerun()  # 화면 갱신

st.divider()

# 2. 등록된 할 일 목록 표시
for index, todo in enumerate(st.session_state.todos):
    cols = st.columns([0.5, 4, 1])
    
    # 체크박스: 완료 여부 표시
    with cols[0]:
        is_completed = st.checkbox("", value=todo["completed"], key=f"check_{index}")
        if is_completed != todo["completed"]:
            st.session_state.todos[index]["completed"] = is_completed
            st.rerun()

    # 할 일 텍스트: 완료 시 취소선 적용
    with cols[1]:
        task_text = todo["task"]
        if todo["completed"]:
            st.markdown(f"~~{task_text}~~")
        else:
            st.write(task_text)

    # 삭제 버튼: 해당 항목 제거
    with cols[2]:
        if st.button("삭제", key=f"del_{index}", use_container_width=True):
            st.session_state.todos.pop(index)
            st.rerun()

# 할 일이 없을 때 안내 문구
if not st.session_state.todos:
    st.info("현재 등록된 할 일이 없습니다.")