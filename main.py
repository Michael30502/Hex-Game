import socket
import sys
import threading

import numpy as np
import pygame
import math
import string

import pyperclip

import gamelogic
import onlinelogic
import export

pygame.init()
font = pygame.font.SysFont("Arial", 36)
user_text = ""
# LINJER 446 og 455 kan gøre baggrund om til hvid
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
#YELLOW = (255,255,0)

FPS = 60

board_size_list = [3, 5, 7, 9, 11]
full_board_size_list = []
for elem in board_size_list:
    full_board_size_list.append(elem**2)
#tile_scale_list = [0.4, 0.4, 0.4 ,0.4 , 0.4]
#x_extra_offset_list = [76.5, 76.5, 76.5, 76.5, 76.5]
#y_extra_offset_list = [40,40,40,40,40]
tile_scale = 0.4
#x_extra_offset = len(x_extra_offset_list)-1
#y_extra_offset= len(y_extra_offset_list)-1
board_size = len(board_size_list)-1
#x_extra_offset = 76.5
ai_difficulty = 1

run = True
first_menu = True
setting_menu = False
second_menu = False
game_running = False
game_paused = False
game_finished = False
player_option = False
online_menu = False


# Surface/Screen size (this shoudl be scaleable
# WIDTH, HEIGHT = 768, 466
WINDOWWIDTH, WINDOWHEIGHT = 640, 480
game_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
# board_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")

# load button images
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
Main_Menu_img = pygame.image.load('assets/Main_Menu.png').convert_alpha()
Play_Again_img = pygame.image.load('assets/Play_Again.png').convert_alpha()
Exit_Game_img = pygame.image.load('assets/Exit_Game.png').convert_alpha()
YELLOW = pygame.image.load('assets/honeycomb2.jpg')
YELLOW = pygame.transform.scale(YELLOW, (640, 480))

start_button_img = pygame.image.load("assets/start_button_img.png").convert_alpha()
hexagon_neutral_img = pygame.image.load("assets/tile_0.png").convert_alpha()
#hexagon_neutral_img = pygame.transform.scale_by(0.7)
hexagon_player1_img = pygame.image.load("assets/tile_1.png").convert_alpha()
#hexagon_player1_img = pygame.transform.scale_by(0.7)
hexagon_player2_img = pygame.image.load("assets/tile_2.png").convert_alpha()
#hexagon_player2_img = pygame.transform.scale_by(0.7)

# game variables
action = False
pos = None
new_pos = False
new_command = False
command = None
thread_started = False
receive_thread_client = None
receive_thread_server = None
running_thread_server = None


def receive_wait(client_no):
    global pos, new_pos, new_command, command
    pos = None
    command = None
    new_pos = None
    new_command = None

    while True:
        if gamelogic.multiplayer == False:
            print("multiplayer off")

            sys.exit()
        if client_no == 2:
            try:
                pos = connection.receive()
            except:
                print('exit thread')
                sys.exit()
        elif onlinelogic.clientsocket is not None:
            print('pos received 2')
            try:
                pos = onlinelogic.clientsocket.recv(5)
            except:
                print('exit thread')
                sys.exit()
        if pos is not None and len(pos) > 0:
            if pos.decode('utf-8') == "contt" or pos.decode('utf-8') == "exitt" or pos.decode('utf-8')[0] == "S":
                print('command received')
                new_command = True
                command = pos.decode('utf-8')
                pos = None
            else:
                print('pos received 1')
                new_pos = True


def restart_game():
    game_surface.fill(WHITE)
    gamelogic.board = np.zeros((gamelogic.board_size, gamelogic.board_size), dtype=int)
    gamelogic.player_won = False
    gamelogic.player_no = gamelogic.default_starting_player
    game1.board.make_grid()


def exit_game():
    global connection
    print("exit")
    restart_game()
    if gamelogic.multiplayer:
        if gamelogic.client_no == 2:
            if connection is not None:
                print("check")
                connection.send(bytes("exitt", 'utf-8'))
                connection.sock.shutdown(socket.SHUT_RDWR)
                connection.sock.close()
                connection = None
        else:
            if onlinelogic.clientsocket is not None:
                try:
                    onlinelogic.clientsocket.send(bytes("exitt", 'utf-8'))
                except:
                    pass
                onlinelogic.clientsocket = None
            onlinelogic.shutdown = True

    game1.running = False
    gamelogic.client_no = 0
    gamelogic.player_won = False
    gamelogic.multiplayer = False
    gamelogic.local_multiplayer = False
    gamelogic.cpu = 0

