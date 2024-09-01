import logging
from typing import List, Optional, Tuple
from threading import Lock
import random
import sys

logging.basicConfig(
    filename='tic_tac_toe.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class TicTacToeError(Exception):
    """Base class for Tic Tac Toe exceptions"""
    pass

class InvalidMoveError(TicTacToeError):
    """Exception raised for invalid moves"""
    def __init__(self, message: str = "Move is not valid"):
        super().__init__(message)

class TicTacToe:
    def __init__(self, play_with_npc: bool = False, difficulty: str = 'easy'):
        self.board: List[List[str]] = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player: str = "X"
        self.lock: Lock = Lock()
        self.play_with_npc = play_with_npc
        self.difficulty = difficulty.lower()
        self.player_symbol = "X"
        self.npc_symbol = "O"

    def draw_board(self) -> None:
        with self.lock:
            print("\nCurrent Board:")
            for row in self.board:
                print(" | ".join(row))
                print("-" * 9)
    
    def make_move(self, row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise InvalidMoveError("Row or column is out of bounds")
        with self.lock:
            if self.board[row][col] != " ":
                raise InvalidMoveError("Spot is already taken")
            self.board[row][col] = self.current_player
            return True

    def switch_player(self) -> None:
        self.current_player = self.npc_symbol if self.current_player == self.player_symbol else self.player_symbol

    def check_winner(self) -> Optional[str]:
        lines = (
            # Rows
            [self.board[i] for i in range(3)] +
            # Columns
            [[self.board[i][j] for i in range(3)] for j in range(3)] +
            # Diagonals
            [[self.board[i][i] for i in range(3)],
             [self.board[i][2 - i] for i in range(3)]]
        )
        for line in lines:
            if line.count(line[0]) == 3 and line[0] != " ":
                return line[0]
        return None

    def is_full(self) -> bool:
        return all(cell != " " for row in self.board for cell in row)

    def npc_move(self) -> Tuple[int, int]:
        if self.difficulty == 'easy':
            return self.random_move()
        elif self.difficulty == 'medium':
            return self.medium_move()
        elif self.difficulty == 'hard':
            return self.hard_move()
        else:
            # Default to easy if invalid difficulty is provided
            return self.random_move()

    def random_move(self) -> Tuple[int, int]:
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
        return random.choice(available_moves)

    def medium_move(self) -> Tuple[int, int]:
        # Check for winning move
        move = self.find_best_move(self.npc_symbol)
        if move:
            return move
        # Check for blocking move
        move = self.find_best_move(self.player_symbol)
        if move:
            return move
        # Take center if available
        if self.board[1][1] == " ":
            return (1, 1)
        # Take a random corner
        corners = [(0,0), (0,2), (2,0), (2,2)]
        available_corners = [corner for corner in corners if self.board[corner[0]][corner[1]] == " "]
        if available_corners:
            return random.choice(available_corners)
        # Take any side
        sides = [(0,1), (1,0), (1,2), (2,1)]
        available_sides = [side for side in sides if self.board[side[0]][side[1]] == " "]
        if available_sides:
            return random.choice(available_sides)
        # Fallback to random move
        return self.random_move()

    def find_best_move(self, symbol: str) -> Optional[Tuple[int, int]]:
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    self.board[row][col] = symbol
                    if self.check_winner() == symbol:
                        self.board[row][col] = " "
                        return (row, col)
                    self.board[row][col] = " "
        return None

    def hard_move(self) -> Tuple[int, int]:
        best_score = -sys.maxsize
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.npc_symbol
                    score = self.minimax(0, False, -sys.maxsize, sys.maxsize)
                    self.board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move

    def minimax(self, depth: int, is_maximizing: bool, alpha: int, beta: int) -> int:
        winner = self.check_winner()
        if winner == self.npc_symbol:
            return 10 - depth
        elif winner == self.player_symbol:
            return depth - 10
        elif self.is_full():
            return 0

        if is_maximizing:
            max_eval = -sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = self.npc_symbol
                        eval = self.minimax(depth + 1, False, alpha, beta)
                        self.board[row][col] = " "
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = self.player_symbol
                        eval = self.minimax(depth + 1, True, alpha, beta)
                        self.board[row][col] = " "
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def play_game(self) -> None:
        while True:
            try:
                self.draw_board()
                if self.play_with_npc and self.current_player == self.npc_symbol:
                    print(f"NPC ({self.difficulty.capitalize()} Difficulty) is making a move...")
                    row, col = self.npc_move()
                else:
                    move = input(f"Player {self.current_player}, enter your move as 'row col' (1-3 each): ")
                    row_col = move.strip().split()
                    if len(row_col) != 2:
                        raise ValueError("Please enter two numbers separated by a space.")
                    row, col = map(int, row_col)
                    row -= 1
                    col -= 1

                self.make_move(row, col)

                winner = self.check_winner()
                if winner:
                    self.draw_board()
                    if winner == self.player_symbol:
                        print("Congratulations! You win!")
                    elif winner == self.npc_symbol:
                        print("NPC wins! Better luck next time.")
                    else:
                        print(f"Player {winner} wins!")
                    break
                elif self.is_full():
                    self.draw_board()
                    print("It's a tie!")
                    break
                self.switch_player()
            except ValueError as ve:
                logging.warning(f"Invalid input: {ve}")
                print(f"Invalid input: {ve}")
            except InvalidMoveError as ime:
                logging.error(ime)
                print(ime)
            except Exception as e:
                logging.critical("An unexpected error occurred", exc_info=True)
                print("An unexpected error occurred. Please try again.")

if __name__ == '__main__':
    play_with_npc_input = input("Do you want to play against an NPC? (yes/no): ").strip().lower()
    play_with_npc = play_with_npc_input == 'yes'
    difficulty = 'easy'
    if play_with_npc:
        difficulty_input = input("Choose difficulty (easy, medium, hard): ").strip().lower()
        if difficulty_input in ['easy', 'medium', 'hard']:
            difficulty = difficulty_input
        else:
            print("Invalid difficulty selected. Defaulting to 'easy'.")
    game = TicTacToe(play_with_npc=play_with_npc, difficulty=difficulty)
    game.play_game()