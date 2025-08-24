class Board:
    def __init__(self):
        # Initialize an 8x8 board with empty spaces
        self.board = [[' ' for _ in range(8)] for _ in range(8)]

        # Set the initial four pieces
        # White ('W') at (3,3) and (4,4)
        # Black ('B') at (3,4) and (4,3)
        # Board positions are 0-indexed, so (3,3) is board[3][3]
        self.board[3][3] = 'W'
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'

    def display_board(self):
        # Print column indicators (a-h)
        print("  a b c d e f g h")

        # Print rows with row indicators (1-8)
        for i in range(8):
            # Print row number (1-indexed)
            print(f"{i+1} ", end="")
            # Print each cell in the row
            for j in range(8):
                cell_content = self.board[i][j]
                # Use '.' for empty squares for display
                display_char = '.' if cell_content == ' ' else cell_content
                print(f"{display_char} ", end="")
            # Newline after each row
            print()

if __name__ == '__main__':
    # Example usage:
    game_board = Board()
    game_board.display_board()
    print("\nBoard initialized and displayed.")
