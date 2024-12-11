import random

class Minimax:
    def __init__(self, rules):
        self.rules = rules

    def get_best_move(self, board, player):
        """
        Determina el mejor movimiento usando Minimax con poda alfa-beta.

        Args:
            board (Board): El estado actual del tablero.
            player (str): El jugador ("P1" o "P2").

        Returns:
            tuple: El mejor movimiento ((inicio_fila, inicio_col), (destino_fila, destino_col)).
        """
        _, best_move = self.minimax(board, depth=2, alpha=float("-inf"), beta=float("inf"), maximizing_player=(player == "P1"))
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Implementa el algoritmo Minimax con poda alfa-beta.

        Args:
            board (Board): El estado actual del tablero.
            depth (int): Profundidad máxima del árbol.
            alpha (float): Mejor puntuación del jugador max.
            beta (float): Mejor puntuación del jugador min.
            maximizing_player (bool): True si es el turno del jugador max.

        Returns:
            tuple: (valor, mejor movimiento).
        """
        if depth == 0 or self.rules.is_game_over():
            eval_score = self.evaluate_board(board)
            print(f"Evaluating board at depth {depth}: {eval_score}")
            return eval_score, None

        if maximizing_player:
            max_eval = float("-inf")
            best_moves = []
            for move in self.generate_moves(board, "P2"):
                new_board = board.copy()
                new_board.move_piece(*move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                print(f"Move {move} evaluated as {eval}")
                if eval > max_eval:
                    max_eval = eval
                    best_moves = [move]
                elif eval == max_eval:
                    best_moves.append(move)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, random.choice(best_moves) if best_moves else None
        else:
            min_eval = float("inf")
            best_moves = []
            for move in self.generate_moves(board, "P2"):
                new_board = board.copy()
                new_board.move_piece(*move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                print(f"Move {move} evaluated as {eval}")
                if eval < min_eval:
                    min_eval = eval
                    best_moves = [move]
                elif eval == min_eval:
                    best_moves.append(move)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, random.choice(best_moves) if best_moves else None

    def evaluate_board(self, board):
        """
        Evalúa el tablero para un jugador en particular, asignando valor a las piezas 
        y las posiciones estratégicas.
    
        board: El tablero de juego.
    
        Returns:
            int: Valor del tablero según la evaluación.
        """
        score = 0

        for row in range(8):  # Asumimos un tablero 8x8
            for col in range(8):
                piece = board.grid[row][col]  # Acceder correctamente a la celda del tablero

                if piece is not None:
                    piece_value = self.piece_value(piece)

                    # Agregar el valor de la pieza según su tipo
                    score += piece_value

                    # Evaluación de la posición de la pieza
                    if piece.name == 'R':  # Conejo
                        # Prioriza los conejos cercanos a la meta
                        if piece.player == "P1":
                            score += 10 * (7 - row)  # Mientras más cerca del final, mayor valor
                        else:
                            score += 10 * row  # Oponente cerca de su meta

                    elif piece.name == 'E':  # Elefante
                        # Prioriza elefantes en posiciones centrales o bloqueando el camino
                        if piece.player == "P1":
                            score += 5 * (4 - abs(3 - row))  # Cerca del centro del tablero
                        else:
                            score += 5 * abs(3 - row)  # Oponente en posición menos favorable
        return score

    def piece_value(self, piece):
        """
        Asigna un valor a cada tipo de pieza.

        Args:
            piece (Piece): La pieza a evaluar.

        Returns:
            int: Valor de la pieza.
        """
        values = {"R": 1, "C": 3, "H": 5, "D": 7, "E": 9}
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
