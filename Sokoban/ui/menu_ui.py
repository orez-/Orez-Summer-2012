import pygame

from constants import SCREEN_SIZE


class MenuUI:
    def __init__(self, main):
        self.main = main
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.title = pygame.font.Font(None, 72).render("Sokorez", True, (0, ) * 3)
        self.font = pygame.font.Font(None, 48)

        self.options = [("Join Game", lambda: self.main.change_screen("join")),
                        ("Host Game", lambda: self.main.change_screen("game")),
                        ("Quit", self.main.stop)]
        self.selected = 0
        self.finger = pygame.image.load("imgs/finger.png")

        self.redraw()

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(self.title, (30, 50))
        for i, (opt, _) in enumerate(self.options):
            self.surface.blit(self.font.render(opt, True, (0, ) * 3), (50, i*40 + 150))

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        surf.blit(self.finger, (30, self.selected*40 + 157))

    def handle_key(self, event):
        if event.key == pygame.K_UP:
            if self.selected > 0:
                self.selected -= 1
        if event.key == pygame.K_DOWN:
            if self.selected < len(self.options) - 1:
                self.selected += 1

        if event.key == pygame.K_SPACE:
            self.options[self.selected][1]()

    def handle_key_up(self, event):
        pass