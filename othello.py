import numpy as np
from copy import deepcopy
from sys import exit


class Game_Player:

    def __init__(self, name, color):
        self.name = name
        self.score = 2
        self.color = color

    def set_color(self, color):
        self.color = color

    def play(self, boardstate, valid_moves, current_score):
        playerInput = input(
            f"{self.color} Input row and column to place piece (e.g. \"0 0\"): ")
        splinput = playerInput.split()
        if (not splinput[0].isdigit()) or (not splinput[1].isdigit()):
            print('Invalid input.')
            return (-1, -1)
        else:
            row = int(splinput[0]) - 1
            column = int(splinput[1]) - 1
            return (row, column)


class Bot (Game_Player):

    def __init__(self, name, color):
        self.heatmap = [[5, 2, 4, 3, 3, 4, 2, 5],
                        [2, 1, 2, 2, 2, 2, 1, 2],
                        [4, 2, 3, 1, 1, 3, 2, 4],
                        [3, 2, 1, 1, 1,	1, 2, 3],
                        [3, 2, 1, 1, 1,	1, 2, 3],
                        [4, 2, 3, 1, 1, 3, 2, 4],
                        [2, 1, 2, 2, 2, 2, 1, 2],
                        [5, 2, 4, 3, 3, 4, 2, 5]]
        self.name = f"Bot {name}"
        self.score = 0
        self.color = color
        self.color_id = True if color == "White" else False

    def fitness_function(self, boardstate):
        points_to_board = boardstate * self.heatmap
        our_point = np.sum(np.where(boardstate == 1))
        their_point = np.sum(np.where(boardstate == -1))
        our_weight = np.sum(np.where(points_to_board > 0))
        their_weight = np.sum(np.where(points_to_board < 0))
        # This Needs To Be Fixed
        total_weight = np.sum(np.where(points_to_board > -100))  # This
        our_score = our_point * (our_weight / total_weight)
        their_score = their_point * (their_weight / total_weight)
        return (our_score, their_score)

    def convert_map(self, boardstate):
        array = np.array(boardstate)
        if self.color == "White":
            array[np.where(array == True)] = 1
            array[np.where(array == False)] = -1
        if self.color == "Black":
            array[np.where(array == True)] = -1
            array[np.where(array == False)] = 1

        array[np.where(array == None)] = np.nan
        return array

    def play(self, boardstate, valid_moves, current_score):
        ''' x, y = valid_moves[0]
         boardstate = self.convert_map(boardstate)
         moves = self.scan_valid_places(x, y, boardstate)'''

        # Use a modified max() function to determine the best move.
        bestscore = -np.inf
        bestmove = (-1, -1)
        for row, column in valid_moves:
            # Create new game state and place piece.
            state = Game(None, None, deepcopy(
                boardstate), deepcopy(current_score))
            state.place_piece(self.color_id, row, column)

            # Get the min score of opponent's possible moves.
            score = self.min(state.WHITE_BOARD, state.get_playable_spaces(
                not self.color_id), current_score, 0, 2, 0, 0)

            # Get max between our current max and this score.
            bestscore = max(bestscore, score)
            if bestscore == score:
                bestmove = (row, column)

        # Return coordinates of best move.
        return bestmove

    def min(self, boardstate, valid_moves, boardscore, depth, depth_limit, alpha, beta):
        # If no more valid moves, return the opponent's score.
        if len(valid_moves) == 0:
            return self.fitness_function(self.convert_map(boardstate))[1]

        bestmin = np.inf
        # Loop through all possible moves.
        for row, column in valid_moves:
            # Create new game state and place piece.
            state = Game(None, None, deepcopy(
                boardstate), deepcopy(boardscore))
            state.place_piece(not self.color_id, row, column)

            # If we are at the maximum depth, use opponent's score.
            if depth == depth_limit:
                score = self.fitness_function(
                    self.convert_map(state.WHITE_BOARD))[1]
            # Else, use the max score of our possible moves.
            else:
                score = self.max(state.WHITE_BOARD, state.get_playable_spaces(
                    self.color_id), state.SCORE, depth+1, depth_limit, alpha, bestmin)

            # Get min between our current min and this score.
            bestmin = min(bestmin, score)
            if beta <= alpha:
                break
        return bestmin

    def max(self, boardstate, valid_moves, boardscore, depth, depth_limit, alpha, beta):
        # If no more valid moves, return our score.
        if len(valid_moves) == 0:
            return self.fitness_function(self.convert_map(boardstate))[0]

        bestmax = -np.inf
        # Loop through all possible moves.
        for row, column in valid_moves:
            # Create new game state and place piece.
            state = Game(None, None, deepcopy(
                boardstate), deepcopy(boardscore))
            state.place_piece(self.color_id, row, column)

            # Get the min score of opponent's possible moves.
            score = self.min(state.WHITE_BOARD, state.get_playable_spaces(
                not self.color_id), state.SCORE, depth, depth_limit, bestmax, beta)

            # Get max between our current max and this score.
            bestmax = max(bestmax, score)
            if beta <= alpha:
                break
        return bestmax


