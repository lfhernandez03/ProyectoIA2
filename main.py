from src.board import Board
from src.rules import Rules
from src.gui import GUI
from src.minimax import Minimax
import pygame

def main():
    # Inicialización del tablero, reglas, GUI y Minimax
    board = Board()
    rules = Rules(board)
    gui = GUI()
    minimax = Minimax(rules)

    current_player = "P1"  # Asegúrate de que los nombres de los jugadores coincidan con los nombres en las piezas
    steps_remaining = 4  # Cada turno tiene un máximo de 4 movimientos
    selected_piece = None
    start_pos = None

    def reset_turn_variables():
        nonlocal selected_piece, start_pos, steps_remaining
        selected_piece = None
        start_pos = None
        steps_remaining = 4

    while True:
        gui.draw_board(board)  # Dibuja el tablero actual
        gui.draw_pieces(board)  # Dibuja las piezas en el tablero
        gui.draw_turn(current_player)  # Dibuja el turno actual
        gui.update()

        # Manejar eventos de cierre
        for event in gui.get_events():
            if event.type == pygame.QUIT:
                return

            # Turno del jugador humano (P1)
            if current_player == "P1":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if selected_piece is None:
                        # Seleccionar pieza
                        selected_piece, start_pos = gui.get_selected_piece(board)
                        if selected_piece and selected_piece.player != current_player:
                            selected_piece = None
                    else:
                        # Seleccionar destino y mover pieza
                        destination_pos = gui.get_mouse_position_on_board()
                        if rules.is_valid_move(selected_piece, start_pos, destination_pos):
                            board.move_piece(start_pos, destination_pos)

                            # Aplicar trampas y verificar victoria
                            if rules.is_trapped(selected_piece, destination_pos):
                                board.remove_piece(destination_pos)

                            if rules.is_game_over():
                                print(f"¡{current_player} gana!")
                                return

                            steps_remaining -= 1
                            if steps_remaining == 0:
                                current_player = "P2"
                                reset_turn_variables()
                            else:
                                selected_piece = None
                                start_pos = None
                        else:
                            # Si el movimiento no es válido, deseleccionamos la pieza
                            selected_piece = None
                            start_pos = None

            # Turno de la IA (P2)
            if current_player == "P2":
                # Ejecutar el algoritmo Minimax para determinar el mejor movimiento
                best_move = minimax.get_best_move(board, current_player)
                if best_move:
                    start_pos, destination_pos = best_move
                    board.move_piece(start_pos, destination_pos)

                    # Aplicar reglas de trampas
                    selected_piece = board.grid[destination_pos[0]][destination_pos[1]]
                    if rules.is_trapped(selected_piece, destination_pos):
                        board.remove_piece(destination_pos)

                    if rules.is_game_over():
                        print(f"¡{current_player} gana!")
                        return

                    steps_remaining -= 1
                    if steps_remaining == 0:
                        current_player = "P1"
                        reset_turn_variables()
                else:
                    # Si no hay movimientos válidos, termina el turno
                    current_player = "P1"
                    reset_turn_variables()

        gui.clock.tick(30)  # Controlar FPS

if __name__ == "__main__":
    main()