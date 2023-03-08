import pygame

class Tiles():
    def __init__(self,x,y,image,scale, unit,game1,board1,hexagon_player1_img,hexagon_player2_img):
        self.image = image  # Store original image
        self.scale = scale
        self.player = None
        self.game1 = game1
        self.board1 = board1
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
        game1 = self.game1
        board1 = self.board1
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
