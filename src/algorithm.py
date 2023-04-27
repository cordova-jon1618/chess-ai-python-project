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


def evaluate_board(board_matrix, color, move, pieces):
    print("--------- DEBUG: Inside evaluate_board() -----------------")
    # Initialize the total evaluation score
    score = 0

    # # Evaluate material score
    # material_score = evaluate_material(board_matrix, color, pieces)
    # print(f"Material Score: {material_score}")
    # score += material_score
    #
    # # Evaluate mobility score
    # mobility_score = evaluate_mobility(board_matrix, color, pieces)
    # print(f"Mobility Score: {mobility_score}")
    # score += mobility_score
    #
    # # Evaluate control score
    # control_score = evaluate_control(board_matrix, color, pieces)
    # print(f"Control Score: {control_score}")
    # score += control_score

    # Evaluate capture score
    capture_score = evaluate_captures(board_matrix, color, move, pieces)
    print(f"Capture Score: {capture_score}")
    score += capture_score

    # Adding a small random value to the score to prevent oscillating between two states
    # score += random.uniform(-0.5, 0.5)

    # Round the score to 2 decimal places
    # score = round(score, 2)

    print("--------- DEBUG: Ending evaluate_board() -----------------", score)
    # Return the total evaluation score
    return score


def evaluate_board(board_matrix, color, move, pieces):
    score = 0

    # Evaluate capture score
    capture_score = evaluate_captures(board_matrix, color, move, pieces)
    print(f"Capture Score: {capture_score}")
    score += capture_score

    return score


def evaluate_material(board_matrix, color, pieces):
    evaluation = 0
    material_weight = 1

    for row in board_matrix:
        for cell in row:
            if cell != " ":
                piece = get_piece_by_position(cell[1], cell[0], pieces)
                if piece is not None:
                    if piece.type.isupper() == (color == 'white'):
                        evaluation += piece.value * material_weight
                    else:
                        evaluation -= piece.value * material_weight
    return evaluation


def evaluate_mobility(board_matrix, color, pieces):
    evaluation = 0
    mobility_weight = 0.05

    moves = generate_moves(board_matrix, color, pieces)
    move_count = len(moves)

    if color == 'white':
        evaluation += move_count * mobility_weight
    else:
        evaluation -= move_count * mobility_weight

    return evaluation


def evaluate_control(board_matrix, color, pieces):
    evaluation = 0
    control_weight = 0.05

    white_controlled_squares, black_controlled_squares = count_controlled_squares(board_matrix, pieces)

    if color == 'white':
        evaluation += (white_controlled_squares - black_controlled_squares) * control_weight
    else:
        evaluation -= (white_controlled_squares - black_controlled_squares) * control_weight

    return evaluation


def evaluate_captures(board_matrix, color, move, pieces):
    evaluation = 0
    capture_weight = 1

    source_col, source_row, target_col, target_row = move
    target_cell = board_matrix[target_row][target_col]

    if target_cell != " ":
        target_piece = get_piece_by_position(target_col, target_row, pieces)
        if target_piece is not None:
            if target_cell.isupper() == (color == 'white'):
                evaluation += target_piece.value
            else:
                evaluation -= target_piece.value

    return evaluation * capture_weight


def count_controlled_squares(board_matrix, pieces):
    # print("--------- DEBUG: Inside count_controlled_squares() -----------------")
    white_controlled_squares = 0
    black_controlled_squares = 0

    for row in range(8):
        for col in range(8):
            if is_controlled_square(board_matrix, col, row, 'white', pieces):
                white_controlled_squares += 1
            elif is_controlled_square(board_matrix, col, row, 'black', pieces):
                black_controlled_squares += 1

    # print("--------- DEBUG: Ending count_controlled_squares() -----------------")
    return white_controlled_squares, black_controlled_squares


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
    start_row, start_col, end_row, end_col = move
    moving_piece = board_matrix[start_row][start_col]
    captured_piece = board_matrix[end_row][end_col]  # Store the captured piece
    board_matrix[end_row][end_col] = moving_piece
    board_matrix[start_row][start_col] = ' '

    print("--------- DEBUG: Ending apply_move() -----------------")
    return captured_piece


