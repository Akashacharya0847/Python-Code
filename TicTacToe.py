import random
from typing import List, Optional


class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'  # Player starts
        self.ai_player = 'O'
        self.player_stats = {'aggressive': 0, 'defensive': 0, 'center_bias': 0}
        self.game_stats = {'moves': 0, 'ai_wins': 0}

    def print_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]}")
            if i < 6: print("---------")

    def available_moves(self) -> List[int]:
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, position: int, player: str) -> bool:
        if self.board[position] == ' ':
            self.board[position] = player
            self.current_player = 'O' if player == 'X' else 'X'
            self.game_stats['moves'] += 1
            return True
        return False

    def check_winner(self) -> Optional[str]:
        # Rows, columns, diagonals
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return 'Draw' if ' ' not in self.board else None

    def update_player_stats(self, move: int):
        """AI learns player patterns"""
        center = 4
        corners = [0, 2, 6, 8]

        if move in corners:
            self.player_stats['aggressive'] += 1
        elif move == center:
            self.player_stats['center_bias'] += 1
        else:
            self.player_stats['defensive'] += 1

    def evaluate_board(self) -> int:
        """Scoring: +10 AI win, -10 Player win, 0 Draw"""
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10
        elif winner == 'X':
            return -10
        else:
            return 0

    def minimax(self, depth: int, is_maximizing: bool) -> int:
        """Core Minimax algorithm with alpha-beta pruning prep"""
        result = self.check_winner()
        if result == self.ai_player: return 10 - depth
        if result == 'X': return depth - 10
        if result == 'Draw': return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in self.available_moves():
                self.board[move] = self.ai_player
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.board[move] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def get_ai_move(self) -> int:
        """AI finds optimal move using Minimax"""
        best_score = float('-inf')
        best_move = None

        # Prioritize center and adapt to player style
        center = 4
        if self.board[center] == ' ':
            self.board[center] = self.ai_player
            score = self.minimax(0, False)
            self.board[center] = ' '
            if score > best_score:
                best_score = score
                best_move = center

        for move in self.available_moves():
            if move == best_move: continue

            self.board[move] = self.ai_player
            score = self.minimax(0, False)
            self.board[move] = ' '

            # Adapt to player patterns
            if self.player_stats['aggressive'] > self.player_stats['defensive']:
                score += 1  # Player aggressive, AI plays safer

            if score > best_score:
                best_score = score
                best_move = move

        return best_move


def play_game():
    game = TicTacToe()
    print("🤖 NEURAL TIC-TAC-TOE vs MINIMAX AI")
    print("Enter moves 0-8 (top-left=0, bottom-right=8)")
    print("AI adapts to your style! Good luck!\n")

    while True:
        game.print_board()

        # Player turn
        while True:
            try:
                move = int(input(f"\nYour move (0-8): "))
                if 0 <= move <= 8 and game.make_move(move, 'X'):
                    game.update_player_stats(move)
                    break
                print("Invalid move!")
            except ValueError:
                print("Enter a number 0-8!")

        result = game.check_winner()
        if result:
            game.print_board()
            if result == 'X':
                print("🎉 YOU WIN! (Extremely rare against Minimax)")
            elif result == self.ai_player:
                print("🤖 AI WINS! (Minimax is unbeatable)")
                game.game_stats['ai_wins'] += 1
            else:
                print("🤝 DRAW!")
            print(f"\nStats: Aggressive:{game.player_stats['aggressive']} "
                  f"Defensive:{game.player_stats['defensive']} "
                  f"AI Wins:{game.game_stats['ai_wins']}")
            break

        # AI turn
        ai_move = game.get_ai_move()
        print(f"\n🤖 AI plays: {ai_move}")
        game.make_move(ai_move, game.ai_player)

        if game.check_winner():
            game.print_board()
            print("🤖 AI WINS!")
            game.game_stats['ai_wins'] += 1
            print(f"\nStats: Aggressive:{game.player_stats['aggressive']} "
                  f"Defensive:{game.player_stats['defensive']} "
                  f"AI Wins:{game.game_stats['ai_wins']}")
            break


if __name__ == "__main__":
    play_game()
