import sys
import threading

import numpy as np
import pygame

import gamelogic
import onlinelogic


pygame.init()
font = pygame.font.SysFont("Arial", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

cpu = 0
board_size_list = [3, 5, 7, 9, 11]
board_size = len(board_size_list) - 1

run = True
first_menu = True
setting_menu = False
second_menu = False
game_running = False
game_paused = False
game_finished = False

# Surface/Screen size (this shoudl be scaleable
WIDTH, HEIGHT = 800, 800
game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")

# load button images
start_game_img = pygame.image.load('assets/Start_Game.png').convert_alpha()
AI_1_img = pygame.image.load('assets/AI_1.png').convert_alpha()
Play_Online_img = pygame.image.load('assets/Play_Online.png').convert_alpha()
AI_2_img = pygame.image.load('assets/AI_2.png').convert_alpha()
AI_3_img = pygame.image.load('assets/AI_3.png').convert_alpha()
Change_Board_Size_img = pygame.image.load('assets/Change_Board_Size.png').convert_alpha()
Continue_img = pygame.image.load('assets/Continue.png').convert_alpha()
Export_Game_img = pygame.image.load('assets/Export_Game.png').convert_alpha()
Import_Game_img = pygame.image.load('assets/Import_Game.png').convert_alpha()
Pause_Game_img = pygame.image.load('assets/Pause_Game.png').convert_alpha()
Settings_img = pygame.image.load('assets/Settings.png').convert_alpha()
Two_Player_img = pygame.image.load('assets/Two_Player.png').convert_alpha()
Go_Back_img = pygame.image.load('assets/Go_Back.png').convert_alpha()

start_button_img = pygame.image.load("assets/start_button_img.png").convert_alpha()
hexagon_neutral_img = pygame.image.load("assets/tile_0.png").convert_alpha()
hexagon_player1_img = pygame.image.load("assets/tile_1.png").convert_alpha()
hexagon_player2_img = pygame.image.load("assets/tile_2.png").convert_alpha()

# game variables
action = False
pos = None
new_pos = False
thread_started = False
receive_thread_client = None
receive_thread_server = None

def receive_wait(client_no):
    global pos, new_pos
    if client_no == 1:
       pos = connection.receive()
    else:
        pos = onlinelogic.clientsocket.recv(5)
    new_pos = True
    sys.exit()

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
                # print(board1.grid)
                board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
            elif gamelogic.board[self.unit[0]][self.unit[1]] == 2:
                board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)

        # checking collision and clicked
        if self.rect.collidepoint(mouse_pos):
            # print('hover:' + str(self.unit))
            # Checking if we are leftclicking a button that has not been clicked, then changing the image

            pygame.event.get()
            if pygame.mouse.get_pressed()[0] == 1 and not action:
                action = True
                self.clicked = True
                gamelogic.make_move(self.unit)
       # print("mulitplayer {}".format(gamelogic.multiplayer))
        #print("client_no {}".format(gamelogic.client_no))
        #print(gamelogic.player_no)
        #print( gamelogic.client_no != gamelogic.player_no)
                        # if game1.get_turn() % 2 == 1 and board1.grid[self.unit[0]][self.unit[1]].get_player() == None:

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

    # DRAW AT CENTER FUNCTION FOR THE MENU NOT HEXAGONS
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
                gamelogic.make_actual_move(self.unit)

            if pygame.mouse.get_pressed()[0] == 0:
                action = False

        # display the image on screen
        rect = self.rect
        rect.center = (dest[0], dest[1])
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
        self.run = True

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
        global new_pos
        global pos
        global thread_started
        global receive_thread_client
        global receive_thread_server
        game_surface.fill(WHITE)
        self.board.make_grid()
        print("check")
        while self.running:
            if gamelogic.player_no == cpu and not gamelogic.has_any_won(gamelogic.board):
                self.unit = gamelogic.make_ai1_move()
            else:
                self.board.draw_grid()
                if gamelogic.has_any_won(gamelogic.board):
                    if gamelogic.has_player_won(1, gamelogic.board):
                        text2 = font.render("Player 1 has won", True, BLACK)
                    elif gamelogic.has_player_won(2, gamelogic.board):
                        text2 = font.render("Player 2 has won", True, BLACK)
                    textRect2 = text2.get_rect()
                    textRect2.center = (100, 100)
                    game_surface.blit(text2, [300, 500])
                    if back_to_menu.drawMenu(game_surface):
                        game_surface.fill(WHITE)
                        gamelogic.board = np.zeros((gamelogic.board_size, gamelogic.board_size), dtype=int)
                        # gamelogic.player_won = False
                        self.board.make_grid()
                        self.running = False
                    if restart_button.drawMenu(game_surface):
                        game_surface.fill(WHITE)
                        gamelogic.board = np.zeros((gamelogic.board_size, gamelogic.board_size), dtype=int)
                        # gamelogic.player_won = False
                        self.board.make_grid()


            if gamelogic.multiplayer:
                if gamelogic.client_no == 1:
                    if len(gamelogic.move_list) > 0:
                        (x, y) = gamelogic.move_list[0]
                        value = str(x) + "," + str(y)
                        while len(value)< 5:
                            value += " "
                        print(len(bytes(value, 'utf-8')))
                        connection.send(bytes(value, 'utf-8'))
                        gamelogic.move_list.clear()
                        print("checkmove")

                    elif gamelogic.client_no != gamelogic.player_no and thread_started == False:
                        receive_thread_client.start()
                        thread_started = True

                    if new_pos:
                        pos = pos.decode('utf-8')
                        print(pos)
                        (x, y) = pos.split(",")
                        pos = (int(x), int(y))
                        gamelogic.board[pos] = 1
                        game1.board.draw_grid()
                        gamelogic.player_no = (gamelogic.player_no + 1) % 2
                        new_pos = False
                        thread_started = False
                        receive_thread_client = threading.Thread(target=receive_wait, args=(1 ,))



                if gamelogic.client_no == 0:
                    if len(gamelogic.move_list) > 0:
                        (x, y) = gamelogic.move_list[0]
                        value = str(x) + "," + str(y)
                        print(value)
                        while len(value) < 5:
                            value += " "

                        print(len(bytes(value, 'utf-8')))
                        onlinelogic.clientsocket.send(bytes(value, 'utf-8'))
                        gamelogic.move_list.clear()

                    elif gamelogic.client_no != gamelogic.player_no and thread_started == False:
                        receive_thread_server.start()
                        thread_started = True
                    if new_pos:
                        pos = pos.decode('utf-8')
                        print(pos)
                        (x, y) = pos.split(",")
                        pos = (int(x), int(y))
                        print(pos)
                        gamelogic.board[pos] = 2
                        game1.board.draw_grid()
                        gamelogic.player_no = (gamelogic.player_no + 1) % 2
                        new_pos = False
                        thread_started = False
                        receive_thread_server = threading.Thread(target=receive_wait, args=(0,))

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
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create button instances
start_game_button = MenuButton(100, 100, start_game_img, 2)
play_online_button = MenuButton(300, 200, Play_Online_img, 2)
ai_2_button = MenuButton(300, 400, AI_2_img, 2)
two_player_button = MenuButton(300, 100, Two_Player_img, 2)
ai_1_button = MenuButton(300, 300, AI_1_img, 2)
ai_3_button = MenuButton(300, 500, AI_3_img, 2)
change_board_size_button = MenuButton(300, 200, Change_Board_Size_img, 2)
settings_button = MenuButton(100, 200, Settings_img, 2)
restart_button = MenuButton(400, 600, Continue_img, 2)
back_to_menu = MenuButton(100, 600, Go_Back_img, 2)
continue_button = MenuButton(300, 200, Continue_img, 2)
export_game_button = MenuButton(300, 100, Export_Game_img, 2)
import_game_button = MenuButton(300, 100, Import_Game_img, 2)
pause_game_button = MenuButton(600, 600, Pause_Game_img, 1)
go_back_button = MenuButton(600, 600, Go_Back_img, 1)
hexagon1 = Button(0, 0, hexagon_neutral_img, 0.5, (0, 0))
hexagon2 = Button(hexagon_neutral_img.get_width() * 0.5, 0, hexagon_neutral_img, 0.5, (0, 1))
hexagon_neutral_img_mask = pygame.mask.from_surface(hexagon_neutral_img)
hexagon_player1 = Button(96, 0, hexagon_player1_img, 0.5, (1, 1))

