from movement import *
from piece import *
import random


# Chess AI Python Project for COMP 469: Intro to Artificial Intelligence
# Authors:
# Jonathan Cordova and Alvaro Lopez-Romero
# California State University Northridge (CSUN)

# NOTE:  This algorithm.py file contains the core functionality for this program, including
#        the minimax algorithm, find_best_move function that calls the minimax, the evaluation functions,
#        a brunch of helper functions, functions such as generate_move that generate all possible moves at the
#        current board state for a color, functions such as apply_move and unapply_move to change the board state
#        in order to go deeper into the minimax tree, then reverse the board states afterwards.


# Helper function
def print_pieces_array(pieces):
    print("-----------------------------------------------")
    for p in pieces:
        print("Selected Piece is: ", p.color + " " + p.type + " " + str(p.value))
    print("-----------------------------------------------")


# Helper function
def print_piece_info(p):
    print("-----------------------------------------------")
    print("This is the piece found to be moved. X=",
          str(p.x) + " Y=" + str(p.y) + " color=" + p.color + " type=" + p.type + " value=" + str(p.value) + ". ")
    print("-----------------------------------------------")


# This function takes the capture score and mobility score for the board state and calculates an evaluation.
# This is first called when the minimax algorithm reaches the bottom of the tree.
def evaluate_board(board_matrix, color, move, pieces, captured_piece):
    # Initialize the total evaluation score
    score = 0

    # Evaluate mobility score
    mobility_score = evaluate_mobility(board_matrix, color, pieces)
    mobility_score = round(mobility_score, 1)
    print(f"Mobility Score: {mobility_score}")
    score += mobility_score

    # Evaluate capture score
    capture_score = evaluate_captures(board_matrix, color, move, pieces, captured_piece)
    print(f"Capture Score: {capture_score}")
    score += capture_score

    # Adding a small random value to the score to prevent oscillating between two states
    # This avoids the potential of local minimum or local maximum
    score += random.uniform(-0.5, 0.5)

    # Round the score to 1 decimal places
    score = round(score, 1)

    print("Evaluated Color at bottom of tree is: ", color)
    # Return the total evaluation score
    return score, color


# This function sums up all the possible moves for the color. A weight is added to decrease the influence.
def evaluate_mobility(board_matrix, color, pieces):
    evaluation = 0
    mobility_weight = 0.05  # We do not want this score to have significant influence

    # Generates possible moves for the board state so algorithm can calculate a mobility score
    moves = generate_moves(board_matrix, color, pieces)
    move_count = len(moves)

    # Evaluation is a positive number for both because the min and max comparison
    # are taken care during the minimax traversal.
    if color == 'black':
        # Black will try to MAXIMIZE this evaluation score in the minimax algorithm (AI is black maximizing)
        evaluation += move_count * mobility_weight
    elif color == 'white':
        # Black will try to MINIMIZE this evaluation score in the minimax algorithm (AI is white minimizing)
        evaluation += move_count * mobility_weight

    return evaluation


# This function calculates the value of capturing a piece during the board state
def evaluate_captures(board_matrix, color, move, pieces, captured_piece):
    evaluation = 0
    capture_weight = 1

    source_col, source_row, target_col, target_row = move
    target_cell = captured_piece

    if target_cell != " ":
        target_piece = get_piece_by_position(target_col, target_row, pieces)
        if target_piece is not None:
            print("Target Cell is: ", target_cell, " and target color is: ", target_piece.color,
                  " and the target value is: ", target_piece.value)
            if target_cell.isupper() == (target_piece.color == 'white'):
                # Black will try to MAXIMIZE this evaluation score in the minimax algorithm (AI is black maximizing)
                evaluation += target_piece.value
            elif target_cell.islower() == (target_piece.color == 'black'):
                # Black will try to MINIMIZE this evaluation score in the minimax algorithm (AI is white minimizing)
                evaluation += target_piece.value

    return evaluation * capture_weight


# Helper function, gets the piece information by the positive X, Y passed as parameter
def get_piece_by_position(x, y, pieces):
    for piece in pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


# generate all possible moves at the
#        current board state for a color
# def generate_moves(board_matrix, color, pieces):
#     moves = []
#     for col in range(8):
#         for row in range(8):
#             piece_symbol = board_matrix[row][col]
#
#             # The reason we are restricting only to black is that the AI is controlling black pieces only
#             if piece_symbol != ' ' and (piece_symbol.islower() == (color == 'black')):
#                 piece_moves = generate_piece_moves(board_matrix, col, row, pieces)
#                 moves.extend(piece_moves)
#     return moves


# This function generate moves for the white pieces as well as AI's black pieces
# allowing the minimax algorithm to correctly evaluate the game tree for both sides.
def generate_moves(board_matrix, color, pieces):
    moves = []
    for col in range(8):
        for row in range(8):
            piece_symbol = board_matrix[row][col]

            # Check if the piece_symbol is of the same color as specified
            if piece_symbol != ' ' and (piece_symbol.islower() == (color == 'black')) or (
                    piece_symbol.isupper() == (color == 'white')):
                piece_moves = generate_piece_moves(board_matrix, col, row, pieces)
                moves.extend(piece_moves)
    return moves


