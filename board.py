import pygame
import tiles

class Board():
    def __init__(self, hexagon, size, surface,game1,board1,hexagon_player1_img,hexagon_player2_img):
        self.hexagon = hexagon
        self.size = size
        self.surface = surface
        self.grid = None
        self.game1 = game1
        self.board1 = board1
        self.hexagon_player1_img = hexagon_player1_img
        self.hexagon_player2_img = hexagon_player2_img

    def make_grid(self):
        x_offset = self.hexagon.image.get_width()*self.hexagon.scale
        y_offset = self.hexagon.image.get_height()*self.hexagon.scale
        hex_grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # Offset for odd rows
                hex_x = (j + i * 0.5)* x_offset
                hex_y = i * y_offset * 0.74
                # if i == 0:
                #     hexagon = Button(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j))
                #     hexagon.set_image(hexagon_player1_img)
                # else:
                hexagon = tiles.Tiles(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j),self.game1,self.board1,hexagon_player1_img,hexagon_player2_img)
                hexagon.draw(self.surface)
                row.append(hexagon)
            hex_grid.append(row)
        self.grid = hex_grid
        return hex_grid

    def get_grid(self):
        return self.grid

    
    def draw_grid(self):
        for row in (self.grid):
            for hexagon in (row):
                hexagon.draw(self.surface)