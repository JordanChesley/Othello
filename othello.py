class Game:

    def __init__(self, bot):
        # Board configurations.
        self.BOARD_SIZE = 8

        # Board is interpreted in terms of White pieces.
        self.WHITE_BOARD = [[]]

        # Constant value configurations.
        self.WHITE = True
        self.BLACK = False

        # Track player scores.
        self.SCORE = {}

        # Expresions to apply to board dimensions during scanning tasks.
        self.EXPRS = ["-1", "+0", "+1"]

        self.set_starting_config()
        self.play()

    def print_board(self, playable_spaces: list = [], with_labels: bool = False):
        # Prints the current board state. Set `with_labels` to `True` to print the row and column labels
        # Board values
        #    None: ' *'
        #    True: ' W'
        #   False: ' B'
        print(
            f'\nBlack - {self.SCORE[self.BLACK]}    White - {self.SCORE[self.WHITE]}')
        if with_labels:
            print(' ', *range(1, self.BOARD_SIZE + 1))
        for i in range(self.BOARD_SIZE):
            if with_labels:
                print(i+1, end='')
            for j in range(self.BOARD_SIZE):
                if (i, j) in playable_spaces:
                    printchar = ' o'
                else:
                    printchar = ' *' if self.WHITE_BOARD[i][j] == None else ' W' if self.WHITE_BOARD[i][j] else ' B'
                print(printchar, end='')
            print('')
        print('')

    def set_starting_config(self):
        # Clear/Set the board and place the initial pieces.

        # Clear the board / Set board dimensions.
        self.WHITE_BOARD = [[None for _ in range(self.BOARD_SIZE)]
                            for _ in range(self.BOARD_SIZE)]

        # Set scores to two, as two pieces of each color will start on the board.
        self.SCORE = {self.BLACK: 2, self.WHITE: 2}

        # Place initial pieces onto the board.
        center = int(self.BOARD_SIZE / 2)
        self.WHITE_BOARD[center-1][center-1] = True
        self.WHITE_BOARD[center-1][center] = False
        self.WHITE_BOARD[center][center-1] = False
        self.WHITE_BOARD[center][center] = True

    def get_piece(self, row: int, col: int):
        # Returns piece value at a given row and column, or None if no piece exists

        if ((row < 0 or row >= self.BOARD_SIZE) or (col < 0 or col >= self.BOARD_SIZE)):
            return None
        return self.WHITE_BOARD[row][col]

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
                if self.get_piece(row, col) == None:
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

        turn_order = [self.BLACK, self.WHITE]
        move = 0
        skipped_turns = 0

        while True:
            # If two consecutive turns have been skipped, the game is over; there are no more valid moves.
            if skipped_turns == 2:
                print('No more valid moves. Game over!')
                print(
                    f'Black - {SCORE[self.BLACK]}    White - {SCORE[self.WHITE]}')
                return

            # Next color turn.
            team = turn_order[move % 2]

            # Scan for possible plays this color can make.
            playable_spaces = self.get_playable_spaces(team)

            # If no spaces are available to play, skip their turn.
            if len(playable_spaces) == 0:
                print(f"{self.WHITE} if team else {self.BLACK}: Cannot place piece.")
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


class Bot:

    def __init__(self):
        self.heatmap = [[]]

    def process_boardstate(self, boardstate):
        pass

    def fitness_function(self, boardstate, heatmap):
        pass


if __name__ == "__main__":
    bot = Bot()
    newGame = Game(bot)
