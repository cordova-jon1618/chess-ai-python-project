import pygame
from board import *
from piece import *
from movement import *
from game_logic import *
from algorithm import *


# Notes: We will not implement the following chess functionality
# No castling by King and Rook
# No winning conditions as this project is to show the AI Chess functionality

def initialize_chess_game():
    chess_board = Board()
    board, screen = chess_board.make_board()

    chess_piece = Piece(None, None, None, None, None)
    pieces_array, white_pieces_array, black_pieces_array = chess_piece.place_pieces_on_board(board, screen)

    running = True
    selected_piece = None
    # heuristic_score = 0  # Initialize heuristic score
    # additional_score = 0  # Initialize additional score


    # IMPORTANT: THE AI ALWAYS PLAYS AS BLACK, WHEN BUILDING A MINIMAX TREE, THE LAST LEVEL IS ODD FOR WHITE AND EVEN
    #           FOR BLACK, TO RETURN THE LONG-TERM HEURISTIC FOR BLACK, MAKE SURE THE DEPTH IS AN EVEN NUMBER.
    depth = 2  # Set the depth of the search tree


    player_color = "black"  # Set AI color (This should be set to "black")

    short_term_heuristic = 0  # Initialize ST heuristic score
    long_term_heuristic = 0  # Initialize LT heuristic score

    # Declare and initialize the board_matrix
    board_matrix = board_to_matrix(pieces_array)

    while running:

        # start_button, reset_button = draw_ui_elements(screen, heuristic_score, additional_score)
        start_button, reset_button = draw_ui_elements(screen, short_term_heuristic, long_term_heuristic)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            # Handling mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Round the scores to 2 decimal places
                # heuristic_score = round(heuristic_score, 1)
                # additional_score = round(additional_score, 1)
                short_term_heuristic = round(short_term_heuristic, 1)
                long_term_heuristic = round(long_term_heuristic, 1)

                # Check if the start or reset button was clicked
                if start_button.collidepoint(event.pos):
                    print("Start button clicked")
                    best_move, best_eval, short_term_heuristic, long_term_heuristic = find_best_move(board_matrix, depth, player_color, pieces_array)
                    print(f"Best move: ({best_move[0]}, {best_move[1]}) -> ({best_move[2]}, {best_move[3]})")
                    print("Best eval:", best_eval)
                    board = matrix_to_board(board_matrix)

                    # Highlight the original position and best move with red
                    highlighted_squares = [(best_move[0], best_move[1]), (best_move[2], best_move[3])]

                    # Redraw the board and pieces with highlighted squares (Before Move)
                    redraw_pieces_on_board_with_red_highlight(pieces_array, board, screen, highlighted_squares)
                    # start_button, reset_button = update_UI_view(screen, heuristic_score, additional_score)
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Wait for some time
                    pygame.time.delay(500)

                    # Update the pieces_array and board_matrix after the move is made
                    pieces_array = update_pieces_array(pieces_array, best_move)
                    board_matrix = board_to_matrix(pieces_array)

                    # Redraw the board and pieces with highlighted squares (After Move)
                    redraw_pieces_on_board_with_red_highlight(pieces_array, board, screen, highlighted_squares)
                    # start_button, reset_button = update_UI_view(screen, heuristic_score, additional_score)
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Wait for some time
                    pygame.time.delay(500)

                    # Update UI WITHOUT the red highlight
                    redraw_pieces_on_board(pieces_array, board, screen)

                    # Update Heuristic Score
                    # heuristic_score += best_eval

                    # Round the scores to 2 decimal places
                    # heuristic_score = round(heuristic_score, 1)
                    # additional_score = round(additional_score, 1)

                    # Update UI buttons and score
                    # start_button, reset_button = update_UI_view(screen, heuristic_score, additional_score)
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)


                elif reset_button.collidepoint(event.pos):
                    print("Reset button clicked")
                    # Clear the board and reset the game
                    chess_board.reset_board(board)
                    pieces_array, white_pieces_array, black_pieces_array = chess_piece.place_pieces_on_board(board,
                                                                                                             screen)

                    # Reset the board_matrix based on the reset pieces_array
                    board_matrix = board_to_matrix(pieces_array)

                    selected_piece = None
                    heuristic_score = 0
                    additional_score = 0
                    short_term_heuristic = 0
                    long_term_heuristic = 0
                    # start_button, reset_button = update_UI_view(screen, heuristic_score, additional_score)
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                else:
                    # Handle piece mouse click events

                    short_term_heuristic = 0
                    long_term_heuristic = 0

                    # selected_piece, pieces_array, heuristic_score, additional_score, board_matrix = handle_mouse_click(
                    #     event, pieces_array, board, screen,
                    #     selected_piece, heuristic_score, additional_score)
                    selected_piece, pieces_array, short_term_heuristic, long_term_heuristic, board_matrix = handle_mouse_click(event, pieces_array, board, screen, selected_piece, short_term_heuristic, long_term_heuristic)

                    # ------------------------------------------------
                    # Print the updated board_matrix for debugging
                    # ------------------------------------------------
                    # print_board_matrix(board_matrix)
                    # Round the scores to 2 decimal places
                    # heuristic_score = round(heuristic_score, 1)
                    # additional_score = round(additional_score, 1)

                    # Update UI buttons
                    # start_button, reset_button = update_UI_view(screen, heuristic_score, additional_score)
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

        pygame.display.flip()


# def print_board_matrix(board_matrix):
#     print("Current board matrix:")
#     for row in board_matrix:
#         print(row)
#     print()


def update_pieces_array(pieces_array, move):
    start_x, start_y, end_x, end_y = move

    # Remove the existing piece at the target location
    pieces_array, _, _ = remove_piece_at_position(pieces_array, end_x, end_y, 0, 0)

    # Move the selected piece to the new location
    for piece in pieces_array:
        if piece.x == start_x and piece.y == start_y:
            piece.x = end_x
            piece.y = end_y
            break

    return pieces_array


def main():
    initialize_chess_game()


if __name__ == "__main__":
    main()
