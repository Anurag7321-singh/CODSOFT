import streamlit as st
import numpy as np
import base64
import time

# --- Background Image + Overlay ---
def set_bg_with_dim(image_file):
    ext = image_file.split('.')[-1]
    try:
        with open(image_file, "rb") as file:
            b64_img = base64.b64encode(file.read()).decode()
    except FileNotFoundError:
        st.error(f"Background image '{image_file}' not found. Please ensure it's in the same directory.")
        return

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
              linear-gradient(rgba(17,18,21,0.7), rgba(17,18,21,0.7)),
              url("data:image/{ext};base64,{b64_img}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_with_dim("ttt.webp")

# --- Styling ---
st.markdown("""
<style>
/* (Your existing CSS style unchanged) */
.glass-card {
    background: rgba(36,38,52, 0.85);
    backdrop-filter: blur(20px) brightness(1.15);
    -webkit-backdrop-filter: blur(20px) brightness(1.15);
    border-radius: 28px;
    padding: 34px 21px 23px 21px;
    box-shadow: 0 7px 52px 14px #00000099, 0 0 4.5px #fff7 inset;
    max-width: 430px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 34px;
    border: 1px solid #49e9ff55;
}
.neon-title {
    text-align: center;
    font-size: 2.7em;
    letter-spacing: 2px;
    margin-bottom: 5px;
    font-weight: 800;
    color: #36f6fd;
    text-shadow: 0 0 28px #10fff3, 0 0 34px #ffe66d;
}
.neon-desc {
    text-align: center;
    font-size: 1.25em;
    color: #ffe66d;
    margin: 0 0 16px 0;
}
.turn-msg {
    text-align: center;
    font-size: 1.22em;
    font-weight: 600;
    color: #00e7ff;
    margin-bottom: 12px;
    text-shadow: 0 0 14px #00d7ffaa;
}
.stButton > button {
    font-family: 'Arial Rounded MT Bold', Arial, emoji, sans-serif;
    color: #fff !important;
    font-size: 45px !important;
    border: 2.2px solid #55fffe99 !important;
    border-radius: 14px !important;
    margin: 7px 0;
    background: rgba(46,72,114,0.945) !important;
    box-shadow: 0 0 13px 3.5px #21ffeeb7, 0 0 4px #38c9ff52 inset;
    transition: box-shadow 0.15s, background 0.18s, color 0.13s;
    min-width: 70px;
    min-height: 70px;
}
.stButton > button:hover {
    background: linear-gradient(85deg, #ffe66d 0%, #ff56fe 100%) !important;
    color: #05354c !important;
    font-size: 47px !important;
    box-shadow: 0 0 38px 14px #fff93779, 0 0 7px #fff9 inset;
}
.stButton > button:disabled {
    background: rgba(46,72,114,0.5) !important;
    border-color: #55fffe55 !important;
    box-shadow: none !important;
    cursor: not-allowed;
}
.winner-msg {
    font-size: 1.5em;
    font-weight: 900;
    text-align: center;
    margin-top: 16px;
    background: linear-gradient(90deg, #ffe66d, #21f5ea, #ff56fe);
    color: #191a30;
    padding: 0.43em 1.3em;
    border-radius: 16px;
    box-shadow: 0 0 29px 8px #fffbbb22;
}
.stButton[data-testid="stButton"] button[key="restart-btn"] {
    background: linear-gradient(90deg, #ff56fe, #21f5ea) !important;
    color: #fff !important;
    font-size: 1.2em !important;
    font-weight: bold;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    margin-top: 20px !important;
    box-shadow: 0 0 15px 5px #ff56fe77, 0 0 5px #21f5ea77 inset;
    transition: all 0.2s ease-in-out;
}
.stButton[data-testid="stButton"] button[key="restart-btn"]:hover {
    box-shadow: 0 0 25px 10px #ff56feaa, 0 0 8px #21f5eaaa inset;
    transform: translateY(-2px);
}
.stRadio > label {
    font-size: 1.1em;
    font-weight: 600;
    color: #00e7ff;
    text-shadow: 0 0 10px #00d7ffaa;
}
.stRadio div[role="radiogroup"] {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 15px;
}
.stRadio div[role="radiogroup"] label {
    background: rgba(46,72,114,0.7);
    border: 1px solid #49e9ff55;
    border-radius: 8px;
    padding: 8px 15px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.stRadio div[role="radiogroup"] label:hover {
    background: rgba(46,72,114,0.9);
    box-shadow: 0 0 10px #21ffeeb7;
}
.stRadio div[role="radiogroup"] input:checked + div {
    background: linear-gradient(85deg, #ffe66d 0%, #ff56fe 100%) !important;
    color: #05354c !important;
    box-shadow: 0 0 15px 5px #fff93779 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Game Logic ---
BOARD_SIZE = 3

def create_board():
    return np.full((BOARD_SIZE, BOARD_SIZE), ' ')

def evaluate(board):
    for row in board:
        if np.all(row == 'X'): return 10
        elif np.all(row == 'O'): return -10
    for col in range(BOARD_SIZE):
        if np.all(board[:, col] == 'X'): return 10
        elif np.all(board[:, col] == 'O'): return -10
    if np.all(np.diag(board) == 'X') or np.all(np.diag(np.fliplr(board)) == 'X'): return 10
    elif np.all(np.diag(board) == 'O') or np.all(np.diag(np.fliplr(board)) == 'O'): return -10
    return 0

def is_moves_left(board):
    return ' ' in board

def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)
    if score == 10: return score - depth
    if score == -10: return score + depth
    if not is_moves_left(board): return 0
    if is_max:
        best = -1000
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[i][j] = ' '
                    alpha = max(alpha, best)
                    if beta <= alpha: return best
        return best
    else:
        best = 1000
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[i][j] = ' '
                    beta = min(beta, best)
                    if beta <= alpha: return best
        return best

def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                move_val = minimax(board, 0, False, -1000, 1000)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

# --- Session State Initialization ---
if "board" not in st.session_state:
    st.session_state.board = create_board()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "current_player_symbol" not in st.session_state:
    st.session_state.current_player_symbol = 'O'
if "game_mode" not in st.session_state:
    st.session_state.game_mode = 'Player vs. AI'
if "ai_needs_to_move" not in st.session_state:
    st.session_state.ai_needs_to_move = False

def check_game_status():
    score = evaluate(st.session_state.board)
    if score == 10:
        st.session_state.game_over = True
        if st.session_state.game_mode == 'Player vs. AI':
            st.session_state.winner = "🤖 AI Wins!"
        else:
            st.session_state.winner = "🎉 Player 2 (❌) Wins!"
    elif score == -10:
        st.session_state.game_over = True
        st.session_state.winner = "🎉 Player 1 (⭕) Wins!"
    elif not is_moves_left(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "🤝 Draw!"

def ai_move_logic():
    move = find_best_move(st.session_state.board)
    if move != (-1, -1):
        st.session_state.board[move] = 'X'
    check_game_status()
    st.session_state.current_player_symbol = 'O'
    st.session_state.ai_needs_to_move = False

# --- Display UI / Gameboard ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="neon-title">🧠 TIC-TAC-TOE</div>', unsafe_allow_html=True)

game_mode_choice = st.radio(
    "Choose Game Mode:",
    ('Player vs. AI', 'Player vs. Player'),
    key="game_mode_radio",
    horizontal=True,
    index=0 if st.session_state.game_mode == 'Player vs. AI' else 1
)

if game_mode_choice != st.session_state.game_mode:
    st.session_state.game_mode = game_mode_choice
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_player_symbol = 'O'
    st.session_state.ai_needs_to_move = False
    st.rerun()

if st.session_state.game_mode == 'Player vs. AI':
    st.markdown('<div class="neon-desc">You: <b style="color:#fc72e6;">⭕</b>  AI: <b style="color:#36f6fd;">❌</b></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="neon-desc">Player 1: <b style="color:#fc72e6;">⭕</b>  Player 2: <b style="color:#36f6fd;">❌</b></div>', unsafe_allow_html=True)

if not st.session_state.game_over:
    if st.session_state.game_mode == 'Player vs. AI':
        if st.session_state.current_player_symbol == 'O':
            st.markdown('<div class="turn-msg">Your turn! Make your move ⏳</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="turn-msg">AI is thinking... 🤖</div>', unsafe_allow_html=True)
    else:
        if st.session_state.current_player_symbol == 'O':
            st.markdown('<div class="turn-msg">Player 1\'s turn (⭕) ⏳</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="turn-msg">Player 2\'s turn (❌) ⏳</div>', unsafe_allow_html=True)

symbol_to_emoji = {'X': '❌', 'O': '⭕', ' ': ' '}
cols = st.columns(BOARD_SIZE, gap="small")

for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        with cols[j]:
            cell = st.session_state.board[i][j]
            btn_label = symbol_to_emoji[cell]

            is_disabled = st.session_state.game_over or cell != ' '
            if st.session_state.game_mode == 'Player vs. AI' and st.session_state.current_player_symbol == 'X':
                is_disabled = True

            if st.button(btn_label if btn_label else " ", key=f"{i}-{j}", use_container_width=True, disabled=is_disabled):
                if not st.session_state.game_over and cell == ' ':
                    st.session_state.board[i][j] = st.session_state.current_player_symbol
                    check_game_status()
                    if not st.session_state.game_over:
                        if st.session_state.game_mode == 'Player vs. AI':
                            st.session_state.current_player_symbol = 'X'
                            st.session_state.ai_needs_to_move = True
                        else:
                            st.session_state.current_player_symbol = 'X' if st.session_state.current_player_symbol == 'O' else 'O'
                    st.rerun()

if st.session_state.game_mode == 'Player vs. AI' and st.session_state.current_player_symbol == 'X' and not st.session_state.game_over and st.session_state.ai_needs_to_move:
    with st.spinner('AI is making its move...'):
        time.sleep(1)
        ai_move_logic()
    st.rerun()

if st.session_state.game_over:
    st.markdown(f'<div class="winner-msg">{st.session_state.winner}</div>', unsafe_allow_html=True)

if st.button("🔄 RESTART", key="restart-btn"):
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_player_symbol = 'O'
    st.session_state.ai_needs_to_move = False
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style='margin-top:19px;text-align:center;color:#fff6;font-family:monospace;font-size:17px;'>
✨ <em>Glow up and challenge the AI!</em> ✨
</div>
""", unsafe_allow_html=True)
