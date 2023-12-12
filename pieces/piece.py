import pygame
import os

# Constants
IMG_PATH = "img/"
IMAGE_SIZE = (55, 55)
BOARD_RECT = (113, 113, 525, 525)

# Dictionary for piece images
piece_images = {
    'b_bishop': pygame.image.load(os.path.join(IMG_PATH, "black_bishop.png")),
    'b_king': pygame.image.load(os.path.join(IMG_PATH, "black_king.png")),
    'b_knight': pygame.image.load(os.path.join(IMG_PATH, "black_knight.png")),
    'b_pawn': pygame.image.load(os.path.join(IMG_PATH, "black_pawn.png")),
    'b_queen': pygame.image.load(os.path.join(IMG_PATH, "black_queen.png")),
    'b_rook': pygame.image.load(os.path.join(IMG_PATH, "black_rook.png")),
    'w_bishop': pygame.image.load(os.path.join(IMG_PATH, "white_bishop.png")),
    'w_king': pygame.image.load(os.path.join(IMG_PATH, "white_king.png")),
    'w_knight': pygame.image.load(os.path.join(IMG_PATH, "white_knight.png")),
    'w_pawn': pygame.image.load(os.path.join(IMG_PATH, "white_pawn.png")),
    'w_queen': pygame.image.load(os.path.join(IMG_PATH, "white_queen.png")),
    'w_rook': pygame.image.load(os.path.join(IMG_PATH, "white_rook.png")),
}

class Piece:
    """
    Represents a chess piece. Each piece has a row, column, color, image key, and a list of valid moves.
    It also has flags indicating whether it is selected, and whether it is a king or a pawn.
    """

    def __init__(self, row, col, color, img_key):
        """
        Initialize a new piece with the given row, column, color, and image key.
        The piece is not selected, is not a king, and is not a pawn by default.

        Parameters
        ----------
        row : int
            The row of the piece on the chess board.
        col : int
            The column of the piece on the chess board.
        color : str
            The color of the piece. It can be either 'w' for white or 'b' for black.
        img_key : str
            The key to the image representing the piece.
        """
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        self.img_key = img_key

    def is_selected(self):
        """
        Check if the piece is selected.

        Returns
        -------
        bool
            True if the piece is selected, False otherwise.
        """
        return self.selected

    def update_valid_moves(self, board):
        """
        Update the list of valid moves for the piece based on the current state of the board.

        Parameters
        ----------
        board : list
            The current state of the chess board.
        """
        self.move_list = self.valid_moves(board)

    def calculate_x(self):
        """
        Calculate the x-coordinate of the piece on the screen based on its column position on the board.
        The calculation takes into account the size and position of the board on the screen.

        Returns
        -------
        int
            The x-coordinate of the piece.
        """
        return (4 - self.col) + round(BOARD_RECT[0] + (self.col * BOARD_RECT[2] / 8))

    def calculate_y(self):
        """
        Calculate the y-coordinate of the piece on the screen based on its row position on the board.
        The calculation takes into account the size and position of the board on the screen.

        Returns
        -------
        int
            The y-coordinate of the piece.
        """
        return 3 + round(BOARD_RECT[1] + (self.row * BOARD_RECT[3] / 8))
        
    def draw(self, win, color):
        """
        Draw the piece on the given window. If the piece is selected and its color matches the given color, it is highlighted with a red rectangle.

        Parameters
        ----------
        win : pygame.Surface
            The window to draw the piece on.
        color : str
            The color to use for highlighting the piece if it is selected. It can be either 'w' for white or 'b' for black.
        """
        image = piece_images[self.img_key]
        x = self.calculate_x()
        y = self.calculate_y()

        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        win.blit(image, (x, y))

# Usage example
# black_bishop = Piece(0, 0, 'b', 'b_bishop')
# white_king = Piece(7, 4, 'w', 'w_king')


















