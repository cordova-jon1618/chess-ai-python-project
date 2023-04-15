from piece import Piece


def handle_mouse_click(event, pieces, board, screen, selected_piece):
    mouse_x, mouse_y = event.pos
    grid_x, grid_y = (mouse_x - 20) // 75, (mouse_y - 20) // 75
    chess_piece = Piece(None, None, None, None)

    # Left mouse click
    if event.button == 1:
        if selected_piece is None:
            for p in pieces:
                if p.x == grid_x and p.y == grid_y:
                    selected_piece = p
                    chess_piece.redraw_pieces_on_board_with_green_highlight(pieces, board, screen, (grid_x, grid_y))
                    break
        else:
            if is_valid_move(selected_piece, grid_x, grid_y, pieces):
                # Remove the existing piece at the target location, if any
                pieces = [p for p in pieces if not (p.x == grid_x and p.y == grid_y)]

                # Move the selected piece to the new location
                selected_piece.x = grid_x
                selected_piece.y = grid_y

                # Redraw the board with the updated pieces
                chess_piece.redraw_pieces_on_board(pieces, board, screen)

                # Deselect the selected piece after moving it or attempting to move it
                selected_piece = None

    # Right mouse click
    elif event.button == 3:
        selected_piece = None
        # Redraw the board
        chess_piece.redraw_pieces_on_board(pieces, board, screen)

    return selected_piece


def is_valid_move(piece, target_x, target_y, pieces):
    dx = abs(target_x - piece.x)
    dy = abs(target_y - piece.y)

    # Pawn movement
    if piece.type == "pawn":
        if piece.color == "white":
            return target_y == piece.y - 1 and target_x == piece.x
        else:
            return target_y == piece.y + 1 and target_x == piece.x

    # Rook movement
    elif piece.type == "rook":
        if dx != 0 and dy != 0:
            return False
        for p in pieces:
            if p.x == target_x and p.y == target_y:
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
            if p.x == target_x and p.y == target_y:
                return False
        return True

    # Queen movement (combination of rook and bishop movements)
    elif piece.type == "queen":
        if not (dx == dy or dx == 0 or dy == 0):
            return False
        for p in pieces:
            if p.x == target_x and p.y == target_y:
                return False
        return True

    # King movement
    elif piece.type == "king":
        return (dx == 1 and dy == 1) or (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    return False
