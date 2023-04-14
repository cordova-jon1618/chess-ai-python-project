import pygame
from board import Board
from piece import Piece


def main():
    chess_board = Board()
    board, screen = chess_board.make_board()

    piece = Piece(None, None, None, None)
    piece.place_pieces_on_board(board, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    main()
