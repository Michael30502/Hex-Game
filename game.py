import pygame
import board

WHITE = (255,255,255)

class Game():

    def __init__(self, surface, board, turn):
        self.surface = surface
        self.turn = turn
        self.board = board
        self.running = True
    
    def play(self,screen):
        screen.fill(WHITE)
        self.board.make_grid()
        while self.running:
            
            self.board.Board.draw_grid()

    def get_turn(self):
        return self.turn
    
    def turn_count(self):
        self.turn += 1