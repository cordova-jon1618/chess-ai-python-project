import pygame


def draw_ui_elements(screen, heuristic_score, additional_score):
    font_name = "calibri"
    font = pygame.font.SysFont(font_name, 24)
    # font = pygame.font.Font(None, 28)
    bold_font = pygame.font.SysFont(font_name, 24)  # Create a separate font for bold text
    bold_font.set_bold(True)  # Make the bold_font bold

    start_button = pygame.Rect(50, 665, 100, 50)
    reset_button = pygame.Rect(200, 665, 100, 50)

    start_text = bold_font.render("Start", True, (255, 255, 255))
    reset_text = bold_font.render("Reset", True, (255, 255, 255))

    score_text = font.render(f"AI Heuristic Score: {heuristic_score}", True, (255, 255, 255))
    additional_score_text = font.render(f"My Heuristic Score: {additional_score}", True, (255, 255, 255))

    # pygame.draw.rect(screen, (0, 255, 0), start_button)
    pygame.draw.rect(screen, (80, 240, 180), start_button)
    # pygame.draw.rect(screen, (255, 0, 0), reset_button)
    pygame.draw.rect(screen, (255, 127, 127), reset_button)

    start_text_x = start_button.x + (start_button.width - start_text.get_width()) // 2
    start_text_y = start_button.y + (start_button.height - start_text.get_height()) // 2
    reset_text_x = reset_button.x + (reset_button.width - reset_text.get_width()) // 2
    reset_text_y = reset_button.y + (reset_button.height - reset_text.get_height()) // 2

    screen.blit(start_text, (start_text_x, start_text_y))
    screen.blit(reset_text, (reset_text_x, reset_text_y))
    screen.blit(score_text, (375, 650))
    screen.blit(additional_score_text, (375, 680))

    return start_button, reset_button


def update_UI_view(screen, heuristic_score, additional_score):
    font_name = "calibri"
    font = pygame.font.SysFont(font_name, 24)
    # font = pygame.font.Font(None, 28)
    bold_font = pygame.font.SysFont(font_name, 24)  # Create a separate font for bold text
    bold_font.set_bold(True)  # Make the bold_font bold

    # Clear the area where the scores are displayed
    pygame.draw.rect(screen, (0, 0, 0), (375, 650, 250, 50))
    pygame.draw.rect(screen, (0, 0, 0), (375, 680, 250, 50))

    # Redraw the score text with the new values
    score_text = font.render(f"AI Heuristic Score: {heuristic_score}", True, (255, 255, 255))
    additional_score_text = font.render(f"My Heuristic Score: {additional_score}", True, (255, 255, 255))
    screen.blit(score_text, (375, 650))
    screen.blit(additional_score_text, (375, 680))

    # Redraw the UI buttons
    start_button, reset_button = draw_ui_elements(screen, heuristic_score, additional_score)

    # Update the display
    pygame.display.flip()

    return start_button, reset_button


def add_to_score(piece_captured, heuristic_score, additional_score):
    if piece_captured.color == 'black':
        additional_score += piece_captured.value
    elif piece_captured.color == 'white':
        heuristic_score += piece_captured.value
    return heuristic_score, additional_score
