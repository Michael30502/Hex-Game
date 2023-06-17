# import sys module
#Written by William, minor improvements Michael

import pygame
import sys
import pyperclip
pygame.init()
base_font = pygame.font.Font(None, 32)

entered = False

def input_field(text, input_rect, screen, color = pygame.Color('chartreuse4')):
    #makes an interactive input field that displays what has been pressed on the keyboard and saves the final string in a variable that is returned
    #text is the variable that holds the text, this is also displayed and dynamically changed while this code is running
    #input_rect is the size and location of the rectangle where the users will be inputing the string
    #screen is the surface we are updating this to
    #color is optional to make it look better
    global entered
    initial_text = text
    input_active = True
    if input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    text = str(pyperclip.paste())
                elif event.key == pygame.K_RETURN:
                    print(text)
                    entered = True
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        input_rect.w = max(100, text_surface.get_width()+10)
        if initial_text != text:
            pygame.display.flip()
    return text
