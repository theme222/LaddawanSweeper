import random
from time import time

class Tile:
    emojis = [
        ":stop_button:",  # 0
        ":one:",
        ":two:",
        ":three:",
        ":four:",
        ":five:",
        ":six:",
        ":seven:",
        "<:warptsd:1286540878545948715>",  # 8
        "<:laddawan:1286535333546295409>",  # bomb 9
        ":blue_square:",  # not revealed 10
        ":triangular_flag_on_post:"  # flagged 11
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.revealed = False
        self.flagged = False

    def __repr__(self):
        return str(self.value)

    def get_emoji(self, show=False):
        if self.revealed or show:
            return Tile.emojis[self.value]
        elif self.flagged:
            return Tile.emojis[11]
        else:
            return Tile.emojis[10]


class Game:
    def __init__(self, x=0, y=0, bombs=0, status="NotStarted",winStreak=0):
        self.status = status  # NotStarted Playing Win Lose Uninitialized
        self.sizeX = x
        self.sizeY = y
        self.board = [[Tile(_, __) for _ in range(x)] for __ in range(y)]
        self.bombCount = bombs
        self.winStreak = winStreak
        self.startTime = int(time())

    # Function to generate the minesweeper board, avoiding the first selected cell
    def first_move(self, first_row, first_col):
        self.status = "Playing"
        bomb_positions = set()

        # Place bombs, avoiding the first selected cell
        while len(bomb_positions) < self.bombCount:
            row = random.randint(0, self.sizeX - 1)
            col = random.randint(0, self.sizeY - 1)

            if (row, col) not in bomb_positions and (row, col) != (first_row, first_col):
                bomb_positions.add((row, col))
                self.board[row][col].value = 9

                # Increment numbers around the bomb
                for i in range(max(0, row - 1), min(self.sizeY, row + 2)):
                    for j in range(max(0, col - 1), min(self.sizeX, col + 2)):
                        if self.board[i][j].value != 9:
                            self.board[i][j].value += 1

        self.flood_fill(first_row, first_col)

    # Flood fill function to reveal all nearby safe cells (0's) and their neighbors
    def flood_fill(self, row, col):
        if row < 0 or row >= self.sizeY or col < 0 or col >= self.sizeX or self.board[row][col].revealed or \
                self.board[row][col].flagged:
            return

        self.board[row][col].revealed = True

        # If the cell is 0, recursively reveal all its neighbors
        if self.board[row][col].value == 0:
            for i in range(max(0, row - 1), min(self.sizeY, row + 2)):
                for j in range(max(0, col - 1), min(self.sizeX, col + 2)):
                    if not self.board[i][j].revealed:  # Only flood fill if not already revealed
                        self.flood_fill(i, j)

    # Check for win condition
    def check_win(self):
        for row in self.board:
            for tile in row:
                if not (tile.revealed or tile.value == 9):
                    return
        self.win()

    # Function to check if the player hit a bomb or needs to reveal cells
    def check_cell(self, row, col):
        if self.board[row][col].value == 9:
            self.lose()
            return

        self.flood_fill(row, col)
        self.check_win()

    def flag(self, row, col):
        self.board[row][col].flagged = not self.board[row][col].flagged
        return

    def lose(self):
        self.status = "Lose"
        self.winStreak = 0
        return

    def win(self):
        self.status = "Win"
        self.winStreak += 1
        return

    def valid_move(self, row, col):
        return (0 <= col < self.sizeX) and (0 <= row < self.sizeY)
