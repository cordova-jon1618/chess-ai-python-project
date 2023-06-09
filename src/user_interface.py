import pygame


# Chess AI Python Project for COMP 469: Intro to Artificial Intelligence
# Authors:
# Jonathan Cordova and Alvaro Lopez-Romero
# California State University Northridge (CSUN)

# NOTE:  This user_interface.py file contains functionality such as the User's ability to select and move pieces,
#        checking if a chess move is valid, converting the board state into a board matrix and helper functions.
def draw_ui_elements(screen, heuristic_score, additional_score):
    font_name = "calibri"
    font = pygame.font.SysFont(font_name, 24)
    bold_font = pygame.font.SysFont(font_name, 24)
    bold_font.set_bold(True)

    start_button = pygame.Rect(50, 665, 100, 50)
    reset_button = pygame.Rect(200, 665, 100, 50)

    start_text = bold_font.render("Start", True, (255, 255, 255))
    reset_text = bold_font.render("Reset", True, (255, 255, 255))

    score_text = font.render(f"AI Short-Term Heuristic: {heuristic_score}", True, (255, 255, 255))
    additional_score_text = font.render(f"AI Long-Term Heuristic: {additional_score}", True, (255, 255, 255))

    pygame.draw.rect(screen, (80, 240, 180), start_button)
    pygame.draw.rect(screen, (255, 127, 127), reset_button)

    start_text_x = start_button.x + (start_button.width - start_text.get_width()) // 2
    start_text_y = start_button.y + (start_button.height - start_text.get_height()) // 2
    reset_text_x = reset_button.x + (reset_button.width - reset_text.get_width()) // 2
    reset_text_y = reset_button.y + (reset_button.height - reset_text.get_height()) // 2

    screen.blit(start_text, (start_text_x, start_text_y))
    screen.blit(reset_text, (reset_text_x, reset_text_y))
    screen.blit(score_text, (325, 650))
    screen.blit(additional_score_text, (325, 680))

    return start_button, reset_button


def clear_scores(screen):
    pygame.draw.rect(screen, (0, 0, 0), (375, 650, 250, 50))
    pygame.draw.rect(screen, (0, 0, 0), (375, 680, 250, 50))


def update_UI_view(screen, heuristic_score, additional_score):
    font_name = "calibri"
    font = pygame.font.SysFont(font_name, 24)
    bold_font = pygame.font.SysFont(font_name, 24)
    bold_font.set_bold(True)

    # Clear the area where the scores are displayed
    clear_scores(screen)

    # Redraw the score text with the new values
    score_text = font.render(f"AI Short-Term Heuristic: {heuristic_score}", True, (255, 255, 255))
    additional_score_text = font.render(f"AI Long-Term Heuristic: {additional_score}", True, (255, 255, 255))
    screen.blit(score_text, (325, 650))
    screen.blit(additional_score_text, (325, 680))

    # Redraw the UI buttons
    start_button, reset_button = draw_ui_elements(screen, heuristic_score, additional_score)

    # Update the display
    pygame.display.flip()

    return start_button, reset_button


# This function is no longer being used.
def add_to_score(piece_captured, heuristic_score, additional_score):
    if piece_captured.color == 'black':
        additional_score += piece_captured.value
    elif piece_captured.color == 'white':
        heuristic_score += piece_captured.value
    return heuristic_score, additional_score
