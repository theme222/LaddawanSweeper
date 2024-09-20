import random

# Constants for difficulty levels
LEVELS = {
    'easy': {'size': 5, 'bombs': 3},
    'medium': {'size': 7, 'bombs': 17},
    'hard': {'size': 10, 'bombs': 38},
    'impossible': {'size': 15, 'bombs': 110}
}


# Utility function to print the board
def print_board(board, revealed, show_all_bombs=False):
    size = len(board)
    for row in range(size):
        line = []
        for col in range(size):
            if revealed[row][col]:
                if board[row][col] == 'B':
                    line.append('B')
                else:
                    line.append(str(board[row][col]))
            else:
                if show_all_bombs and board[row][col] == 'B':
                    line.append('B')  # Show all bombs when the game ends
                else:
                    line.append('□')  # Unrevealed cells are represented by a square
        print(" ".join(line))


# Function to generate the minesweeper board, avoiding the first selected cell
def generate_board(size, bombs, first_row, first_col):
    board = [[0 for _ in range(size)] for _ in range(size)]
    bomb_positions = set()

    # Place bombs, avoiding the first selected cell
    while len(bomb_positions) < bombs:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)

        if (row, col) not in bomb_positions and (row, col) != (first_row, first_col):
            bomb_positions.add((row, col))
            board[row][col] = 'B'

            # Increment numbers around the bomb
            for i in range(max(0, row - 1), min(size, row + 2)):
                for j in range(max(0, col - 1), min(size, col + 2)):
                    if board[i][j] != 'B':
                        board[i][j] += 1
    return board


# Flood fill function to reveal all nearby safe cells (0's) and their neighbors
def flood_fill(board, revealed, row, col):
    size = len(board)
    if row < 0 or row >= size or col < 0 or col >= size or revealed[row][col]:
        return

    revealed[row][col] = True

    # If the cell is 0, recursively reveal all its neighbors
    if board[row][col] == 0:
        for i in range(max(0, row - 1), min(size, row + 2)):
            for j in range(max(0, col - 1), min(size, col + 2)):
                if not revealed[i][j]:  # Only flood fill if not already revealed
                    flood_fill(board, revealed, i, j)


# Function to check if the player hit a bomb or needs to reveal cells
def check_cell(board, revealed, row, col):
    if board[row][col] == 'B':
        return 'bomb'
    elif board[row][col] == 0:
        flood_fill(board, revealed, row, col)
        return 'safe'
    else:
        revealed[row][col] = True
        return 'safe'


# Check for win condition
def check_win(board, revealed):
    size = len(board)
    return all(all(revealed[r][c] or board[r][c] == 'B' for c in range(size)) for r in range(size))


# Initialize the game
def initialize_game(level, first_row, first_col):
    size = LEVELS[level]['size']
    bombs = LEVELS[level]['bombs']

    board = generate_board(size, bombs, first_row, first_col)
    revealed = [[False for _ in range(size)] for _ in range(size)]

    # Reveal the first cell after generating the board
    check_cell(board, revealed, first_row, first_col)

    game = {
        'board': board,
        'revealed': revealed,
        'size': size,
        'game_over': False,
        'win': False
    }
    return game


# Play a single turn
def play_turn(game, row, col):
    if game['game_over']:
        print("Game is already over.")
        return game

    result = check_cell(game['board'], game['revealed'], row, col)

    if result == 'bomb':
        print("Boom! You hit a bomb. Game over.")
        game['game_over'] = True
        return game
    elif check_win(game['board'], game['revealed']):
        print("Congratulations! You've cleared the minefield!")
        game['win'] = True
        game['game_over'] = True

    return game


# Print the current board state
def print_game(game):
    if game['game_over']:
        # If game is over, show all bombs
        print_board(game['board'], game['revealed'], show_all_bombs=True)
        if game['win']:
            print("You won the game!")
        else:
            print("Game over! You lost.")
    else:
        print_board(game['board'], game['revealed'])


# Main function to set up and play the game
def main():
    print("Choose difficulty level: easy, medium, hard, impossible")
    level = input("Enter difficulty level: ").lower()

    if level not in LEVELS:
        print("Invalid level. Please choose from easy, medium, hard, impossible.")
        return

    # Get the first move from the player to initialize the game
    size = LEVELS[level]['size']
    while True:
        try:
            first_row, first_col = map(int, input(
                f"Enter row and column (0-{size - 1}) to start the game (format: row col): ").split())
            if not (0 <= first_row < size and 0 <= first_col < size):
                print(f"Invalid input. Please choose values between 0 and {size - 1}.")
                continue
            break
        except ValueError:
            print("Invalid input format. Please enter two numbers separated by space.")

    # Initialize the game
    game = initialize_game(level, first_row, first_col)
    print_game(game)

    # Play the game turn by turn
    while not game['game_over']:
        try:
            row, col = map(int, input(f"Enter row and column (0-{size - 1}) to uncover (format: row col): ").split())
            if not (0 <= row < size and 0 <= col < size):
                print(f"Invalid input. Please choose values between 0 and {size - 1}.")
                continue
        except ValueError:
            print("Invalid input format. Please enter two numbers separated by space.")
            continue

        # Play a single turn
        game = play_turn(game, row, col)
        print_game(game)


if __name__ == "__main__":
    main()