# generate all possible moves at the
#        current board state for a piece
def generate_piece_moves(board_matrix, col, row, pieces):
    piece_symbol = board_matrix[row][col]
    color = 'white' if piece_symbol.isupper() else 'black'
    piece_type = piece_symbol.lower()

    piece = Piece(color, col, row, piece_type, None)
    moves = []

    for target_col in range(8):
        for target_row in range(8):
            if is_valid_move(piece, target_col, target_row, pieces):
                moves.append((col, row, target_col, target_row))

    return moves


# This function we are using for the mobility evaluation only


# This function applies a move to the board_matrix to calculate the next level nodes in the tree
def apply_move(board_matrix, move):
    start_col, start_row, end_col, end_row = move

    # Gets moving piece
    moving_piece = board_matrix[start_row][start_col]

    # Gets captured piece (if any)
    captured_piece = board_matrix[end_row][end_col]
    print("Moving Piece is: ", moving_piece)
    print("Captured Piece is: ", captured_piece)

    # Updates board state
    board_matrix[end_row][end_col] = moving_piece
    board_matrix[start_row][start_col] = ' '

    # Debugging
    # print_board_matrix(board_matrix)

    return captured_piece


# The function reverses the move by moving the piece back to its original position
# used for calculating reversing possible states when building minimax tree
def unapply_move(board_matrix, move, captured_piece):
    start_col, start_row, end_col, end_row = move
    # Reverses the move by moving the piece back to its original position
    # Used for calculating reversing possible states when building minimax tree
    board_matrix[start_row][start_col] = board_matrix[end_row][end_col]
    board_matrix[end_row][end_col] = captured_piece

    return board_matrix


# Minimax Algorithm
def minimax(board_matrix, depth, is_maximizing_player, alpha, beta, color, move, pieces, captured_piece):
    # Base case: if depth is 0, reaching the bottom of the minimax tree, evaluate the board and return the evaluation
    if depth == 0:
        return evaluate_board(board_matrix, color, move, pieces, captured_piece)

    # Apply the move and store the captured piece
    captured_piece = apply_move(board_matrix, move)
    # Determine the opponent's color, this switches between colors at each level down the tree
    opponent_color = 'white' if color == 'black' else 'black'
    moves = generate_moves(board_matrix, opponent_color, pieces)

    if is_maximizing_player:
        max_eval = float('-inf')
        max_color = None
        for next_move in moves:
            # Recursively call minimax for each move and update evaluation and color
            eval, curr_color = minimax(board_matrix, depth - 1, False, alpha, beta, opponent_color, next_move, pieces,
                                       captured_piece)
            if eval > max_eval:
                max_eval = eval
                max_color = curr_color
                print("max_color is: ", max_color)
            # Update alpha for alpha-beta pruning
            alpha = max(alpha, eval)
            # Prune if necessary
            if beta <= alpha:
                break

    else:
        min_eval = float('inf')
        min_color = None
        for next_move in moves:
            # Recursively call minimax for each move and update evaluation and color
            eval, curr_color = minimax(board_matrix, depth - 1, True, alpha, beta, opponent_color, next_move, pieces,
                                       captured_piece)
            if eval < min_eval:
                min_eval = eval
                min_color = curr_color
                print("min_color is: ", min_color)
            # Update beta for alpha-beta pruning
            beta = min(beta, eval)
            # Prune if necessary
            if beta <= alpha:
                break

    # Undo the move and restore the captured piece
    unapply_move(board_matrix, move, captured_piece)

    # Return the best evaluation and the color associated with it
    return (max_eval, color) if is_maximizing_player else (min_eval, color)


def find_best_move(board_matrix, depth, color, pieces):
    best_move = None
    best_eval = float('inf') if color == 'white' else float('-inf')  # Black max, White min
    best_short_term_eval = 0
    best_long_term_eval = 0
    # base_eval_color = None

    moves = generate_moves(board_matrix, color, pieces)
    print("Generated Moves:", moves)

    for move in moves:
        captured_piece = apply_move(board_matrix, move)
        opponent_color = 'white' if color == 'black' else 'black'

        # Evaluate capture score for the next move
        capture_score = evaluate_captures(board_matrix, color, move, pieces, captured_piece)

        # Call minimax to calculate the best move in the future
        eval, eval_color = minimax(board_matrix, depth - 1, color == 'black', float('-inf'), float('inf'),
                                   opponent_color, move, pieces, captured_piece)

        # Combine capture score and minimax evaluation
        total_eval = capture_score + eval

        # The eval_color only tells what color was the previous level, no real value in logging it
        # print(f"Move {move} eval {eval}, capture score {capture_score},
        # evaluated {total_eval} prev color {eval_color}")

        unapply_move(board_matrix, move, captured_piece)

        # if color == 'white' and total_eval > best_eval:  # Black min, White max
        if color == 'white' and total_eval < best_eval: # Black max, White min
            best_move = move
            best_eval = total_eval
            best_short_term_eval = capture_score
            best_long_term_eval = eval
        # elif color == 'black' and total_eval < best_eval: # Black min, White max
        elif color == 'black' and total_eval > best_eval: # Black max, White min
            best_move = move
            best_eval = total_eval
            best_short_term_eval = capture_score
            best_long_term_eval = eval

    print("Short-Term Heuristic Score: ", best_short_term_eval)
    print("Long-Term Heuristic Score: ", best_long_term_eval)
    print(f"Move {move} total evaluated as {total_eval}")

    return best_move, best_eval, best_short_term_eval, best_long_term_eval


def print_board_matrix(board_matrix):
    print("Current board matrix:")
    for row in board_matrix:
        print(row)
    print()