class Player(Game_Player):
    def __init__(self, name, color):
        self.name = f"Player {name}"
        self.score = 0
        self.color = color


class Game:
    def __init__(self, PlayerA: Game_Player, PlayerB: Game_Player, board: list = [[]], score: dict = {}):
        # Board configurations.
        self.BOARD_SIZE = 8

        # Board is interpreted in terms of White pieces.
        self.WHITE_BOARD = board

        # Constant value configurations.
        self.WHITE = True
        self.BLACK = False

        # Player A is White, Player B is Black
        self.players = [PlayerA, PlayerB]

        # Track player scores.
        self.SCORE = score

        # Expresions to apply to board dimensions during scanning tasks.
        self.EXPRS = ["-1", "+0", "+1"]

    def print_board(self, playable_spaces: list = [], with_labels: bool = False):
        '''Prints the current board state. Set `with_labels` to `True` to print the row and column labels. '''

        # Board values:
        #    None: ' *'
        #    True: ' W'
        #   False: ' B'
        print(f'Black-{self.SCORE[self.BLACK]} White-{self.SCORE[self.WHITE]}')
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
        '''Clear/Set the board and place the initial pieces.'''

        # Clear the board / Set board dimensions.
        if len(self.WHITE_BOARD) == 1:
            self.WHITE_BOARD = [
                [None]*self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

        # Set scores to two, as two pieces of each color will start on the board.
        self.SCORE = {self.BLACK: 2, self.WHITE: 2}

        # Place initial pieces onto the board.
        center = int(self.BOARD_SIZE / 2)
        self.WHITE_BOARD[center-1][center-1] = True
        self.WHITE_BOARD[center-1][center] = False
        self.WHITE_BOARD[center][center-1] = False
        self.WHITE_BOARD[center][center] = True

    def get_piece(self, row: int, col: int):
        '''Returns piece value at a given row and column, or None if no piece exists.'''
        if ((row < 0 or row >= self.BOARD_SIZE) or (col < 0 or col >= self.BOARD_SIZE)):
            return None
        return self.WHITE_BOARD[row][col]

    def check_playable(self, color: bool, row: int, col: int, row_expr: str, col_expr: str, i: int = 0):
        '''Recursive function that checks if a piece can be played at a certain space on the board.'''

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
        '''Returns all possible moves for the given color.'''

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
                                if (row, col) not in playable_spaces:
                                    playable_spaces.append((row, col))
                                # We only need to find at least one playable path. Break to reduce calculations.
                                break
        return playable_spaces

    def flip_pieces(self, color: bool, row: int, col: int, row_expr: str, col_expr: str):
        '''Recursive function that checks if pieces following a direction can be flipped, flips them if so, and updates the scores.'''

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

    def place_piece(self, team, row, column):
        # Place piece and increase score by one.
        self.WHITE_BOARD[row][column] = team
        self.SCORE[team] += 1

        # Flip board pieces as necessary.
        for row_rule in self.EXPRS:
            for col_rule in self.EXPRS:
                self.flip_pieces(
                    team, row, column, row_rule, col_rule)

    def play(self):
        '''Othello game loop.'''

        turn_order = [self.BLACK, self.WHITE]
        move = 0
        skipped_turns = 0

        while True:

            # Next color turn.
            team = turn_order[move % 2]
            player = self.players[team]

            # Print Current Player
            print(f'{player.color}\'s Turn')

            # If two consecutive turns have been skipped, the game is over; there are no more valid moves.
            if skipped_turns == 2:
                print('No more valid moves. Game over!')
                print(
                    f'Black - {self.SCORE[self.BLACK]}    White - {self.SCORE[self.WHITE]}')
                return

            # Scan for possible plays this color can make.
            playable_spaces = self.get_playable_spaces(team)

            # If no spaces are available to play, skip their turn.
            if len(playable_spaces) == 0:
                print(f"{team}: Cannot place piece.")
                skipped_turns += 1
                move += 1
                continue

            # Print the board.
            self.print_board(playable_spaces, with_labels=True)

            # Get input.
            row = -1
            column = -1
            while (row, column) not in playable_spaces:
                row, column = player.play(
                    self.WHITE_BOARD, playable_spaces, self.SCORE)
                # Do not allow player to place in an invalid space.
                if (row, column) not in playable_spaces:
                    print('Cannot place there.')

            # Place piece perform piece flipping.
            self.place_piece(team, row, column)
            print(f"{player.color} plays at {(row + 1, column + 1)}.\n")

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

    Player_B = 1  # input("Player B: (1) Bot, (2) Person")
    if int(Player_B) == 1:
        Player_B = Bot("B", "Black")
    else:
        Player_B = Player("B", "Black")

    newGame = Game(Player_B, Player_A)
    newGame.set_starting_config()
    try:
        newGame.play()
    except KeyboardInterrupt:
        print("Quitting game...")
        exit(0)
