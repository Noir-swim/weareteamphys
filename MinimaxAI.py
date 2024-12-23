import math
import random

BLACK = 1
WHITE = 2

# 6x6のオセロボード（初期配置）
board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
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

def can_place(board, stone):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def get_valid_moves(board, stone):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def apply_move(board, stone, x, y):
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    board[y][x] = stone

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        tiles_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            tiles_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for flip_x, flip_y in tiles_to_flip:
                board[flip_y][flip_x] = stone

class MinimaxAI(object):

    def face(self):
        return "🤖"  # 顔を「🤖」に変更

    def evaluate_board(self, board):
        """
        現在のボード状態を評価する。
        """
        evaluation_table = [
            [100, -20, 10, 10, -20, 100],
            [-20, -50, -2, -2, -50, -20],
            [ 10,  -2,  1,  1,  -2,  10],
            [ 10,  -2,  1,  1,  -2,  10],
            [-20, -50, -2, -2, -50, -20],
            [100, -20, 10, 10, -20, 100],
        ]
        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == BLACK:
                    score += evaluation_table[y][x]
                elif board[y][x] == WHITE:
                    score -= evaluation_table[y][x]
        return score

    def minimax(self, board, depth, stone, maximizing_player):
        if depth == 0 or not can_place(board, stone):
            return self.evaluate_board(board), None, None

        valid_moves = get_valid_moves(board, stone)
        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for x, y in valid_moves:
                temp_board = [row[:] for row in board]
                apply_move(temp_board, stone, x, y)
                eval, _, _ = self.minimax(temp_board, depth - 1, 3 - stone, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
            return max_eval, best_move[0], best_move[1]
        else:
            min_eval = float('inf')
            for x, y in valid_moves:
                temp_board = [row[:] for row in board]
                apply_move(temp_board, stone, x, y)
                eval, _, _ = self.minimax(temp_board, depth - 1, 3 - stone, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
            return min_eval, best_move[0], best_move[1]

    def place(self, board, stone):
        _, x, y = self.minimax(board, 3, stone, True)
        return x, y
