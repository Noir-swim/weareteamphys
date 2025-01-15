import math
import random
import time

BLACK = 1
WHITE = 2

class weareteamphysAI:
    def __init__(self, total_game_time=60, max_depth=8):
        self.total_game_time = total_game_time  # ゲーム全体の最大思考時間 (秒)
        self.used_time = 0  # 現在までに使用した思考時間
        self.max_depth = max_depth  # 最大探索深さ
        self.corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
        self.danger_zones = [
            (0, 1), (1, 0), (1, 1),  # 左上
            (0, 4), (1, 4), (1, 5),  # 右上
            (4, 0), (4, 1), (5, 1),  # 左下
            (4, 4), (4, 5), (5, 4),  # 右下
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
                for flip_x, flip_y in stones_to_flip:
                    new_board[flip_y][flip_x] = stone
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

    def evaluate_board(self, board, stone):
        weights = [
            [1000, -200, 50, 50, -200, 1000],
            [-200, -500, 10, 10, -500, -200],
            [50, 10, 5, 5, 10, 50],
            [50, 10, 5, 5, 10, 50],
            [-200, -500, 10, 10, -500, -200],
            [1000, -200, 50, 50, -200, 1000],
        ]
        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += weights[y][x]
                elif board[y][x] == 3 - stone:
                    score -= weights[y][x]
        my_mobility = len(self.get_valid_moves(board, stone))
        opponent_mobility = len(self.get_valid_moves(board, 3 - stone))
        score += (my_mobility - opponent_mobility) * 15
        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player, stone):
        if depth == 0 or not self.get_valid_moves(board, stone):
            return self.evaluate_board(board, stone), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_valid_moves(board, stone):
                new_board = self.apply_move(board, stone, move[0], move[1])
                eval, _ = self.alpha_beta(new_board, depth - 1, alpha, beta, False, 3 - stone)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves(board, stone):
                new_board = self.apply_move(board, stone, move[0], move[1])
                eval, _ = self.alpha_beta(new_board, depth - 1, alpha, beta, True, 3 - stone)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def place(self, board, stone):
        start_time = time.time()
        depth = 4  # 初期深さ
        best_move = None
        while time.time() - start_time < self.total_game_time / 60:
            eval, move = self.alpha_beta(board, depth, float('-inf'), float('inf'), True, stone)
            if move:
                best_move = move
            depth += 1
        return best_move
