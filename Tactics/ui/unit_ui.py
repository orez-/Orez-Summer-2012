import pygame

import ui
from unit import Unit
from constants import SCREEN_SIZE


class UnitUI(ui.TacticsUI):
    def __init__(self, *args, **kwargs):
        super(UnitUI, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface(SCREEN_SIZE)
        # do not redraw in here i guess; this screen does nothing
        # until set_unit is called.

    def set_unit(self, menuunit):
        self.menu_unit = menuunit
        self.redraw()

    def redraw(self):
        self.surface.fill((0, 0, 0))
        self.menu_unit.reblit(self.surface)

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))

    def k_CANCEL(self):
        self.main.ui_back()

    @staticmethod
    def name():
        return "unit"
