import math
import time

BLACK = 1
WHITE = 2

class weareteamphysAI:
    def __init__(self, max_time_per_game=60):
        self.max_time_per_game = max_time_per_game
        self.max_time_per_turn = max_time_per_game / 36
        self.start_time = None
        self.time_used = 0
        self.corner_positions = [(0, 0), (0, 5), (5, 0), (5, 5)]
        self.central_positions = [(2, 2), (2, 3), (3, 2), (3, 3)]
        self.danger_zone = [
            (0, 1), (1, 0), (1, 1),
            (0, 4), (1, 5), (1, 4),
            (4, 0), (5, 1), (4, 1),
            (5, 4), (4, 5), (4, 4)
        ]

    def face(self):
        return "🎓nori"

    def apply_move(self, board, stone, x, y):
        new_board = [row[:] for row in board]
        new_board[y][x] = stone
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []
            while 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board) and new_board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            if stones_to_flip and 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board) and new_board[ny][nx] == stone:
                for fx, fy in stones_to_flip:
                    new_board[fy][fx] = stone
        return new_board

    def get_valid_moves(self, board, stone):
        valid_moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def can_place_x_y(self, board, stone, x, y):
        if board[y][x] != 0:
            return False
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                nx += dx
                ny += dy
                found_opponent = True
            if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                return True
        return False

    def evaluate_board(self, board, stone, move_count):
        """評価関数"""
        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    if (x, y) in self.central_positions:
                        score += 100  # 中央を最優先
                    elif (x, y) in self.corner_positions:
                        score += 50  # 角は次点
                    elif (x, y) in self.danger_zone:
                        score -= 30  # 危険地帯は減点
                    else:
                        score += 1

        # 序盤：中央を重視、中盤以降：外側への展開を評価
        if move_count < 20:
            score += sum(1 for x, y in self.central_positions if board[y][x] == stone) * 20
        else:
            score += sum(1 for x, y in self.corner_positions if board[y][x] == stone) * 10

        # 相手の選択肢を減らす
        opponent_moves = len(self.get_valid_moves(board, 3 - stone))
        score -= opponent_moves * 5  # 相手の手数を抑える

        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing, stone, move_count, start_time):
        legal_moves = self.get_valid_moves(board, stone)
        if depth == 0 or not legal_moves or time.time() - start_time > self.max_time_per_turn:
            return self.evaluate_board(board, stone, move_count), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                x, y = move
                simulated_board = self.apply_move(board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, depth - 1, alpha, beta, False, 3 - stone, move_count + 1, start_time)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                x, y = move
                simulated_board = self.apply_move(board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, depth - 1, alpha, beta, True, 3 - stone, move_count + 1, start_time)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def place(self, board, stone):
        self.start_time = time.time()
        remaining_time = self.max_time_per_game - self.time_used
        depth = 1
        best_move = None

        while time.time() - self.start_time < min(self.max_time_per_turn, remaining_time):
            eval, move = self.alpha_beta(board, depth, float('-inf'), float('inf'), True, stone, 0, self.start_time)
            if move:
                best_move = move
            depth += 1

        self.time_used += time.time() - self.start_time
        return best_move
