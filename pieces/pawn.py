from pieces.piece import Piece
class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first_move = True

    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []

        # Define the direction of pawn movement based on its color
        direction = 1 if self.color == "b" else -1

        # Regular move forward
        if 0 <= i + direction < 8 and board[i + direction][j] == 0:
            moves.append((j, i + direction))

            # Double move on first move
            if self.first_move and board[i + 2 * direction][j] == 0:
                moves.append((j, i + 2 * direction))

        # Diagonal captures
        for dj in [-1, 1]:
            if 0 <= i + direction < 8 and 0 <= j + dj < 8:
                piece = board[i + direction][j + dj]
                if piece != 0 and piece.color != self.color:
                    moves.append((j + dj, i + direction))

        return moves
