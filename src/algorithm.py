from movement import is_valid_move, remove_piece_at_position


# def start_algorithms(pieces_array, board, screen, selected_piece, heuristic_score, additional_score):
#     # print_pieces_array(pieces_array)
#     handle_algebraic_notation_move('e2e3', pieces_array, board, screen, selected_piece, heuristic_score,
#                                    additional_score)
#     handle_algebraic_notation_move('e3e4', pieces_array, board, screen, selected_piece, heuristic_score,
#                                     additional_score)
#     # handle_algebraic_notation_move('Nd2', pieces_array, board, screen, selected_piece, heuristic_score,
#     #                                 additional_score)




def print_pieces_array(pieces):
    print("-----------------------------------------------")
    for p in pieces:
        print("Selected Piece is: ", p.color + " " + p.type + " " + str(p.value))
    print("-----------------------------------------------")


def print_piece_info(p):
    print("-----------------------------------------------")
    print("This is the piece found to be moved. X=",
          str(p.x) + " Y=" + str(p.y) + " color=" + p.color + " type=" + p.type + " value=" + str(p.value) + ". ")
    print("-----------------------------------------------")

# def algebraic_notation_to_coordinates(move):
#     # Convert the algebraic notation to grid coordinates
#     x = ord(move[0]) - ord('a')
#     y = int(move[1]) - 1
#     return x, y

# def algebraic_notation_to_coordinates(move):
#     # Check if the input contains a piece type and adjust the input string
#     if move[0].isupper():
#         move = move[1:]
#
#     # Convert the algebraic notation to grid coordinates
#     y = 7 - (int(move[1]) - 1)
#     x = ord(move[0]) - ord('a')
#
#     print(f"Calculated coordinates: x = {x}, y = {y}")
#     return x, y

# def handle_algebraic_notation_move(move, pieces_array, board, screen, selected_piece, heuristic_score,
#                                    additional_score):
#     # Get the initial and target positions from the move string
#     move_from = move[:2]
#     move_to = move[2:]
#
#     # Convert the algebraic notation to grid coordinates
#     print("From:")
#     grid_x_from, grid_y_from = algebraic_notation_to_coordinates(move_from)
#     print("To:")
#     grid_x_to, grid_y_to = algebraic_notation_to_coordinates(move_to)
#
#     # Get the selected_piece based on the initial position
#     for p in pieces_array:
#         if p.x == grid_x_from and p.y == grid_y_from:
#             selected_piece = p
#             print_piece_info(selected_piece)
#             break
#
#     if selected_piece is None:
#         print("No piece found at the initial position.")
#         return selected_piece, pieces_array, heuristic_score, additional_score
#
#     if is_valid_move(selected_piece, grid_x_to, grid_y_to, pieces_array):
#
#         # Remove the existing piece at the target location
#         pieces_array, heuristic_score, additional_score = remove_piece_at_position(pieces_array, grid_x_to, grid_y_to,
#                                                                                    heuristic_score, additional_score)
#
#         # Move the selected piece to the new location
#         selected_piece.x = grid_x_to
#         selected_piece.y = grid_y_to
#
#         # Update the selected_piece in the pieces list
#         for i, p in enumerate(pieces_array):
#             if p == selected_piece:
#                 pieces_array[i] = selected_piece
#                 break
#
#         # Redraw the board with the updated pieces
#         selected_piece.redraw_pieces_on_board(pieces_array, board, screen)
#
#     else:
#         print("Invalid move")
#
#     return selected_piece, pieces_array, heuristic_score, additional_score
