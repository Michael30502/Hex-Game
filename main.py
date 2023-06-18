# Written by everyone, specific sections marked

import socket
import sys
import threading

import numpy as np
import pygame

import math
import inputting
import gamelogic
import onlinelogic
import export
import importing

pygame.init()
font = pygame.font.SysFont("Arial", 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

board_size_list = [3, 4, 5, 7, 9, 11, 12, 13, 99]
full_board_size_list = []
for elem in board_size_list:
    full_board_size_list.append(elem ** 2)
tile_scale = 0.4
board_size = len(board_size_list) - 1
ai_difficulty = 0

run = True
first_menu = True
setting_menu = False
second_menu = False
game_running = False
game_paused = False
game_finished = False
player_option = False
online_menu = False
imported = False  # TODO
import_game = False

# Surface/Screen size
WINDOWWIDTH, WINDOWHEIGHT = 640, 480
game_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("HEX")
user_text = ""

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
Drone_Bee_Img_flip = pygame.transform.flip(Drone_Bee_Img, True, False)
Drone_Bee_img = pygame.transform.scale(Drone_Bee_Img, (50, 50))
Worker_Bee_Img = pygame.image.load('assets/Worker_Bee_pic.png').convert_alpha()
Worker_Bee_Img_flip = pygame.transform.flip(Worker_Bee_Img, True, False)
Worker_Bee_img = pygame.transform.scale(Worker_Bee_Img, (50, 50))
Queen_Bee_Img = pygame.image.load('assets/Queen_Bee_pic.png').convert_alpha()
Queen_Bee_Img_flip = pygame.transform.flip(Queen_Bee_Img, True, False)
Queen_Bee_img = pygame.transform.scale(Queen_Bee_Img, (50, 50))
Player_1_pic_Img = pygame.image.load('assets/Player_1_pic.png').convert_alpha()
Player_1_pic_img = pygame.transform.scale(Player_1_pic_Img, (50, 50))
Player_2_pic_Img = pygame.image.load('assets/Player_2_pic.png').convert_alpha()
Player_2_pic_Img_flip = pygame.transform.flip(Player_2_pic_Img, True, False)
Player_2_pic_img = pygame.transform.scale(Player_2_pic_Img_flip, (50, 50))
Main_Menu_img = pygame.image.load('assets/Main_Menu.png').convert_alpha()
Play_Again_img = pygame.image.load('assets/Play_Again.png').convert_alpha()
Exit_Game_img = pygame.image.load('assets/Exit_Game.png').convert_alpha()

Player_1_Wins_Img = pygame.image.load('assets/Player_1_Wins.png').convert_alpha()
Player_1_Wins_img = pygame.transform.scale(Player_1_Wins_Img, (50, 50))
Player_2_Wins_Img = pygame.image.load('assets/Player_2_Wins.png').convert_alpha()
Player_2_Wins_img = pygame.transform.scale(Player_2_Wins_Img, (50, 50))

Player_1_Turn = pygame.image.load('assets/Player_1_Turn.png').convert_alpha()
Player_2_Turn = pygame.image.load('assets/Player_2_Turn.png').convert_alpha()

Player_1_man_img = pygame.transform.scale(Player_2_pic_Img_flip, (50, 50))
Player_2_man_img = pygame.transform.scale(Player_1_pic_Img, (50, 50))
Player_1_ai1_img = pygame.transform.scale(Drone_Bee_Img, (50, 50))
Player_2_ai1_img = pygame.transform.scale(Drone_Bee_Img_flip, (50, 50))
Player_1_ai2_img = pygame.transform.scale(Worker_Bee_Img_flip, (50, 50))
Player_2_ai2_img = pygame.transform.scale(Worker_Bee_Img, (50, 50))
Player_1_ai3_img = pygame.transform.scale(Queen_Bee_Img_flip, (50, 50))
Player_2_ai3_img = pygame.transform.scale(Queen_Bee_Img, (50, 50))

YELLOW = pygame.image.load('assets/honeycomb2.jpg')
YELLOW = pygame.transform.scale(YELLOW, (640, 480))

start_button_img = pygame.image.load("assets/start_button_img.png").convert_alpha()
hexagon_neutral_img = pygame.image.load("assets/tile_0.png").convert_alpha()
hexagon_player1_img = pygame.image.load("assets/tile_1.png").convert_alpha()
hexagon_player2_img = pygame.image.load("assets/tile_2.png").convert_alpha()

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
        if not gamelogic.multiplayer:
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
    global ai_difficulty
    ai_difficulty = 0
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


class Button:
    def __init__(self, x, y, image, scale, unit):
        self.image = image  # Store original image
        self.scale = scale
        self.player = None
        self.width = int(self.image.get_width() * self.scale)
        self.height = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.unit = unit
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

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
                board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player1_img)
            elif gamelogic.board[self.unit[0]][self.unit[1]] == 2:
                board1.grid[self.unit[0]][self.unit[1]].set_image(hexagon_player2_img)

        # checking collision and clicked buttons (hitboxes)
        if self.rect.collidepoint(mouse_pos) and not game1.paused:
            # Checking if we are leftclicking a button that has not been clicked, then changing the image

            pygame.event.get()
            if pygame.mouse.get_pressed()[0] == 1 and not action:
                action = True
                self.clicked = True
                gamelogic.make_actual_move(self.unit)

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
        x_extra_offset = (640 - (self.size * 44.2)) * 0.5
        y_extra_offset = 95 - (self.size * 5)
        hex_grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                hex_x = (j + i * 0.5) * x_offset + x_extra_offset
                hex_y = i * y_offset * 0.74 + y_extra_offset
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

        top_left = (self.grid[0][0].rect.left - 17, self.grid[0][0].rect.centery - 8)
        top_right = (self.grid[0][-1].rect.right - 10, self.grid[0][-1].rect.centery - 8)
        bottom_left = (self.grid[-1][0].rect.left - 10, self.grid[-1][0].rect.centery + 10)
        bottom_right = (self.grid[-1][-1].rect.right, self.grid[-1][-1].rect.centery + 10)
        top_left_red = (self.grid[0][0].rect.left + 2, self.grid[0][0].rect.centery - 25)
        top_right_red = (self.grid[0][-1].rect.right - 2, self.grid[0][-1].rect.centery - 25)
        bottom_left_red = (self.grid[-1][0].rect.left + 2, self.grid[-1][0].rect.centery + 8)
        bottom_right_red = (self.grid[-1][-1].rect.right - 2, self.grid[-1][-1].rect.centery + 8)

        top_bottom_border_color = (160, 44, 44)
        sides_border_color = (0, 0, 170)
        border_thickness = 20

        self.draw_custom_line(self.surface, top_bottom_border_color, top_left_red, top_right_red, border_thickness,
                              True)  # top
        self.draw_custom_line(self.surface, top_bottom_border_color, bottom_left_red, bottom_right_red,
                              border_thickness, True)  # bottom
        self.draw_custom_line(self.surface, sides_border_color, top_left, bottom_left, border_thickness, False)  # left
        self.draw_custom_line(self.surface, sides_border_color, top_right, bottom_right, border_thickness,
                              False)  # right

        for row in self.grid:
            for hexagon in row:
                hexagon.draw(self.surface)


