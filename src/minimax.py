class Minimax:
    def __init__(self, rules):
        self.rules = rules

    def get_best_move(self, board, player):
        _, best_move = self.minimax(board, depth=2, alpha=float("-inf"), beta=float("inf"), maximizing_player=(player == "P1"))
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.rules.is_game_over():
            return self.evaluate_board(board), None

        if maximizing_player:
            max_eval = float("-inf")
            best_move = None
            for move in self.generate_moves(board, "P1"):
                new_board = self.simulate_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in self.generate_moves(board, "P2"):
                new_board = self.simulate_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, board):
        score = 0
        for row in range(board.size):
            for col in range(board.size):
                piece = board.grid[row][col]
                if piece:
                    piece_value = self.piece_value(piece)
                    score += piece_value if piece.player == "P1" else -piece_value

                    # Adyacentes aliados y enemigos
                    adjacent_allies = sum(
                        1 for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if board.is_ally((row + d_row, col + d_col), piece.player)
                    )
                    adjacent_enemies = sum(
                        1 for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if board.is_ally((row + d_row, col + d_col), "P2" if piece.player == "P1" else "P1")
                    )
                    score += 20 * adjacent_allies - 10 * adjacent_enemies

                    # Movilidad
                    mobility = sum(
                        1 for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if self.rules.is_valid_move(piece, (row, col), (row + d_row, col + d_col))
                    )
                    score += mobility * (1 if piece.player == "P1" else -1)

        return score

    def piece_value(self, piece):
        values = {
            "R": 1,  # Conejo
            "G": 2,  # Gato
            "C": 3,  # Camello
            "H": 4,  # Caballo
            "D": 5,  # Perro
            "E": 6   # Elefante
        }
        return values.get(piece.name, 0)

    def generate_moves(self, board, player):
        """
        Genera todos los movimientos posibles para un jugador.

        Args:
            board (Board): El tablero actual.
            player (str): El jugador para el que generar movimientos ("P1" o "P2").

        Returns:
            list: Lista de movimientos posibles.
        """
        moves = []
        for row in range(board.size):
            for col in range(board.size):
                piece = board.grid[row][col]
                if piece and piece.player == player:
                    for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = row + d_row, col + d_col
                        if 0 <= new_row < board.size and 0 <= new_col < board.size and board.grid[new_row][new_col] is None:
                            moves.append(((row, col), (new_row, new_col)))
        print(f"Generated moves for {player}: {moves}")
        return moves

    def simulate_move(self, board, move):
        new_board = board.copy()
        start_pos, end_pos = move
        piece = new_board.grid[start_pos[0]][start_pos[1]]
        new_board.grid[end_pos[0]][end_pos[1]] = piece
        new_board.grid[start_pos[0]][start_pos[1]] = None
        return new_board