import pygame

import ui
from constants import SCREEN_SIZE


class ConfigUI(ui.TacticsUI):
    def __init__(self, *args, **kwargs):
        super(ConfigUI, self).__init__(*args, **kwargs)

        self.font = pygame.font.Font(None, 48)
        self.surface = pygame.Surface(SCREEN_SIZE)

        self.options = ["Ok", "Cancel", "Up", "Down", "Left", "Right"]
        self.osurf = pygame.Surface((800, (len(self.options) + 1) * 48))
        self.option_width = max(map(lambda x: self.font.size(x)[0],
            self.options)) + 10
        self.column_x1 = self.option_width + 20
        self.column_x2 = (self.osurf.get_width() + self.column_x1) / 2
        self.redraw_osurf()
        self.redraw()

    def redraw_osurf(self):
        self.osurf.fill((0, 0, 0xFF))
        self.osurf.blit(self.font.render("Key", True, (0xFF, ) * 3), 
            (self.column_x1, 5))
        self.osurf.blit(self.font.render("Alternate", True, (0xFF, ) * 3),
            (self.column_x2, 5))
        for i, o in enumerate(self.options):
            text = self.font.render(o, True, (0xFF, ) * 3)
            self.osurf.blit(text,
                (self.option_width - text.get_width(), 10 + 48 * (i + 1)))
        pygame.draw.line(self.osurf, (0xFF, ) * 3, (self.option_width + 10, 5),
            (self.option_width + 10, self.osurf.get_height() - 5), 2)
        pygame.draw.line(self.osurf, (0xFF, ) * 3, (self.column_x2 - 10, 5),
            (self.column_x2 - 10, self.osurf.get_height() - 5), 2)
        pygame.draw.line(self.osurf, (0xFF, ) * 3, (self.option_width, 48),
            (self.osurf.get_width() - 5, 48), 2)

    def redraw(self):
        self.surface.fill((0, ) * 3)
        self.surface.blit(self.osurf, (100, 100))

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))

    def keydown(self, event):
        pass

    def keyup(self, event):
        pass

    def keep_moving(self):
        pass

    def k_UP(self):
        pass

    def k_DOWN(self):
        pass

    def k_LEFT(self):
        pass

    def k_RIGHT(self):
        pass

    def k_CANCEL(self):
        pass

    def k_OK(self):
        pass

    @staticmethod
    def name():
        return "config"