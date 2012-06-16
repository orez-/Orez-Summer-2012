import pygame

from board import Player
from level_save import LevelLoad

class GameUI:
    def __init__(self, main, player2, level="level1"):
        self.main = main
        loc, self.board = LevelLoad.load_level(level)
        #self.board = Board()
        self.player1 = Player(self.board, loc)
        self.player2 = Player(self.board, loc, self.player1)
        self.which_player = player2
        self.view_player = player2

    def reblit(self, screen):
        center = (self.player1.x, self.player1.y)
        if self.view_player:
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
        if event.key == pygame.K_TAB:
            self.view_player = not self.which_player

    def handle_key_up(self, event):
        if event.key == pygame.K_TAB:
            self.view_player = self.which_player