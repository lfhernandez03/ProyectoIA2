class Rules:
    def __init__(self, board):
        self.board = board

    def is_valid_move(self, piece, start_pos, destination_pos):
        """Verifica si el movimiento es válido."""
        start_row, start_col = start_pos
        end_row, end_col = destination_pos

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

    def is_trapped(self, piece, pos):
        """Verifica si una pieza está atrapada."""
        row, col = pos
        return self.board.is_trap(row, col)

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
            if self.board.grid[self.board.size - 1][col] and self.board.grid[self.board.size - 1][col].name == "R" and self.board.grid[self.board.size - 1][col].player == "P2":
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

        # No hay ganador aún
        return None