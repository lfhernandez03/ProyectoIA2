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

    def check_traps():
        """Verifica y elimina piezas atrapadas en casillas trampa."""
        for row in range(board.size):
            for col in range(board.size):
                piece = board.grid[row][col]
                if piece and rules.is_trapped(piece, (row, col)):
                    board.remove_piece((row, col))

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
                    pos = gui.get_mouse_position_on_board()  # Obtener la posición del ratón en el tablero
                    row, col = pos

                    if selected_piece is None:
                        # Seleccionar una pieza
                        if board.grid[row][col] and board.grid[row][col].player == current_player:
                            selected_piece = board.grid[row][col]
                            start_pos = (row, col)
                    else:
                        # Intentar mover la pieza seleccionada
                        end_pos = (row, col)
                        if rules.is_valid_move(selected_piece, start_pos, end_pos):
                            if rules.can_move(start_pos, end_pos):
                                board.move_piece(start_pos, end_pos)
                            elif rules.can_push(start_pos, end_pos):
                                push_pos = (end_pos[0] + (end_pos[0] - start_pos[0]), end_pos[1] + (end_pos[1] - start_pos[1]))
                                if 0 <= push_pos[0] < board.size and 0 <= push_pos[1] < board.size and board.grid[push_pos[0]][push_pos[1]] is None:
                                    rules.push_piece(start_pos, end_pos, push_pos)
                            elif rules.can_pull(start_pos, end_pos):
                                pull_pos = (start_pos[0] - (end_pos[0] - start_pos[0]), start_pos[1] - (end_pos[1] - start_pos[1]))
                                if 0 <= pull_pos[0] < board.size and 0 <= pull_pos[1] < board.size and board.grid[pull_pos[0]][pull_pos[1]] is None:
                                    rules.pull_piece(start_pos, end_pos, pull_pos)
                            steps_remaining -= 1

                            # Verificar y eliminar piezas atrapadas en casillas trampa
                            check_traps()

                            if steps_remaining == 0:
                                current_player = "P2"
                                reset_turn_variables()
                            else:
                                selected_piece = None
                                start_pos = None
                                
                            if rules.is_game_over():
                                print(f"¡{current_player} gana!")
                                return
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
                    if rules.is_valid_move(board.grid[start_pos[0]][start_pos[1]], start_pos, destination_pos):
                        if rules.can_move(start_pos, destination_pos):
                            board.move_piece(start_pos, destination_pos)
                        elif rules.can_push(start_pos, destination_pos):
                            push_pos = (destination_pos[0] + (destination_pos[0] - start_pos[0]), destination_pos[1] + (destination_pos[1] - start_pos[1]))
                            if 0 <= push_pos[0] < board.size and 0 <= push_pos[1] < board.size and board.grid[push_pos[0]][push_pos[1]] is None:
                                rules.push_piece(start_pos, destination_pos, push_pos)
                        elif rules.can_pull(start_pos, destination_pos):
                            pull_pos = (start_pos[0] - (destination_pos[0] - start_pos[0]), start_pos[1] - (destination_pos[1] - start_pos[1]))
                            if 0 <= pull_pos[0] < board.size and 0 <= pull_pos[1] < board.size and board.grid[pull_pos[0]][pull_pos[1]] is None:
                                rules.pull_piece(start_pos, destination_pos, pull_pos)

                        # Verificar y eliminar piezas atrapadas en casillas trampa
                        check_traps()

                    if rules.is_game_over():
                        print(f"¡{current_player} gana!")
                        return

                    steps_remaining -= 1
                    if steps_remaining == 0:
                        current_player = "P1"
                        reset_turn_variables()

                    # Añadir un retraso para hacer la animación de la IA más lenta
                    pygame.time.delay(500)  # Retraso de 500 ms

        gui.clock.tick(30)  # Controlar FPS

if __name__ == "__main__":
    main()