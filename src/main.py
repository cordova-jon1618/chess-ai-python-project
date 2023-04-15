import pygame
from board import Board
from piece import Piece
from movement import handle_mouse_click


def main():
    chess_board = Board()
    board, screen = chess_board.make_board()

    chess_piece = Piece(None, None, None, None)
    pieces = chess_piece.place_pieces_on_board(board, screen)

    running = True
    selected_piece = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            # Handling mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_piece = handle_mouse_click(event, pieces, board, screen, selected_piece)


if __name__ == "__main__":
    main()
