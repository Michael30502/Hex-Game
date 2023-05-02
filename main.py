import pygame
import gamelogic
import numpy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

cpu = 2

run = True

pygame.init()
# Surface/Screen size (this shoudl be scaleable
WIDTH, HEIGHT = 800, 800
game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HEX")
clock = pygame.time.Clock()

# load button images
start_game_img = pygame.image.load("assets/Start_Game.png").convert_alpha()
AI_1_img = pygame.image.load("assets/AI_1.png").convert_alpha()
Play_Online_img = pygame.image.load("assets/Play_Online.png").convert_alpha()
AI_2_img = pygame.image.load("assets/AI_2.png").convert_alpha()
AI_3_img = pygame.image.load("assets/AI_3.png").convert_alpha()
Change_Board_Size_img = pygame.image.load(
    "assets/Change_Board_Size.png"
).convert_alpha()
Continue_img = pygame.image.load("assets/Continue.png").convert_alpha()
Export_Game_img = pygame.image.load("assets/Export_Game.png").convert_alpha()
Import_Game_img = pygame.image.load("assets/Import_Game.png").convert_alpha()
Pause_Game_img = pygame.image.load("assets/Pause_Game.png").convert_alpha()
Settings_img = pygame.image.load("assets/Settings.png").convert_alpha()
Two_Player_img = pygame.image.load("assets/Two_Player.png").convert_alpha()
Go_Back_img = pygame.image.load("assets/Go_Back.png").convert_alpha()

start_button_img = pygame.image.load("assets/start_button_img.png").convert_alpha()
hexagon_neutral_img = pygame.image.load("assets/tile_0.png").convert_alpha()
hexagon_player1_img = pygame.image.load("assets/tile_1.png").convert_alpha()
hexagon_player2_img = pygame.image.load("assets/tile_2.png").convert_alpha()

# game variables

first_menu = True
setting_menu = False
second_menu = False
game_running = False
game_paused = False
game_finished = False
action = False
import_game = False


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

        # stringify object
        def __str__(self):
            return f"BUTTONOBJ= x,y: {self.rect.topleft}, image:{self.image}, scale:{self.scale}, unit:{self.unit}"

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
                gamelogic.make_move(self.unit)

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
        print("position:" + str(self.rect.topleft) + "unit" + str(self.unit))
        pass


class MenuButton:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def drawMenuButton(self, surface):
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


# class Menu:
#     def __init__(self, surface):
#         self.surface = surface

#     def menu_init(self):
#         game_surface.fill((200, 200, 255))
#         if first_menu == True:
#             self.first_menu()

#     def first_menu(self):

#         start_game_button.drawMenuButton(game_surface)


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
                hexagon = Button(
                    hex_x, hex_y, self.hexagon.image, self.hexagon.scale, (i, j)
                )
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

    def set_board(self):
        # TODO set board in gamelogic with import string

        # stringify object
        def __str__(self):
            return f"BoardOBJ= hexgaon: {self.hexagon}, size:{self.size}, surface:{self.surface}"


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
        print("in game")
        game_surface.fill(WHITE)
        self.board.make_grid()
        while self.running:
            if gamelogic.player_no == cpu:
                self.unit = gamelogic.make_cpu_move()
            else:
                self.board.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quit clicked, shutting down")
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_menu = True
                        print("ESC clicked, starting menu")
                        Menu(run)

            pygame.display.flip()

    def get_turn(self):
        return self.turn

    def set_board(self, board):

        self.board = board

    def turn_count(self):
        self.turn += 1


# create button instances
start_game_button = MenuButton(100, 100, start_game_img, 2)
play_online_button = MenuButton(300, 200, Play_Online_img, 2)
ai_2_button = MenuButton(300, 400, AI_2_img, 2)
two_player_button = MenuButton(300, 100, Two_Player_img, 2)
ai_1_button = MenuButton(300, 300, AI_1_img, 2)
ai_3_button = MenuButton(300, 500, AI_3_img, 2)
change_board_size_button = MenuButton(300, 200, Change_Board_Size_img, 2)
settings_button = MenuButton(100, 200, Settings_img, 2)
continue_button = MenuButton(300, 200, Continue_img, 2)
export_game_button = MenuButton(300, 100, Export_Game_img, 2)
import_game_button = MenuButton(300, 100, Import_Game_img, 2)
pause_game_button = MenuButton(600, 600, Pause_Game_img, 1)
go_back_button = MenuButton(600, 600, Go_Back_img, 1)
hexagon1 = Button(0, 0, hexagon_neutral_img, 0.5, (0, 0))
hexagon2 = Button(
    hexagon_neutral_img.get_width() * 0.5, 0, hexagon_neutral_img, 0.5, (0, 1)
)
hexagon_neutral_img_mask = pygame.mask.from_surface(hexagon_neutral_img)
hexagon_player1 = Button(96, 0, hexagon_player1_img, 0.5, (1, 1))
board1 = Board(hexagon1, 11, game_surface)
board1.make_grid()


