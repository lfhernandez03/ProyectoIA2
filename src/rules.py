class Rules:
    def __init__(self, board):
        self.board = board

    def can_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Verifica que el destino esté dentro del tablero
        if not (0 <= end_row < self.board.size and 0 <= end_col < self.board.size):
            return False

        # Verifica que el destino esté vacío
        if self.board.grid[end_row][end_col] is not None:
            return False

        # Verifica que el movimiento sea a una celda adyacente
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            return False

        return True

    def can_push(self, start_pos, end_pos):
        """Verifica si una pieza puede empujar a otra."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Verifica que el destino esté dentro del tablero
        if not (0 <= end_row < self.board.size and 0 <= end_col < self.board.size):
            return False

        # Verifica que el destino esté ocupado por una pieza enemiga
        if self.board.grid[end_row][end_col] is None or self.board.grid[start_row][start_col] is None or self.board.grid[end_row][end_col].player == self.board.grid[start_row][start_col].player:
            return False

        # Verifica que el movimiento sea a una celda adyacente
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            return False

        # Verifica que la pieza que empuja sea más fuerte
        piece = self.board.grid[start_row][start_col]
        target_piece = self.board.grid[end_row][end_col]
        if piece and target_piece and piece.strength > target_piece.strength:
            return True

        return False

    def can_pull(self, start_pos, end_pos):
        """Verifica si una pieza puede tirar de otra."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Verifica que el destino esté dentro del tablero
        if not (0 <= end_row < self.board.size and 0 <= end_col < self.board.size):
            return False

        # Verifica que el destino esté ocupado por una pieza enemiga
        if self.board.grid[end_row][end_col] is None or self.board.grid[start_row][start_col] is None or self.board.grid[end_row][end_col].player == self.board.grid[start_row][start_col].player:
            return False

        # Verifica que el movimiento sea a una celda adyacente
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            return False

        # Verifica que la pieza que tira sea más fuerte
        piece = self.board.grid[start_row][start_col]
        target_piece = self.board.grid[end_row][end_col]
        if piece and target_piece and piece.strength > target_piece.strength:
            return True

        return False

    def push_piece(self, start_pos, end_pos, push_pos):
        """Empuja una pieza enemiga a una nueva posición."""
        self.board.grid[push_pos[0]][push_pos[1]] = self.board.grid[end_pos[0]][end_pos[1]]
        self.board.grid[end_pos[0]][end_pos[1]] = self.board.grid[start_pos[0]][start_pos[1]]
        self.board.grid[start_pos[0]][start_pos[1]] = None

    def pull_piece(self, start_pos, end_pos, pull_pos):
        """Tira de una pieza enemiga a una nueva posición."""
        self.board.grid[pull_pos[0]][pull_pos[1]] = self.board.grid[start_pos[0]][start_pos[1]]
        self.board.grid[start_pos[0]][start_pos[1]] = self.board.grid[end_pos[0]][end_pos[1]]
        self.board.grid[end_pos[0]][end_pos[1]] = None

    def is_valid_move(self, piece, start_pos, end_pos):
        """Verifica si un movimiento es válido."""
        if self.can_move(start_pos, end_pos):
            return True
        if self.can_push(start_pos, end_pos):
            return True
        if self.can_pull(start_pos, end_pos):
            return True
        return False

    def is_trapped(self, piece, pos):
        """Verifica si una pieza está atrapada."""
        row, col = pos
        if not self.board.is_trap(row, col):
            return False
        # Verifica si hay piezas aliadas adyacentes
        for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.board.is_ally((row + d_row, col + d_col), piece.player):
                return False
        return True

    def is_game_over(self):
        """
        Verifica si el juego ha terminado debido a una victoria o derrota.

        Returns:
            str: 'P1', 'P2' o None según el estado del juego.
        """
        # Verifica si algún conejo alcanzó el lado opuesto
        for col in range(self.board.size):
            if self.board.grid[self.board.size - 1][col] and self.board.grid[self.board.size - 1][col].name == "R" and self.board.grid[self.board.size - 1][col].player == "P1":
                print("Player 1 wins by reaching the opposite side with a rabbit.")  # Mensaje de depuración
                return "P1"
            if self.board.grid[0][col] and self.board.grid[0][col].name == "R" and self.board.grid[0][col].player == "P2":
                print("Player 2 wins by reaching the opposite side with a rabbit.")  # Mensaje de depuración
                return "P2"

        # Verifica si algún jugador no tiene piezas
        player1_pieces = any(piece and piece.player == "P1" for row in self.board.grid for piece in row)
        player2_pieces = any(piece and piece.player == "P2" for row in self.board.grid for piece in row)

        if not player1_pieces:
            print("Player 2 wins because Player 1 has no pieces left.")  # Mensaje de depuración
            return "P2"
        if not player2_pieces:
            print("Player 1 wins because Player 2 has no pieces left.")  # Mensaje de depuración
            return "P1"

        return None