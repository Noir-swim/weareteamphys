class EagarAI(object):

    def face(self):
        return "🐈"

    def flip_count(self, board, stone, x, y):
        """
        指定の座標に石を置いた場合にひっくり返せる石の数を計算する。
        """
        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        total_flips = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            flips = 0

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                nx += dx
                ny += dy
                flips += 1

            if flips > 0 and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                total_flips += flips

        return total_flips

    def get_valid_moves(self, board, stone):
        """
        置けるすべての有効な座標をリストとして返す。
        """
        valid_moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def prioritize_moves(self, moves, board):
        """
        コーナーとエッジを優先するため、スコアを付けて評価する。
        """
        score_map = {}
        width, height = len(board[0]), len(board)

        for x, y in moves:
            # 初期スコア（通常のマス）
            score = 1

            # コーナー
            if (x, y) in [(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)]:
                score += 100

            # エッジ
            elif x == 0 or x == width - 1 or y == 0 or y == height - 1:
                score += 10

            score_map[(x, y)] = score

        # スコアで降順ソートしてリストを返す
        return sorted(score_map.items(), key=lambda item: item[1], reverse=True)

    def place(self, board, stone):
        valid_moves = self.get_valid_moves(board, stone)

        if not valid_moves:
            return None  # 有効な手がない場合

        # 各手のひっくり返せる数を計算
        move_scores = [(x, y, self.flip_count(board, stone, x, y)) for x, y in valid_moves]

        # 最多ひっくり返せる手を抽出
        max_flips = max(move_scores, key=lambda m: m[2])[2]
        best_moves = [(x, y) for x, y, flips in move_scores if flips == max_flips]

        # 最多の手の中からコーナーやエッジを優先
        prioritized_moves = self.prioritize_moves(best_moves, board)

        # 最も優先度の高い手を選択
        best_move = prioritized_moves[0][0]  # 優先度の高い手の座標を取得
        return best_move
