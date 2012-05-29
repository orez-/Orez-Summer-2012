import pygame
import math

import ui
from unit import Unit
from constants import SCREEN_SIZE


class UnitUI(ui.TacticsUI):
    IN_MODE = 1
    ACTIVE_MODE = 2
    OUT_MODE = 3

    FADE_STEPS = 18

    def __init__(self, *args, **kwargs):
        super(UnitUI, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.darksurface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.darksurface.fill((0, 0, 0, 255))
        self.darkstep = 0
        self.mode = UnitUI.IN_MODE
        # do not redraw in here i guess; this screen does nothing
        # until set_unit is called.

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == UnitUI.IN_MODE:
            self.darkstep = 0
        if self.mode == UnitUI.OUT_MODE:
            self.darkstep = 0
        if self.mode == UnitUI.ACTIVE_MODE:
            self.darksurface.fill((0, 0, 0, 0))

    def set_unit(self, menuunit):
        self.menu_unit = menuunit
        self.redraw()

    def redraw(self):
        self.surface.fill((0, 0x33, 0xCC))

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))
        screen.blit(self.darksurface, (0, 0))
        self.menu_unit.reblit(screen)

    def k_CANCEL(self):
        if self.mode == UnitUI.ACTIVE_MODE:
            self.set_mode(UnitUI.OUT_MODE)

    def keep_moving(self):
        if self.mode == UnitUI.OUT_MODE:
            def on_done():
                self.main.ui_back()
            self.fade(True, on_done)
        elif self.mode == UnitUI.IN_MODE:
            def on_done():
                self.set_mode(UnitUI.ACTIVE_MODE)
            self.fade(False, on_done)

    def fade(self, out, on_done):
        if self.darkstep >= UnitUI.FADE_STEPS:
            on_done()
            return
        d = math.cos((math.pi / 2) * self.darkstep / UnitUI.FADE_STEPS)
        if not out:
            d = 1 - d
        self.darksurface.fill((0, 0, 0, 255 - int(d * 255)))
        self.darkstep += 1

    @staticmethod
    def name():
        return "unit"