def draw_textbox(screen, rect, text):
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, (255, 255, 255)) # White color text
    pygame.draw.rect(screen, (0, 0, 0), rect) # Black color box
    screen.blit(text_surface, (rect[0]+5, rect[1]+5))

class Button:
    def __init__(self, x, y, image, scale, unit):
        self.image = image  # Store original image
        self.scale = scale
        self.player = None
        self.width = int(self.image.get_width() * self.scale)
        self.height = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.mask = pygame.mask.from_surface(self.image)
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
            if gamelogic.board[self.unit[0]][self.unit[1]] == gamelogic.default_starting_player:
                # print(board1.grid)
                board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
            elif gamelogic.board[self.unit[0]][self.unit[1]] != 0:
                board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)

        # checking collision and clicked
        if self.rect.collidepoint(mouse_pos) and not game1.paused:
            # print('hover:' + str(self.unit))
            # Checking if we are leftclicking a button that has not been clicked, then changing the image

            pygame.event.get()
            if pygame.mouse.get_pressed()[0] == 1 and not action:
                action = True
                self.clicked = True
                gamelogic.make_actual_move(self.unit)
            # print("mulitplayer {}".format(gamelogic.multiplayer))
            # print("client_no {}".format(gamelogic.client_no))
            # print(gamelogic.player_no)
            # print( gamelogic.client_no != gamelogic.player_no)
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

        if gamelogic.board[self.unit[0]][self.unit[1]] == gamelogic.default_starting_player:
            board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
        elif gamelogic.board[self.unit[0]][self.unit[1]] != 0:
            board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)

        # checking colision and clicked
        if self.rect.collidepoint(mouse_pos) and not game1.paused:
            pygame.event.get()
            if pygame.mouse.get_pressed()[0] == 1 and not action:
                action = True
                self.clicked = True
                gamelogic.make_actual_move(self.unit)
                game1.board.draw_grid()

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
             y_extra_offset = 50
        elif self.size==7:
             x_extra_offset=165
             y_extra_offset = 60
        elif self.size==5:
             x_extra_offset=209.3
             y_extra_offset = 70
        elif self.size==3:
             x_extra_offset=253.6
             y_extra_offset = 80
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

        top_bottom_border_color = (160, 44, 44)
        sides_border_color = (0, 0, 170)
        border_thickness = 20

        self.draw_custom_line(self.surface, top_bottom_border_color, top_left_red, top_right_red, border_thickness, True)  # top
        self.draw_custom_line(self.surface, top_bottom_border_color, bottom_left_red, bottom_right_red, border_thickness, True)  # bottom
        self.draw_custom_line(self.surface, sides_border_color, top_left, bottom_left, border_thickness, False)  # left
        self.draw_custom_line(self.surface, sides_border_color, top_right, bottom_right, border_thickness, False)  # right

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
        global new_pos, new_command
        global pos
        global thread_started
        global receive_thread_client
        global receive_thread_server
        global running_thread_server
        on_connect = True
        game_surface.blit(YELLOW,(0,0))
        #game_surface.fill(WHITE)
        self.board.make_grid()
        print("check")
        
        global user_text
        # boardToDisplay = pygame.transform.scale_by(board_surface,0.7)
        #game_surface.blit(boardToDisplay, (51.2, 30))
        while self.running:

            game_surface.blit(YELLOW, (0,0))
            #game_surface.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        # exporting game as a string to load
                        user_text = array_to_string(gamelogic.board)
                    if event.key == pygame.K_ESCAPE:
                        self.game_menu = True

            if self.paused:
                if export_game_button.drawMenu(game_surface):
                    if(is_board_legal(gamelogic.board)):
                        print(gamelogic.board)
                        export.export_board(gamelogic.board)
                        user_text = array_to_string(gamelogic.board)
                        with open('export.txt', 'a') as f:
                            f.write("\n")
                            f.write(array_to_string(gamelogic.board))
                        print("board exported")
                    else:
                        print("board is not legal and cant be exported ")
                    self.paused = False
                if go_back_button.drawMenu(game_surface):
                    self.paused = False
                self.board.draw_grid()
                if exit_game_button.drawMenu(game_surface):
                    exit_game()
            if not self.paused:
                #game_surface.fill(YELLOW)
                if not gamelogic.has_any_won(gamelogic.board):
                    if pause_game_button.drawMenu(game_surface):
                        self.paused = True 
                if gamelogic.client_no == 1 and gamelogic.multiplayer:
                    if running_thread_server is not None:
                        if not running_thread_server.is_alive():
                            print("Server dead")
                            exit_game()
                            running_thread_server = None
                    else:
                        exit_game()

                if gamelogic.update_board:
                    game1.board.draw_grid()
                # print(gamelogic.has_any_won(gamelogic.board))
                if gamelogic.player_no == gamelogic.cpu and not gamelogic.has_any_won(gamelogic.board) and not gamelogic.multiplayer and ai_difficulty ==1:
                    self.unit = gamelogic.make_ai1_move()
                if gamelogic.player_no == gamelogic.cpu and not gamelogic.has_any_won(gamelogic.board) and not gamelogic.multiplayer and ai_difficulty == 2:
                    self.unit = gamelogic.make_ai2_move()
                if gamelogic.player_no == gamelogic.cpu and not gamelogic.has_any_won(gamelogic.board) and not gamelogic.multiplayer and ai_difficulty == 3:
                    self.unit = gamelogic.make_ai3_move()
                else:
                    self.board.draw_grid()
                    if gamelogic.has_any_won(gamelogic.board):
                        if gamelogic.has_player_won(1, gamelogic.board):
                            text2 = font.render("Player 1 has won", True, BLACK)
                        elif gamelogic.has_player_won(2, gamelogic.board):
                            text2 = font.render("Player 2 has won", True, BLACK)
                        textRect2 = text2.get_rect()
                        textRect2.center = (100, 100)
                        game_surface.blit(text2, [195, 200])
                        if not gamelogic.multiplayer or gamelogic.client_no == 1:


                            if main_menu_button.drawMenu(game_surface):
                                if gamelogic.multiplayer:
                                    onlinelogic.clientsocket.send(bytes("exitt", 'utf-8'))

                                exit_game()

                            if play_again_button.drawMenu(game_surface):
                                if gamelogic.multiplayer:
                                    onlinelogic.clientsocket.send((bytes("contt", 'utf-8')))

                                restart_game()
                        else:
                            text3 = font.render("Waiting for host...", True, BLACK)
                            # textRect3 = text2.get_rect()
                            # textRect3.center = (100, 100)
                            game_surface.blit(text3, [300, 650])

                if gamelogic.multiplayer:
                    if gamelogic.client_no == 2:
                        if len(gamelogic.move_list) > 0:
                            (x, y) = gamelogic.move_list[0]
                            value = str(x) + "," + str(y)
                            while len(value) < 5:
                                value += " "
                            print(len(bytes(value, 'utf-8')))
                            connection.send(bytes(value, 'utf-8'))
                            gamelogic.move_list.clear()
                            print("checkmove")


                    # print(onlinelogic.clientsocket)
                    if gamelogic.client_no == 1 and onlinelogic.clientsocket is not None:
                        if on_connect:
                            game_surface.fill(WHITE)
                            self.board.make_grid()
                            on_connect = False
                        if len(gamelogic.move_list) > 0:
                            (x, y) = gamelogic.move_list[0]
                            value = str(x) + "," + str(y)
                            print(value)
                            while len(value) < 5:
                                value += " "

                            print(len(bytes(value, 'utf-8')))
                            onlinelogic.clientsocket.send(bytes(value, 'utf-8'))
                            gamelogic.move_list.clear()


                    elif onlinelogic.clientsocket is None and gamelogic.client_no == 1:
                        # print("checks")
                        text2 = font.render("Waiting for player...", True, BLACK)
                        textRect2 = text2.get_rect()
                        textRect2.center = (100, 100)
                        game_surface.blit(text2, [200, 420])

                    if new_command:
                        if command == "contt":
                            restart_game()
                        if command == "exitt":
                            exit_game()
                            # Settings
                        if command[0] == "S":
                            if command[1] == "s":
                                gamelogic.board_size = int(command[2:])
                                print(gamelogic.board_size)
                                board1.size = gamelogic.board_size
                                restart_game()
                            elif command[1] == "p":
                                gamelogic.default_starting_player = int(command[2:])
                                print("current player = {}".format(gamelogic.default_starting_player))
                                gamelogic.player_no = gamelogic.default_starting_player
                                restart_game()

                        new_command = False
                    if new_pos:
                        print(pos)
                        pos = pos.decode('utf-8')
                        (x, y) = pos.split(",")
                        print(pos)
                        pos = (int(x), int(y))
                        gamelogic.make_actual_move(pos, True)
                        pos = None
                        new_pos = False
            pygame.display.flip()

    def get_turn(self):
        return self.turn

    def set_board(self, board):

        self.board = board

    def turn_count(self):
        self.turn += 1


