import unittest
from othello_game.game import OthelloGame, _get_opponent
from othello_game.board import Board
from othello_game.piece import BLACK, WHITE, EMPTY

class TestOthelloLogic(unittest.TestCase):

    def test_board_initialization(self):
        """
        Test the initial setup of the Othello board.
        """
        board_obj = Board()
        board = board_obj.board # Get the 2D list

        # Check dimensions
        self.assertEqual(len(board), 8, "Board should have 8 rows")
        for row in board:
            self.assertEqual(len(row), 8, "Each row should have 8 columns")

        # Check initial pieces (0-indexed)
        # Standard Othello setup:
        #   (3,3) -> board[3][3] = WHITE
        #   (4,4) -> board[4][4] = WHITE
        #   (3,4) -> board[3][4] = BLACK
        #   (4,3) -> board[4][3] = BLACK
        self.assertEqual(board[3][3], WHITE, "Board[3][3] should be WHITE")
        self.assertEqual(board[4][4], WHITE, "Board[4][4] should be WHITE")
        self.assertEqual(board[3][4], BLACK, "Board[3][4] should be BLACK")
        self.assertEqual(board[4][3], BLACK, "Board[4][3] should be BLACK")

        # Check some other squares are EMPTY
        empty_count = 0
        for r in range(8):
            for c in range(8):
                if r in [3,4] and c in [3,4]: # Skip the center squares
                    continue
                self.assertEqual(board[r][c], EMPTY, f"Board[{r}][{c}] should be EMPTY")
                if board[r][c] == EMPTY:
                    empty_count +=1

        self.assertEqual(empty_count, 64 - 4, "There should be 60 empty squares initially")

    def test_initial_valid_moves(self):
        """
        Test that the initial valid moves for Black are correctly identified.
        """
        game = OthelloGame()
        # Black plays first by default
        self.assertEqual(game.current_player, BLACK)

        valid_moves = game.get_valid_moves(BLACK)

        # Standard initial valid moves for Black (0-indexed):
        # (2,3) -> flips (3,3)W
        # (3,2) -> flips (3,3)W
        # (4,5) -> flips (4,4)W
        # (5,4) -> flips (4,4)W
        expected_moves = [(2,3), (3,2), (4,5), (5,4)]

        self.assertEqual(len(valid_moves), 4, "Black should have 4 initial valid moves")
        for move in expected_moves:
            self.assertIn(move, valid_moves, f"Expected move {move} not found in valid moves: {valid_moves}")
        # Also ensure no unexpected moves
        for move in valid_moves:
            self.assertIn(move, expected_moves, f"Unexpected move {move} found in valid moves: {valid_moves}")

    def test_is_valid_move_and_flipping(self):
        """
        Test the is_valid_move logic and the subsequent flipping of pieces.
        """
        game = OthelloGame()
        # Clear the board and set up a custom scenario
        for r in range(8):
            for c in range(8):
                game.board[r][c] = EMPTY

        # Scenario: . . . . .
        #           . B W . .  // B at (1,1), W at (1,2) (0-indexed)
        #           . . . . .
        game.board[1][1] = BLACK
        game.board[1][2] = WHITE
        game.current_player = BLACK # Set current player to BLACK

        # Check if placing BLACK at (1,3) is valid
        # It should flip the WHITE piece at (1,2)
        pieces_to_flip = game.is_valid_move(1, 3, BLACK)
        self.assertIsNotNone(pieces_to_flip, "is_valid_move should not return None for a valid move")
        self.assertNotEqual(len(pieces_to_flip), 0, "is_valid_move should return a non-empty list for a valid move")
        self.assertIn((1,2), pieces_to_flip, "Piece at (1,2) should be marked for flipping")
        self.assertEqual(len(pieces_to_flip), 1, "Only one piece should be flipped")

        # Make the move
        move_successful = game.make_move(1, 3, BLACK)
        self.assertTrue(move_successful, "make_move should return True for a valid move")

        # Assertions after the move
        self.assertEqual(game.board[1][3], BLACK, "Piece at (1,3) should now be BLACK")
        self.assertEqual(game.board[1][2], BLACK, "Piece at (1,2) should have been flipped to BLACK")
        self.assertEqual(game.board[1][1], BLACK, "Piece at (1,1) should remain BLACK") # Sanity check

        # Test an invalid move in the same setup
        pieces_to_flip_invalid = game.is_valid_move(0, 0, BLACK) # No adjacent opponent
        self.assertEqual(len(pieces_to_flip_invalid), 0, "is_valid_move should return empty list for invalid move")


    def test_no_valid_moves_skip_turn(self):
        """
        Test the scenario where a player has no valid moves.
        """
        game = OthelloGame()
        # Setup:
        # B B B . .
        # B W . . .
        # B . . . .
        # . . . . .
        # If it's White's turn, White has no valid moves.
        game.board[0][0] = BLACK
        game.board[0][1] = BLACK
        game.board[0][2] = BLACK
        game.board[1][0] = BLACK
        game.board[1][1] = WHITE # White piece surrounded by Black
        game.board[2][0] = BLACK

        # Clear other pieces to ensure controlled environment for this test
        # Keep game.board[1][1] as WHITE, others around it BLACK as above
        # All other pieces EMPTY
        for r in range(8):
            for c in range(8):
                if not ((r==0 and c in [0,1,2]) or \
                        (r==1 and c==0) or \
                        (r==1 and c==1) or \
                        (r==2 and c==0) ):
                    if not (r==1 and c==1): # Don't overwrite W
                       game.board[r][c] = EMPTY

        game.board[0][0] = BLACK; game.board[0][1] = BLACK; game.board[0][2] = BLACK
        game.board[1][0] = BLACK; game.board[1][1] = WHITE; game.board[1][2] = EMPTY # Ensure this is empty
        game.board[2][0] = BLACK; game.board[2][1] = EMPTY; game.board[2][2] = EMPTY

        game.current_player = WHITE # Set current player to WHITE

        valid_moves_white = game.get_valid_moves(WHITE)
        self.assertEqual(len(valid_moves_white), 0, "White should have no valid moves in this scenario")

        # If we were in a game loop, we'd call switch_player()
        # Here, we just verify that get_valid_moves correctly reports no moves.

    def test_game_over_conditions(self):
        """
        Test the game over conditions: full board or no moves for either player.
        """
        # 1. Full Board
        game_full = OthelloGame()
        for r in range(8):
            for c in range(8):
                # Fill with alternating pieces, doesn't matter for 'full' check
                game_full.board[r][c] = BLACK if (r + c) % 2 == 0 else WHITE
        self.assertTrue(game_full.is_game_over(), "Game should be over when the board is full")

        # 2. No Moves for Either Player
        game_no_moves = OthelloGame()
        # Create a scenario where no moves are possible (e.g., checkerboard of one color)
        # This is a bit artificial but tests the logic
        for r in range(8):
            for c in range(8):
                game_no_moves.board[r][c] = BLACK # All black, no white pieces to flip

        # Make sure there are some empty squares, otherwise it's "full board" condition
        if game_no_moves.board[0][0] == BLACK: # Ensure at least one empty for this specific test
             game_no_moves.board[0][0] = EMPTY # So it's not full
             game_no_moves.board[0][1] = EMPTY # And another one

        # With only black pieces and some empty squares, neither black nor white can move.
        # (Black can't move because no opponent pieces to flip)
        # (White can't move because no opponent pieces to flip, and no own pieces to anchor)
        # To make this scenario more robust for White:
        game_no_moves.board[7][7] = WHITE # Add one white piece, but still no valid moves
                                          # if surrounding squares are black or out of bounds.
        # Example: B B B
        #          B W B
        #          B B B
        # White at (1,1) cannot move. Black cannot move if all other empty squares don't allow flips.
        # For simplicity, let's use the all-black board with one white piece and a few empty squares
        # where no flips are possible.

        # Re-setup for a clearer "no moves" scenario:
        for r in range(8):
            for c in range(8):
                game_no_moves.board[r][c] = EMPTY
        game_no_moves.board[0][0] = BLACK
        game_no_moves.board[0][1] = WHITE
        # B W . . . . . . (No moves for Black or White if rest is empty)
        # . . . . . . . .

        self.assertTrue(game_no_moves.is_game_over(),
                        "Game should be over if neither player has valid moves, even if board not full.")


    def test_determine_winner(self):
        """
        Test the logic for determining the winner based on piece counts.
        """
        game = OthelloGame()

        # Scenario 1: Black wins
        for r in range(8): # Clear board
            for c in range(8):
                game.board[r][c] = EMPTY
        game.board[0][0] = BLACK
        game.board[0][1] = BLACK
        game.board[0][2] = WHITE
        # Score: B=2, W=1
        self.assertEqual(game.determine_winner(), BLACK, "Black should be the winner")

        # Scenario 2: White wins
        for r in range(8): # Clear board
            for c in range(8):
                game.board[r][c] = EMPTY
        game.board[0][0] = WHITE
        game.board[0][1] = WHITE
        game.board[0][2] = BLACK
        # Score: W=2, B=1
        self.assertEqual(game.determine_winner(), WHITE, "White should be the winner")

        # Scenario 3: Draw
        for r in range(8): # Clear board
            for c in range(8):
                game.board[r][c] = EMPTY
        game.board[0][0] = BLACK
        game.board[0][1] = WHITE
        # Score: B=1, W=1
        self.assertEqual(game.determine_winner(), "Draw", "Game should be a Draw")

        # Scenario 4: Empty board (also a draw by current logic, score 0-0)
        for r in range(8): # Clear board
            for c in range(8):
                game.board[r][c] = EMPTY
        self.assertEqual(game.determine_winner(), "Draw", "Game should be a Draw on an empty board (0-0)")


if __name__ == '__main__':
    unittest.main()
