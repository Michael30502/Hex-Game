import pygame
import button
import board
import tiles
import game


#create display window
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800

FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),)
pygame.display.set_caption('Hex')


#load button images
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
hexagon_neutral_img = pygame.image.load('assets/tile_0.png').convert_alpha()
hexagon_player1_img = pygame.image.load("assets/tile_1.png").convert_alpha()
hexagon_player2_img = pygame.image.load("assets/tile_2.png").convert_alpha()



#create button instances
start_game_button = button.Button(100, 100, start_game_img, 2)
play_online_button = button.Button(300, 200, Play_Online_img, 2)
ai_2_button = button.Button(300, 400, AI_2_img, 2)
two_player_button = button.Button(300, 100, Two_Player_img, 2)
ai_1_button = button.Button(300, 300, AI_1_img, 2)
ai_3_button = button.Button(300, 500, AI_3_img, 2)
change_board_size_button = button.Button(300, 200, Change_Board_Size_img, 2)
settings_button = button.Button(100, 200, Settings_img, 2)
continue_button = button.Button(300, 200, Continue_img, 2)
export_game_button = button.Button(300, 100, Export_Game_img, 2)
import_game_button = button.Button(300, 100, Import_Game_img, 2)
pause_game_button = button.Button(600, 600, Pause_Game_img, 1)
go_back_button = button.Button(600, 600, Go_Back_img, 1)
hexagon1 = tiles.Tiles(0,0, hexagon_neutral_img,0.5, (0,0))
hexagon2 = tiles.Tiles(hexagon_neutral_img.get_width()*0.5,0,hexagon_neutral_img,0.5,(0,1))
hexagon_player1 = tiles.Tiles(96, 0, hexagon_player1_img, 0.5, (1, 1))


#game loop
run = True
first_menu = True
setting_menu = False
second_menu = False
game_running = False
game_paused = False
game_finished = False

while run:

	screen.fill((200, 200, 255))
	if first_menu == True:
		if start_game_button.draw(screen):
			second_menu = True
			first_menu = False
		if settings_button.draw(screen):
			first_menu = False
			setting_menu = True

	if second_menu == True:
		if two_player_button.draw(screen):
			print('2 player')
			game_running = True
			second_menu = False	
		if ai_1_button.draw(screen):
			print('playing against bot 1')
		if ai_2_button.draw(screen):
			print('playing against bot 1')
		if ai_3_button.draw(screen):
			print('playing against bot 1')
		if play_online_button.draw(screen):
			print('playing against bot 1')
		if go_back_button.draw(screen):
			first_menu = True
			second_menu = False
	
	if game_running == True:
			board1 = board.Board(hexagon1,11,screen,game1,board1,hexagon_player1_img,hexagon_player2_img)
			game1 = game.Game(screen,board1,0)
			game1.play(screen)

	
	if setting_menu == True:
		if change_board_size_button.draw(screen):
			print('change board size')
		if import_game_button.draw(screen):
			print('import saved game')
		if go_back_button.draw(screen):
			setting_menu = False
			first_menu = True
	

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()