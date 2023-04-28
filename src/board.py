import pygame
from piece import *

# Chess AI Python Project for COMP 469: Intro to Artificial Intelligence
# Authors:
# Jonathan Cordova and Alvaro Lopez-Romero
# California State University Northridge (CSUN)

# NOTE:  This board.py file contains functionality for creating the Board object and making, resetting, converting,
#        These functions involve the Board object
class Board:

    def __init__(self):
        pygame.init()
        self.size = (640, 740)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("AI Chess ")

        self.board = pygame.Surface((600, 600))
        self.board.fill((255, 206, 158))

        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(self.board, (210, 180, 140), (x * 75, y * 75, 75, 75))
                pygame.draw.rect(self.board, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

        self.screen.blit(self.board, (20, 20))
        pygame.display.flip()

    # Makes the UI board
    def make_board(self):

        pygame.init()

        # Setting up window object
        size = (640, 740)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("AI Chess Game Project - COMP 469 by Jonathan Cordova and Alvaro Lopez-Romero")

        # Setting up board object
        board = pygame.Surface((600, 600))
        board.fill((255, 206, 158))

        # Drawing the board object
        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, (210, 180, 140), (x * 75, y * 75, 75, 75))
                pygame.draw.rect(board, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

        # Adding the board to the screen object
        screen.blit(board, (20, 20))

        # pygame.transform.flip()
        pygame.display.flip()

        return board, screen

    # Resets the UI board
    def reset_board(self, board_surface):
        # Clear the board surface
        board_surface.fill((255, 206, 158))

        # Redraw the squares with the original colors
        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board_surface, (210, 180, 140), (x * 75, y * 75, 75, 75))
                pygame.draw.rect(board_surface, (210, 180, 140), ((x + 1) * 75, (y + 1) * 75, 75, 75))

        return board_surface


# Converts matrix array to board object
def matrix_to_board(matrix):
    board = Board()
    surface, screen = board.make_board()
    for row_idx, row in enumerate(matrix):
        for col_idx, col in enumerate(row):
            if col != " ":
                color = "white" if col.isupper() else "black"
                piece_type = col.lower()
                piece = Piece(color, col_idx, row_idx, piece_type, None)
                piece.draw(surface)
    pygame.display.update()
    return surface
