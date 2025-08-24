from .board import Board
from .piece import BLACK, WHITE, EMPTY

def _get_opponent(player):
    """Given a player, returns the opponent's color."""
    return WHITE if player == BLACK else BLACK

class OthelloGame:
    def __init__(self):
        """
        Initializes the game with a new board and sets the starting player.
        Black typically starts in Othello.
        """
        self.board_obj = Board()  # Renamed to avoid conflict with 'board' property
        self.current_player = BLACK

    @property
    def board(self):
        """Allows direct access to the board's 2D list representation."""
        return self.board_obj.board

    def is_valid_move(self, row, col, player):
        """
        Checks if placing a 'player' piece at (row, col) is a valid move.
        A move is valid if:
            - The square (row, col) is empty.
            - Placing a piece at (row, col) flanks at least one opponent piece.
        Returns:
            A list of (r, c) tuples of opponent pieces that would be flipped.
            Returns an empty list if the move is invalid.
        """
        if not (0 <= row < 8 and 0 <= col < 8 and self.board[row][col] == EMPTY):
            return [] # Square is not on board or not empty

        opponent = _get_opponent(player)
        pieces_to_flip = []

        # Directions to check (horizontal, vertical, diagonals)
        # (dr, dc) -> change in row, change in column
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Up-Left, Up, Up-Right
            (0, -1),           (0, 1),   # Left, Right
            (1, -1), (1, 0), (1, 1)    # Down-Left, Down, Down-Right
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            current_line_flips = []

            # Check if the adjacent square in this direction has an opponent's piece
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                current_line_flips.append((r, c))
                # Continue in this direction
                r, c = r + dr, c + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == player:
                        # Found a bracketing piece of the current player
                        pieces_to_flip.extend(current_line_flips)
                        break  # End of this direction
                    elif self.board[r][c] == opponent:
                        current_line_flips.append((r, c))
                    else: # self.board[r][c] == EMPTY
                        break # Empty square, no bracket
                    r, c = r + dr, c + dc
            # If loop finishes without finding player's piece, current_line_flips are not added

        return pieces_to_flip

    def make_move(self, row, col, player):
        """
        Places the player's piece on the board and flips opponent's pieces.
        Assumes is_valid_move has been checked or implicitly relies on it
        returning the pieces to flip.
        Returns True if the move was made, False otherwise (though current
        implementation assumes valid pieces_to_flip are passed or calculated).
        """
        pieces_to_flip = self.is_valid_move(row, col, player)
        if not pieces_to_flip:
            # Or raise an error: raise ValueError("Invalid move")
            return False

        self.board[row][col] = player
        for r_flip, c_flip in pieces_to_flip:
            self.board[r_flip][c_flip] = player
        return True

    def get_valid_moves(self, player):
        """
        Returns a list of (row, col) tuples representing all valid moves for the player.
        """
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == EMPTY:
                    if self.is_valid_move(r, c, player): # Checks if pieces_to_flip is non-empty
                        valid_moves.append((r, c))
        return valid_moves

    def switch_player(self):
        """Changes self.current_player from BLACK to WHITE or vice-versa."""
        self.current_player = _get_opponent(self.current_player)

    def is_game_over(self):
        """
        Checks if the game has ended. The game ends if:
            - The board is full.
            - Neither player has any valid moves.
        """
        # Check if board is full
        has_empty_square = False
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == EMPTY:
                    has_empty_square = True
                    break
            if has_empty_square:
                break

        if not has_empty_square:
            return True # Board is full

        # Check if either player has valid moves
        if not self.get_valid_moves(BLACK) and not self.get_valid_moves(WHITE):
            return True # No player has valid moves

        return False

    def get_score(self):
        """
        Counts the number of BLACK pieces and WHITE pieces on the board.
        Returns a dictionary: {BLACK: count_black, WHITE: count_white}.
        """
        score = {BLACK: 0, WHITE: 0, EMPTY: 0}
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece in score:
                    score[piece] += 1
        # We only care about player scores, not EMPTY, but counting it helps verify board state
        return {BLACK: score[BLACK], WHITE: score[WHITE]}


    def determine_winner(self):
        """
        Determines the winner based on the current score.
        Returns BLACK, WHITE, or "Draw".
        Should generally be called once the game is over.
        """
        score = self.get_score()
        if score[BLACK] > score[WHITE]:
            return BLACK
        elif score[WHITE] > score[BLACK]:
            return WHITE
        else:
            return "Draw" # Or None, as per original suggestion

