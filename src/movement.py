import pygame
from piece import *
from game_logic import add_to_score


def board_to_matrix(pieces_array):
    board_matrix = [[' ' for _ in range(8)] for _ in range(8)]

    for piece in pieces_array:
        row, col = piece.y, piece.x  # Assuming y corresponds to rows and x to columns
        board_matrix[row][col] = piece.type.upper() if piece.color == 'white' else piece.type.lower()

    return board_matrix


def handle_mouse_click(event, pieces_array, board, screen, selected_piece, heuristic_score, additional_score):
    # Board Only Mouse Controls
    # ------------------------------------------------------------
    mouse_x, mouse_y = event.pos
    grid_x, grid_y = (mouse_x - 20) // 75, (mouse_y - 20) // 75
    # grid_x, grid_y = (mouse_x - 20) // 75, 7 - ((mouse_y - 20) // 75)
    # chess_piece = Piece(None, None, None, None, None)

    # Left mouse click
    if event.button == 1:
        if selected_piece is None:
            print("Selected Piece is: ", selected_piece)
            for p in pieces_array:
                if p.x == grid_x and p.y == grid_y:
                    selected_piece = p
                    # Debugging
                    # -------------------------------
                    print_piece_info(selected_piece)
                    # -------------------------------
                    redraw_pieces_on_board_with_green_highlight(pieces_array, board, screen,
                                                                (grid_x, grid_y))
                    break

        else:
            if (selected_piece != None):
                print("Current Selected Piece is: ", selected_piece.color + selected_piece.type)

            if is_valid_move(selected_piece, grid_x, grid_y, pieces_array):

                if (selected_piece != None):
                    print("Current Selected Piece is: ", selected_piece.color + selected_piece.type)

                # Remove the existing piece at the target location
                pieces_array, heuristic_score, additional_score = remove_piece_at_position(pieces_array, grid_x, grid_y,
                                                                                           heuristic_score,
                                                                                           additional_score)

                # Debugging
                # --------------------------------
                # display_pieces_array(pieces_array)
                # --------------------------------

                # Move the selected piece to the new location
                selected_piece.x = grid_x
                selected_piece.y = grid_y

                # Update the selected_piece in the pieces list
                for i, p in enumerate(pieces_array):
                    if p == selected_piece:
                        pieces_array[i] = selected_piece
                        break

                # Debugging
                # --------------------------------
                # display_pieces_array(pieces_array)
                # --------------------------------

                # Redraw the board with the updated pieces
                redraw_pieces_on_board(pieces_array, board, screen)

                # Debugging
                # --------------------------------
                # display_pieces_array(pieces_array)
                # --------------------------------

                # Deselect the selected piece after moving it or attempting to move it
                selected_piece = None

    # Right mouse click
    elif event.button == 3:
        selected_piece = None
        # Redraw the board
        redraw_pieces_on_board(pieces_array, board, screen)

    # Get the updated board matrix
    board_matrix = board_to_matrix(pieces_array)

    return selected_piece, pieces_array, heuristic_score, additional_score, board_matrix


# def remove_piece_at_position(pieces_array, grid_x, grid_y, selected_piece):
#     updated_pieces = [p for p in pieces_array if not (p.x == grid_x and p.y == grid_y)]
#
#     return updated_pieces

def print_piece_info(p):
    print("-----------------------------------------------")
    print("This is the piece found to be moved. X=",
          str(p.x) + " Y=" + str(p.y) + " color=" + p.color + " type=" + p.type + " value=" + str(p.value) + ". ")
    print("-----------------------------------------------")


def remove_piece_at_position(pieces_array, grid_x, grid_y, heuristic_score, additional_score):
    piece_to_remove = None
    updated_pieces = []
    for p in pieces_array:
        if p.x == grid_x and p.y == grid_y:
            piece_to_remove = p
        else:
            # if it is not the piece that needs to be removed, it adds it back to the array
            updated_pieces.append(p)

    if piece_to_remove:
        heuristic_score, additional_score = add_to_score(piece_to_remove, heuristic_score, additional_score)

    return updated_pieces, heuristic_score, additional_score


