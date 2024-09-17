# Board configurations.
BOARD_SIZE = 8

# Board is interpreted in terms of White pieces.
WHITE_BOARD = [[]]

# Constant value configurations.
WHITE = True
BLACK = False

SCORE = {}

EXPRS = ["-1", "+0", "+1"]

def print_board(with_labels: bool=False):
  '''Prints the current board state. Set `with_labels` to `True` to print the row and column labels. '''
  # Board values:
  #    None: ' *'
  #    True: ' W'
  #   False: ' B'
  print(f'Black - {SCORE[BLACK]}    White - {SCORE[WHITE]}')
  if with_labels: print(' ', *range(1, BOARD_SIZE + 1))
  for i in range(BOARD_SIZE):
    if with_labels: print(i+1, end='')
    for j in range(BOARD_SIZE):
      printchar = ' *' if WHITE_BOARD[i][j] == None else ' W' if WHITE_BOARD[i][j] else ' B'
      print(printchar, end='')
    print('')
  print('')

def set_starting_config():
  '''Clear/Set the board and place the initial pieces.'''
  global WHITE_BOARD
  global SCORE

  # Clear the board / Set board dimensions.
  WHITE_BOARD = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

  # Set scores to two.
  SCORE = {BLACK: 2, WHITE: 2}

  # Place initial pieces onto the board.
  center = int(BOARD_SIZE / 2)
  WHITE_BOARD[center-1][center-1] = True
  WHITE_BOARD[center-1][center] = False
  WHITE_BOARD[center][center-1] = False
  WHITE_BOARD[center][center] = True

def get_piece(row: int, col: int):
  if ((row < 0 or row >= BOARD_SIZE) or (col < 0 or col >= BOARD_SIZE)): return None
  return WHITE_BOARD[row][col]

def place_piece(color: bool, row: int, col: int):
  # Check if the piece can be placed at the given spot.
  if ((row < 0 or row >= BOARD_SIZE) or (col < 0 or col >= BOARD_SIZE)): return False
  if (WHITE_BOARD[row][col] != None): return False
  # If we can place, then place.
  WHITE_BOARD[row][col] = color
  return True

def flip_pieces(color: bool, row: int, col: int, row_expr, col_expr):
  piece = get_piece(row, col)
  # print(f'Checking {row+1} {col+1}: {piece}') ### DEBUG
  # If the piece is non-existent, we cannot flip. Return False.
  if piece == None: return False

  # If the piece is the same color, we've determined that our pieces are flippable,
  # and this one is already flipped. Return True.
  elif piece == color: return True

  # If piece is the other color, perform the expressions against our row and column integer. Continue to check if we can flip.
  elif piece != color:
    flippable = flip_pieces(color, eval(f"{row}{row_expr}"), eval(f"{col}{col_expr}"), row_expr, col_expr)

    # If flippable, flip the piece, and update the scores by one point.
    # If not flippable, do nothing.
    if (flippable):
      WHITE_BOARD[row][col] = not piece
      SCORE[color] += 1
      SCORE[not color] -= 1
      return True
    else:
      return False

  # We get here if the piece is the opposite color of the current playing color.

def play():
  turn_order = [BLACK, WHITE]
  move = 0

  while True:
    # Next color turn.
    team = turn_order[move % 2]

    # Print the board.
    print_board(with_labels=True)

    # Black == Player. Ask player where they want to move.
    if team == BLACK:
      player_input = input("BLACK: Input row and column to place piece (e.g. \"0 0\"): ")
      row, column = list(map(int, player_input.split()))
      row -= 1; column -= 1

    # White == AI. Ask AI for where it wants to move.
    else:
      ai_input = input("WHITE: Input row and column to place piece (e.g. \"0 0\"): ")
      row, column = list(map(int, ai_input.split()))
      row -= 1; column -= 1
    
    # Attempt to place a new piece.
    placed = place_piece(team, row, column)
    if not placed:
      print('Cannot place there.')
      continue
    # Increase score by one.
    SCORE[team] += 1

    # Flip board pieces as necessary.
    for row_rule in EXPRS:
      for col_rule in EXPRS:
        flip_pieces(team, eval(f'{row}{row_rule}'), eval(f"{column}{col_rule}"), row_rule, col_rule)

    # Next move.
    move += 1


# MAIN PROGRAM

set_starting_config()

play()