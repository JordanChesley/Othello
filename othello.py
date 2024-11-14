

class Game_Player:

    def __init__(self, name, color):
        self.name = name
        self.score = 2
        self.color = color

    def set_color(self, color):
        self.color = color


class Bot (Game_Player):

    def __init__(self, name, color):
        self.heatmap = [[5, 2, 4, 3, 3, 4, 2, 5], [2, 1, 2, 2, 2, 2, 1, 2], [4, 2, 3, 1, 1, 3, 2, 4], [3, 2, 1, 1,	1,	1,	2,	3], [
            3, 2, 1,	1,	1,	1,	2,	3], [4, 2, 3, 1, 1, 3, 2, 4], [2, 1, 2, 2, 2, 2, 1, 2], [5, 2, 4, 3, 3, 4, 2, 5]]
        self.name = f"Bot {name}"
        self.score = 0
        self.color = color

    def transform_boardstate(self, boardstate):
        if self.color == "Black":
            boardstate[boardstate == 1] = 2
            boardstate[boardstate == 0] = 1
            boardstate[boardstate == -1] = 0
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
        self.WHITE_BOARD = [[None]*self.BOARD_SIZE] * self.BOARD_SIZE

        # Constant value configurations.
        self.WHITE = Player_A
        self.BLACK = Player_B
        self.players = [self.WHITE, self.BLACK]

        self.set_starting_config()
        self.play()

    def print_board(self):
        print(
            f'\nBlack {self.score[self.BLACK]}    White {self.score[self.WHITE]}')
        temp_board = self.WHITE_BOARD
        temp_board[temp_board == 0] = "W"
        temp_board[temp_board == 1] = "B"
        temp_board[temp_board == None] = "*"
        print(temp_board)

    def set_starting_config(self):

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

    # Recursive function that checks if a piece can be played at a certain space on the board.
    def check_playable(self, color: bool, row: int, col: int, onRun: bool = False):
        pass

    # Recursive Function That Checks All Valid Spaces For A Player To Possibly Move
    def get_playable_spaces(self, color):
        for rows in self.BOARD_SIZE:
            for cols in rows

    def flip_pieces(self, color: bool, row: int, col: int, row_expr: str, col_expr: str):
        pass

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
