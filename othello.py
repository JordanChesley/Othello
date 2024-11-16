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
        self.score = 2
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

    def play(self, boardstate, valid_moves, current_score):

        # Use a modified max() function to determine the best move.
        bestscore = -np.inf
        bestmove = (-1, -1)
        for row, column in valid_moves:
            # Create new game state and place piece.
            state = Game(None, None, deepcopy(
                boardstate), deepcopy(current_score))
            state.flip_pieces(row, column)

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
            return self.fitness_function(self.convert_map_bin(boardstate))[1]

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
                    self.convert_map_bin(state.WHITE_BOARD))[1]
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
            return self.fitness_function(self.convert_map_bin(boardstate))[0]

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
        self.score = 2
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

    def scan_valid_place(self, x, y):
        boardstate = self.WHITE_BOARD
        # Make Sure Piece Is in The Board
        if ((x >= len(boardstate[0]) or x < 0)) or ((y >= len(boardstate[:, 0]) or y < 0)):
            return False

        # Make Sure Its A np.nan To Be Able To Place There
        if not (np.isnan(boardstate[x, y])):
            return False

        offset = y - x  # Calculate The Offset From The Main Diagonal
        # Get all spaces to the left of the x,y and invert the list
        left = boardstate[x, :y][::-1]
        # Get all the spaces to the right of the x,y
        right = boardstate[x, y+1:]
        # Get all the spaces above the origin and invert the list
        up = boardstate[:x, y][::-1]
        down = boardstate[x+1:, y]  # Get all the spaces below the x, y
        # Get the spaces to the ltr diag above x, y and invert the list
        left_diagonal_high = np.diagonal(
            boardstate, offset=offset)[:x][::-1]
        # Get the spaces to the ltr diag below x, y
        left_diagonal_low = np.diagonal(boardstate, offset=offset)[x+1:]
        right_diagonal_high = np.diagonal(
            np.fliplr(boardstate), offset=offset)[:x][::-1]
        right_diagonal_low = np.diagonal(
            np.fliplr(boardstate), offset=offset)[x+1:]
        # All Possible Paths From Origin In Every Direction
        possible_paths = [left_diagonal_low, left_diagonal_high,
                          right_diagonal_high, right_diagonal_low, left, right, up, down]
        # Scan each array from x,y. Check to make sure there is only -1 between x,y and the first 1.
        for dirs in possible_paths:
            if len(dirs) >= 2:
                index = np.where(dirs == 1)[0]
                if len(index) == 0:
                    continue
                if np.all(dirs[:index[0]] == -1):
                    return True
        return False

    def flip_pieces(self, x, y):
        boardstate = self.WHITE_BOARD
        # Make Sure Piece Is in The Board
        if ((x >= len(boardstate[0]) or x < 0)) or ((y >= len(boardstate[:, 0]) or y < 0)):
            return False

        # Make Sure Its A np.nan To Be Able To Place There
        if not (np.isnan(boardstate[x, y])):
            return False

        offset = y - x  # Calculate The Offset From The Main Diagonal
        # Get all spaces to the left of the x,y and invert the list
        left = boardstate[x, :y][::-1]
        # Get all the spaces to the right of the x,y
        right = boardstate[x, y+1:]
        # Get all the spaces above the origin and invert the list
        up = boardstate[:x, y][::-1]
        down = boardstate[x+1:, y]  # Get all the spaces below the x, y
        # Get the spaces to the ltr diag above x, y and invert the list
        left_diagonal_high = np.diagonal(boardstate, offset=offset)[:x][::-1]
        # Get the spaces to the ltr diag below x, y
        left_diagonal_low = np.diagonal(boardstate, offset=offset)[x+1:]
        right_diagonal_high = np.diagonal(
            np.fliplr(boardstate), offset=offset)[:x][::-1]
        right_diagonal_low = np.diagonal(
            np.fliplr(boardstate), offset=offset)[x+1:]
        # All Possible Paths From Origin In Every Direction
        possible_paths = [
            left, right, up, down, left_diagonal_low, left_diagonal_high, right_diagonal_high, right_diagonal_low]
        # Scan each array from x,y. Check to make sure there is only -1 between x,y and the first 1.
        for dirs in possible_paths:
            if len(dirs) >= 2:
                index = np.where(dirs == 1)[0]
                if len(index) == 0:
                    continue
                if np.all(dirs[:index[0]] == -1):
                    # dirs[:index[0]] = 1
                    pass

    def print_board(self, playable_spaces: list = [], with_labels: bool = False):
        '''Prints the current board state. Set `with_labels` to `True` to print the row and column labels. '''

        # Board values:
        #    None: ' *'
        #    True: ' W'
        #   False: ' B'
        print(f'Black-{self.SCORE[self.BLACK]} White-{self.SCORE[self.WHITE]}')
        if with_labels:
            print(' ', *range(0, self.BOARD_SIZE))
        for i in range(self.BOARD_SIZE):
            if with_labels:
                print(i, end='')
            for j in range(self.BOARD_SIZE):
                if (i, j) in playable_spaces:
                    printchar = ' o'
                else:
                    if np.isnan(self.WHITE_BOARD[i, j]):
                        printchar = ' *'
                if self.WHITE_BOARD[i, j] == 1:
                    printchar = ' W'
                if self.WHITE_BOARD[i, j] == -1:
                    printchar = ' B'
                print(printchar, end='')
            print('')
        print('')

    def set_starting_config(self):
        '''Clear/Set the board and place the initial pieces.'''

        # Clear the board / Set board dimensions.
        if len(self.WHITE_BOARD) == 1:
            self.WHITE_BOARD = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
        self.WHITE_BOARD[np.where(self.WHITE_BOARD == 0)] = np.nan
        # Set scores to two, as two pieces of each color will start on the board.
        self.SCORE = {self.BLACK: 2, self.WHITE: 2}

        # Place initial pieces onto the board.
        center = int(self.BOARD_SIZE / 2)
        self.WHITE_BOARD[center-1, center-1] = 1
        self.WHITE_BOARD[center-1, center] = -1
        self.WHITE_BOARD[center, center-1] = -1
        self.WHITE_BOARD[center, center] = 1

    def get_piece(self, row: int, col: int):
        '''Returns piece value at a given row and column, or None if no piece exists.'''
        if ((row < 0 or row >= self.BOARD_SIZE) or (col < 0 or col >= self.BOARD_SIZE)):
            return None
        return self.WHITE_BOARD[row][col]

    # Get Valid Playable Spaces
    def get_playable_spaces(self):
        playable_spaces = []
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.scan_valid_place(x, y):
                    playable_spaces.append((x, y))
        return playable_spaces

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

            # Get Playable Spaces
            playable_spaces = self.get_playable_spaces()

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
            self.flip_pieces(row, column)
            print(f"{player.color} plays at {(row + 1, column + 1)}.\n")

            # A successful turn has occurred. Reset skip counter.
            skipped_turns = 0

            # Next move.
            move += 1


# On Game Start User Picks A and B, They Then Game. If No Player is selected, the bots will play against each other.
if __name__ == "__main__":
    Player_A = input("Player A: (1) Bot, (2) Person")
    if int(Player_A) == 1:
        Player_A = Bot("A", "White")
    else:
        Player_A = Player("A", "White")

    Player_B = input("Player B: (1) Bot, (2) Person")
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
