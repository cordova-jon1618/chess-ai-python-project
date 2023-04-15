import pygame


class Board:

    def make_board(self):

        pygame.init()

        # Setting up window object
        size = (640, 640)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("AI Chess Game Project")

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

        pygame.display.flip()

        return board, screen