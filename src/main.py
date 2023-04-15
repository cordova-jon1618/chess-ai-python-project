import pygame
from board import Board
from piece import Piece


def main():
    chess_board = Board()
    board, screen = chess_board.make_board()

    chess_piece = Piece(None, None, None, None)
    pieces = chess_piece.place_pieces_on_board(board, screen)

    # movement = Movement(board, screen)
    running = True
    selected_piece = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            # Handling mouse click
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     selected_piece = movement.handle_mouse_click(event, selected_piece, pieces, board, screen)

            # Handling mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = (mouse_x - 20) // 75, (mouse_y - 20) // 75

                if selected_piece is None:
                    for p in pieces:
                        if p.x == grid_x and p.y == grid_y:
                            selected_piece = p
                            break
                else:
                    # Remove the existing piece at the target location, if any
                    pieces = [p for p in pieces if not (p.x == grid_x and p.y == grid_y)]

                    # Move the selected piece to the new location
                    selected_piece.x = grid_x
                    selected_piece.y = grid_y
                    selected_piece = None

                    # Redraw the board with the updated pieces
                    chess_piece.redraw_pieces_on_board(pieces, board, screen)


if __name__ == "__main__":
    main()
