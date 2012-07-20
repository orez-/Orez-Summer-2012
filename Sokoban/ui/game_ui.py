import pygame

from board import Player
from level_save import LevelLoad
from chatbox import Chatbox
from ui import UI


class GameUI(UI):
    PLAY_MODE = 1
    TYPE_MODE = 2

    def __init__(self, main, parent, level="division_of_labor"):
        super(GameUI, self).__init__(main, parent)
        self.level_name = level

        self.chatbox = Chatbox()

        player2 = parent.player2
        loc, self.board = LevelLoad.load_level(level)
        self.board.add_client(self.main.client)

        self.player1 = Player(self.board, loc, not player2)
        self.player2 = Player(self.board, loc, player2, self.player1)
        self.which_player = player2
        self.view_player = player2

        self.mode = GameUI.PLAY_MODE

    def reload_level(self):
        return GameUI(self.main, self.parent, self.level_name)

    def reblit(self, screen):
        center = (self.player1.x, self.player1.y)
        if self.view_player:
            center = (self.player2.x, self.player2.y)
        self.board.reblit(screen, center)
        self.player1.reblit(screen, center)
        self.player2.reblit(screen, center)

        self.chatbox.reblit(screen)

    def set_mode(self, mode):
        if self.mode == GameUI.TYPE_MODE:
            self.chatbox.hide_time = None
        self.mode = mode
        if self.mode == GameUI.TYPE_MODE:
            self.chatbox.hide_time = True

    def handle_key(self, event):
        if self.mode == GameUI.PLAY_MODE:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.set_mode(GameUI.TYPE_MODE)
            if event.key == pygame.K_DOWN:
                self.main.send_msg("MOVED 0 1")
            if event.key == pygame.K_UP:
                self.main.send_msg("MOVED 0 -1")
            if event.key == pygame.K_LEFT:
                self.main.send_msg("MOVED -1 0")
            if event.key == pygame.K_RIGHT:
                self.main.send_msg("MOVED 1 0")
            if event.key == pygame.K_TAB:
                self.view_player = not self.which_player
        elif self.mode == GameUI.TYPE_MODE:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.set_mode(GameUI.PLAY_MODE)
                self.chatbox.input_box.submit(self.main.client)
            elif event.key == pygame.K_BACKSPACE:
                self.chatbox.remove_chars()
            elif event.unicode != "":
                self.chatbox.add_string(event.unicode)

    def handle_key_up(self, event):
        if event.key == pygame.K_TAB:
            self.view_player = self.which_player


class SinglePlayerUI(UI):
    PLAY_MODE = 1
    TYPE_MODE = 2

    def set_which(self, value):
        self._which_player = value
        self.me = self.players[self._which_player]

    which_player = property(lambda self: self._which_player, set_which)

    def __init__(self, main, parent):
        super(SinglePlayerUI, self).__init__(main, parent)
        #self.level_name = level

        self.dx, self.dy = 0, 0
        self.chatbox = Chatbox()

        self.board = parent.board.clone()
        self.board.add_client(self.main.client)
        loc = parent.start.x, parent.start.y

        player2 = False

        self.players = []
        self.players.append(Player(self.board, loc, not player2))
        self.players.append(Player(self.board, loc, player2, self.players[0]))
        self.which_player = player2

        self.mode = GameUI.PLAY_MODE

    def reblit(self, screen):
        center = (self.me.x, self.me.y)
        self.board.reblit(screen, center)
        for x in self.players:
            x.reblit(screen, center)

        self.chatbox.reblit(screen)

    def set_mode(self, mode):
        if self.mode == GameUI.TYPE_MODE:
            self.chatbox.hide_time = None
        self.mode = mode
        if self.mode == GameUI.TYPE_MODE:
            self.chatbox.hide_time = True

    def handle_key(self, event):
        if self.mode == GameUI.PLAY_MODE:
            if event.key == pygame.K_DOWN:
                self.me.move(y=1)
            if event.key == pygame.K_UP:
                self.me.move(y=-1)
            if event.key == pygame.K_LEFT:
                self.me.move(x=-1)
            if event.key == pygame.K_RIGHT:
                self.me.move(x=1)
            if event.key == pygame.K_TAB:
                self.which_player = not self.which_player
            if event.key == pygame.K_ESCAPE:
                self.main.ui_back()
