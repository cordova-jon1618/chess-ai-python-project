import pygame
from board import Board
from piece import Piece


def main():
    chess_board = Board()
    board, screen = chess_board.make_board()

    chess_piece = Piece(None, None, None, None)
    pieces = chess_piece.place_pieces_on_board(board, screen)

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()
    #
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             # Get the position of the click
    #             pos = pygame.mouse.get_pos()
    #
    #             # Convert the position to board coordinates
    #             x = (pos[0] - 20) // 75
    #             y = (pos[1] - 20) // 75
    #
    #             # Find the piece at the clicked position
    #             for piece in pieces:
    #                 if piece.x == x and piece.y == y:
    #                     # move the piece
    #                     pos = pygame.mouse.get_pos()
    #                     x = (pos[0] - 20) // 75
    #                     y = (pos[1] - 20) // 75
    #                     piece.x = x
    #                     piece.y = y
    #             print("Mouse event has been called.")
    #
    #     # Redraws the board after a move
    #     chess_piece.redraw_pieces_on_board(pieces, board, screen)
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
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = (mouse_x - 20) // 75, (mouse_y - 20) // 75

                if selected_piece is None:
                    for p in pieces:
                        if p.x == grid_x and p.y == grid_y:
                            selected_piece = p
                            break
                else:
                    selected_piece.x = grid_x
                    selected_piece.y = grid_y
                    selected_piece = None

                    chess_piece.redraw_pieces_on_board(pieces, board, screen)


if __name__ == "__main__":
    main()
