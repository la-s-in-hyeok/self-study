import streamlit as st
import random
import re

# 찬양 리스트
songs = [
    "나로부터 시작되리", "하나님의 사랑이", "주의 나라가 비전인 세대", "우리 주 안에서 노래하며",
    "유월절 어린 양의 피로", "예수 열방의 소망", "우리 죄 위해 죽으신 주", "여호와께 돌아가자",
    "주님만이 왕이십니다", "예수 나의 첫사랑 되시네", "내 마음을 가득채운", "하나님께서 세상을 사랑하사",
    "내 영혼은 안전합니다", "성령의 불타는 교회", "성령이 오셨네", "주님 다시 오실 때까지"
]

# 세션 상태 초기화
def init_game():
    st.session_state['selected_song'] = random.choice(songs)
    st.session_state['display_word'] = re.sub(r'[^ ]', '_', st.session_state['selected_song'])
    st.session_state['remaining_attempts'] = 18
    st.session_state['guessed_letters'] = set()
    st.session_state['guessed_words'] = []
    st.session_state['game_over'] = False
    st.session_state['message'] = ""

if 'selected_song' not in st.session_state:
    init_game()

st.title("찬양 맞추기 (행맨) 게임")
st.subheader("다음 찬양 제목을 맞춰보세요!")

# 현재 상태 표시
st.write("현재 상태(업데이트 되는게 느려요 이해좀): ", st.session_state['display_word'])
st.write(f"남은 기회: {st.session_state['remaining_attempts']}")

if not st.session_state['game_over']:
    col1, col2 = st.columns(2)
    with col1:
        user_input = st.text_input("한 글자를 입력하세요:", max_chars=1, key="user_input")
        submit_letter = st.button("글자 제출(더블 클릭)")
    with col2:
        full_guess = st.text_input("정답을 입력하세요:", key="full_guess")
        submit_word = st.button("정답 제출(더블 클릭)")
    
    if submit_letter and user_input:
        user_input = user_input.strip()
        if user_input in st.session_state['guessed_letters']:
            st.session_state['message'] = "이미 입력한 글자입니다!"
        else:
            st.session_state['guessed_letters'].add(user_input)
            st.session_state['remaining_attempts'] -= 1
            
            if user_input in st.session_state['selected_song']:
                st.session_state['message'] = "정답입니다!"
            else:
                st.session_state['message'] = "틀렸습니다!"
            
            # 언더바 업데이트
            st.session_state['display_word'] = "".join(
                c if c in st.session_state['guessed_letters'] or c == " " else "_"
                for c in st.session_state['selected_song']
            )
            
            # 정답 확인
            if "_" not in st.session_state['display_word']:
                st.session_state['game_over'] = True
                st.success(f"축하합니다! 정답: {st.session_state['selected_song']}")
                st.markdown("<h1 style='font-size:100px; text-align:center;'>1</h1>", unsafe_allow_html=True)
    
    if submit_word and full_guess:
        full_guess = full_guess.strip()
        st.session_state['guessed_words'].append(full_guess)
        st.session_state['remaining_attempts'] -= 1
        if full_guess == st.session_state['selected_song']:
            st.session_state['game_over'] = True
            st.success(f"축하합니다! 정답: {st.session_state['selected_song']}")
            st.markdown("<h1 style='font-size:100px; text-align:center;'>1</h1>", unsafe_allow_html=True)
        else:
            st.session_state['message'] = "틀렸습니다! 다시 시도하세요."
    
    if st.session_state['remaining_attempts'] <= 0:
        st.session_state['game_over'] = True
        st.error(f"게임 오버! 정답은 '{st.session_state['selected_song']}'였습니다.")
    
    # 메시지 출력
    st.write(f"### {st.session_state['message']}")
    
    # 입력한 글자 및 정답 히스토리 표시
    st.write("### 입력한 글자들: ", ", ".join(sorted(st.session_state['guessed_letters'])))
    st.write("### 입력한 정답들: ", ", ".join(st.session_state['guessed_words']))
else:
    if st.button("다시 시작하기"):
        init_game()