import discord
import random
from discord.ext import commands
from pybase64 import standard_b64decode as DECODE

# Constants for difficulty levels
LEVELS = {
    'easy': {'size': 5, 'bombs': 6},
    'medium': {'size': 7, 'bombs': 17},
    'hard': {'size': 10, 'bombs': 38},
    'impossible': {'size': 15, 'bombs': 110}
}

# Function to print the board as a string
def get_board_string(board, revealed, show_all_bombs=False):
    size = len(board)
    output = "    " + " ".join([str(i+1) for i in range(size)]) + "\n"  # Column numbers
    output += "   " + "---" * size + "\n"
    
    for row in range(size):
        line = [str(row+1)]
        for col in range(size):
            if revealed[row][col]:
                if board[row][col] == 'B':
                    line.append('B')
                else:
                    line.append(str(board[row][col]))
            else:
                if show_all_bombs and board[row][col] == 'B':
                    line.append('B')
                else:
                    line.append('□')
        output += f"{str(row+1).rjust(2)} | " + " ".join(line) + "\n"
    return output

# Function to generate the minesweeper board, avoiding the first selected cell
def generate_board(size, bombs, first_row, first_col):
    board = [[0 for _ in range(size)] for _ in range(size)]
    bomb_positions = set()
    
    while len(bomb_positions) < bombs:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        
        if (row, col) not in bomb_positions and (row, col) != (first_row, first_col):
            bomb_positions.add((row, col))
            board[row][col] = 'B'

            for i in range(max(0, row-1), min(size, row+2)):
                for j in range(max(0, col-1), min(size, col+2)):
                    if board[i][j] != 'B':
                        board[i][j] += 1
    return board

# Flood fill function to reveal all nearby safe cells (0's) and their neighbors
def flood_fill(board, revealed, row, col):
    size = len(board)
    if row < 0 or row >= size or col < 0 or col >= size or revealed[row][col]:
        return
    
    revealed[row][col] = True

    if board[row][col] == 0:
        for i in range(max(0, row-1), min(size, row+2)):
            for j in range(max(0, col-1), min(size, col+2)):
                if not revealed[i][j]:
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
        return "Game is already over."
    
    result = check_cell(game['board'], game['revealed'], row, col)
    
    if result == 'bomb':
        game['game_over'] = True
        return "Boom! You hit a bomb. Game over."
    elif check_win(game['board'], game['revealed']):
        game['win'] = True
        game['game_over'] = True
        return "Congratulations! You've cleared the minefield!"
    
    return None

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store games per user
user_games = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def start_game(ctx, first_row: int, first_col: int,  level: str):
    await ctx.send("asdfasfdasfdasfdasfd")
    if level not in LEVELS:
        await ctx.send("Invalid difficulty level. Please choose from: easy, medium, hard, impossible.")
        return
    
    game = initialize_game(level, first_row - 1, first_col - 1)  # Convert to 0-based
    user_games[ctx.author.id] = game

    board_str = get_board_string(game['board'], game['revealed'])
    await ctx.send(f"Game started! Here's the current board:\n{board_str}")

@bot.command(name="play")
async def play(ctx, row: int, col: int):
    game = user_games.get(ctx.author.id)
    if not game:
        await ctx.send("You haven't started a game yet. Use `!start` to begin a game.")
        return
    
    if game['game_over']:
        await ctx.send("The game is over. Start a new game using `!start`.")
        return
    
    result = play_turn(game, row - 1, col - 1)  # Convert to 0-based
    if result:
        await ctx.send(result)

    board_str = get_board_string(game['board'], game['revealed'], game['game_over'])
    await ctx.send(f"Here's the current board:\n{board_str}")

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual bot token from the Discord developer portal
TOKEN = str(DECODE(DECODE(
    b'VFZSSk5FMVVVVEpQVkVFeFRXcE5ORTVFUlRSTmFrazBUV2N1UjFaMFN6VkpMamhKUlZZNWFEaGhOWFJrVkdkSFpYbEpVMHA1VG5wT1VuQnVOMVpwYVhwSloyNTJlVVZ6')))[
        2:-1]
bot.run(TOKEN)
