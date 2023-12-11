from pieces.piece import Piece
class Rook(Piece):
    img = 5

    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []

        # Define all possible directions for rook movement
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            for step in range(1, 8):
                new_row, new_col = i + step * dy, j + step * dx

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board[new_row][new_col]

                    if piece == 0:
                        moves.append((new_col, new_row))
                    elif piece.color != self.color:
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break

        return moves