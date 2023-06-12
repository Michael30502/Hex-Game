import numpy as np
import pygame

import gamelogic
pygame.init()
font = pygame.font.SysFont("Arial", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
#YELLOW = (255,255,0)

FPS = 60

cpu = 2
board_size_list = [3, 5, 7, 9, 11]
#tile_scale_list = [0.4, 0.4, 0.4 ,0.4 , 0.4]
#x_extra_offset_list = [76.5, 76.5, 76.5, 76.5, 76.5]
#y_extra_offset_list = [40,40,40,40,40]
tile_scale = 0.4
#x_extra_offset = len(x_extra_offset_list)-1
#y_extra_offset= len(y_extra_offset_list)-1
board_size = len(board_size_list)-1
#x_extra_offset = 76.5

run = True
first_menu = True
setting_menu = False
second_menu = False
game_running = False
game_paused = False
game_finished = False
player_option = False


# Surface/Screen size (this shoudl be scaleable
# WIDTH, HEIGHT = 768, 466
WINDOWWIDTH, WINDOWHEIGHT = 640, 480
game_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
# board_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")


#load button images
start_game_img = pygame.image.load('assets/Start_Game.png').convert_alpha()
AI_1_img = pygame.image.load('assets/Drone_Bee.png').convert_alpha()
Play_Online_img = pygame.image.load('assets/Play_Online.png').convert_alpha()
AI_2_img = pygame.image.load('assets/Worker_Bee.png').convert_alpha()
AI_3_img = pygame.image.load('assets/Queen_Bee.png').convert_alpha()
Change_Board_Size_img = pygame.image.load('assets/Change_Board_Size.png').convert_alpha()
Continue_img = pygame.image.load('assets/Continue.png').convert_alpha()
Export_Game_img = pygame.image.load('assets/Export_Game.png').convert_alpha()
Import_Game_img = pygame.image.load('assets/Import_Game.png').convert_alpha()
Pause_Game_img = pygame.image.load('assets/Pause_Game.png').convert_alpha()
Settings_img = pygame.image.load('assets/Settings.png').convert_alpha()
Two_Player_img = pygame.image.load('assets/Two_Player.png').convert_alpha()
Go_Back_img = pygame.image.load('assets/Go_Back.png').convert_alpha()
Player_1_img = pygame.image.load('assets/Player_1.png').convert_alpha()
Player_2_img = pygame.image.load('assets/Player_2.png').convert_alpha()
Host_Game_img = pygame.image.load('assets/Host_Game.png').convert_alpha() 
Join_Game_img = pygame.image.load('assets/Join_Game.png').convert_alpha()
Change_Player_img = pygame.image.load('assets/Change_Player.png').convert_alpha()
Drone_Bee_Img = pygame.image.load('assets/Drone_Bee_pic.png').convert_alpha()
Drone_Bee_img = pygame.transform.scale(Drone_Bee_Img, (50, 50))
Worker_Bee_Img = pygame.image.load('assets/Worker_Bee_pic.png').convert_alpha()
Worker_Bee_img = pygame.transform.scale(Worker_Bee_Img, (50, 50))
Queen_Bee_Img = pygame.image.load('assets/Queen_Bee_pic.png').convert_alpha()
Queen_Bee_img = pygame.transform.scale(Queen_Bee_Img, (50, 50))
Player_1_pic_Img = pygame.image.load('assets/Player_1_pic.png').convert_alpha()
Player_1_pic_img = pygame.transform.scale(Player_1_pic_Img, (50, 50))
Player_2_pic_Img = pygame.image.load('assets/Player_2_pic.png').convert_alpha()
Player_2_pic_img = pygame.transform.scale(Player_2_pic_Img, (50, 50))
YELLOW = pygame.image.load('assets/honeycomb2.jpg')
YELLOW = pygame.transform.scale(YELLOW, (640, 480))

start_button_img =  pygame.image.load("assets/start_button_img.png").convert_alpha()
hexagon_neutral_img = pygame.image.load("assets/tile_0.png").convert_alpha()
#hexagon_neutral_img = pygame.transform.scale_by(0.7)
hexagon_player1_img = pygame.image.load("assets/tile_1.png").convert_alpha()
#hexagon_player1_img = pygame.transform.scale_by(0.7)
hexagon_player2_img = pygame.image.load("assets/tile_2.png").convert_alpha()
#hexagon_player2_img = pygame.transform.scale_by(0.7)

# game variables
action = False

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
        if board1.grid is not None:
            if gamelogic.board[self.unit[0]][self.unit[1]] == 1:
                #print(board1.grid)
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
        self.top_bottom_border_color = (255, 0, 0)
        self.sides_border_color = (0, 0, 255)
        self.border_thickness = 20

    def make_grid(self):
        x_offset = self.hexagon.image.get_width() * self.hexagon.scale
        y_offset = self.hexagon.image.get_height() * self.hexagon.scale
        if self.size==11:
            x_extra_offset = 76.5
            y_extra_offset = 40
        elif self.size==9:
             x_extra_offset=120.8
             y_extra_offset = 40
        elif self.size==7:
             x_extra_offset=165
             y_extra_offset = 40
        elif self.size==5:
             x_extra_offset=209.3
             y_extra_offset = 40
        elif self.size==3:
             x_extra_offset=253.6
             y_extra_offset = 40
        hex_grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # Offset for odd rows
                distance_from_center_x = abs(j - (self.size - 1) / 2)
                distance_from_center_y = abs(i - (self.size - 1) / 2)
                hex_x = (j + i * 0.5) * x_offset + x_extra_offset
                hex_y = i * y_offset * 0.74 + y_extra_offset
                # if i == 0:
                #     hexagon = Button(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j))
                #     hexagon.set_image(hexagon_player1_img)
                # else:
                hexagon = Button(hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j))
                hexagon.draw(self.surface)
                row.append(hexagon)
            hex_grid.append(row)
        self.grid = hex_grid

        self.grid = hex_grid

        return hex_grid
    
    def get_grid(self):
        return self.grid

    @staticmethod
    def draw_custom_line(surface, color, start_pos, end_pos, thickness, horizontal):
        if horizontal:
            points = [
                start_pos,
                end_pos,
                (end_pos[0], end_pos[1] + thickness),
                (start_pos[0], start_pos[1] + thickness),
            ]
        else:

            points = [
                start_pos,
                end_pos,
                (end_pos[0] + thickness, end_pos[1]),
                (start_pos[0] + thickness, start_pos[1]),
            ]
        pygame.draw.polygon(surface, color, points)

    def draw_grid(self):

        top_left = (self.grid[0][0].rect.left-17, self.grid[0][0].rect.centery-8)
        top_right = (self.grid[0][-1].rect.right-10, self.grid[0][-1].rect.centery-8)
        bottom_left = (self.grid[-1][0].rect.left-10, self.grid[-1][0].rect.centery+10)
        bottom_right = (self.grid[-1][-1].rect.right, self.grid[-1][-1].rect.centery+10)
        top_left_red = (self.grid[0][0].rect.left+2, self.grid[0][0].rect.centery-25)
        top_right_red = (self.grid[0][-1].rect.right-2, self.grid[0][-1].rect.centery-25)
        bottom_left_red = (self.grid[-1][0].rect.left+2, self.grid[-1][0].rect.centery+8)
        bottom_right_red = (self.grid[-1][-1].rect.right-2, self.grid[-1][-1].rect.centery+8)

        top_bottom_border_color = (255, 0, 0)
        sides_border_color = (0, 0, 255)
        border_thickness = 20

        self.draw_custom_line(self.surface, top_bottom_border_color, top_left_red, top_right_red, border_thickness, True)  # top
        self.draw_custom_line(self.surface, top_bottom_border_color, bottom_left_red, bottom_right_red, border_thickness, True)  # bund
        self.draw_custom_line(self.surface, sides_border_color, top_left, bottom_left, border_thickness, False)  # venstre
        self.draw_custom_line(self.surface, sides_border_color, top_right, bottom_right, border_thickness, False)  # højre

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
        self.run = True
        self.paused = False