# takes gamelogic board and changes it
# better name may be needed TODO
def import_game_setter(game_arr_str):
    gamelogic.board = game_arr_str
    print("board set")
    print(gamelogic.board)
    print(type(gamelogic.board))
    return gamelogic.board


def array_to_string(array):
    # (this will be a list of integers sep by ' ')
    return " ".join(str(elem) for elem in array.flat)


# the line bellow makes it so that the array_to_string function is used when printing the array or getting string version. Was used while testing
# np.set_string_function(array_to_string, repr=False)


def string_to_square_numpy_array(string):
    # Split the string into integers and convert them to a numpy array
    flat_array = np.array([int(elem) for elem in string.split()])

    # assumes that the  array is square
    # TODO if we are moving into none-square arrays another method will be needed
    array_size = int(np.sqrt(flat_array.size))

    # Reshape the flat array into a square array
    array = flat_array.reshape((array_size, array_size))

    return array


# gameloop
def Menu(run):
    # import stuff
    # user input
    base_font = pygame.font.Font(None, 32)
    user_text = ""
    # rect for input
    input_rect = pygame.Rect(0, 600, 200, 800)
    color_active = pygame.Color("lightskyblue3")
    color_passive = pygame.Color("chartreuse4")
    color = color_passive
    input_active = False

    first_menu = True
    setting_menu = False
    second_menu = False
    game_running = False
    import_game = False
    # game_paused = False
    # game_finished = False
    while run:
        game_surface.fill((200, 200, 255))

        if first_menu == True:
            if start_game_button.drawMenuButton(game_surface):
                print("first menu")
                print(gamelogic.board)
                second_menu = True
                first_menu = False
            if settings_button.drawMenuButton(game_surface):
                first_menu = False
                setting_menu = True

        if second_menu == True:
            if two_player_button.drawMenuButton(game_surface):
                game_running = True
                second_menu = False
            if ai_1_button.drawMenuButton(game_surface):
                # board1.draw_grid()
                game_running = True
                second_menu = False
                print(cpu)
            if ai_2_button.drawMenuButton(game_surface):
                print("playing against bot 1")
            if ai_3_button.drawMenuButton(game_surface):
                print("playing against bot 1")
            if play_online_button.drawMenuButton(game_surface):
                print("playing against bot 1")
            if go_back_button.drawMenuButton(game_surface):
                print("go back pressed")
                first_menu = True
                second_menu = False

        if game_running == True:
            print("------------------------------------------")
            board1 = Board(hexagon1, gamelogic.board_size, game_surface)
            game1 = Game(game_surface, board1, 0)
            game1.play()

        if setting_menu == True:
            if change_board_size_button.drawMenuButton(game_surface):
                print("change board size")

            if import_game_button.drawMenuButton(game_surface):
                import_game = True

        if import_game:

            game_surface.fill((200, 200, 255))
            pygame.draw.rect(game_surface, (255, 255, 255), input_rect)

            text_surface = base_font.render(user_text, True, (255, 255, 255))

            # render at position stated in arguments
            game_surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            # set width of textfield so that text cannot get
            # outside of user's text input
            input_rect.w = max(100, text_surface.get_width() + 10)

            # display.flip() will update only a portion of the
            # screen to updated, not full area
            pygame.display.flip()
            clock.tick(60)
            if input_active:
                color = color_active
            else:
                color = color_passive

            # import game
            # board1 = Board(hexagon1, 11, game_surface)
            # board1.make_grid()
            # game1 = Game(game_surface, board1, 0)
            # game1.play()

        if go_back_button.drawMenuButton(game_surface):
            setting_menu = False
            first_menu = True

        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            # Source https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
            if event.type == pygame.KEYDOWN:
                # check for escape
                if event.key == pygame.K_ESCAPE:
                    print("ESC clicked, starting menu")
                    Menu(run)
                # check for enter/return only checking in import
                if (
                    event.key == pygame.K_KP_ENTER
                    or event.key == pygame.K_RETURN
                    and import_game == True
                ):
                    # TODO find a way to import game using stanard paste string method. current idea is to save the game when players presses export
                    # and loading set variable
                    print("Enter importing game")
                    print(type(gamelogic.board))
                    print(user_text)
                    gamelogic.board[(5, 5)] = 5
                    test = str(gamelogic.board)
                    print(gamelogic.board)
                    # import_game_setter(test)
                    # import_game = False
                    # board1 = Board(hexagon1, 11, game_surface)
                    # board1.make_grid()
                    # game1 = Game(game_surface, board1, 0)
                    # game1.play()

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode
                    print(user_text)
        pygame.display.flip()
    pygame.quit()


Menu(run)
