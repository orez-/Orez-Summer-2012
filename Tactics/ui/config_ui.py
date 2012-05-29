import pygame

import ui
from config import Config
from constants import SCREEN_SIZE


class ConfigUI(ui.TacticsUI):
    SELECT_MODE = 1
    INPUT_MODE = 2

    def __init__(self, *args, **kwargs):
        super(ConfigUI, self).__init__(*args, **kwargs)

        self.font = pygame.font.Font(None, 48)
        self.surface = pygame.Surface(SCREEN_SIZE)

        self.selected = 0
        self.options = ["Ok", "Cancel", "Pause", "Up", "Down", "Left", "Right"]
        self.osurf = pygame.Surface((800, (len(self.options) + 1) * 48))
        self.option_width = max(map(lambda x: self.font.size(x)[0],
            self.options)) + 10
        self.column_x1 = self.option_width + 20
        self.column_x2 = (self.osurf.get_width() + self.column_x1) / 2
        self.mode = ConfigUI.SELECT_MODE

        self.redraw_osurf()

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == ConfigUI.SELECT_MODE:
            self.main.config.keymode = Config.CONTROLLER_MODE
        elif self.mode == ConfigUI.INPUT_MODE:
            self.main.config.keymode = Config.KEYBOARD_MODE

    def redraw_osurf(self):
        self.osurf.fill((0x00, 0x66, 0xFF))
        pygame.draw.rect(self.osurf, (0, ) * 3, ((0, 0), (self.osurf.get_size())), 3)
        self.osurf.blit(self.font.render("Key", True, (0xFF, ) * 3),
            (self.column_x1, 5))
        self.osurf.blit(self.font.render("Alternate", True, (0xFF, ) * 3),
            (self.column_x2, 5))

        row = 10 + 48 * ((self.selected // 2) + 1)
        col = self.column_x1
        if self.selected % 2:
            col = self.column_x2
        color = (0x66, 0x88, 0xFF)
        if self.mode == ConfigUI.INPUT_MODE:
            color = (0x88, 0xCC, 0xFF)
        pygame.draw.rect(self.osurf, color, ((col, row), (300, 35)))

        config = self.main.config  # alias for readability

        for i, o in enumerate(self.options):    # for each option
            text = self.font.render(o, True, (0xFF, ) * 3)  # write the name
            y = 10 + 48 * (i + 1)   # TODO: Magic numbers
            self.osurf.blit(text, (self.option_width - text.get_width(), y))
            for j, k in enumerate(config.get_keys(o)):  # for each key
                name = "<unbound>"  # if no key bound
                color = (0xCC, ) * 3
                if k is not None:   # otherwise
                    name = pygame.key.name(k)   # lookup the pygame name
                    color = (0xFF, ) * 3
                self.osurf.blit(self.font.render(name, True, color),
                    (self.column_x2 if j else self.column_x1, y))

        pygame.draw.line(self.osurf, (0xFF, ) * 3, (self.option_width + 10, 5),
            (self.option_width + 10, self.osurf.get_height() - 5), 2)
        pygame.draw.line(self.osurf, (0xFF, ) * 3, (self.column_x2 - 10, 5),
            (self.column_x2 - 10, self.osurf.get_height() - 5), 2)
        pygame.draw.line(self.osurf, (0xFF, ) * 3, (self.option_width, 48),
            (self.osurf.get_width() - 5, 48), 2)
        self.redraw()

    def redraw(self):
        self.surface.fill((0x00, 0x33, 0x99))
        self.surface.blit(self.osurf, (100, 50))

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))

    def keydown(self, event):
        self.main.config.set_key(self.options[self.selected // 2],
            self.selected % 2, event.key)
        self.set_mode(ConfigUI.SELECT_MODE)
        self.redraw_osurf()

    def keyup(self, event):
        pass

    def keep_moving(self):
        pass

    def k_UP(self):
        if self.selected - 2 >= 0:
            self.selected -= 2
            self.redraw_osurf()

    def k_DOWN(self):
        if self.selected + 2 < len(self.options) * 2:
            self.selected += 2
            self.redraw_osurf()

    def k_LEFT(self):
        if self.selected % 2:
            self.selected -= 1
            self.redraw_osurf()

    def k_RIGHT(self):
        if not (self.selected % 2):
            self.selected += 1
            self.redraw_osurf()

    def k_CANCEL(self):
        self.main.ui_back()

    def k_OK(self):
        self.set_mode(ConfigUI.INPUT_MODE)
        self.redraw_osurf()

    def k_PAUSE(self):
        self.main.config.clear_key(self.options[self.selected // 2],
            self.selected % 2)
        self.redraw_osurf()

    @staticmethod
    def name():
        return "config"