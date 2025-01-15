import math
import random
import copy
from concurrent.futures import ThreadPoolExecutor

BLACK = 1
WHITE = 2

class weareteamphysAI(object):
    def face(self):
        return "🎓nori"

    def __init__(self):
        self.corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
        self.danger_zones = [
            (0, 1), (1, 0), (1, 1),  # 左上
            (0, 4), (1, 4), (1, 5),  # 右上
            (4, 0), (4, 1), (5, 1),  # 左下
            (4, 4), (4, 5), (5, 4),  # 右下
        ]

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

    def evaluate_board(self, board, stone, phase):
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

    def mcts(self, board, stone, simulations=200):
        moves = self.get_valid_moves(board, stone)
        if not moves:
            return None

        def simulate_move(move):
            scores = 0
            for _ in range(simulations // len(moves)):
                simulated_board = self.apply_move(board, stone, move[0], move[1])
                current_stone = 3 - stone
                for _ in range(10):  # 最大10手のランダムプレイアウト
                    valid_moves = self.get_valid_moves(simulated_board, current_stone)
                    if not valid_moves:
                        break
                    random_move = random.choice(valid_moves)
                    simulated_board = self.apply_move(simulated_board, current_stone, random_move[0], random_move[1])
                    current_stone = 3 - current_stone
                scores += self.evaluate_board(simulated_board, stone, "mid")
            return scores

        with ThreadPoolExecutor() as executor:
            results = executor.map(simulate_move, moves)

        move_scores = {move: score for move, score in zip(moves, results)}
        best_move = max(move_scores, key=move_scores.get)
        return best_move

    def place(self, board, stone):
        total_stones = sum(row.count(0) for row in board)
        if total_stones > 40:
            phase = "early"
        elif total_stones > 20:
            phase = "mid"
        else:
            phase = "late"

        return self.mcts(board, stone, simulations=1000)
