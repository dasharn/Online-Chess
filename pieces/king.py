from pieces.piece import Piece
class King(Piece):
    img = 1

    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []

        # Define all possible directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            new_row, new_col = i + dy, j + dx

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                p = board[new_row][new_col]

                if p == 0 or p.color != self.color:
                    moves.append((new_col, new_row))

        return moves