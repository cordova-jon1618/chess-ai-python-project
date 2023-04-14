# piece.py

import pygame


class Piece:
    def __init__(self, color, x, y, piece_type):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type

    def draw(self, surface):
        img = pygame.image.load(f"img/{self.type}-{self.color}.png")
        surface.blit(img, (self.x * 75 + 10, self.y * 75 + 10))

    def place_pieces_on_board(self, board, screen):

        pieces = []
        for i in range(8):
            pieces.append(Piece("black", i, 1, "pawn"))
            pieces.append(Piece("white", i, 6, "pawn"))

            # Adding rooks
            pieces.append(Piece("black", 0, 0, "rook"))
            pieces.append(Piece("black", 7, 0, "rook"))
            pieces.append(Piece("white", 0, 7, "rook"))
            pieces.append(Piece("white", 7, 7, "rook"))

            # Adding knights
            pieces.append(Piece("black", 1, 0, "knight"))
            pieces.append(Piece("black", 6, 0, "knight"))
            pieces.append(Piece("white", 1, 7, "knight"))
            pieces.append(Piece("white", 6, 7, "knight"))

            # Adding bishops
            pieces.append(Piece("black", 2, 0, "bishop"))
            pieces.append(Piece("black", 5, 0, "bishop"))
            pieces.append(Piece("white", 2, 7, "bishop"))
            pieces.append(Piece("white", 5, 7, "bishop"))

            # Adding queens
            pieces.append(Piece("black", 3, 0, "queen"))
            pieces.append(Piece("white", 3, 7, "queen"))

            # Adding kings
            pieces.append(Piece("black", 4, 0, "king"))
            pieces.append(Piece("white", 4, 7, "king"))

        # Drawing all the chess pieces on board surface
        for piece in pieces:
            piece.draw(board)

        # Drawing the updated board on the screen surface
        screen.blit(board, (20, 20))

        # Updating the display
        pygame.display.flip()

# def place_pieces_on_board(board, screen):
#   piece = Piece(None, None, None, None)
#   piece.place_pieces_on_board(board, screen)
