# import sys module
import pygame
import sys
import pyperclip

# pygame.init() will initialize all
# imported module
pygame.init()
  
# clock = pygame.time.Clock()
  
# it will display on screen
base_font = pygame.font.Font(None, 32)

# input_rect = pygame.Rect(200, 200, 140, 32)
text = ""
def input_field(text, input_rect, screen, color = pygame.Color('chartreuse4')):
    initial_text = text
    input_active = True
    if input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(text)
                    input_active = False
                if event.key == pygame.K_v:
                    text = str(pyperclip.paste())
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        # The color the line below is where the color is set need to be of format pygame.Color('presetcolorname')
        # this could be made prettyer

        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        input_rect.w = max(100, text_surface.get_width()+10)
        if initial_text!= text:
            pygame.display.flip()
    return text

# input_field(text, input_rect, game_surface)