class Game:
    def __init__(self, surface, board, turn):
        self.surface = surface
        self.turn = turn
        self.board = board
        self.running = True
        self.game_menu = False
        self.run = True
        self.paused = False

    def play(self):
        global new_pos, new_command
        global pos
        global thread_started
        global receive_thread_client
        global receive_thread_server
        global running_thread_server
        on_connect = True
        game_surface.blit(YELLOW, (0, 0))
        # game_surface.fill(WHITE)  # COMMENT TO BRING BACK BACKGROUND
        self.board.make_grid()
        print("check")

        global user_text
        while self.running:

            game_surface.blit(YELLOW, (0, 0))
            # game_surface.fill(WHITE)  # COMMENT TO BRING BACK BACKGROUND
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        # exporting game as a string to load
                        user_text = importing.array_to_string(gamelogic.board)
                    if event.key == pygame.K_ESCAPE:
                        self.game_menu = True

            if self.paused:
                if export_game_button.draw_menu(game_surface):
                    if importing.is_board_legal(gamelogic.board):
                        print(np.array2string(gamelogic.board, separator=','))
                        #we export the board as seen in the export file
                        export.export_board(gamelogic.board)
                        user_text = importing.array_to_string(gamelogic.board)
                        #we write the import string to the export file aswell
                        with open('export.txt', 'a') as f:
                            f.write("\n")
                            f.write(importing.array_to_string(gamelogic.board))
                        print("board exported")
                    else:
                        print("board is not legal and cant be exported ")
                    self.paused = False
                if go_back_button.draw_menu(game_surface):
                    self.paused = False
                self.board.draw_grid()
                if exit_game_button.draw_menu(game_surface):
                    exit_game()
            if not self.paused:
                if self.running and not gamelogic.has_any_won(gamelogic.board):
                    if ai_difficulty == 0:
                        game_surface.blit(Player_1_man_img, (70, 270))
                        game_surface.blit(Player_2_man_img, (500, 100))
                        # print("Test")
                    if ai_difficulty == 1:
                        if gamelogic.default_starting_player == 1:
                            game_surface.blit(Player_1_man_img, (70, 270))
                            game_surface.blit(Player_2_ai1_img, (500, 100))
                        else:
                            game_surface.blit(Player_1_ai1_img, (70, 270))
                            game_surface.blit(Player_2_man_img, (500, 100))
                    if ai_difficulty == 2:
                        if gamelogic.default_starting_player == 1:
                            game_surface.blit(Player_1_man_img, (70, 270))
                            game_surface.blit(Player_2_ai2_img, (500, 100))
                        else:
                            game_surface.blit(Player_1_ai2_img, (70, 270))
                            game_surface.blit(Player_2_man_img, (500, 100))

                    if ai_difficulty == 3:
                        if gamelogic.default_starting_player == 1:
                            game_surface.blit(Player_1_man_img, (70, 270))
                            game_surface.blit(Player_2_ai3_img, (500, 100))
                        else:
                            game_surface.blit(Player_1_ai3_img, (70, 270))
                            game_surface.blit(Player_2_man_img, (500, 100))
                    if gamelogic.player_no == 1 and gamelogic.default_starting_player == 1:
                        game_surface.blit(Player_1_Turn, (50, 300))
                    elif gamelogic.player_no == 2 and gamelogic.default_starting_player == 1:
                        game_surface.blit(Player_2_Turn, (450, 50))
                    if gamelogic.player_no == 1 and gamelogic.default_starting_player == 2:
                        game_surface.blit(Player_2_Turn, (450, 50))
                    elif gamelogic.player_no == 2 and gamelogic.default_starting_player == 2:
                        game_surface.blit(Player_1_Turn, (50, 300))
                if not gamelogic.has_any_won(gamelogic.board):
                    if pause_game_button.draw_menu(game_surface):
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

                if gamelogic.player_no == gamelogic.cpu and not gamelogic.has_any_won(
                        gamelogic.board) and not gamelogic.multiplayer and ai_difficulty == 1:
                    self.unit = gamelogic.make_ai1_move()
                if gamelogic.player_no == gamelogic.cpu and not gamelogic.has_any_won(
                        gamelogic.board) and not gamelogic.multiplayer and ai_difficulty == 2:
                    self.unit = gamelogic.make_ai2_move()
                if gamelogic.player_no == gamelogic.cpu and not gamelogic.has_any_won(
                        gamelogic.board) and not gamelogic.multiplayer and ai_difficulty == 3:
                    self.unit = gamelogic.make_ai3_move()
                else:
                    self.board.draw_grid()
                    if gamelogic.has_any_won(gamelogic.board):
                        if gamelogic.has_player_won(1, gamelogic.board):
                            game_surface.blit(Player_1_Wins_Img, (180, 200))
                        elif gamelogic.has_player_won(2, gamelogic.board):
                            game_surface.blit(Player_2_Wins_Img, (180, 200))
                        if not gamelogic.multiplayer or gamelogic.client_no == 1:

                            if main_menu_button.draw_menu(game_surface):
                                if gamelogic.multiplayer:
                                    onlinelogic.clientsocket.send(bytes("exitt", 'utf-8'))

                                exit_game()

                            if play_again_button.draw_menu(game_surface):
                                if gamelogic.multiplayer:
                                    onlinelogic.clientsocket.send((bytes("contt", 'utf-8')))

                                restart_game()
                        else:
                            text3 = font.render("Waiting for host...", True, BLACK)
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
                        text2 = font.render("Waiting for player...", True, BLACK)
                        text_rect2 = text2.get_rect()
                        text_rect2.center = (100, 100)
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

    def draw_menu(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create button instances
exit_game_button = MenuButton(350, 50, Exit_Game_img, 1)
play_again_button = MenuButton(343.4, 400, Play_Again_img, 1)
main_menu_button = MenuButton(46.6, 400, Main_Menu_img, 1)
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

# game loop
def server_thread():
    global receive_thread_client
    global receive_thread_server
    global running_thread_server
    server = onlinelogic.serversocket()
    server.create_server()


while run:
    game_surface.fill((200, 200, 255))

    if first_menu:
        if start_game_button.draw_menu(game_surface):
            print('first menu')
            second_menu = True
            first_menu = False
            action = True
            gamelogic.multiplayer = False
            gamelogic.player_won = False
        if settings_button.draw_menu(game_surface):
            first_menu = False
            setting_menu = True
            action = True

    if second_menu:
        game_surface.blit(Drone_Bee_img, (140, 175))
        game_surface.blit(Worker_Bee_img, (450, 250))
        game_surface.blit(Queen_Bee_img, (140, 325))

        if two_player_button.draw_menu(game_surface) and not action:
            game_running = True
            second_menu = False
            gamelogic.local_multiplayer = True
            action = True
        if ai_1_button.draw_menu(game_surface) and not action:
            gamelogic.cpu = 2
            ai_difficulty = 1
            game_running = True
            second_menu = False
            action = True
        if ai_2_button.draw_menu(game_surface) and not action:
            gamelogic.cpu = 2
            ai_difficulty = 2
            game_running = True
            second_menu = False
            print('Playing gainst bot 2')
        if ai_3_button.draw_menu(game_surface) and not action:
            gamelogic.cpu = 2
            ai_difficulty = 3
            game_running = True
            second_menu = False
            print('playing against bot 3')
            action = True
        if play_online_button.draw_menu(game_surface) and not action:
            online_menu = True
            second_menu = False
            print('joining a server')
            action = True
        if go_back_button.draw_menu(game_surface) and not action:
            first_menu = True
            second_menu = False
            action = True

    if online_menu:
        input_box = pygame.Rect(200, 210, 243, 32)
        onlinelogic.ip_text = inputting.input_field(onlinelogic.ip_text, input_box, game_surface)
        if go_back_button.draw_menu(game_surface) and not action:
            second_menu = True
            online_menu = False
        if join_game_button.draw_menu(game_surface) and not action:
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

        if host_game_button.draw_menu(game_surface) and not action:
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

    if game_running:
        board1 = Board(hexagon1, gamelogic.board_size, game_surface)
        game1 = Game(game_surface, board1, 1)
        game1.play()
        game_running = False
        print(gamelogic.player_no)
        if pause_game_button.draw_menu(game_surface):
            game_paused = True

        if game_paused:
            if export_game_button.draw_menu(game_surface):
                print('ExportGame')
                game_paused = False
            if go_back_button.draw_menu(game_surface):
                game_paused = False
        first_menu = True
        setting_menu = False

    if setting_menu:

        text = font.render(str(gamelogic.board_size), True, WHITE)
        textRect = text.get_rect()
        textRect.center = (100, 100)
        game_surface.blit(text, [450, 160])
        if change_board_size_button.draw_menu(game_surface) and not action:

            board_size += 1
            if board_size >= len(board_size_list):
                board_size = 0
            if board_size < 0:
                board_size = len(board_size_list)
            gamelogic.board_size = board_size_list[board_size]
            gamelogic.board = np.zeros((board_size_list[board_size], board_size_list[board_size]), dtype=int)
        
        #import game
        if import_game_button.draw_menu(game_surface) and not action:
            input_rect = pygame.Rect(200, 110, 243, 32)
            user_text = ""
            import_game = True
        if import_game:
            #We initialize the input field
            user_text = inputting.input_field(user_text, input_rect, game_surface, pygame.Color('black'))
            if inputting.entered:
                user_text_size = user_text.split()
                if len(user_text_size) not in full_board_size_list:
                    print("board size is not a perfect square or letters used")
                    print("please try again")
                    import_game = False
                    inputting.entered = False
                # error handling
                else:

                    placeholder_arr = importing.string_to_square_numpy_array(user_text)
                    if importing.is_board_legal(placeholder_arr):
                        try:
                            root = int(math.sqrt(len(user_text_size)))
                            print("board has been imported")
                            board1 = Board(hexagon1, root, game_surface)
                            gamelogic.board_size = root
                            gamelogic.board = importing.string_to_square_numpy_array(user_text)
                            imported = True
                            import_game = False
                            setting_menu = False
                            second_menu = True
                            inputting.entered = False

                        except ValueError:
                            print("wrong format")
                            user_text = ""
                        except:
                            print("something else")
                            user_text = ""
                        import_game = False
                        inputting.entered = False
                    else:
                        print("board is illegal")

        if change_player_button.draw_menu(game_surface) and not action:
            setting_menu = False
            player_option = True
            print('Change player menu')
            action = True

        if go_back_button.draw_menu(game_surface):
            setting_menu = False
            first_menu = True

    if player_option:
        if player_1_button.draw_menu(game_surface) and not action:
            print('choose player 1')
            gamelogic.default_starting_player = 1
            gamelogic.player_no = gamelogic.default_starting_player
            action = True
        if player_2_button.draw_menu(game_surface) and not action:
            print('choose player 2')
            gamelogic.default_starting_player = 2
            gamelogic.player_no = gamelogic.default_starting_player
            action = True
        if go_back_button.draw_menu(game_surface) and not action:
            player_option = False
            setting_menu = True
            action = True

    if pygame.mouse.get_pressed()[0] == 0:
        action = False
    if not online_menu:
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # exporting game as a string to load
                    user_text = importing.array_to_string(gamelogic.board)
                elif event.key == pygame.K_b:
                    if importing.is_board_legal(gamelogic.board):
                        print(gamelogic.board)
                        export.export_board(gamelogic.board)
                        print("board exported")
                    else:
                        print("board not legal")

    pygame.display.flip()

pygame.quit()
