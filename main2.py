import pygame

WHITE = (255,255,255)
BLACK =(0,0,0)
RED = (255,0,0)

FPS = 60


#Surface/Screen size (this shoudl be scaleable)

WIDTH, HEIGHT= 900, 500
game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
menu_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")




hexagon_neutral_img = pygame.image.load("Hex-Game/assets/tile_0.png").convert_alpha()
hexagon_player1_img = pygame.image.load("Hex-Game/assets/tile_1.png").convert_alpha()
hexagon_player2_img = pygame.image.load("Hex-Game/assets/tile_2.png").convert_alpha()

#game variables
game_pause = False

game_menu = False




class Button():
    def __init__(self,x,y,image,scale, unit):
        self.image = image  # Store original image
        self.scale = scale
        self.player = None
        self.width = int(self.image.get_width() * self.scale)
        self.height = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        #for more precise clicking collision look into masks and sprites.
        # self.mask = pygame.mask.from_surface(self.image)
        self.unit = unit
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def __str__(self):
        return (f'BUTTONOBJ= x,y: {self.rect.topleft}, image:{self.image}, scale:{self.scale}, unit:{self.unit}')

    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player

    #draw and check for mouseover/clicked
    def draw(self,surface):
        #the action allows us to check if a button has been pressed
        action = False
        #getting mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # checking colision and cliked
        if self.rect.collidepoint(mouse_pos):
            # print('hover:' + str(self.unit))
            #Checking if we are leftclicking a button that has not been clicked, then changing the image
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print("clicked")
                if game1.get_turn() % 2 == 1 and board1.grid[self.unit[0]][self.unit[1]].get_player()==None:
                    board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
                    board1.grid[self.unit[0]][self.unit[1]].set_player(1)
                    game1.turn_count()
                if not (game1.get_turn() % 2 == 1) and board1.grid[self.unit[0]][self.unit[1]].get_player()==None:
                    board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)
                    board1.grid[self.unit[0]][self.unit[1]].set_player(2)
                    game1.turn_count()
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        
        #display the image on screen
        surface.blit(self.image, self.rect)
        return action

    def set_image(self,image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        

    def get_hex_pos(self):
        print('position:' + str(self.rect.topleft)+ "unit" + str(self.unit))
        pass

class Board():
    def __init__(self, hexagon, size, surface):
        self.hexagon = hexagon
        self.size = size
        self.surface = surface
        self.grid = None

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
                hexagon = Button(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j))
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


class Menu():
    def __init__(self, surface):
        self.surface = surface




class EventHandler():
    def __init__(self,event):
        self.event = event

def menu(game_menu):
    while game_menu:
        menu_surface.fill(WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_menu = False
    
class Game():
    def __init__(self, surface, board, turn):
        self.surface = surface
        self.turn = turn
        self.board = board
        self.running = True
    
    def play(self):
        game_surface.fill(WHITE)
        self.board.make_grid()
        while self.running:
            
            self.board.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_menu = True
                        menu(game_menu)

            pygame.display.update()

    def get_turn(self):
        return self.turn
    
    def turn_count(self):
        self.turn += 1

            
#button inits
hexagon1 = Button(0,0, hexagon_neutral_img,0.5, (0,0))
hexagon2 = Button(hexagon_neutral_img.get_width()*0.5,0,hexagon_neutral_img,0.5,(0,1))

hexagon_player1 = Button(96, 0, hexagon_player1_img, 0.5, (1, 1))

board1 = Board(hexagon1,11,game_surface)
game1 = Game(game_surface,board1,0)
game1.play()