class MenuButton:

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


#create button instances
exit_game_button = MenuButton(350, 50, Exit_Game_img, 1)
play_again_button = MenuButton(195, 275, Play_Again_img, 1)
main_menu_button = MenuButton(195, 350, Main_Menu_img, 1)
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
join_game_button = MenuButton(195, 150, Join_Game_img, 1)
host_game_button = MenuButton(195, 50, Host_Game_img, 1)
pause_game_button = MenuButton(195, 350, Pause_Game_img, 1)
player_1_button = MenuButton(195, 50, Player_1_img, 1)
player_2_button = MenuButton(195, 150, Player_2_img, 1)
change_player_button = MenuButton(195, 250, Change_Player_img, 1)
hexagon1 = Button(0, 0, hexagon_neutral_img, tile_scale, (0, 0))
hexagon2 = Button(hexagon_neutral_img.get_width() * tile_scale, 0, hexagon_neutral_img, tile_scale, (0, 1))
hexagon_neutral_img_mask = pygame.mask.from_surface(hexagon_neutral_img)
hexagon_player1 = Button(96, 0, hexagon_player1_img, tile_scale, (1, 1))

# import -----------------------------------------------------------------------------------------
clock = pygame.time.Clock()

# it will display on screen

# basic font for user typed
base_font = pygame.font.Font(None, 32)
user_text = ''

