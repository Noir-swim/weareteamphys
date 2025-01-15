import math

BLACK = 1
WHITE = 2

class weareteamphysAI:
    def face(self):
        return "🎓nori"

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

    def get_legal_moves(self, board, stone):
        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    moves.append((x, y))
        return moves

    def simulate_place(self, board, stone, x, y):
        new_board = [row[:] for row in board]
        new_board[y][x] = stone
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy

            if stones_to_flip and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == stone:
                for fx, fy in stones_to_flip:
                    new_board[fy][fx] = stone

        return new_board

    def evaluate_board(self, board, stone):
        corner_positions = [(0, 0), (0, 5), (5, 0), (5, 5)]
        bad_positions = [(0, 1), (1, 0), (4, 0), (5, 1), (0, 4), (1, 5), (4, 5), (5, 4)]

        score = 0

        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    if (x, y) in corner_positions:
                        score += 100
                    elif (x, y) in bad_positions:
                        score -= 50
                    else:
                        score += 1
                elif board[y][x] == 3 - stone:
                    if (x, y) in corner_positions:
                        score -= 100
                    elif (x, y) in bad_positions:
                        score += 50
                    else:
                        score -= 1

        # モビリティ（合法手数）の評価
        my_moves = len(self.get_legal_moves(board, stone))
        opponent_moves = len(self.get_legal_moves(board, 3 - stone))
        mobility = my_moves - opponent_moves
        score += mobility * 10

        return score

    def alpha_beta(self, board, stone, depth, alpha, beta, maximizing):
        legal_moves = self.get_legal_moves(board, stone)
        if depth == 0 or not legal_moves:
            return self.evaluate_board(board, stone), None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = self.simulate_place(board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, 3 - stone, depth - 1, alpha, beta, False)
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
                simulated_board = self.simulate_place(board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, 3 - stone, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def place(self, board, stone):
        depth = self.determine_depth(board)
        _, best_move = self.alpha_beta(board, stone, depth, -math.inf, math.inf, True)
        return best_move

    def determine_depth(self, board):
        total_stones = sum(row.count(BLACK) + row.count(WHITE) for row in board)
        if total_stones < 20:
            return 4  # 序盤
        elif total_stones < 50:
            return 6  # 中盤
        else:
            return 10  # 終盤
