import pygame
from board import Board
from piece import Piece
from movement import handle_mouse_click
from game_logic import draw_ui_elements


# Notes: We will not implement the following chess functionality
# No two space move by pawns during their first move
# No castling by King and Rook

def initialize_chess_game():
    chess_board = Board()
    board, screen = chess_board.make_board()

    chess_piece = Piece(None, None, None, None)
    pieces_array = chess_piece.place_pieces_on_board(board, screen)

    running = True
    selected_piece = None
    heuristic_score = 0  # Initialize heuristic score
    additional_score = 0  # Initialize additional score

    while running:
        start_button, reset_button = draw_ui_elements(screen, heuristic_score, additional_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            # Handling mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_piece, pieces_array = handle_mouse_click(event, pieces_array, board, screen, selected_piece,
                                                                  start_button, reset_button)

        pygame.display.flip()


def main():
    initialize_chess_game()


if __name__ == "__main__":
    main()
