# Constants for representing pieces on the Othello board

# Represents an empty square on the board
EMPTY = ' '

# Represents a black piece
BLACK = 'B'

# Represents a white piece
WHITE = 'W'

# It can be useful to have a list of all player pieces
PLAYERS = [BLACK, WHITE]

# Example of how these might be used (optional, for illustration)
if __name__ == '__main__':
    print(f"Empty square representation: '{EMPTY}'")
    print(f"Black piece representation: '{BLACK}'")
    print(f"White piece representation: '{WHITE}'")
    print(f"Player pieces: {PLAYERS}")

    # Simulating a board cell
    cell_1 = EMPTY
    cell_2 = BLACK
    cell_3 = WHITE

    print(f"Cell 1 is empty: {cell_1 == EMPTY}")
    print(f"Cell 2 is black: {cell_2 == BLACK}")
    print(f"Cell 3 is white: {cell_3 == WHITE}")
