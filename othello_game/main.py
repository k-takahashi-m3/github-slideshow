from .game import OthelloGame
from .piece import BLACK, WHITE, EMPTY # EMPTY might not be directly used here but good for context

def main_game_loop():
    """
    Manages the main flow of an Othello game.
    """
    game = OthelloGame()
    print("Welcome to Othello!")

    while not game.is_game_over():
        # Display current state
        print("\n" + "="*20)
        # Need to access the display_board method via the Board object instance
        game.board_obj.display_board()
        scores = game.get_score()
        print(f"Scores: Black (B) - {scores[BLACK]}, White (W) - {scores[WHITE]}")

        player_name = "Black (B)" if game.current_player == BLACK else "White (W)"
        print(f"\n{player_name}'s turn.")

        # Get valid moves for the current player
        valid_moves = game.get_valid_moves(game.current_player)

        if not valid_moves:
            print(f"{player_name} has no valid moves. Turn skipped.")
            game.switch_player()
            # Check if the other player also has no moves (game might end)
            # This is implicitly handled by is_game_over() at the loop's start
            # but we could add an explicit check here if desired for an early exit message.
            # For example:
            # if not game.get_valid_moves(game.current_player):
            #    print("Neither player has moves. Game might be over.")
            #    # is_game_over() will confirm this in the next iteration
            continue

        # Display valid moves
        print("Valid moves are:")
        for i, move in enumerate(valid_moves):
            # Convert 0-indexed (row, col) to 1-indexed (row+1, chr(ord('a')+col)) for display
            print(f"  {i+1}: ({move[0]+1}, {chr(ord('a')+move[1])})  ", end="")
            if (i+1) % 4 == 0: # Print 4 moves per line
                 print()
        if (i+1) % 4 != 0: # Ensure a newline if the last line wasn't full
            print()


        # Get player input
        chosen_move = None
        while True:
            try:
                # Ask for numerical index first for simplicity
                move_input_idx_str = input(f"{player_name}, enter the number of your chosen move (e.g., 1): ")
                move_idx = int(move_input_idx_str) -1 # 1-indexed to 0-indexed

                if 0 <= move_idx < len(valid_moves):
                    chosen_move = valid_moves[move_idx]
                    # Convert chosen_move (0-indexed) for display confirmation
                    display_row = chosen_move[0]+1
                    display_col_char = chr(ord('a')+chosen_move[1])
                    print(f"You chose: ({display_row}, {display_col_char})")
                    break
                else:
                    print(f"Invalid move number. Please choose a number between 1 and {len(valid_moves)}.")
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your chosen move.")
            except Exception as e: # Catch any other unexpected errors during input
                print(f"An unexpected error occurred: {e}. Please try again.")

        # Make the move
        row, col = chosen_move
        game.make_move(row, col, game.current_player)

        # Switch player
        game.switch_player()

    # Game End
    print("\n" + "="*20)
    print("Game Over!")
    print("Final Board:")
    game.board_obj.display_board()
    final_scores = game.get_score()
    print(f"Final Scores: Black (B) - {final_scores[BLACK]}, White (W) - {final_scores[WHITE]}")

    winner = game.determine_winner()
    if winner == "Draw":
        print("The game is a Draw!")
    else:
        winner_name = "Black (B)" if winner == BLACK else "White (W)"
        print(f"Congratulations! {winner_name} wins!")

if __name__ == "__main__":
    main_game_loop()
