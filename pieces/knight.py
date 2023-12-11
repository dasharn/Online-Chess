from pieces.piece import Piece
class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []

        # Define all possible knight move offsets
        knight_moves = [
            (1, 2), (-1, 2), (1, -2), (-1, -2),
            (2, 1), (-2, 1), (2, -1), (-2, -1)
        ]

        for dx, dy in knight_moves:
            new_row, new_col = i + dy, j + dx

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                p = board[new_row][new_col]

                if p == 0 or p.color != self.color:
                    moves.append((new_col, new_row))

        return moves