# The function reverses the move by moving the piece back to its original position
# used for calculating reversing possible states when building minimax tree
def unapply_move(board_matrix, move, captured_piece):
    print("--------- DEBUG: Inside unapply_move() -----------------")
    start_row, start_col, end_row, end_col = move
    board_matrix[start_row][start_col] = board_matrix[end_row][end_col]
    board_matrix[end_row][end_col] = captured_piece
    print("--------- DEBUG: Ending unapply_move() -----------------")

    return board_matrix


# def minimax(board_matrix, depth, is_maximizing_player, alpha, beta, color, pieces):
#     if depth == 0:
#         return evaluate_board(board_matrix, color, pieces)
#
#     moves = generate_moves(board_matrix, color, pieces)
#
#     if is_maximizing_player:
#         max_eval = float('-inf')
#         for move in moves:
#             captured_piece = apply_move(board_matrix, move)
#             # the depth -1 calls the evaluation function once it reaches depth of 0
#             eval = minimax(board_matrix, depth - 1, False, alpha, beta, color, pieces)
#             unapply_move(board_matrix, move, captured_piece)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         # print("Max Eval:", max_eval)
#         return max_eval
#
#     else:
#         min_eval = float('inf')
#         for move in moves:
#             captured_piece = apply_move(board_matrix, move)
#             # the depth -1 calls the evaluation function once it reaches depth of 0
#             eval = minimax(board_matrix, depth - 1, True, alpha, beta, color, pieces)
#             unapply_move(board_matrix, move, captured_piece)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         # print("Min Eval:", min_eval)
#         return min_eval

def minimax(board_matrix, depth, is_maximizing_player, alpha, beta, color, move, pieces):
    print("--------- DEBUG: Inside minimax() -----------------")
    if depth == 0:
        return evaluate_board(board_matrix, color, move, pieces)

    captured_piece = apply_move(board_matrix, move)
    opponent_color = 'white' if color == 'black' else 'black'
    moves = generate_moves(board_matrix, opponent_color, pieces)

    if is_maximizing_player:
        max_eval = float('-inf')
        for next_move in moves:
            eval = minimax(board_matrix, depth - 1, False, alpha, beta, opponent_color, next_move, pieces)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

    else:
        min_eval = float('inf')
        for next_move in moves:
            eval = minimax(board_matrix, depth - 1, True, alpha, beta, opponent_color, next_move, pieces)
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
    best_eval = float('-inf') if color == 'white' else float('inf')
    best_short_term_eval = 0
    best_long_term_eval = 0

    moves = generate_moves(board_matrix, color, pieces)
    print("Generated Moves:", moves)

    for move in moves:
        captured_piece = apply_move(board_matrix, move)
        opponent_color = 'white' if color == 'black' else 'black'

        # Evaluate capture score for the next move
        capture_score = evaluate_captures(board_matrix, color, move, pieces)

        # Call minimax to calculate the best move in the future
        eval = minimax(board_matrix, depth - 1, color == 'black', float('-inf'), float('inf'), opponent_color, move,
                       pieces)

        # Combine capture score and minimax evaluation
        total_eval = capture_score + eval

        unapply_move(board_matrix, move, captured_piece)

        if color == 'white' and total_eval > best_eval:
            best_move = move
            best_eval = total_eval
            best_short_term_eval = capture_score
            best_long_term_eval = eval
        elif color == 'black' and total_eval < best_eval:
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



def update_pieces_array(selected_piece, grid_x, grid_y, pieces_array, board, screen, heuristic_score, additional_score):
    if selected_piece is None:
        print("Selected Piece is: ", selected_piece)
        for p in pieces_array:
            if p.x == grid_x and p.y == grid_y:
                selected_piece = p
                print_piece_info(selected_piece)
                redraw_pieces_on_board_with_green_highlight(pieces_array, board, screen, (grid_x, grid_y))
                break
    else:
        if selected_piece is not None:
            print("Current Selected Piece is: ", selected_piece.color + selected_piece.type)

        if is_valid_move(selected_piece, grid_x, grid_y, pieces_array):

            if selected_piece is not None:
                print("Current Selected Piece is: ", selected_piece.color + selected_piece.type)

            # Remove the existing piece at the target location
            pieces_array, heuristic_score, additional_score = remove_piece_at_position(pieces_array, grid_x, grid_y,
                                                                                       heuristic_score,
                                                                                       additional_score)

            # Move the selected piece to the new location
            selected_piece.x = grid_x
            selected_piece.y = grid_y

            # Update the selected_piece in the pieces list
            for i, p in enumerate(pieces_array):
                if p == selected_piece:
                    pieces_array[i] = selected_piece
                    break

            # Redraw the board with the updated pieces
            redraw_pieces_on_board(pieces_array, board, screen)

            return pieces_array, heuristic_score, additional_score

    return selected_piece, pieces_array, heuristic_score, additional_score


