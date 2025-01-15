import math
import time
from concurrent.futures import ThreadPoolExecutor

BLACK = 1
WHITE = 2

class weareteamphysAI:
    def __init__(self, max_time=10):
        self.max_time = max_time  # 1手あたりの最大思考時間（秒）
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
        """石を置いた後の盤面を返す"""
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
        """合法手をリストで返す"""
        valid_moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def can_place_x_y(self, board, stone, x, y):
        """指定の位置に石を置けるか確認"""
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
        """評価関数"""
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
        score += (my_mobility - opponent_mobility) * 10
        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing, stone):
        """α-β枝刈りによる探索"""
        legal_moves = self.get_valid_moves(board, stone)
        if depth == 0 or not legal_moves:
            return self.evaluate_board(board, stone), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                x, y = move
                new_board = self.apply_move(board, stone, x, y)
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
            for move in legal_moves:
                x, y = move
                new_board = self.apply_move(board, stone, x, y)
                eval, _ = self.alpha_beta(new_board, depth - 1, alpha, beta, True, 3 - stone)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def place(self, board, stone):
        """最適な手を探索"""
        start_time = time.time()
        depth = 4
        best_move = None
        while time.time() - start_time < self.max_time:
            eval, move = self.alpha_beta(board, depth, float('-inf'), float('inf'), True, stone)
            if move:
                best_move = move
            depth += 1
        return best_move
