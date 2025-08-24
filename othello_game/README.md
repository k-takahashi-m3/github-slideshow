# Othello Game

This is a simple text-based Othello (Reversi) game implemented in Python.

## How to Play

1.  **Navigate to the game directory:**
    Open your terminal or command prompt.
    If you are in the root of the repository, type:
    ```bash
    cd othello_game
    ```

2.  **Run the game:**
    Execute the main game file using Python:
    ```bash
    python main.py
    ```

3.  **Gameplay:**
    *   The game is played on an 8x8 board.
    *   Players are 'B' (Black) and 'W' (White). Black plays first.
    *   The board starts with four pieces in the center:
        ```
          a b c d e f g h
        1 . . . . . . . .
        2 . . . . . . . .
        3 . . . W B . . .  <-- Note: Standard Othello is (3,3)W, (4,4)W, (3,4)B, (4,3)B
        4 . . . B W . . .  <-- This display should be corrected if using 0-indexed (3,3) for d4
        5 . . . . . . . .
        6 . . . . . . . .
        7 . . . . . . . .
        8 . . . . . . . .
        ```
    *   On your turn, the game will display a list of valid moves.
    *   Enter your chosen move by selecting the number corresponding to the move in the list (e.g., if "(2,3)" is the first option, type "1").
    *   A move is valid if you place your piece so that it flanks one or more of your opponent's pieces (forms a straight line - horizontal, vertical, or diagonal - with another of your pieces at the other end and opponent pieces in between).
    *   All flanked opponent pieces will be flipped to your color.
    *   If a player has no valid moves, their turn is skipped.
    *   The game ends when the board is full or neither player has a valid move.
    *   The player with the most pieces of their color on the board at the end wins.

## Files

*   `main.py`: The main script to run the game.
*   `game.py`: Contains the core game logic (OthelloGame class).
*   `board.py`: Handles the game board representation and display.
*   `piece.py`: Defines constants for game pieces.
*   `test_othello.py`: Unit tests for the game logic.
