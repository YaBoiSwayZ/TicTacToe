# Tic-Tac-Toe Game

This is a simple implementation of the classic Tic-Tac-Toe game in Python. The game can be played either between 2 players or against an NPC with varying levels of difficulty.

## Features

- Play in two-player mode or against an NPC.
- Three levels of difficulty when playing against the NPC: **Easy**, **Medium**, and **Hard**.
- Simple command-line interface.
- Error handling with informative logging.

## Installation

To run this script, you need to have Python installed on your machine. You can download Python from the official website: [Python.org](https://www.python.org/).

No additional libraries are required beyond Python's standard library.

## Usage

1. Clone the repository or download the script.
2. Navigate to the directory where the script is located.
3. Run the script using Python:

    ```
    python tic_tac_toe.py
    ```

4. Follow the prompts to either play against another player or against the NPC.

## Game Modes

### Two-Player Mode

- The game prompts both players alternately to enter their moves.
- Players input their move as two numbers separated by a space, representing the row and column on the 3x3 board (e.g., `1 1` for the top-left corner).

### NPC Mode

- You can choose to play against an NPC at one of three difficulty levels:
  - **Easy**: The NPC makes random moves.
  - **Medium**: The NPC tries to block your winning moves and makes strategic decisions.
  - **Hard**: The NPC uses the minimax algorithm to play optimally.

## Logging

- The game logs all significant events, including invalid inputs and errors, to a file named `tic_tac_toe.log`.
- This log can be useful for debugging or reviewing the game's events.

## Gameplay

```
Do you want to play against an NPC? (yes/no): yes
Choose difficulty (easy, medium, hard): medium

Current Board:
  |   |  
---------
  |   |  
---------
  |   |  

Player X, enter your move as 'row col' (1-3 each): 1 1

Current Board:
X |   |  
---------
  |   |  
---------
  |   |  

NPC (Medium Difficulty) is making a move...

Current Board:
X |   |  
---------
  | O |  
---------
  |   |  
```
