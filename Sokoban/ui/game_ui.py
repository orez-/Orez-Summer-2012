import pygame

from board import Board
from board import Player

class GameUI:
    def __init__(self, main, player2):
        self.main = main
        self.board = Board()
        self.player1 = Player(self.board)
        self.player2 = Player(self.board, self.player1)
        self.which_player = player2

    def reblit(self, screen):
        center = (self.player1.x, self.player1.y)
        if self.which_player:
            center = (self.player2.x, self.player2.y)
        self.board.reblit(screen, center)
        self.player1.reblit(screen, center)
        self.player2.reblit(screen, center)

    def handle_key(self, event):
        if event.key == pygame.K_DOWN:
            #self.player1.move(y=1)
            self.main.send_msg("MOVED 0 1")
        if event.key == pygame.K_UP:
            #self.player1.move(y=-1)
            self.main.send_msg("MOVED 0 -1")
        if event.key == pygame.K_LEFT:
            #self.player1.move(x=-1)
            self.main.send_msg("MOVED -1 0")
        if event.key == pygame.K_RIGHT:
            #self.player1.move(x=1)
            self.main.send_msg("MOVED 1 0")