def display_pieces_array(pieces):
    print("-----------------------------------------------")
    for p in pieces:
        print("Selected Piece is: ", p.color + p.type)
    print("-----------------------------------------------")


def is_valid_move(piece, target_x, target_y, pieces):
    dx = abs(target_x - piece.x)
    dy = abs(target_y - piece.y)

    # Check if there is a piece of the same color at the target position
    for p in pieces:
        if p.x == target_x and p.y == target_y and p.color == piece.color:
            return False

    #     # Pawn movement
    # if piece.type == "pawn":
    #     if piece.color == "white":
    #         return target_y == piece.y - 1 and target_x == piece.x
    #     else:
    #         return target_y == piece.y + 1 and target_x == piece.x
    # Pawn movement
    if piece.type == "pawn":
        if piece.color == "white":
            # Check for the standard one-step move
            if target_y == piece.y - 1 and target_x == piece.x and not any(p.x == target_x and p.y == target_y for p in pieces):
                return True
            # Check for the two-step move from the starting position
            elif piece.y == 6 and target_y == piece.y - 2 and target_x == piece.x and not any(p.x == target_x and p.y == target_y for p in pieces) and not any(p.x == target_x and p.y == piece.y - 1 for p in pieces):
                return True
            # Check for captures
            elif target_y == piece.y - 1 and abs(target_x - piece.x) == 1:
                for p in pieces:
                    if p.x == target_x and p.y == target_y and p.color != piece.color:
                        return True
        else:
            # Check for the standard one-step move
            if target_y == piece.y + 1 and target_x == piece.x and not any(p.x == target_x and p.y == target_y for p in pieces):
                return True
            # Check for the two-step move from the starting position
            elif piece.y == 1 and target_y == piece.y + 2 and target_x == piece.x and not any(p.x == target_x and p.y == target_y for p in pieces) and not any(p.x == target_x and p.y == piece.y + 1 for p in pieces):
                return True
            # Check for captures
            elif target_y == piece.y + 1 and abs(target_x - piece.x) == 1:
                for p in pieces:
                    if p.x == target_x and p.y == target_y and p.color != piece.color:
                        return True

        return False
        # -------------------------------------------------------------------------------------------

        # Rook movement
    elif piece.type == "rook":
        if dx != 0 and dy != 0:
            return False
        for p in pieces:
            if (p.x == target_x and p.y < max(piece.y, target_y) and p.y > min(piece.y, target_y)) or (
                    p.y == target_y and p.x < max(piece.x, target_x) and p.x > min(piece.x, target_x)):
                return False
        return True

        # Knight movement
    elif piece.type == "knight":
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

        # Bishop movement
    elif piece.type == "bishop":
        if dx != dy:
            return False
        for p in pieces:
            if abs(p.x - piece.x) == abs(p.y - piece.y) and max(piece.x, target_x) > p.x > min(piece.x,
                                                                                               target_x) and p.y < max(
                piece.y, target_y) and p.y > min(piece.y, target_y):
                return False
        return True

        # Queen movement (combination of rook and bishop movements)
    elif piece.type == "queen":
        # Rook movement
        if dx == 0 or dy == 0:
            for p in pieces:
                if (p.x == target_x and p.y < max(piece.y, target_y) and p.y > min(piece.y, target_y)) or \
                        (p.y == target_y and p.x < max(piece.x, target_x) and p.x > min(piece.x, target_x)):
                    return False
            return True

        # Bishop movement
        elif dx == dy:
            for p in pieces:
                if abs(p.x - piece.x) == abs(p.y - piece.y) and \
                        max(piece.x, target_x) > p.x > min(piece.x, target_x) and \
                        max(piece.y, target_y) > p.y > min(piece.y, target_y):
                    return False
            return True

        return False

        # King movement
    elif piece.type == "king":
        return (dx == 1 and dy == 1) or (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    return False