# create rectangle for input 
input_rect = pygame.Rect(0, 210, WINDOWWIDTH, 32)
input_rect_color = pygame.Color('chartreuse4')
# color_passive = pygame.Color('chartreuse4')
# input_rect_color = color_passive

# takes gamelogic board and changes it
# better name may be needed TODO
def import_game_setter(game_arr_str):
    gamelogic.board = game_arr_str
    print("board set")
    print(gamelogic.board)
    print(type(gamelogic.board))
    return gamelogic.board


def array_to_string(array):
    # (this will be a list of integers sepperated by ' ')
    return " ".join(str(elem) for elem in array.flat)

# the line bellow makes it so that the array_to_string function is used when printing the array or getting string version. Was used while testing
# np.set_string_function(array_to_string, repr=False)

#TODO check size of array in this function maybe
def string_to_square_numpy_array(input_string):
    # Split the string into integers and convert them to a numpy array
    flat_array = np.array([int(elem) for elem in input_string.split()])
    print("flat array is")
    print(flat_array)
    # assumes that the  array is square
    # TODO if we are moving into none-square arrays another method will be needed
    array_size = int(np.sqrt(flat_array.size))

    # Reshape the flat array into a square array
    array = flat_array.reshape((array_size, array_size))
    print("new array is")
    print(array)
    print(type(array))
    return array