# game loop
def server_thread():
    global receive_thread_client
    global receive_thread_server
    server = onlinelogic.serversocket()
    server.create_server()

while run:
    game_surface.fill((200, 200, 255))

    if first_menu == True:
        if start_game_button.drawMenu(game_surface):
            print('first menu')
            second_menu = True
            first_menu = False
            action = True
            gamelogic.multiplayer = False
            gamelogic.player_won = False
        if settings_button.drawMenu(game_surface) :
            first_menu = False
            setting_menu = True
            action = True

    if second_menu == True:
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
                print('hosting a server')
                thread = threading.Thread(target=server_thread)
                thread.start()
                receive_thread_server = threading.Thread(target=receive_wait, args=(0,))

                gamelogic.client_no = 0
                game_running = True
                second_menu = False
                gamelogic.multiplayer = True
                action = True
        if ai_3_button.drawMenu(game_surface) and not action:
            print('playing against bot 1')
            action = True
        if play_online_button.drawMenu(game_surface) and not action:
                print('joining a server')
                connection = onlinelogic.GameSocket()
                gamelogic.multiplayer = True
                receive_thread_client = threading.Thread(target=receive_wait, args=(1,))
                gamelogic.client_no = 1
                try:
                    connection.connect("10.209.175.124", 25565)
                    game_running = True
                    second_menu = False
                except:
                    print("Connection not made")
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
        first_menu = True


    if setting_menu == True:
        text = font.render(str(gamelogic.board_size), True, WHITE)
        textRect = text.get_rect()
        textRect.center = (100, 100)
        game_surface.blit(text, [220, 225])
        if change_board_size_button.drawMenu(game_surface) and not action:

            board_size += 1
            if board_size >= len(board_size_list):
                board_size = 0
            if board_size < 0:
                board_size = len(board_size_list)
            gamelogic.board_size = board_size_list[board_size]
            gamelogic.board = np.zeros((board_size_list[board_size], board_size_list[board_size]), dtype=int)

        if import_game_button.drawMenu(game_surface):
            print('import saved game')
        if go_back_button.drawMenu(game_surface):
            setting_menu = False
            first_menu = True
    if pygame.mouse.get_pressed()[0] == 0:
        action = False
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
