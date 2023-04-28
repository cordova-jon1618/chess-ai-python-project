import pygame
from board import *
from piece import *
from movement import *
from user_interface import *
from algorithm import *


# Chess AI Python Project for COMP 469: Intro to Artificial Intelligence
# Authors:
# Jonathan Cordova and Alvaro Lopez-Romero
# California State University Northridge (CSUN)


# NOTE:  We will not implement the following chess functionality:
#        No castling by King and Rook
#        No winning conditions as this project is to showcase our AI Chess functionality

def initialize_chess_game():

    # Declare Board object
    chess_board = Board()
    # Make board and screen
    board, screen = chess_board.make_board()
    # Declare Piece object
    chess_piece = Piece(None, None, None, None, None)

    # Returns the pieces array of black and white, we are no longer using the other return arrays
    pieces_array, _, _ = chess_piece.place_pieces_on_board(board, screen)

    running = True
    selected_piece = None

    # NOTE:     The AI is set to play as black, when updating the 'depth' variable, keep in mind that when
    #           building a minimax tree, the last level of the tree is odd for white and even for black. Please keep
    #           depth as an even number in order for the last level to return the long-term heuristic for black into
    #           the UI interface.

    depth = 2  # Set the depth of the search tree

    player_color = "black"  # Set AI color (This should be set to "black")

    short_term_heuristic = 0  # Initialize ST heuristic score
    long_term_heuristic = 0  # Initialize LT heuristic score

    # Declare and initialize the board_matrix
    board_matrix = board_to_matrix(pieces_array)

    # while the UI chess board window is not closed
    while running:

        # Drawing UI elements
        start_button, reset_button = draw_ui_elements(screen, short_term_heuristic, long_term_heuristic)

        # if window is closed, then stop program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            # Handling mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Round the scores to 1 decimal place
                short_term_heuristic = round(short_term_heuristic, 1)
                long_term_heuristic = round(long_term_heuristic, 1)

                # Check if the start or reset button is clicked
                if start_button.collidepoint(event.pos):
                    print("Start button clicked.")

                    # Find Best Move function is called, this will start the minimax algorithm
                    best_move, best_eval, short_term_heuristic, long_term_heuristic = find_best_move(board_matrix,
                                                                                                     depth,
                                                                                                     player_color,
                                                                                                     pieces_array)
                    print(f"Best move: ({best_move[0]}, {best_move[1]}) -> ({best_move[2]}, {best_move[3]})")
                    print("Best eval:", best_eval)

                    # Turns the matrix array into a board object
                    board = matrix_to_board(board_matrix)

                    # Highlight the original position and AI's best move with red highlight
                    highlighted_squares = [(best_move[0], best_move[1]), (best_move[2], best_move[3])]

                    # Redraw the board and pieces with highlighted squares (Before AI's Best Move is applied)
                    redraw_pieces_on_board_with_red_highlight(pieces_array, board, screen, highlighted_squares)

                    # Update UI view
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Wait for some time
                    pygame.time.delay(500)

                    # Update the pieces_array and board_matrix after the move is made
                    pieces_array = update_pieces_array(pieces_array, best_move)
                    board_matrix = board_to_matrix(pieces_array)

                    # Redraw the board and pieces with highlighted squares (After AI's Best Move is applied)
                    redraw_pieces_on_board_with_red_highlight(pieces_array, board, screen, highlighted_squares)
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Wait for some time
                    pygame.time.delay(500)

                    # Update UI WITHOUT the red highlight
                    redraw_pieces_on_board(pieces_array, board, screen)

                    # Update UI buttons and score
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Print for debug
                    print_board_matrix(board_matrix)

                elif reset_button.collidepoint(event.pos):
                    print("Reset button clicked.")

                    # Clear the board and reset the game
                    chess_board.reset_board(board)
                    pieces_array, _, _ = chess_piece.place_pieces_on_board(board, screen)

                    # Reset the board_matrix based on the reset pieces_array
                    board_matrix = board_to_matrix(pieces_array)

                    selected_piece = None
                    short_term_heuristic = 0
                    long_term_heuristic = 0
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Print for debug
                    print_board_matrix(board_matrix)

                else:
                    # Handles User's mouse piece move events
                    short_term_heuristic = 0
                    long_term_heuristic = 0

                    selected_piece, pieces_array, short_term_heuristic, long_term_heuristic, board_matrix = handle_mouse_click(
                        event, pieces_array, board, screen, selected_piece, short_term_heuristic, long_term_heuristic)

                    # Update UI buttons
                    start_button, reset_button = update_UI_view(screen, short_term_heuristic, long_term_heuristic)

                    # Print for debug
                    print_board_matrix(board_matrix)

        pygame.display.flip()


def update_pieces_array(pieces_array, move):
    start_x, start_y, end_x, end_y = move

    # Remove the existing piece at the target location, no longer passing scores here, so using 0, 0 as last parameters
    pieces_array, _, _ = remove_piece_at_position(pieces_array, end_x, end_y, 0, 0)

    # Move the selected piece to the new location
    for piece in pieces_array:
        if piece.x == start_x and piece.y == start_y:
            piece.x = end_x
            piece.y = end_y
            break

    # Returns new updated pieces_array
    return pieces_array


def main():
    # Starts everything
    initialize_chess_game()


if __name__ == "__main__":
    main()
