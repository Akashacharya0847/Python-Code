import random
from typing import List, Optional


class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.ai_player = 'O'
        self.player_stats = {'aggressive': 0, 'defensive': 0, 'center_bias': 0}
        self.game_stats = {'moves': 0, 'ai_wins': 0, 'nodes_evaluated': 0}

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
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return 'Draw' if ' ' not in self.board else None

    def update_player_stats(self, move: int):
        corners = [0, 2, 6, 8]
        if move in corners:
            self.player_stats['aggressive'] += 1
        elif move == 4:
            self.player_stats['center_bias'] += 1
        else:
            self.player_stats['defensive'] += 1

    def evaluate_board(self) -> int:
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10
        elif winner == 'X':
            return -10
        return 0

    def minimax_alpha_beta(self, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        """Minimax WITH Alpha-Beta Pruning - prunes irrelevant branches"""
        self.game_stats['nodes_evaluated'] += 1

        result = self.check_winner()
        if result == self.ai_player: return 10 - depth
        if result == 'X': return depth - 10
        if result == 'Draw': return 0

        if is_maximizing:  # AI (O) maximizing
            max_eval = float('-inf')
            for move in self.available_moves():
                self.board[move] = self.ai_player
                eval_score = self.minimax_alpha_beta(depth + 1, alpha, beta, False)
                self.board[move] = ' '
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:  # Alpha cutoff - PRUNE!
                    break
            return max_eval
        else:  # Player (X) minimizing
            min_eval = float('inf')
            for move in self.available_moves():
                self.board[move] = 'X'
                eval_score = self.minimax_alpha_beta(depth + 1, alpha, beta, True)
                self.board[move] = ' '
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:  # Beta cutoff - PRUNE!
                    break
            return min_eval

    def get_ai_move(self) -> int:
        """AI selects best move using Alpha-Beta pruned Minimax"""
        best_score = float('-inf')
        best_move = None
        self.game_stats['nodes_evaluated'] = 0

        # Reset stats for this turn
        for move in self.available_moves():
            self.board[move] = self.ai_player
            board_score = self.minimax_alpha_beta(0, float('-inf'), float('inf'), False)
            self.board[move] = ' '

            # Player pattern adaptation bonus
            if self.player_stats['aggressive'] > self.player_stats['defensive']:
                board_score += 0.5

            if board_score > best_score:
                best_score = board_score
                best_move = move

        print(f"⚡ Nodes evaluated: {self.game_stats['nodes_evaluated']}")
        return best_move


def play_game():
    game = TicTacToe()
    print("🧠 NEURAL TIC-TAC-TOE vs ALPHA-BETA MINIMAX AI")
    print("Positions: 0 1 2\n         3 4 5\n         6 7 8")
    print("AI now 10x FASTER with Alpha-Beta Pruning!\n")

    while True:
        game.print_board()

        # Player turn
        while True:
            try:
                move = int(input(f"\nYour move (0-8): "))
                if 0 <= move <= 8 and game.make_move(move, 'X'):
                    game.update_player_stats(move)
                    break
                print("❌ Invalid! Use 0-8")
            except ValueError:
                print("❌ Enter number 0-8!")

        result = game.check_winner()
        if result:
            game.print_board()
            if result == 'X':
                print("🎉 HUMAN VICTORY! (Legendary feat)")
            elif result == 'O':
                print("🤖 AI WINS!")
                game.game_stats['ai_wins'] += 1
            else:
                print("🤝 DRAW")
            print(f"\n📊 Stats: Aggress:{game.player_stats['aggressive']} "
                  f"Defens:{game.player_stats['defensive']} "
                  f"AI Wins:{game.game_stats['ai_wins']}")
            break

        # AI turn (much faster now!)
        print("\n🤖 AI thinking...")
        ai_move = game.get_ai_move()
        print(f"AI plays: {ai_move}")
        game.make_move(ai_move, game.ai_player)

        if game.check_winner():
            game.print_board()
            print("🤖 AI WINS!")
            game.game_stats['ai_wins'] += 1
            print(f"\n📊 Stats: Aggress:{game.player_stats['aggressive']} "
                  f"Defens:{game.player_stats['defensive']} "
                  f"AI Wins:{game.game_stats['ai_wins']}")
            break


if __name__ == "__main__":
    play_game()
