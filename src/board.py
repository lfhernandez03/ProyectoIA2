from .pieces import Piece
import random

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.traps = [(2, 2), (2, 5), (5, 2), (5, 5)]  # Coordenadas de trampas
        self.setup_pieces()

    def setup_pieces(self):
        """Coloca las piezas iniciales de ambos jugadores de forma aleatoria."""
        # Piezas del Jugador 1 (P1)
        p1_pieces = [
            Piece("E", "P1"), Piece("C", "P1"), Piece("H", "P1"), Piece("H", "P1"),
            Piece("D", "P1"), Piece("D", "P1"), Piece("G", "P1"), Piece("G", "P1")
        ] + [Piece("R", "P1") for _ in range(8)]  # Añadir 8 conejos
        p1_positions = [(0, i) for i in range(8)] + [(1, i) for i in range(8)]
        random.shuffle(p1_positions)
        for pos, piece in zip(p1_positions, p1_pieces):
            self.grid[pos[0]][pos[1]] = piece

        # Piezas del Jugador 2 (P2)
        p2_pieces = [
            Piece("E", "P2"), Piece("C", "P2"), Piece("H", "P2"), Piece("H", "P2"),
            Piece("D", "P2"), Piece("D", "P2"), Piece("G", "P2"), Piece("G", "P2")
        ] + [Piece("R", "P2") for _ in range(8)]  # Añadir 8 conejos
        p2_positions = [(6, i) for i in range(8)] + [(7, i) for i in range(8)]
        random.shuffle(p2_positions)
        for pos, piece in zip(p2_positions, p2_pieces):
            self.grid[pos[0]][pos[1]] = piece

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
            
    def is_ally(self, pos, player):
        """Verifica si la pieza en la posición dada es aliada."""
        row, col = pos
        if 0 <= row < self.size and 0 <= col < self.size:
            piece = self.grid[row][col]
            return piece is not None and piece.player == player
        return False