from movement import is_valid_move, remove_piece_at_position
from piece import *
import random


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


def evaluate_board(board_matrix, color, move, pieces, captured_piece):
    print("--------- DEBUG: Inside evaluate_board() -----------------")
    # Initialize the total evaluation score
    score = 0

    # Evaluate mobility score
    mobility_score = evaluate_mobility(board_matrix, color, pieces)
    print(f"Mobility Score: {mobility_score}")
    score += mobility_score

    # Evaluate capture score
    capture_score = evaluate_captures(board_matrix, color, move, pieces, captured_piece)
    print(f"Capture Score: {capture_score}")
    score += capture_score

    # Adding a small random value to the score to prevent oscillating between two states
    score += random.uniform(-0.5, 0.5)

    # Round the score to 1 decimal places
    score = round(score, 1)

    print("--------- DEBUG: Ending evaluate_board() -----------------", score)
    # Return the total evaluation score
    return score


# This function sums up all the possible moves for the color. A weight is added to decrease the influence.
def evaluate_mobility(board_matrix, color, pieces):
    evaluation = 0
    mobility_weight = 0.05

    moves = generate_moves(board_matrix, color, pieces)
    move_count = len(moves)

    if color == 'white':
        evaluation += move_count * mobility_weight
    elif color == 'black':
        evaluation += move_count * mobility_weight

    return evaluation


def evaluate_captures(board_matrix, color, move, pieces, captured_piece):
    evaluation = 0
    capture_weight = 1

    source_col, source_row, target_col, target_row = move
    target_cell = captured_piece

    if target_cell != " ":
        target_piece = get_piece_by_position(target_col, target_row, pieces)
        if target_piece is not None:
            # When AI is black, it will try to maximize evaluation, hence, white captures are [+]
            # if target_cell.isupper() == (color == 'white'): # white was maximizing as color refers to the curr piece
            print("Target Cell is: ", target_cell, " and target color is: ", target_piece.color,
                  " and the target value is: ", target_piece.value)
            if target_cell.isupper() == (target_piece.color == 'white'):
                evaluation += target_piece.value  # now black is maximizing
            elif target_cell.islower() == (target_piece.color == 'black'):
                # evaluation -= target_piece.value # black minimizing
                evaluation -= target_piece.value  # now white minimizing

    return evaluation * capture_weight


def get_piece_by_position(x, y, pieces):
    # print("--------- DEBUG: Inside get_piece_by_position() -----------------")
    for piece in pieces:
        if piece.x == x and piece.y == y:
            # print("--------- DEBUG: Ending get_piece_by_position() -----------------")
            return piece

    # print("--------- DEBUG: Ending get_piece_by_position() -----------------")
    return None


def generate_moves(board_matrix, color, pieces):
    print("--------- DEBUG: Inside generate_moves() -----------------")
    moves = []
    for col in range(8):
        for row in range(8):
            piece_symbol = board_matrix[row][col]
            if piece_symbol != ' ' and (piece_symbol.islower() == (color == 'black')):
                piece_moves = generate_piece_moves(board_matrix, col, row, pieces)
                moves.extend(piece_moves)

    print(f"--------- DEBUG: Ending generate_moves() -----------------")
    return moves


def generate_piece_moves(board_matrix, col, row, pieces):
    # print("--------- DEBUG: Inside generate_piece_moves() -----------------")
    piece_symbol = board_matrix[row][col]
    color = 'white' if piece_symbol.isupper() else 'black'
    piece_type = piece_symbol.lower()

    piece = Piece(color, col, row, piece_type, None)
    moves = []

    for target_col in range(8):
        for target_row in range(8):
            if is_valid_move(piece, target_col, target_row, pieces):
                moves.append((col, row, target_col, target_row))

    # print("--------- DEBUG: Ending generate_piece_moves() -----------------")
    return moves


