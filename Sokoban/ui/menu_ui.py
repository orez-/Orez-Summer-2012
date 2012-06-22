import pygame

from constants import SCREEN_SIZE
from ui import UI


class MenuUI(UI):
    def __init__(self, main, parent):
        super(MenuUI, self).__init__(main, parent)
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.title = pygame.font.Font(None, 72).render("Sokorez", True, (0, ) * 3)
        self.font = pygame.font.Font(None, 48)

        self.options = [("Join Game", lambda: self.main.change_screen("join")),
                        ("Host Game", lambda: self.main.change_screen("host")),
                        ("Level Editor", lambda: self.main.change_screen("editor")),
                        ("Quit", self.main.stop)]
        self.selected = 0
        self.finger = pygame.image.load("imgs/finger.png")

        self.counter = 12
        self.message = None

        self.redraw()

    def set_message(self, message=None):
        self.counter = 12
        self.message = None
        if message is not None:
            msg = pygame.font.Font(None, 72).render(message, True, (0, ) * 3)
            self.message = pygame.Surface(map(lambda x: x + 40, msg.get_size()))
            self.message.fill((0xEE, ) * 3)
            self.blink_msg_outline()
            self.message.blit(msg, (20, 20))

    def blink_msg_outline(self):
        pygame.draw.rect(self.message, (0xFF if self.counter < 50 else 0, 0, 0),
            ((0, 0), (self.message.get_size())), 3)

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(self.title, (30, 50))
        for i, (opt, _) in enumerate(self.options):
            self.surface.blit(self.font.render(opt, True, (0, ) * 3), (50, i*40 + 150))

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        surf.blit(self.finger, (30, self.selected*40 + 157))
        if self.message is not None:
            self.counter += 1
            if self.counter == 50:
                self.blink_msg_outline()
            if self.counter >= 100:
                self.counter = 0
                self.blink_msg_outline()
            surf.blit(self.message, (50, 50))

    def handle_key(self, event):
        if self.message is None:
            if event.key == pygame.K_UP:
                if self.selected > 0:
                    self.selected -= 1
            if event.key == pygame.K_DOWN:
                if self.selected < len(self.options) - 1:
                    self.selected += 1

            if event.key == pygame.K_SPACE:
                self.options[self.selected][1]()
        else:
            if event.key == pygame.K_SPACE:
                self.message = None

    def on_reentry(self, child):
        self.main.stop_multiplayer()
