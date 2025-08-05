import numpy as np

# Initialize the game board (3x3 grid)
def create_board():
    return np.full((3, 3), ' ')

# Print the board in terminal
def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
    print("\n")

# Check if there are any empty spaces
def is_moves_left(board):
    return ' ' in board

# Evaluate the board for Minimax
def evaluate(board):
    # Check rows
    for row in board:
        if np.all(row == 'X'):
            return 10
        elif np.all(row == 'O'):
            return -10

    # Check columns
    for col in range(3):
        if np.all(board[:, col] == 'X'):
            return 10
        elif np.all(board[:, col] == 'O'):
            return -10

    # Check diagonals
    if np.all(np.diag(board) == 'X') or np.all(np.diag(np.fliplr(board)) == 'X'):
        return 10
    elif np.all(np.diag(board) == 'O') or np.all(np.diag(np.fliplr(board)) == 'O'):
        return -10

    return 0

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)

    # If AI wins
    if score == 10:
        return score - depth
    # If human wins
    if score == -10:
        return score + depth
    # Draw
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[i][j] = ' '
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        return best
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[i][j] = ' '
                    beta = min(beta, best)
                    if beta <= alpha:
                        return best
        return best

# Find the best move for AI
def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                move_val = minimax(board, 0, False, -1000, 1000)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

# Main game loop
def play_game():
    board = create_board()
    print("Welcome to Tic-Tac-Toe AI (You are 'O', AI is 'X')")
    print_board(board)

    while True:
        # Human move
        while True:
            try:
                row, col = map(int, input("Enter your move (row and column: 0 1 2): ").split())
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    break
                else:
                    print("Cell already taken. Try again.")
            except:
                print("Invalid input. Enter row and column separated by space.")

        print_board(board)

        if evaluate(board) == -10:
            print("🎉 You win!")
            break
        if not is_moves_left(board):
            print("🤝 It's a draw!")
            break

        # AI move
        print("AI is thinking...")
        ai_move = find_best_move(board)
        board[ai_move] = 'X'
        print_board(board)

        if evaluate(board) == 10:
            print("🤖 AI wins!")
            break
        if not is_moves_left(board):
            print("🤝 It's a draw!")
            break

if __name__ == "__main__":
    play_game()