def apply_move(board_matrix, move):
    print("--------- DEBUG: Inside apply_move() -----------------")
    start_col, start_row, end_col, end_row = move
    moving_piece = board_matrix[start_row][start_col]
    captured_piece = board_matrix[end_row][end_col]  # Store the captured piece
    print("Moving Piece is: ", moving_piece)
    print("Captured Piece is: ", captured_piece)
    board_matrix[end_row][end_col] = moving_piece
    board_matrix[start_row][start_col] = ' '
    print_board_matrix(board_matrix)

    print("--------- DEBUG: Ending apply_move() -----------------")
    return captured_piece


# The function reverses the move by moving the piece back to its original position
# used for calculating reversing possible states when building minimax tree
def unapply_move(board_matrix, move, captured_piece):
    print("--------- DEBUG: Inside unapply_move() -----------------")
    start_col, start_row, end_col, end_row = move
    board_matrix[start_row][start_col] = board_matrix[end_row][end_col]
    board_matrix[end_row][end_col] = captured_piece
    print("--------- DEBUG: Ending unapply_move() -----------------")

    return board_matrix


def minimax(board_matrix, depth, is_maximizing_player, alpha, beta, color, move, pieces, captured_piece):
    print("--------- DEBUG: Inside minimax() -----------------")
    if depth == 0:
        return evaluate_board(board_matrix, color, move, pieces, captured_piece)

    captured_piece = apply_move(board_matrix, move)
    opponent_color = 'white' if color == 'black' else 'black'
    moves = generate_moves(board_matrix, opponent_color, pieces)

    if is_maximizing_player:
        max_eval = float('-inf')
        for next_move in moves:
            eval = minimax(board_matrix, depth - 1, False, alpha, beta, opponent_color, next_move, pieces,
                           captured_piece)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

    else:
        min_eval = float('inf')
        for next_move in moves:
            eval = minimax(board_matrix, depth - 1, True, alpha, beta, opponent_color, next_move, pieces,
                           captured_piece)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

    unapply_move(board_matrix, move, captured_piece)
    print("--------- DEBUG: Ending minimax() -----------------")
    return max_eval if is_maximizing_player else min_eval


def find_best_move(board_matrix, depth, color, pieces):
    print("--------- DEBUG: Inside find_best_move()-----------------")
    best_move = None
    # best_eval = float('-inf') if color == 'white' else float('inf') # Black min, White max
    best_eval = float('inf') if color == 'white' else float('-inf')  # Black max, White min
    best_short_term_eval = 0
    best_long_term_eval = 0

    moves = generate_moves(board_matrix, color, pieces)
    print("Generated Moves:", moves)

    for move in moves:
        captured_piece = apply_move(board_matrix, move)
        opponent_color = 'white' if color == 'black' else 'black'

        # Evaluate capture score for the next move
        capture_score = evaluate_captures(board_matrix, color, move, pieces, captured_piece)

        # Call minimax to calculate the best move in the future
        eval = minimax(board_matrix, depth - 1, color == 'black', float('-inf'), float('inf'), opponent_color, move,
                       pieces, captured_piece)

        # Combine capture score and minimax evaluation
        total_eval = capture_score + eval

        unapply_move(board_matrix, move, captured_piece)

        # if color == 'white' and total_eval > best_eval:  # Black min, White max
        if color == 'white' and total_eval < best_eval:
            best_move = move
            best_eval = total_eval
            best_short_term_eval = capture_score
            best_long_term_eval = eval
        # elif color == 'black' and total_eval < best_eval: # Black min, White max
        elif color == 'black' and total_eval > best_eval:
            best_move = move
            best_eval = total_eval
            best_short_term_eval = capture_score
            best_long_term_eval = eval

        print(f"Move {move} evaluated as {total_eval}")

    print("Short-Term Heuristic Score: ", best_short_term_eval)
    print("Long-Term Heuristic Score: ", best_long_term_eval)
    print(f"Move {move} total evaluated as {total_eval}")

    print("--------- DEBUG: Ending find_best_move()-----------------")
    return best_move, best_eval, best_short_term_eval, best_long_term_eval

def print_board_matrix(board_matrix):
    print("Current board matrix:")
    for row in board_matrix:
        print(row)
    print()
