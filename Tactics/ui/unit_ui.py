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
        self.leftsurf = pygame.Surface((470, 450))
        self.rightsurf = EquipmentPage()
        self.redraw_both()

        self.darksurface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.darksurface.fill((0, 0, 0, 255))
        self.darkstep = 0
        
        self.mode = UnitUI.IN_MODE
        # do not redraw in here i guess; this screen does nothing
        # until set_unit is called.

    def redraw_both(self):
        self.redraw_left(False)
        self.redraw_right(False)

    def redraw_left(self, do_redraw=True):
        self.leftsurf.fill((0, 0x66, 0xFF))
        pygame.draw.rect(self.leftsurf, (0, ) * 3, ((0, 0), (470, 450)), 3)
        if do_redraw:
            self.redraw()

    def redraw_right(self, do_redraw=True):
        self.rightsurf.redraw()
        if do_redraw:
            self.redraw()

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
        self.surface.blit(self.leftsurf, (26, 30))
        self.surface.blit(self.rightsurf, (514, 30))

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

class UnitPages(pygame.Surface):
    """ Nominally abstract """
    def __init__(self):  # probably want to send the unit too
        super(UnitPages, self).__init__((470, 450))
        self.tabwidth = 33

    def redraw(self, tabnum):
        self.fill((0, 0x66, 0xFF))
        pygame.draw.lines(self, (0, ) * 3, False,
            ((tabnum * self.tabwidth, 0), (0, 0), (0, 450),
             (470, 450), (470, 0), ((tabnum + 1) * self.tabwidth, 0)), 3)


class EquipmentPage(UnitPages):
    def __init__(self):
        super(EquipmentPage, self).__init__()
        self.font = pygame.font.Font(None, 40)
        self.slots = ["Head", "Armor", "Mainhand", "Offhand", "Accessories"]
        self.slot_width = max(map(lambda x: self.font.size(x)[0], self.slots))

    def redraw(self):
        super(EquipmentPage, self).redraw(0)
        for i, slot in enumerate(self.slots):
            slot_text = self.font.render(slot, True, (0xFF, ) * 3)
            self.blit(slot_text, (self.slot_width - slot_text.get_size()[0] + 5,
                i*(5+slot_text.get_size()[1]) + 5))

