from pieces.piece import Piece
class Bishop(Piece):
    img = 0

    def valid_moves(self, board):
        moves = []

        # Define the possible directions for bishop movement
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            for i in range(1, 8):  # Maximum board size is 8x8
                new_row, new_col = self.row + i * dy, self.col + i * dx

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    p = board[new_row][new_col]
                    if p == 0:
                        moves.append((new_col, new_row))
                    elif p.color != self.color:
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break

        return moves