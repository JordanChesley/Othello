import numpy as np
import pandas as pd


class Game_Player:

    def __init__(self, name, color):
        self.heatmap = [[5, 2, 4, 3, 3, 4, 2, 5], [2, 1, 2, 2, 2, 2, 1, 2], [4, 2, 3, 1, 1, 3, 2, 4], [3, 2, 1,	1,	1,	1,	2,	3], [
            3, 2, 1,	1,	1,	1,	2,	3], [4, 2, 3, 1, 1, 3, 2, 4], [2, 1, 2, 2, 2, 2, 1, 2], [5, 2, 4, 3, 3, 4, 2, 5]]
        self.name = name
        self.score = 0
        self.color = color

    def set_color(self, color):
        self.color = color


class Bot (Game_Player):

    def __init__(self, name, color):
        self.heatmap = np.array([[5, 2, 4, 3, 3, 4, 2, 5], [2, 1, 2, 2, 2, 2, 1, 2], [4, 2, 3, 1, 1, 3, 2, 4], [3, 2, 1, 1,	1,	1,	2,	3], [
                                3, 2, 1,	1,	1,	1,	2,	3], [4, 2, 3, 1, 1, 3, 2, 4], [2, 1, 2, 2, 2, 2, 1, 2], [5, 2, 4, 3, 3, 4, 2, 5]])
        self.name = f"Bot {name}"
        self.score = 0
        self.color = color

    def transform_boardstate(self, boardstate):
        if self.color == "Black":
            boardstate[boardstate == 1] = 2
            boardstate[boardstate == 0] = 1
            boardstate[boardstate == 1] = 0
        return boardstate

    def fitness_function(self, boardstate):
        points_to_board = boardstate * self.heatmap

    def print_heatmap(self):
        print(self.heatmap)


class Player(Game_Player):
    def __init__(self, name, color):
        self.name = f"Player {name}"
        self.score = 0
        self.color = color


