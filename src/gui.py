import pygame
from .images import load_images

# Dimensiones del tablero
CELL_SIZE = 80  # Tamaño de cada celda
BOARD_SIZE = 8  # Tamaño del tablero (8x8)

# Colores
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
TRAP_COLOR = (255, 0, 0)

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE + 50))  # Añadir espacio para el texto
        pygame.display.set_caption("Arimaa")
        self.clock = pygame.time.Clock()
        self.running = True
        self.images = load_images(cell_size=CELL_SIZE-20)
        if not self.images:
            print("No se pudieron cargar las imágenes.")

    def draw_board(self, board):
        """Dibuja el tablero en la pantalla."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(
                    self.screen, color, 
                    (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
                if board.is_trap(row, col):  # Dibuja trampas
                    pygame.draw.circle(
                        self.screen, TRAP_COLOR, 
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 
                        10
                    )

    def draw_pieces(self, board):
        """Dibuja las piezas usando imágenes."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.grid[row][col]
                if piece:
                    key = f"{piece.name}{piece.player[-1]}"  # Genera la clave de la imagen
                    image = self.images.get(key)
                    if image:
                        # Calcula la posición para centrar la imagen en la celda
                        x = col * CELL_SIZE + (CELL_SIZE - image.get_width()) // 2
                        y = row * CELL_SIZE + (CELL_SIZE - image.get_height()) // 2
                        self.screen.blit(image, (x, y))

    def draw_text(self, text, color, x, y):
        """Dibuja texto centrado en una celda."""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_turn(self, current_player):
        """Dibuja el turno actual en la pantalla."""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Turno de: {current_player}", True, WHITE)
        self.screen.blit(text_surface, (10, CELL_SIZE * BOARD_SIZE + 10))

    def get_mouse_position_on_board(self):
        """
        Devuelve las coordenadas del clic del jugador en el tablero.
        
        Returns:
            tuple: Coordenadas en el formato (fila, columna).
        """
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // CELL_SIZE
        col = mouse_pos[0] // CELL_SIZE
        print(f"Mouse position on board: (row: {row}, col: {col})")  # Mensaje de depuración
        return (row, col)
    
    def run(self, board):
        """Ciclo principal de la GUI."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(BLACK)
            self.draw_board(board)
            self.draw_pieces(board)
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS

        pygame.quit()

    def update(self):
        """Actualiza la pantalla."""
        pygame.display.flip()

    def get_events(self):
        """Devuelve la lista de eventos de Pygame."""
        return pygame.event.get()

    def get_selected_piece(self, board):
        """Obtiene la pieza seleccionada según el clic del jugador."""
        x, y = pygame.mouse.get_pos()
        row, col = y // CELL_SIZE, x // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            piece = board.grid[row][col]
            print(f"Selected piece at (row: {row}, col: {col}): {piece}")  # Mensaje de depuración
            return piece, (row, col)
        else:
            print(f"Clicked outside the board at (row: {row}, col: {col})")  # Mensaje de depuración
            return None, None