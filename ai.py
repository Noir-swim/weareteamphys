import math

BLACK = 1
WHITE = 2

# 6×6のオセロボードの初期状態
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
            found_opponent = True
            nx += dx
            ny += dy
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True
    return False

def can_place(board, stone):
    return any(can_place_x_y(board, stone, x, y) for y in range(len(board)) for x in range(len(board[0])))

def get_valid_moves(board, stone):
    return [(x, y) for y in range(len(board)) for x in range(len(board[0])) if can_place_x_y(board, stone, x, y)]

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

def count_stable_discs(board, stone):
    stable = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                stable_flag = True
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                        if board[ny][nx] != stone:
                            stable_flag = False
                            break
                        nx += dx
                        ny += dy
                    if not stable_flag:
                        break
                if stable_flag:
                    stable += 1
    return stable

class weareteamphysAI:
    def face(self):
        return "🎓nori"

    def get_progressive_evaluation(self, board):
        empty_count = sum(row.count(0) for row in board)
        total_cells = len(board) * len(board[0])

        if empty_count > total_cells * 0.6:  # 序盤
            return [
                [500, -20, 10, 10, -20, 500],
                [-20, -50, -2, -2, -50, -20],
                [10, -2, 1, 1, -2, 10],
                [10, -2, 1, 1, -2, 10],
                [-20, -50, -2, -2, -50, -20],
                [500, -20, 10, 10, -20, 500],
            ]
        elif empty_count > total_cells * 0.3:  # 中盤
            return [
                [250, -10, 10, 10, -10, 250],
                [-10, -20, 5, 5, -20, -10],
                [10, 5, 1, 1, 5, 10],
                [10, 5, 1, 1, 5, 10],
                [-10, -20, 5, 5, -20, -10],
                [250, -10, 10, 10, -10, 250],
            ]
        else:  # 終盤
            return [
                [500, 100, 100, 100, 100, 500],
                [100, 50, 50, 50, 50, 100],
                [100, 50, 10, 10, 50, 100],
                [100, 50, 10, 10, 50, 100],
                [100, 50, 50, 50, 50, 100],
                [500, 100, 100, 100, 100, 500],
            ]

    def evaluate_board(self, board):
        evaluation_table = self.get_progressive_evaluation(board)
        score = 0

        # 基本的な盤面スコア計算
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == BLACK:
                    score += evaluation_table[y][x]
                elif board[y][x] == WHITE:
                    score -= evaluation_table[y][x]

        # 有効手の数を加味
        black_moves = len(get_valid_moves(board, BLACK))
        white_moves = len(get_valid_moves(board, WHITE))
        mobility_score = (black_moves - white_moves) * 10
        score += mobility_score

        # 安定石の評価を追加
        stable_black = count_stable_discs(board, BLACK)
        stable_white = count_stable_discs(board, WHITE)
        stable_score = (stable_black - stable_white) * 20
        score += stable_score

        return score

    def minimax(self, board, depth, stone, maximizing_player, alpha=-math.inf, beta=math.inf):
        if depth == 0 or not can_place(board, stone):
            return self.evaluate_board(board), None

        valid_moves = get_valid_moves(board, stone)
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for x, y in valid_moves:
                temp_board = [row[:] for row in board]
                apply_move(temp_board, stone, x, y)
                eval, _ = self.minimax(temp_board, depth - 1, 3 - stone, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for x, y in valid_moves:
                temp_board = [row[:] for row in board]
                apply_move(temp_board, stone, x, y)
                eval, _ = self.minimax(temp_board, depth - 1, 3 - stone, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def place(self, board, stone):
        empty_count = sum(row.count(0) for row in board)
        depth = 3 if empty_count > 20 else 5
        _, move = self.minimax(board, depth, stone, True)
        return move