# Checking the elements in arr are either 0,1,2 and that ther is only a difference of 1 in the ammount of player elements
def is_board_legal(board):
    #for player tile checking
    values, counts = np.unique(board, return_counts=True)
    #we start by determining if the size is a perfect square
    #TODO this is not working. a bad fix is hardcoding for the specific size we allow
    #check if other values than 0,1,2 is in the array
    if(np.amax(board) > 2):
        print(" wrong values in array, entries cant be larger than 2")
        return False
    elif(np.amin(board) < 0):
        print(" wrong values in array, entries cant be smaller than 0")
        return False
    #checks if the boards only contains 0's
    elif(len(values) < 2):
        print("board is empty but legal")
        return True
    #if player 1 has more or equal 2 tiles while player 2 has 0 board is illegal
    elif len(values) < 3 and (0 in values and 1 in values):
        if counts[1] >= 2:
            print("player 1 has too many tiles")
            return False
        else:
            #this is when the only move made is player 1
            return True
    #same with player 2 but this time since player 1 always starts the number cant exceed 1
    elif len(values) < 3 and (0 in values and 2 in values):
        if counts[1] >= 1:
            print("player 2 has too many tiles")
            return False
        else:
            print("this should not be possible to reach 2")
            return True
        
    elif len(values) < 3 and (1 in values and 2 in values):
        #this is a case where the board we are trying to import is full
        #TODO maybe give a prompt to the user that player x has won
        print("player has won")
        return False
    #checking if the difference between player tiles is larger than 1
    elif abs(counts[1] - counts[2]) >= 2:
        print("difference in player tiles is too big")
        return False
        
    else:
        print("board is legal")
        return True   
    

def calculate_player_turn(board):
    values = np.unique(board)
    #absolute difference between player tiles (must not exceed 1)
    
    #if there is only 1 element in values assuming the only element present is 0 #TODO
    if len(values) < 2:
        return 1
    #if there are 2 elements present in our array and 1 of them is 1 assuming rest is 0 then it must be player 2's turn
    elif len(values) < 3 and (1 in values):
        return 2
    elif len(values) < 3 and (2 in values):
        return 1
    elif values[1] <= values[2]:
        return 1
    elif values[2] < values[1]:
        return 2
    else:
        print("calculate_player_turn ERROR")
        return 0

#import end -----------------------------------------------------------------------------------------

