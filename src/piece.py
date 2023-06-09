
import pygame

# Chess AI Python Project for COMP 469: Intro to Artificial Intelligence
# Authors:
# Jonathan Cordova and Alvaro Lopez-Romero
# California State University Northridge (CSUN)

# NOTE:  This piece.py file contains functionality for creating the Piece object,
#        placing pieces on board, the pieces are placed starting at (0, 0) from the top left corner of the board,
#        to (7,7) in the bottom right corner of the board, the reason for this is that after the board is converted
#        to a matrix array, it makes it easier to read this way and view in the console window.
#        Additionally, this contains the functions that allow for the board to be highlighted green or red upon
#        either the User selecting the piece, or the AI making a move.

class Piece:
    def __init__(self, color, x, y, piece_type, value):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type
        self.value = value

    def draw(self, surface):
        img = pygame.image.load(f"img/{self.type}-{self.color}.png")
        surface.blit(img, (self.x * 75 + 10, self.y * 75 + 10))

    def place_pieces_on_board(self, board, screen):

        # Values of the chess pieces
        PIECE_VALUES = {
            "pawn": 1.0,
            "knight": 3.0,
            "bishop": 3.0,
            "rook": 5.0,
            "queen": 9.0,
            "king": 100.0,
        }

        pieces = []
        white_pieces = []
        black_pieces = []
        for row in range(8):
            # Adding pawns to initial positions
            black_pawn = Piece("black", row, 1, "pawn", PIECE_VALUES["pawn"])
            white_pawn = Piece("white", row, 6, "pawn", PIECE_VALUES["pawn"])
            pieces.extend([black_pawn, white_pawn])
            black_pieces.append(black_pawn)
            white_pieces.append(white_pawn)

        # Adding rooks, knights, bishops, queens, and kings to initial positions
        for col, piece_type in enumerate(["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]):
            black_piece = Piece("black", col, 0, piece_type, PIECE_VALUES[piece_type])
            white_piece = Piece("white", col, 7, piece_type, PIECE_VALUES[piece_type])
            pieces.extend([black_piece, white_piece])
            black_pieces.append(black_piece)
            white_pieces.append(white_piece)

        # Drawing all the chess pieces on board surface
        for piece in pieces:
            piece.draw(board)

        # Drawing the updated board on the screen surface
        screen.blit(board, (20, 20))

        # Updating the display
        pygame.display.flip()

        # Return the pieces array to main.py
        return pieces, white_pieces, black_pieces


def redraw_pieces_on_board(pieces_array, board, screen):
    # redraw the board and pieces
    board.fill((255, 206, 158))
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(board, (210, 180, 140), (x * 75, y * 75, 75, 75))
            pygame.draw.rect(board, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

    for piece in pieces_array:
        piece.draw(board)

    # add the board to the screen
    screen.blit(board, (20, 20))

    # update the display
    pygame.display.update()


def redraw_pieces_on_board_with_green_highlight(pieces, board, screen, highlighted_square):
    # Redraw the board and pieces
    board.fill((255, 206, 158))
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(board, (210, 180, 140), (x * 75, y * 75, 75, 75))
            pygame.draw.rect(board, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

    # Highlight the selected square with light green
    pygame.draw.rect(board, (180, 240, 180), (highlighted_square[0] * 75, highlighted_square[1] * 75, 75, 75))

    for piece in pieces:
        piece.draw(board)

    # Add the board to the screen
    screen.blit(board, (20, 20))

    # Update the display
    pygame.display.update()


def redraw_pieces_on_board_with_red_highlight(pieces, board, screen, highlighted_squares):
    # Redraw the board and pieces
    board.fill((255, 206, 158))
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(board, (210, 180, 140), (x * 75, y * 75, 75, 75))
            pygame.draw.rect(board, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

    # Highlight the original move square in red
    pygame.draw.rect(board, (255, 0, 0), (highlighted_squares[0][0] * 75, highlighted_squares[0][1] * 75, 75, 75))

    # Highlight the best move square in light red
    pygame.draw.rect(board, (200, 0, 0), (highlighted_squares[-1][0] * 75, highlighted_squares[-1][1] * 75, 75, 75))

    for piece in pieces:
        piece.draw(board)

    # Add the board to the screen
    screen.blit(board, (20, 20))

    # Update the display
    pygame.display.update()


