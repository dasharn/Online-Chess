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
    def __init__(self, row, col, color, img_key):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        self.img_key = img_key

    def is_selected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def calculate_x(self):
        return (4 - self.col) + round(BOARD_RECT[0] + (self.col * BOARD_RECT[2] / 8))

    def calculate_y(self):
        return 3 + round(BOARD_RECT[1] + (self.row * BOARD_RECT[3] / 8))

    def draw(self, win, color):
        image = piece_images[self.img_key]
        x = self.calculate_x()
        y = self.calculate_y()

        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        win.blit(image, (x, y))
        
    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return f"{self.col} {self.row}"

# Usage example
# black_bishop = Piece(0, 0, 'b', 'b_bishop')
# white_king = Piece(7, 4, 'w', 'w_king')


