# game loop
def server_thread():
    global receive_thread_client
    global receive_thread_server
    global running_thread_server
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
        if settings_button.drawMenu(game_surface):
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
            gamelogic.local_multiplayer = True
            action = True
        if ai_1_button.drawMenu(game_surface) and not action:
            #print(cpu)
            gamelogic.cpu = 2
            ai_difficulty = 1
            #cpu = 2 #TODO this need to be no hard coded if the change player works
            game_running = True
            second_menu = False
            #print(cpu)
            action = True
        if ai_2_button.drawMenu(game_surface) and not action:
            gamelogic.cpu = 2
            ai_difficulty = 2
            game_running = True
            second_menu = False
            print('Playing gainst bot 2')
        if ai_3_button.drawMenu(game_surface) and not action:
            gamelogic.cpu = 2
            ai_difficulty = 3
            game_running = True
            second_menu = False
            print('playing against bot 3')
            action = True
        if play_online_button.drawMenu(game_surface) and not action:
            online_menu = True
            second_menu = False
            print('joining a server')
            action = True
        if go_back_button.drawMenu(game_surface) and not action:
            first_menu = True
            second_menu = False
            action = True
            
    if online_menu == True:
        input_box = pygame.Rect(200, 210, 243, 32)
        ip_text = onlinelogic.ip_text
        draw_textbox(game_surface, input_box, onlinelogic.ip_text)
        if go_back_button.drawMenu(game_surface) and not action:
            second_menu = True
            online_menu = False
        if join_game_button.drawMenu(game_surface) and not action:
            try:
                connection = onlinelogic.GameSocket()
                connection.connect(onlinelogic.ip_text, onlinelogic.port_text)
                gamelogic.multiplayer = True
                game_running = True
                second_menu = False
                receive_thread_client = threading.Thread(target=receive_wait, args=(2,))
                receive_thread_client.start()
                gamelogic.client_no = 2
                online_menu = False


            except:
                print("Connection not made")

        if host_game_button.drawMenu(game_surface) and not action:
            online_menu = False
            print('hosting a server')
            gamelogic.multiplayer = True
            running_thread_server = threading.Thread(target=server_thread)
            running_thread_server.start()
            receive_thread_server = threading.Thread(target=receive_wait, args=(1,))
            receive_thread_server.start()

            gamelogic.client_no = 1
            game_running = True
            second_menu = False
            action = True

    if game_running == True:
        board1 = Board(hexagon1, gamelogic.board_size, game_surface)
        game1 = Game(game_surface, board1, 1)
        game1.play()
        game_running = False
        print(gamelogic.player_no)
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
        game_surface.blit(text, [450, 160])
        if change_board_size_button.drawMenu(game_surface) and not action:

            board_size += 1
            if board_size >= len(board_size_list):
                board_size = 0
            if board_size < 0:
                board_size = len(board_size_list)
            gamelogic.board_size = board_size_list[board_size]
            gamelogic.board = np.zeros((board_size_list[board_size], board_size_list[board_size]), dtype=int)

        if import_game_button.drawMenu(game_surface):
            import_game = True

            while (import_game):
                
                for event in pygame.event.get():
                    # quit game
                    # TODO make the other settings buttons work in this loop
                    if event.type == pygame.QUIT:
                        import_game = False
                        user_text = ""
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_rect.collidepoint(event.pos):
                            active = True
                        else:
                            active = False
                    if event.type == pygame.KEYDOWN:
                        # TODO add arrow keys in order to changes parts of an exported string
                        if event.key == pygame.K_BACKSPACE:
                            # delete character from string
                            user_text = user_text[:-1]
                        elif event.key == pygame.K_b:
                            user_text = str(pyperclip.paste())
                        elif event.key == pygame.key.get_mods():
                            pass
                        elif event.key == pygame.K_RETURN:
                            #TODO change the game logic boardsize
                            #TODO make some variable to show that the game has been imported and let
                            #the function "calculate_player" determine whos turn it is
                            user_text_size = user_text.split()
                            # print(len(user_text_size))
                            if(len(user_text_size) not in full_board_size_list):
                                print("board size is not a perfect square ")
                                print("please try again")
                                import_game = False
                            # print(array_to_string(gamelogic.board))
                            #temporary fix for my dimension check #TODO remove this
                            # try:
                            #     placeholder_arr = string_to_square_numpy_array(user_text)

                            # except:
                            #     #TODO we need to prompt the user that the board was not successfully imported
                            #     placeholder_arr = gamelogic.board
                            #     print("wrong format, original board loaded")
                                
                            #error handling
                            else:
                                
                                placeholder_arr = string_to_square_numpy_array(user_text)
                                if (is_board_legal(placeholder_arr)):
                                    try:
                                        gamelogic.board = string_to_square_numpy_array(user_text)
                                        print("board has been imported")
                                    except ValueError:
                                        print("wrong format")
                                        user_text = ""
                                    except:
                                        print("something else")
                                        user_text = ""
                                    import_game = False
                                else:
                                    print("board is illegal")
                                
                                # gamelogic.board = string_to_square_numpy_array(user_text)
                        # Unicode standard is used for string
                        else:
                            user_text += event.unicode
                #ez input field with less settings solution
                # draw_textbox(game_surface,input_rect, user_text)
                pygame.draw.rect(game_surface, input_rect_color, input_rect)
                text_surface = base_font.render(user_text, True, (255, 255, 255))

                # render at position stated in arguments
                game_surface.blit(text_surface, (input_rect.x, input_rect.y))
                input_rect.w = max(100, text_surface.get_width()+1000)
                pygame.display.flip()
                clock.tick(60)
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
            gamelogic.default_starting_player = 1
            gamelogic.player_no = gamelogic.default_starting_player
        if player_2_button.drawMenu(game_surface):
            print('choose player 2')
            gamelogic.default_starting_player = 2
            gamelogic.player_no = gamelogic.default_starting_player
        if go_back_button.drawMenu(game_surface):
            player_option = False
            setting_menu = True

    if pygame.mouse.get_pressed()[0] == 0:
        action = False

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                # exporting game as a string to load
                user_text = array_to_string(gamelogic.board)
            elif event.key == pygame.K_v:
                if(is_board_legal(gamelogic.board)):
                    print(gamelogic.board)
                    export.export_board(gamelogic.board)
                    print("board exported")
                else:
                    print("board not legal")
            elif event.key == pygame.K_b:
                user_text = str(pyperclip.paste())
            elif event.key == pygame.K_RETURN:
                print(user_text)
                user_text = ''

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    pygame.display.flip()

pygame.quit()
