from .pieces import Piece

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.traps = [(2, 2), (2, 5), (5, 2), (5, 5)]  # Coordenadas de trampas
        self.setup_pieces()

    def setup_pieces(self):
        """Coloca las piezas iniciales de ambos jugadores."""
        # Piezas del Jugador 1 (P1)
        self.grid[0] = [
            Piece("E", "P1"), Piece("C", "P1"), Piece("H", "P1"), Piece("D", "P1"),
            Piece("D", "P1"), Piece("H", "P1"), Piece("C", "P1"), Piece("E", "P1")
        ]
        self.grid[1] = [Piece("R", "P1") for _ in range(8)]  # Conejos del jugador 1

        # Piezas del Jugador 2 (P2)
        self.grid[7] = [
            Piece("E", "P2"), Piece("C", "P2"), Piece("H", "P2"), Piece("D", "P2"),
            Piece("D", "P2"), Piece("H", "P2"), Piece("C", "P2"), Piece("E", "P2")
        ]
        self.grid[6] = [Piece("R", "P2") for _ in range(8)]  # Conejos del jugador 2

    def is_trap(self, row, col):
        """Verifica si la posición dada es una trampa."""
        return (row, col) in self.traps

    def move_piece(self, start_pos, destination_pos):
        """Mueve una pieza de start_pos a destination_pos."""
        piece = self.grid[start_pos[0]][start_pos[1]]
        self.grid[destination_pos[0]][destination_pos[1]] = piece
        self.grid[start_pos[0]][start_pos[1]] = None
        print(f"Moved piece from {start_pos} to {destination_pos}")  # Mensaje de depuración

    def remove_piece(self, pos):
        """Elimina una pieza de la posición dada."""
        self.grid[pos[0]][pos[1]] = None
        print(f"Removed piece at {pos}")  # Mensaje de depuración

    def copy(self):
        """Crea una copia del tablero."""
        new_board = Board()
        new_board.grid = [[piece for piece in row] for row in self.grid]
        new_board.traps = self.traps[:]
        return new_board

    def display(self):
        """Muestra el tablero en consola."""
        print("  " + " ".join("ABCDEFGH"))  # Etiquetas de columnas
        for i, row in enumerate(self.grid):
            row_str = f"{8-i} "  # Etiqueta de filas
            for cell in row:
                if cell is None:
                    row_str += ". "
                else:
                    row_str += str(cell) + " "
            print(row_str)