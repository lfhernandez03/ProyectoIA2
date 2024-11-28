from src.board import Board
from src.rules import Rules
from src.gui import GUI
import pygame

def main():
    # Inicialización del tablero, reglas y GUI
    board = Board()
    rules = Rules(board)
    gui = GUI()

    current_player = "P1"  # Asegúrate de que los nombres de los jugadores coincidan con los nombres en las piezas
    steps_remaining = 4  # Cada turno tiene un máximo de 4 movimientos
    selected_piece = None
    start_pos = None

    while True:
        gui.draw_board(board)  # Dibuja el tablero actual
        gui.draw_pieces(board)  # Dibuja las piezas en el tablero
        gui.draw_turn(current_player)  # Dibuja el turno actual
        gui.update()

        # Manejar eventos
        for event in gui.get_events():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button down event detected")  # Mensaje de depuración
                if selected_piece is None:
                    # Obtener la pieza seleccionada
                    selected_piece, start_pos = gui.get_selected_piece(board)
                    if selected_piece:
                        if selected_piece.player != current_player:
                            print("Selected piece does not belong to the current player")  # Mensaje de depuración
                            selected_piece = None  # Deseleccionar si la pieza no pertenece al jugador actual
                        else:
                            print(f"Selected piece: {selected_piece}, Start position: {start_pos}")  # Mensaje de depuración
                else:
                    # Obtener la posición destino
                    destination_pos = gui.get_mouse_position_on_board()
                    print(f"Destination position: {destination_pos}")  # Mensaje de depuración

                    # Verificar si el movimiento es válido
                    if rules.is_valid_move(selected_piece, start_pos, destination_pos):
                        print("Move is valid")  # Mensaje de depuración
                        # Mover la pieza
                        board.move_piece(start_pos, destination_pos)
                        print(f"Moved piece to {destination_pos}")  # Mensaje de depuración

                        # Aplicar reglas de trampas
                        if rules.is_trapped(selected_piece, destination_pos):
                            board.remove_piece(destination_pos)
                            print(f"Piece at {destination_pos} is trapped and removed")  # Mensaje de depuración

                        # Reducir pasos restantes
                        steps_remaining -= 1

                        # Verificar condiciones de victoria
                        winner = rules.is_game_over()
                        if winner:
                            print(f"¡{winner} gana!")
                            return

                        # Si no hay más pasos, cambiar de turno
                        if steps_remaining == 0:
                            current_player = "P2" if current_player == "P1" else "P1"
                            steps_remaining = 4

                    # Resetear la selección de pieza
                    selected_piece = None
                    start_pos = None

        gui.clock.tick(30)  # Controlar FPS

if __name__ == "__main__":
    main()