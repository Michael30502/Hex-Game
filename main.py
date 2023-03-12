import pygame
import gamelogic

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

# Surface/Screen size (this shoudl be scaleable)

WIDTH, HEIGHT = 900, 500
game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")

start_button_img =  pygame.image.load("Hex-Game/assets/start_button_img.png").convert_alpha()
hexagon_neutral_img = pygame.image.load("Hex-Game/assets/tile_0.png").convert_alpha()
hexagon_player1_img = pygame.image.load("Hex-Game/assets/tile_1.png").convert_alpha()
hexagon_player2_img = pygame.image.load("Hex-Game/assets/tile_2.png").convert_alpha()

# game variables
action= False


class Button:
    def __init__(self, x, y, image, scale, unit):
        self.image = image  # Store original image
        self.scale = scale
        self.player = None
        self.width = int(self.image.get_width() * self.scale)
        self.height = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        # for more precise clicking collision look into masks and sprites.
        self.mask = pygame.mask.from_surface(self.image)
        # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
        self.unit = unit
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    #    def __str__(self):
    #        return (f'BUTTONOBJ= x,y: {self.rect.topleft}, image:{self.image}, scale:{self.scale}, unit:{self.unit}')

    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player

    # draw and check for mouseover/clicked
    def draw(self, surface):
        global action

        # getting mouse pos
        mouse_pos = pygame.mouse.get_pos()

        if gamelogic.board[self.unit[0]][self.unit[1]] == 1:
            board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
        elif gamelogic.board[self.unit[0]][self.unit[1]] == 2:
            board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)

        # checking colision and clicked
        if self.rect.collidepoint(mouse_pos):
            # print('hover:' + str(self.unit))
            # Checking if we are leftclicking a button that has not been clicked, then changing the image
            
            pygame.event.get()
            if pygame.mouse.get_pressed()[0] == 1 and not action:
                action = True
                self.clicked = True
                gamelogic.make_move(self.unit)


                # if game1.get_turn() % 2 == 1 and board1.grid[self.unit[0]][self.unit[1]].get_player() == None:
                #     board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
                #     board1.grid[self.unit[0]][self.unit[1]].set_player(1)
                #     game1.turn_count()
                # if not (game1.get_turn() % 2 == 1) and board1.grid[self.unit[0]][self.unit[1]].get_player() == None:
                #     board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)
                #     board1.grid[self.unit[0]][self.unit[1]].set_player(2)
                #     game1.turn_count()


            if pygame.mouse.get_pressed()[0] == 0:
                action = False

        # display the image on screen
        surface.blit(self.image, self.rect)

    #DRAW AT CENTER FUNCTION FOR THE MENU NOT HEXAGONS
    def draw_at_center(self, surface, dest):
        global action

        # getting mouse pos
        mouse_pos = pygame.mouse.get_pos()

        if gamelogic.board[self.unit[0]][self.unit[1]] == 1:
            board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
        elif gamelogic.board[self.unit[0]][self.unit[1]] == 2:
            board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)

        # checking colision and clicked
        if self.rect.collidepoint(mouse_pos):
            pygame.event.get()
            if pygame.mouse.get_pressed()[0] == 1 and not action:
                action = True
                self.clicked = True
                gamelogic.make_move(self.unit)

            if pygame.mouse.get_pressed()[0] == 0:
                action = False

        # display the image on screen
        rect = self.rect
        rect.center = (dest[0],dest[1]) 
        surface.blit(self.image, rect)

    def set_image(self, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def get_hex_pos(self):
        print('position:' + str(self.rect.topleft) + "unit" + str(self.unit))
        pass


class Board:
    def __init__(self, hexagon, size, surface):
        self.hexagon = hexagon
        self.size = size
        self.surface = surface
        self.grid = None

    def make_grid(self):
        x_offset = self.hexagon.image.get_width() * self.hexagon.scale
        y_offset = self.hexagon.image.get_height() * self.hexagon.scale
        hex_grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # Offset for odd rows
                hex_x = (j + i * 0.5) * x_offset
                hex_y = i * y_offset * 0.74
                # if i == 0:
                #     hexagon = Button(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j))
                #     hexagon.set_image(hexagon_player1_img)
                # else:
                hexagon = Button(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j))
                hexagon.draw(self.surface)
                row.append(hexagon)
            hex_grid.append(row)
        self.grid = hex_grid
        return hex_grid

    def get_grid(self):
        return self.grid

    def draw_grid(self):
        for row in self.grid:
            for hexagon in row:
                hexagon.draw(self.surface)


class EventHandler:
    def __init__(self, event):
        self.event = event




class Game:
    def __init__(self, surface, board, turn):
        self.surface = surface
        self.turn = turn
        self.board = board
        self.running = True
        self.game_menu = False

    def menu(self):
        height = game_surface.get_height()
        width = game_surface.get_width()
        game_surface.fill(WHITE)
        start_button = Button(-300, -300, start_button_img, 0.5, (1, 1))
        # start_button.set_image(start_button.get_image())
        
        while self.game_menu:
            start_button.draw_at_center(game_surface,(width/2, height/4))
            pygame.display.flip()
            print(start_button.clicked)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_menu = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_surface.fill(WHITE)
                        self.game_menu = False
            #if startbutton is pressed, makes new board which it gives to the play function
            if start_button.clicked == True:
                size = 3
                custom_board = Board(hexagon1,size,self.surface)
                game_surface.fill(WHITE)
                self.game_menu = False
                gamelogic.player_no = 0
                custom_board.make_grid()
                self.set_board(custom_board)

    def play(self):
        game_surface.fill(WHITE)
        self.board.make_grid()
        while self.running:
            if gamelogic.player_no == gamelogic.cpu:
                self.unit = gamelogic.make_cpu_move()
            else:
                self.board.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_menu = True
                        self.menu()

            pygame.display.flip()

    def get_turn(self):
        return self.turn
    
    def set_board(self, board):

        self.board = board

    def turn_count(self):
        self.turn += 1


# button inits
hexagon1 = Button(0, 0, hexagon_neutral_img, 0.5, (0, 0))
hexagon2 = Button(hexagon_neutral_img.get_width() * 0.5, 0, hexagon_neutral_img, 0.5, (0, 1))
# hexagon_neutral_img = pygame.image.load("Hex-Game/assets/tile_0.png").convert_alpha()
hexagon_neutral_img_mask = pygame.mask.from_surface(hexagon_neutral_img)
# hexagon3 = Button(0,0, hexagon_neutral_img_mask,0.5, (0,0))

hexagon_player1 = Button(96, 0, hexagon_player1_img, 0.5, (1, 1))

board1 = Board(hexagon1, gamelogic.board_size, game_surface)
game1 = Game(game_surface, board1, 0)
game1.play()

# running = True
# while running:
#     board1.make_grid()
#     board1.draw_grid()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 game_menu = True
#                 menu(game_menu)


# Main game loop

# clicks is away to distinguish between players

# Handle events


# pygame.draw.line(screen, RED, (0,56),(600,56))
# pygame.display.update()
