import streamlit as st
import numpy as np
import base64

# --- Background Image + Overlay ---
def set_bg_with_dim(image_file):
    """
    Sets a background image for the Streamlit app with a dimming overlay.
    The image is read, base64 encoded, and applied via custom CSS.
    """
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

# Assuming 'ttt.webp' is in the same directory as your script
set_bg_with_dim("ttt.webp")

# --- Styling ---
st.markdown("""
<style>
/* Glassmorphism card container */
.glass-card {
    background: rgba(36,38,52, 0.85); /* Semi-transparent dark background */
    backdrop-filter: blur(20px) brightness(1.15); /* Blur and brightness for glass effect */
    -webkit-backdrop-filter: blur(20px) brightness(1.15); /* Webkit prefix for compatibility */
    border-radius: 28px; /* Rounded corners */
    padding: 34px 21px 23px 21px; /* Padding inside the card */
    box-shadow: 0 7px 52px 14px #00000099, 0 0 4.5px #fff7 inset; /* Outer and inner shadows */
    max-width: 430px; /* Max width for responsiveness */
    margin-left: auto; /* Center the card horizontally */
    margin-right: auto;
    margin-top: 34px; /* Top margin */
    border: 1px solid #49e9ff55; /* Light blue border */
}

/* Neon title styling */
.neon-title {
    text-align: center; /* Center align text */
    font-size: 2.7em; /* Large font size */
    letter-spacing: 2px; /* Spacing between letters */
    margin-bottom: 5px; /* Bottom margin */
    font-weight: 800; /* Bold font weight */
    color: #36f6fd; /* Bright blue color */
    text-shadow: 0 0 28px #10fff3, 0 0 34px #ffe66d; /* Neon glow effect */
}

/* Neon description styling */
.neon-desc {
    text-align: center; /* Center align text */
    font-size: 1.25em; /* Font size */
    color: #ffe66d; /* Yellowish color */
    margin: 0 0 16px 0; /* Margins */
}

/* Turn message styling */
.turn-msg {
    text-align: center; /* Center align text */
    font-size: 1.22em; /* Font size */
    font-weight: 600; /* Medium bold font weight */
    color: #00e7ff; /* Bright blue color */
    margin-bottom: 12px; /* Bottom margin */
    text-shadow: 0 0 14px #00d7ffaa; /* Subtle neon glow */
}

/* Tic-Tac-Toe button styling (targets the actual button element) */
.stButton > button {
    font-family: 'Arial Rounded MT Bold', Arial, emoji, sans-serif; /* Custom font stack */
    color: #fff !important; /* White text color */
    font-size: 45px !important; /* Large font size for symbols */
    border: 2.2px solid #55fffe99 !important; /* Border color */
    border-radius: 14px !important; /* Rounded corners */
    margin: 7px 0; /* Vertical margin */
    background: rgba(46,72,114,0.945) !important; /* Dark blue background */
    box-shadow: 0 0 13px 3.5px #21ffeeb7, 0 0 4px #38c9ff52 inset; /* Outer and inner shadows */
    transition: box-shadow 0.15s, background 0.18s, color 0.13s; /* Smooth transitions for hover effects */
    min-width: 70px; /* Minimum width for buttons */
    min-height: 70px; /* Minimum height for buttons */
}

/* Hover effects for Tic-Tac-Toe buttons */
.stButton > button:hover {
    background: linear-gradient(85deg, #ffe66d 0%, #ff56fe 100%) !important; /* Gradient background on hover */
    color: #05354c !important; /* Dark text color on hover */
    font-size: 47px !important; /* Slightly larger font on hover */
    box-shadow: 0 0 38px 14px #fff93779, 0 0 7px #fff9 inset; /* Enhanced glow on hover */
}

/* Disabled button styling */
.stButton > button:disabled {
    background: rgba(46,72,114,0.5) !important; /* Dimmed background when disabled */
    border-color: #55fffe55 !important; /* Dimmed border */
    box-shadow: none !important; /* No shadow when disabled */
    cursor: not-allowed; /* Change cursor for disabled state */
}


/* Winner message styling */
.winner-msg {
    font-size: 1.5em; /* Large font size */
    font-weight: 900; /* Extra bold */
    text-align: center; /* Center align text */
    margin-top: 16px; /* Top margin */
    background: linear-gradient(90deg, #ffe66d, #21f5ea, #ff56fe); /* Gradient background */
    color: #191a30; /* Dark text color */
    padding: 0.43em 1.3em; /* Padding */
    border-radius: 16px; /* Rounded corners */
    box-shadow: 0 0 29px 8px #fffbbb22; /* Subtle glow */
}

/* Restart button styling */
.stButton[data-testid="stButton"] button[key="restart-btn"] {
    background: linear-gradient(90deg, #ff56fe, #21f5ea) !important; /* Gradient background */
    color: #fff !important; /* White text */
    font-size: 1.2em !important; /* Font size */
    font-weight: bold; /* Bold font */
    border: none !important; /* No border */
    border-radius: 10px !important; /* Rounded corners */
    padding: 10px 20px !important; /* Padding */
    margin-top: 20px !important; /* Top margin */
    box-shadow: 0 0 15px 5px #ff56fe77, 0 0 5px #21f5ea77 inset; /* Glow effect */
    transition: all 0.2s ease-in-out; /* Smooth transition */
}

.stButton[data-testid="stButton"] button[key="restart-btn"]:hover {
    box-shadow: 0 0 25px 10px #ff56feaa, 0 0 8px #21f5eaaa inset; /* Enhanced glow on hover */
    transform: translateY(-2px); /* Slight lift effect */
}

/* Styling for the game mode radio buttons */
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
    """Initializes a new 3x3 Tic-Tac-Toe board with empty spaces."""
    return np.full((BOARD_SIZE, BOARD_SIZE), ' ')

def evaluate(board):
    """
    Evaluates the current state of the board to determine if there's a winner.
    Returns 10 if 'X' wins, -10 if 'O' wins, and 0 otherwise.
    """
    # Check rows
    for row in board:
        if np.all(row == 'X'): return 10
        elif np.all(row == 'O'): return -10

    # Check columns
    for col in range(BOARD_SIZE):
        if np.all(board[:, col] == 'X'): return 10
        elif np.all(board[:, col] == 'O'): return -10

    # Check diagonals
    if np.all(np.diag(board) == 'X') or np.all(np.diag(np.fliplr(board)) == 'X'): return 10
    elif np.all(np.diag(board) == 'O') or np.all(np.diag(np.fliplr(board)) == 'O'): return -10

    return 0 # No winner yet

def is_moves_left(board):
    """Checks if there are any empty cells left on the board."""
    return ' ' in board

def minimax(board, depth, is_max, alpha, beta):
    """
    Implements the Minimax algorithm with Alpha-Beta Pruning to find the best move.
    `is_max` is True for the maximizing player (AI, 'X'), False for the minimizing player (Player, 'O').
    `alpha` and `beta` are for pruning.
    """
    score = evaluate(board)

    # Base cases: If a player wins or it's a draw
    if score == 10: return score - depth # AI wins, prefer faster win
    if score == -10: return score + depth # Player wins, prefer slower loss
    if not is_moves_left(board): return 0 # Draw

    if is_max: # AI's turn (maximizing player)
        best = -1000
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'X' # Make the move
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[i][j] = ' ' # Undo the move
                    alpha = max(alpha, best)
                    if beta <= alpha: # Alpha-Beta Pruning
                        return best
        return best
    else: # Player's turn (minimizing player)
        best = 1000
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O' # Make the move
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[i][j] = ' ' # Undo the move
                    beta = min(beta, best)
                    if beta <= alpha: # Alpha-Beta Pruning
                        return best
        return best

def find_best_move(board):
    """
    Finds the optimal move for the AI ('X') using the Minimax algorithm.
    Returns the (row, col) of the best move.
    """
    best_val = -1000
    best_move = (-1, -1)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'X' # Try this move for AI
                # Calculate value of this move assuming player plays optimally
                move_val = minimax(board, 0, False, -1000, 1000)
                board[i][j] = ' ' # Undo the move

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

# --- Session State Initialization ---
# Initialize session state variables if they don't exist.
# This ensures game state persists across reruns.
if "board" not in st.session_state:
    st.session_state.board = create_board()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "current_player_symbol" not in st.session_state:
    st.session_state.current_player_symbol = 'O' # 'O' for Player 1, 'X' for Player 2/AI
if "game_mode" not in st.session_state:
    st.session_state.game_mode = 'AI' # Default mode

# --- Check for game over & Update winner ---
def check_game_status():
    """
    Checks the current game status (win, loss, draw) and updates session state accordingly.
    """
    score = evaluate(st.session_state.board)
    if score == 10: # 'X' wins
        st.session_state.game_over = True
        if st.session_state.game_mode == 'AI':
            st.session_state.winner = "🤖 AI Wins!"
        else:
            st.session_state.winner = "🎉 Player 2 (❌) Wins!"
    elif score == -10: # 'O' wins
        st.session_state.game_over = True
        st.session_state.winner = "🎉 Player 1 (⭕) Wins!"
    elif not is_moves_left(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "🤝 Draw!"

# --- AI Move ---
def ai_move():
    """
    Executes the AI's move if it's the AI's turn and the game is not over.
    Updates the board and checks game status.
    """
    # Only proceed if it's AI mode, AI's turn ('X'), and game is not over
    if st.session_state.game_mode == 'AI' and st.session_state.current_player_symbol == 'X' and not st.session_state.game_over:
        move = find_best_move(st.session_state.board)
        if move != (-1, -1): # Ensure a valid move was found
            st.session_state.board[move] = 'X'
        check_game_status() # Check status after AI's move
        st.session_state.current_player_symbol = 'O' # Switch back to player 1's turn
        st.rerun() # Force a rerun to display AI's move and update turn message

# --- Display UI / Gameboard ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="neon-title">🧠 TIC-TAC-TOE</div>', unsafe_allow_html=True)

# Game Mode Selection
game_mode_choice = st.radio(
    "Choose Game Mode:",
    ('Player vs. AI', 'Player vs. Player'),
    key="game_mode_radio",
    horizontal=True,
    index=0 if st.session_state.game_mode == 'AI' else 1
)

# If game mode changes, reset the game
if game_mode_choice != st.session_state.game_mode:
    st.session_state.game_mode = game_mode_choice
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_player_symbol = 'O'
    st.rerun()

# Display player symbols based on mode
if st.session_state.game_mode == 'AI':
    st.markdown('<div class="neon-desc">You: <b style="color:#fc72e6;">⭕</b>  AI: <b style="color:#36f6fd;">❌</b></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="neon-desc">Player 1: <b style="color:#fc72e6;">⭕</b>  Player 2: <b style="color:#36f6fd;">❌</b></div>', unsafe_allow_html=True)


# Display turn message based on current state
if not st.session_state.game_over:
    if st.session_state.game_mode == 'AI':
        if st.session_state.current_player_symbol == 'O':
            st.markdown('<div class="turn-msg">Your turn! Make your move ⏳</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="turn-msg">AI is thinking... 🤖</div>', unsafe_allow_html=True)
    else: # Player vs. Player mode
        if st.session_state.current_player_symbol == 'O':
            st.markdown('<div class="turn-msg">Player 1\'s turn (⭕) ⏳</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="turn-msg">Player 2\'s turn (❌) ⏳</div>', unsafe_allow_html=True)

symbol_to_emoji = {'X':'❌', 'O':'⭕', ' ':' '}
cols = st.columns(BOARD_SIZE, gap="small")

# Render the game board buttons
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        with cols[j]:
            cell = st.session_state.board[i][j]
            btn_label = symbol_to_emoji[cell]

            # Create a button for each cell
            # Button is disabled if game is over, or if the cell is already occupied,
            # or if it's AI mode and currently the AI's turn.
            is_disabled = st.session_state.game_over or cell != ' '
            if st.session_state.game_mode == 'AI' and st.session_state.current_player_symbol == 'X':
                is_disabled = True

            if st.button(btn_label if btn_label else " ",
                         key=f"{i}-{j}",
                         use_container_width=True,
                         disabled=is_disabled):
                # This code runs ONLY when the button is clicked by the active player
                if not st.session_state.game_over and cell == ' ':
                    st.session_state.board[i][j] = st.session_state.current_player_symbol # Place current player's symbol
                    check_game_status() # Check if this move ended the game

                    if not st.session_state.game_over:
                        # Switch turns
                        if st.session_state.game_mode == 'AI':
                            st.session_state.current_player_symbol = 'X' # Switch to AI's turn
                        else: # Player vs. Player
                            st.session_state.current_player_symbol = 'X' if st.session_state.current_player_symbol == 'O' else 'O'
                    st.rerun() # Force a rerun to immediately show the move and update turn/trigger AI

# --- AI Move Trigger ---
# This block executes on every rerun. If it's AI's turn and game is not over, AI makes a move.
# This ensures AI's move happens in a separate rerun after player's move is displayed.
if st.session_state.game_mode == 'AI' and st.session_state.current_player_symbol == 'X' and not st.session_state.game_over:
    ai_move()

# Display winner message if game is over
if st.session_state.game_over:
    st.markdown(f'<div class="winner-msg">{st.session_state.winner}</div>', unsafe_allow_html=True)

# Restart button
if st.button("🔄 RESTART", key="restart-btn"):
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_player_symbol = 'O' # Player 1 starts again
    # Game mode remains as selected, no need to reset it
    st.rerun() # Force a rerun to reset the UI

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style='margin-top:19px;text-align:center;color:#fff6;font-family:monospace;font-size:17px;'>
✨ <em>Glow up and challenge the AI!</em> ✨
</div>
""", unsafe_allow_html=True)
