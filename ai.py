import math

BLACK = 1
WHITE = 2

class weareteamphysAI:
    def face(self):
        return "🎓nori"

    def apply_move(self, board, stone, x, y):
        new_board = [row[:] for row in board]
        new_board[y][x] = stone
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]

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
        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    moves.append((x, y))
        return moves

    def can_place_x_y(self, board, stone, x, y):
        if board[y][x] != 0:
            return False
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]

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
            [100, -20, 10, 10, -20, 100],
            [-20, -50, -2, -2, -50, -20],
            [10, -2, 1, 1, -2, 10],
            [10, -2, 1, 1, -2, 10],
            [-20, -50, -2, -2, -50, -20],
            [100, -20, 10, 10, -20, 100],
        ]

        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += weights[y][x]
                elif board[y][x] == 3 - stone:
                    score -= weights[y][x]
        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing, stone):
        legal_moves = self.get_valid_moves(board, stone)
        if depth == 0 or not legal_moves:
            return self.evaluate_board(board, stone), None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = self.apply_move(board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, depth - 1, alpha, beta, False, 3 - stone)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = self.apply_move(board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, depth - 1, alpha, beta, True, 3 - stone)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def place(self, board, stone):
        valid_moves = self.get_valid_moves(board, stone)
        if not valid_moves:
            return None

        best_move = None
        best_score = -math.inf

        for x, y in valid_moves:
            temp_board = self.apply_move(board, stone, x, y)
            score, _ = self.alpha_beta(temp_board, depth=3, alpha=-math.inf, beta=math.inf, maximizing=False, stone=3 - stone)

            if score > best_score:
                best_score = score
                best_move = (x, y)

        return best_move
