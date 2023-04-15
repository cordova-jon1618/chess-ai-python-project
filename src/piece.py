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
            # Adding pawns to initial positions
            pieces.append(Piece("black", i, 1, "pawn"))
            pieces.append(Piece("white", i, 6, "pawn"))

        # Adding rooks, knights, bishops, queens, and kings to initial positions
        for i, piece_type in enumerate(["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]):
            pieces.append(Piece("black", i, 0, piece_type))
            pieces.append(Piece("white", i, 7, piece_type))

        # Drawing all the chess pieces on board surface
        for piece in pieces:
            piece.draw(board)

        # Drawing the updated board on the screen surface
        screen.blit(board, (20, 20))

        # Updating the display
        pygame.display.flip()

        # Return the pieces array to main.py
        return pieces

    def redraw_pieces_on_board(self, pieces, board, screen):
        # redraw the board and pieces
        board.fill((255, 206, 158))
        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, (210, 180, 140), (x * 75, y * 75, 75, 75))
                pygame.draw.rect(board, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

        for piece in pieces:
            piece.draw(board)

        # add the board to the screen
        screen.blit(board, (20, 20))

        # update the display
        pygame.display.update()

# def place_pieces_on_board(board, screen):
#   piece = Piece(None, None, None, None)
#   piece.place_pieces_on_board(board, screen)