if __name__ == '__main__':
    # Example Usage (basic test)
    game = OthelloGame()
    print("Initial board state:")
    game.board_obj.display_board() # Using the display method from Board class
    print(f"Current player: {game.current_player}")

    # Test valid moves for BLACK
    print(f"Valid moves for BLACK: {game.get_valid_moves(BLACK)}")

    # Make a move (example: Black plays at (2,3) if valid)
    # Valid moves for BLACK (initial board) are typically:
    # (2,3), (3,2), (4,5), (5,4)
    # Let's try one:
    move_made = False
    if game.get_valid_moves(BLACK):
        # Example: Black plays at (2,3)
        # For standard Othello, with W at (3,3)(4,4) and B at (3,4)(4,3):
        # A black piece at (2,3) would flip (3,3) (W)
        # A black piece at (3,2) would flip (3,3) (W)
        # A black piece at (4,5) would flip (4,4) (W)
        # A black piece at (5,4) would flip (4,4) (W)

        # Let's try (2,3) for Black
        # Board:
        #   a b c d e f g h
        # 1 . . . . . . . .
        # 2 . . . B . . . .  <- Black places here
        # 3 . . . W . . . .  <- This W should flip to B
        # 4 . . . B W . . .
        # 5 . . . W B . . .
        # 6 . . . . . . . .
        # 7 . . . . . . . .
        # 8 . . . . . . . .

        print("\nMaking move for BLACK at (2,3)...")
        if game.make_move(2, 3, BLACK): # (row 2, col 3)
            move_made = True
            print("Move successful.")
            game.board_obj.display_board()
            print(f"Score: {game.get_score()}")
        else:
            print("Move (2,3) for BLACK failed or was invalid.")
            # This case should ideally not be hit if get_valid_moves is checked first
    else:
        print("BLACK has no valid moves at the start (unexpected).")


    if move_made:
        game.switch_player()
        print(f"\nCurrent player: {game.current_player}")

        # Test valid moves for WHITE
        # After Black plays at (2,3) and flips (3,3) to B:
        # Board:
        #   a b c d e f g h
        # 1 . . . . . . . .
        # 2 . . . B . . . .
        # 3 . . . B . . . .  <- Was W, now B
        # 4 . . . B W . . .
        # 5 . . . W B . . .
        # 6 . . . . . . . .
        # 7 . . . . . . . .
        # 8 . . . . . . . .
        # Valid moves for WHITE could be e.g. (2,2) to flip (2,3)B, (2,4) to flip (3,4)B, (4,2) to flip (4,3)B
        print(f"Valid moves for WHITE: {game.get_valid_moves(WHITE)}")
        if game.get_valid_moves(WHITE):
             # Example: White plays at (2,4)
             # This would flip the black piece at (3,4)
            print("\nMaking move for WHITE at (2,4)...")
            if game.make_move(2, 4, WHITE):
                print("Move successful.")
                game.board_obj.display_board()
                print(f"Score: {game.get_score()}")
            else:
                print("Move (2,4) for WHITE failed or was invalid.")
        else:
            print("WHITE has no valid moves (unexpected).")

    # Test game over (not likely at this stage)
    print(f"\nIs game over? {game.is_game_over()}")
    if game.is_game_over():
        print(f"Winner: {game.determine_winner()}")

    print("\nBasic game logic tests completed.")
