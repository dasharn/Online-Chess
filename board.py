from pieces.bishop import Bishop
from pieces.bishop import King
from pieces.bishop import Rook
from pieces.bishop import Pawn
from pieces.bishop import Queen
from pieces.bishop import Knight
import time
import pygame


class Board:
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.ready = False
        self.last = None
        self.copy = True
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self._initialize_pieces()
        self.player_one_name = "Player 1"
        self.player_two_name = "Player 2"
        self.turn = "w"
        self.time_one = 900
        self.time_two = 900
        self.stored_time_one = 0
        self.stored_time_two = 0
        self.winner = None
        self.startTime = time.time()

    def _initialize_pieces(self):
        pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.board[0][i] = pieces_order[i](0, i, "b")
            self.board[1][i] = Pawn(1, i, "b")
            self.board[7][i] = pieces_order[i](7, i, "w")
            self.board[6][i] = Pawn(6, i, "w")
    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self, win, color):
        if self.last and color == self.turn:
            self._draw_last_move(win)

        s = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, color)
                    if self.board[i][j].isSelected:
                        s = (i, j)

    def _draw_last_move(self, win):
        y, x = self.last[0]
        y1, x1 = self.last[1]

        xx = self._calculate_position(x)
        yy = self._calculate_position(y)
        pygame.draw.circle(win, (0,0,255), (xx+32, yy+30), 34, 4)

        xx1 = self._calculate_position(x1)
        yy1 = self._calculate_position(y1)
        pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

    def _calculate_position(self, pos):
        return (4 - pos) + round(self.startX + (pos * self.rect[2] / 8))


    def get_danger_moves(self, color):
        return [move for i in range(self.rows) for j in range(self.cols) 
                if self.board[i][j] != 0 and self.board[i][j].color != color 
                for move in self.board[i][j].move_list]

    def is_checked(self, color):
        self.update_moves()
        king_pos = self._get_king_position(color)
        return king_pos in self.get_danger_moves(color)

    def _get_king_position(self, color):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].king and self.board[i][j].color == color:
                    return (j, i)
        return (-1, -1)

    def select(self, col, row, color):
        changed = False
        prev = self._get_previous_selected()

        # if piece
        if self.board[row][col] == 0 and prev != (-1, -1):
            moves = self.board[prev[0]][prev[1]].move_list
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)
        else:
            changed = self._handle_piece_selection(prev, row, col, color)

        if changed:
            self._toggle_turn()

        return changed

    def _get_previous_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].selected:
                    return (i, j)
        return (-1, -1)

    def _handle_piece_selection(self, prev, row, col, color):
        changed = False
        if prev == (-1, -1):
            self.reset_selected()
            if self.board[row][col] != 0:
                self.board[row][col].selected = True
        else:
            if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                moves = self.board[prev[0]][prev[1]].move_list
                if (col, row) in moves:
                    changed = self.move(prev, (row, col), color)

                if self.board[row][col].color == color:
                    self.board[row][col].selected = True
            else:
                if self.board[row][col].color == color:
                    changed = self._handle_castling(prev, row, col, color)
        return changed

    def _handle_castling(self, prev, row, col, color):
        changed = False
        self.reset_selected()
        if self.board[prev[0]][prev[1]].moved == False and self.board[prev[0]][prev[1]].rook and self.board[row][col].king and col != prev[1] and prev != (-1, -1):
            castle = self._is_castling_possible(prev, row, col)
            if castle:
                changed = self._perform_castling(prev, row, col, color)
            if not changed:
                self.board[row][col].selected = True
        else:
            self.board[row][col].selected = True
        return changed

    def _is_castling_possible(self, prev, row, col):
        castle = True
        if prev[1] < col:
            for j in range(prev[1] + 1, col):
                if self.board[row][j] != 0:
                    castle = False
        else:
            for j in range(col + 1, prev[1]):
                if self.board[row][j] != 0:
                    castle = False
        return castle

    def _perform_castling(self, prev, row, col, color):
        changed = False
        if prev[1] < col:
            changed = self.move(prev, (row, 3), color)
            changed = self.move((row, col), (row, 2), color)
        else:
            changed = self.move(prev, (row, 6), color)
            changed = self.move((row, col), (row, 5), color)
        return changed

    def _toggle_turn(self):
        self.turn = "b" if self.turn == "w" else "w"
        self.reset_selected()

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        pass

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        self._swap_pieces(start, end)

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            self._swap_pieces(end, start)  # revert the move
            if self.board[start[0]][start[1]].pawn:
                self.board[start[0]][start[1]].first = True
            changed = False
        else:
            self.reset_selected()
            changed = True
            self.last = [start, end]
            self._update_time()

        self.update_moves()
        return changed

    def _swap_pieces(self, start, end):
        if self.board[start[0]][start[1]].pawn:
            self.board[start[0]][start[1]].first = False

        self.board[start[0]][start[1]].change_pos((end[0], end[1]))
        self.board[end[0]][end[1]], self.board[start[0]][start[1]] = self.board[start[0]][start[1]], 0

    def _update_time(self):
        if self.turn == "w":
            self.stored_time_one += (time.time() - self.startTime)
        else:
            self.stored_time_two += (time.time() - self.startTime)
        self.startTime = time.time()