def heuristic_board_control(board_matrix, pieces):
    # Initialize scores to 0
    white_score = 0
    black_score = 0

    # Check each piece's position and add to the corresponding score
    for piece in pieces:
        if piece.color == "white":
            # Check the number of empty squares surrounding the piece
            empty_squares = 0
            for row in range(max(0, piece.y - 1), min(8, piece.y + 2)):
                for col in range(max(0, piece.x - 1), min(8, piece.x + 2)):
                    if board_matrix[row][col] == " ":
                        empty_squares += 1
            white_score += empty_squares
        else:
            # Check the number of empty squares surrounding the piece
            empty_squares = 0
            for row in range(max(0, piece.y - 1), min(8, piece.y + 2)):
                for col in range(max(0, piece.x - 1), min(8, piece.x + 2)):
                    if board_matrix[row][col] == " ":
                        empty_squares += 1
            black_score += empty_squares

    return white_score - black_score


def is_controlled_square(board_matrix, x, y, color, pieces):
    opp_color = 'white' if color == 'black' else 'black'
    opp_pieces = [p for p in pieces if p.color == opp_color]

    for p in opp_pieces:
        if p.type == 'pawn':
            if color == 'white' and x == p.x - 1 and (y == p.y - 1 or y == p.y + 1):
                return True
            elif color == 'black' and x == p.x + 1 and (y == p.y - 1 or y == p.y + 1):
                return True
        elif p.type == 'knight':
            if abs(x - p.x) == 2 and abs(y - p.y) == 1:
                return True
            elif abs(x - p.x) == 1 and abs(y - p.y) == 2:
                return True
        elif p.type == 'bishop':
            if abs(x - p.x) == abs(y - p.y):
                dx, dy = 1 if x < p.x else -1, 1 if y < p.y else -1
                for i in range(1, abs(x - p.x)):
                    if not is_valid_empty_square(board_matrix, p.x + i * dx, p.y + i * dy, pieces):
                        return False
                return True
        elif p.type == 'rook':
            if x == p.x:
                dy = 1 if y > p.y else -1
                for i in range(p.y + dy, y, dy):
                    if not is_valid_empty_square(board_matrix, x, i, pieces):
                        return False
                return True
            elif y == p.y:
                dx = 1 if x > p.x else -1
                for i in range(p.x + dx, x, dx):
                    if not is_valid_empty_square(board_matrix, i, y, pieces):
                        return False
                return True
        elif p.type == 'queen':
            if abs(x - p.x) == abs(y - p.y):
                dx, dy = 1 if x < p.x else -1, 1 if y < p.y else -1
                for i in range(1, abs(x - p.x)):
                    if not is_valid_empty_square(board_matrix, p.x + i * dx, p.y + i * dy, pieces):
                        return False
                return True
            elif x == p.x:
                dy = 1 if y > p.y else -1
                for i in range(p.y + dy, y, dy):
                    if not is_valid_empty_square(board_matrix, x, i, pieces):
                        return False
                return True
            elif y == p.y:
                dx = 1 if x > p.x else -1
                for i in range(p.x + dx, x, dx):
                    if not is_valid_empty_square(board_matrix, i, y, pieces):
                        return False
                return True
        elif p.type == 'king':
            if abs(x - p.x) <= 1 and abs(y - p.y) <= 1:
                return True

    return False


def is_valid_empty_square(board_matrix, x, y, pieces):
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    if board_matrix[y][x] != ' ':
        return False


def print_board_matrix(board_matrix):
    print("Current board matrix:")
    for row in board_matrix:
        print(row)
    print()