#    def menu(self):
#        height = game_surface.get_height()
#        width = game_surface.get_width()
#        game_surface.fill(WHITE)
#        start_button = Button(-300, -300, start_button_img, 0.5, (1, 1))
#        # start_button.set_image(start_button.get_image())
#        
#        while self.game_menu:
#            start_button.draw_at_center(game_surface,(width/2, height/4))
#            pygame.display.flip()
#            print(start_button.clicked)
#            for event in pygame.event.get():
#               if event.type == pygame.QUIT:
#                    self.game_menu = False
#                    self.running = False
#                    self.run = False
#                if event.type == pygame.KEYDOWN:
#                    if event.key == pygame.K_ESCAPE:
#                        game_surface.fill(WHITE)
#                        self.game_menu = False
#            #if startbutton is pressed, makes new board which it gives to the play function
#            if start_button.clicked == True:
#                size = 3
#                custom_board = Board(hexagon1,size,self.surface)
#                self.game_menu = False
#                gamelogic.player_no = 0
#                custom_board.make_grid()
#                self.set_board(custom_board)
#
    def play(self):
        game_surface.blit(YELLOW, (0,0))
        self.board.make_grid()
        print("check")
        
        # boardToDisplay = pygame.transform.scale_by(board_surface,0.7)
        #game_surface.blit(boardToDisplay, (51.2, 30))
        while self.running:
            game_surface.blit(YELLOW, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_menu = True
                        self.menu()

            if self.paused:
                if export_game_button.drawMenu(game_surface):
                    print('ExportGame')
                    self.paused = False
                if go_back_button.drawMenu(game_surface):
                    self.paused = False
                self.board.draw_grid()

            if not self.paused:
                #game_surface.fill(YELLOW)
                if pause_game_button.drawMenu(game_surface):
                    self.paused = True 
                if gamelogic.player_no == cpu and gamelogic.player_won == False:
                    self.unit = gamelogic.make_cpu_move()
                else:
                    self.board.draw_grid()
                    if gamelogic.has_player_won(1) or gamelogic.has_player_won(2):
                        text2 = font.render(("Player "+str(gamelogic.player_no+1)+" has won"), True, BLACK)
                        textRect2 = text2.get_rect()
                        textRect2.center = (100, 100)
                        game_surface.blit(text2, [195,200])
                        if back_to_menu.drawMenu(game_surface):
                            #game_surface.fill(YELLOW)
                            gamelogic.board = np.zeros((gamelogic.board_size, gamelogic.board_size), dtype=int)
                            gamelogic.player_won = False
                            self.board.make_grid()
                            self.running = False
                        if restart_button.drawMenu(game_surface):
                            #game_surface.fill(YELLOW)
                            gamelogic.board = np.zeros((gamelogic.board_size, gamelogic.board_size), dtype=int)
                            gamelogic.player_won = False
                            self.board.make_grid()




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

class MenuButton():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def drawMenu(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create button instances
start_game_button = MenuButton(195, 50, start_game_img, 1)
play_online_button = MenuButton(195, 100, Play_Online_img, 1)
ai_2_button = MenuButton(195, 250, AI_2_img, 1)
two_player_button = MenuButton(195, 25, Two_Player_img, 1)
ai_1_button = MenuButton(195, 175, AI_1_img, 1)
ai_3_button = MenuButton(195, 325, AI_3_img, 1)
change_board_size_button = MenuButton(195, 150, Change_Board_Size_img, 1)
settings_button = MenuButton(195, 150, Settings_img, 1)
restart_button = MenuButton(195, 300, Continue_img, 1)
back_to_menu = MenuButton(195, 300, Go_Back_img, 1)
continue_button = MenuButton(195, 100, Continue_img, 1)
export_game_button = MenuButton(46.6, 400, Export_Game_img, 1)
import_game_button = MenuButton(195, 50, Import_Game_img, 1)
go_back_button = MenuButton(343.4, 400, Go_Back_img, 1)
join_game_button = MenuButton(195, 400, Join_Game_img, 1)
host_game_button = MenuButton(195, 400, Host_Game_img, 1)
pause_game_button = MenuButton(195, 350, Pause_Game_img, 1)
player_1_button = MenuButton(195, 50, Player_1_img, 1)
player_2_button = MenuButton(195, 150, Player_2_img, 1)
change_player_button = MenuButton(195, 250, Change_Player_img, 1)
hexagon1 = Button(0, 0, hexagon_neutral_img, tile_scale, (0, 0))
hexagon2 = Button(hexagon_neutral_img.get_width() * tile_scale, 0, hexagon_neutral_img, tile_scale, (0, 1))
hexagon_neutral_img_mask = pygame.mask.from_surface(hexagon_neutral_img)
hexagon_player1 = Button(96, 0, hexagon_player1_img, tile_scale, (1, 1))



# game loop

while run:
    game_surface.fill((200, 200, 255))


    if first_menu == True:
        if start_game_button.drawMenu(game_surface):
            print('first menu')
            second_menu = True
            first_menu = False
            action = True
            gamelogic.player_won = False
        if settings_button.drawMenu(game_surface) :
            first_menu = False
            setting_menu = True
            action = True
            
    if second_menu == True:
        game_surface.blit(Drone_Bee_img, (140, 175))
        game_surface.blit(Worker_Bee_img, (450, 250))
        game_surface.blit(Queen_Bee_img, (140, 325))

        if two_player_button.drawMenu(game_surface) and not action:
                game_running = True
                second_menu = False
                action = True
        if ai_1_button.drawMenu(game_surface) and not action:
                print(cpu)
                cpu = 1
                game_running = True
                second_menu = False
                print(cpu)
                action = True
        if ai_2_button.drawMenu(game_surface) and not action:
                print('playing against bot 1')
                action = True
        if ai_3_button.drawMenu(game_surface) and not action:
                print('playing against bot 1')
                action = True
        if play_online_button.drawMenu(game_surface) and not action:
                print('playing against bot 1')
                action = True
        if go_back_button.drawMenu(game_surface) and not action:
                first_menu = True
                second_menu = False
                action = True



    if game_running == True:

        board1 = Board(hexagon1, gamelogic.board_size, game_surface)
        game1 = Game(game_surface, board1, 0)
        game1.play()
        game_running = False
        if pause_game_button.drawMenu(game_surface):
                game_paused = True

        if game_paused == True:
            if export_game_button.drawMenu(game_surface):
                 print('ExportGame')
                 game_paused = False
                 
            if go_back_button.drawMenu(game_surface):
                 game_paused = False
        first_menu = True

    
    if setting_menu == True:
            text = font.render(str(gamelogic.board_size), True, WHITE)
            textRect = text.get_rect()
            textRect.center = (100, 100)
            game_surface.blit(text, [450, 155])
            if change_board_size_button.drawMenu(game_surface) and not action:
                board_size += 1
                if board_size >= len(board_size_list):
                    board_size = 0
                if board_size < 0:
                    board_size = len(board_size_list)
                #tile_scale += 1
                #if tile_scale >= len(tile_scale_list):
                #    tile_scale = 0
                #if tile_scale < 0:
                #    tile_scale = len(tile_scale_list)
                #x_extra_offset += 1
                #if x_extra_offset >= len(x_extra_offset_list):
                #    x_extra_offset = 0
                #if x_extra_offset < 0:
                #    x_extra_offset = len(x_extra_offset_list)
                #y_extra_offset += 1
                #if y_extra_offset >= len(y_extra_offset_list):
                #    y_extra_offset = 0
                #if y_extra_offset < 0:
                #    y_extra_offset = len(y_extra_offset_list)
                gamelogic.board_size = board_size_list[board_size]
                gamelogic.board = np.zeros((board_size_list[board_size], board_size_list[board_size]), dtype=int)


            if import_game_button.drawMenu(game_surface):
                print('import saved game')
            if change_player_button.drawMenu(game_surface):
                setting_menu = False
                player_option = True
                print('import saved game') 
            if go_back_button.drawMenu(game_surface):
                setting_menu = False
                first_menu = True

    if player_option == True:
        if player_1_button.drawMenu(game_surface):
            print('choose player 1')
        if player_2_button.drawMenu(game_surface):
            print('choose player 2')
        if go_back_button.drawMenu(game_surface):
            player_option = False
            setting_menu = True
        
    if pygame.mouse.get_pressed()[0] == 0:
        action = False
    for event in pygame.event.get():
		    #quit game
            if event.type == pygame.QUIT:
                run = False
    pygame.display.flip()
pygame.quit()