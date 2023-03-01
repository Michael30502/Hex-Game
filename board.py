import pygame


class Hexagon:

    def __init__(self, x1, x2, x3, x4, x5, x6, y1, y2, y3, y4, y5, y6, screen):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5
        self.x6 = x6
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.y4 = y4
        self.y5 = y5
        self.y6 = y6
        self.screen = screen

    def draw_hexagon(self):
        pygame.draw.polygon(self.screen, 255,
                            [(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3), (self.x4, self.y4),
                             (self.x5, self.y5), (self.x6, self.y6)])


def draw_hexagon_field(screen):
    hexagon_list = list()

    newline_offset = 20
    x_size = 40
    y_size = 10
    x_offset = 40
    y_offset = 30
    for x in range(11):
        for y in range(11):
            x1 = x * x_offset + y * newline_offset
            y1 = y * y_offset + y_size
            x2 = x * x_offset + y * newline_offset
            y2 = y * y_offset + y_size * 3
            x3 = x * x_offset + x_size / 2 + y * newline_offset
            y3 = y * y_offset + y_size * 4
            x4 = x * x_offset + x_size + y * newline_offset
            y4 = y * y_offset + y_size * 3
            x5 = x * x_offset + x_size + y * newline_offset
            y5 = y * y_offset + y_size
            x6 = x * x_offset + x_size / 2 + y * newline_offset
            y6 = y * y_offset
            hexagon_list.append(Hexagon(x1, x2, x3, x4, x5, x6, y1, y2, y3, y4, y5, y6, screen))

    for hex in hexagon_list:
        hex.draw_hexagon()
    pygame.display.flip()