class Game:

    def __init__(self, Player_A: Game_Player, Player_B: Game_Player):
        # Board configurations.
        self.BOARD_SIZE = 8

        # Board is interpreted in terms of White pieces.
        self.WHITE_BOARD = np.full((8, 8), np.nan)

        # Constant value configurations.
        self.WHITE = 0
        self.BLACK = 1

        # Track player for turn order
        self.players = [Player_A, Player_B]

        # Scores Per Game Instance
        self.score = {2, 2}

        # Expressions to apply to board dimensions during scanning tasks.
        self.EXPRS = ["-1", "+0", "+1"]

        self.set_starting_config()
        self.play()

    def print_board(self):
        print(
            f'\nBlack {self.score[self.BLACK]}    White {self.score[self.WHITE]}')
        temp_board = self.WHITE_BOARD
        temp_board[temp_board == 0] = "W"
        temp_board[temp_board == 1] = "B"
        temp_board[temp_board == np.nan] = "*"
        print(temp_board)

    def set_starting_config(self):

        # Set scores to two, as two pieces of each color will start on the board.
        self.SCORE = {self.BLACK: 2, self.WHITE: 2}

        # Place initial pieces onto the board.
        center = int(self.BOARD_SIZE / 2)
        self.WHITE_BOARD[center-1, center-1] = 0
        self.WHITE_BOARD[center-1, center] = 1
        self.WHITE_BOARD[center, center-1] = 1
        self.WHITE_BOARD[center, center] = 0

    def get_piece(self, row: int, col: int):
        # Returns piece value at a given row and column, or None if no piece exists

        if ((row < 0 or row >= self.BOARD_SIZE) or (col < 0 or col >= self.BOARD_SIZE)):
            return None
        return self.WHITE_BOARD[row, col]

    def check_playable(self, color: bool, row: int, col: int, row_expr: str, col_expr: str, i: int = 0):
        # Recursive function that checks if a piece can be played at a certain space on the board.

        # Get adjacent piece in the specified direction.
        adj_row = eval(f"{row}{row_expr}")
        adj_col = eval(f"{col}{col_expr}")
        piece = self.get_piece(adj_row, adj_col)

        # If the piece is non-existent, we cannot place the piece. Return False.
        if piece == None:
            return False

        # During our first iteration, the immediate adjacent piece must be of the opposite color.
        if i == 0:
            if piece == color:
                return False
            elif piece != color:
                return self.check_playable(color, eval(f"{row}{row_expr}"), eval(f"{col}{col_expr}"), row_expr, col_expr, i+1)

        # For all other iterations:

        # If the piece is the same color, we have a valid placement.
        elif piece == color:
            return True

        # If piece is the other color, continue checking.
        elif piece != color:
            return self.check_playable(color, adj_row, adj_col, row_expr, col_expr, i+1)

    def get_playable_spaces(self, color):

        # Returns all possible moves for the given color
        playable_spaces = []
        # Iterate through our entire board.
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Pieces can only be placed on empty spaces.
                if np.isnan(self.get_piece(row, col)):
                    # In each direction from our point, check if the piece can be placed.
                    for row_expr in self.EXPRS:
                        for col_expr in self.EXPRS:
                            if (self.check_playable(color, row, col, row_expr, col_expr)):
                                playable_spaces.append((row, col))
                                # We only need to find at least one playable path. Break to reduce calculations.
                                break
        return playable_spaces

    def flip_pieces(self, color: bool, row: int, col: int, row_expr: str, col_expr: str):
        # Recursive function that checks if pieces following a direction can be flipped, flips them if so, and updates the scores.

        # Get adjacent piece.
        adj_row = eval(f"{row}{row_expr}")
        adj_col = eval(f"{col}{col_expr}")
        piece = self.get_piece(adj_row, adj_col)
        x = np.where(np.diff(self.WHITE_BOARD) != 0) [1,0,0,nan,0,0,0,1]

        # If the piece is non-existent, we cannot flip. Return False.
        if piece == None:
            return False

        # If the piece is the same color, we've determined that our pieces are flippable,
        # and this one is already flipped. Return True.
        elif piece == color:
            return True

        # If piece is the other color, perform the expressions against our row and column integer. Continue to check if we can flip.
        elif piece != color:
            flippable = self.flip_pieces(
                color, adj_row, adj_col, row_expr, col_expr)

            # If flippable, flip the piece, and update the scores by one point.
            # If not flippable, do nothing.
            if (flippable):
                self.WHITE_BOARD[adj_row][adj_col] = not piece
                self.SCORE[color] += 1
                self.SCORE[not color] -= 1
                return True
            else:
                return False

    # We get here if the piece is the opposite color of the current playing color.
    def play(self):

        # Othello Game Loop
        move = 0
        skipped_turns = 0

        while True:
            # If two consecutive turns have been skipped, the game is over; there are no more valid moves.
            if skipped_turns >= 2:
                print('No more valid moves. Game over!')
                print(
                    f'Black - {self.players[0].score}    White - {self.players[1].score}')
                return

            # Next color turn.
            team = self.players[move % 2]

            # Scan for possible plays this color can make.
            playable_spaces = self.get_playable_spaces(team.color)

            # If no spaces are available to play, skip their turn.
            if len(playable_spaces) == 0:
                print(
                    f"{self.players[0].color} if team else {self.players[1].color}: Cannot place piece.")
                skipped_turns += 1
                move += 1
                continue

            # Print the board.
            self.print_board(playable_spaces, with_labels=True)
            # Get input.
            row = -1
            column = -1
            while (row, column) not in playable_spaces:
                # Black == Player. Ask player where they want to move.
                if team == self.BLACK:
                    player_input = input(
                        "self.BLACK: Input row and column to place piece (e.g. \"0 0\"): ")
                    splinput = player_input.split()
                    if (not splinput[0].isdigit()) or (not splinput[1].isdigit()):
                        print('Invalid input.')
                        continue
                    row = int(splinput[0]) - 1
                    column = int(splinput[1]) - 1

                # White == AI. Ask AI for where it wants to move.
                else:
                    ai_input = input(
                        "self.WHITE: Input row and column to place piece (e.g. \"0 0\"): ")
                    splinput = ai_input.split()
                    if (not splinput[0].isdigit()) or (not splinput[1].isdigit()):
                        print('Invalid input.')
                        continue
                    row = int(splinput[0]) - 1
                    column = int(splinput[1]) - 1

                # Do not allow player to place in an invalid space.
                if (row, column) not in playable_spaces:
                    print('Cannot place there.')

            # Place piece and increase score by one.
            self.WHITE_BOARD[row][column] = team
            self.SCORE[team] += 1

            # Flip board pieces as necessary.
            for row_rule in self.EXPRS:
                for col_rule in self.EXPRS:
                    self.flip_pieces(team, row, column, row_rule, col_rule)

            # A successful turn has occurred. Reset skip counter.
            skipped_turns = 0

            # Next move.
            move += 1


# On Game Start User Picks A and B, They Then Game. If No Player is selected, the bots will play against each other.
if __name__ == "__main__":
    Player_A = 1  # input("Player A: (1) Bot, (2) Person")
    if int(Player_A) == 1:
        Player_A = Bot("A", "White")
    else:
        Player_A = Player("A", "White")

    Player_B = 1  # input("Player A: (1) Bot, (2) Person")
    if int(Player_B) == 1:
        Player_B = Bot("B", "Black")
    else:
        Player_B = Player("B", "Black")

    newGame = Game(Player_A, Player_B)
