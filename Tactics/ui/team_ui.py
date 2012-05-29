import pygame
import math

import ui
from ui import MenuUnit
from unit import Unit
from constants import SCREEN_SIZE


class TeamUI(ui.TacticsUI):
    """ Used on the overworld to deal with units/inventory """
    MENU_MODE = 1
    SQUAD_MODE = 2
    OUT_MODE = 3
    IN_MODE = 4

    FADE_STEPS = 18

    def __init__(self, *args, **kwargs):
        super(TeamUI, self).__init__(*args, **kwargs)
        self.size = SCREEN_SIZE
        self.surface = pygame.Surface(self.size)
        self.darksurface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.darkstep = 0
        self.units = [MenuUnit(Unit("trainee", name="Orez" + str(i)), i)
            for i in xrange(6)]
        self.highlighted = 0    # the highlighted unit
        self.sidebar = Sidebar([
            ("Squad", lambda: self.set_mode(TeamUI.SQUAD_MODE)),
            ("Inventory", self.nothing),
            ("Options", lambda: self.main.push_ui("config")),
            ("Save", self.nothing)])
        self.mode = TeamUI.MENU_MODE
        self.redraw()

    def nothing(self):
        pass

    def select_unit(self, amt=None, absolute=False):
        """ Move the highlight over the units on the selection screen by `amt`
        amount. If no `amt` is specified, deselects all units. """
        if self.highlighted is not None:
            self.units[self.highlighted].set_selected(False)
        if amt is not None:
            if absolute:
                self.highlighted = amt
            else:
                self.highlighted = (self.highlighted + amt) % len(self.units)
            self.units[self.highlighted].set_selected(True)
        self.redraw()

    def redraw(self):
        self.surface.fill((0x00, 0x33, 0x99))
        for u in self.units:
            u.reblit(self.surface)
        self.sidebar.reblit(self.surface)

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))
        if self.mode == TeamUI.OUT_MODE or self.mode == TeamUI.IN_MODE:
            screen.blit(self.darksurface, (0, 0))
            self.units[self.highlighted].reblit(screen)

    def keyup(self, event):
        pass

    def set_mode(self, mode):
        if self.mode == TeamUI.MENU_MODE:
            self.sidebar.set_focus(False)
            self.redraw()
        elif self.mode == TeamUI.SQUAD_MODE:
            self.select_unit()
            self.redraw()
        elif self.mode == TeamUI.OUT_MODE:
            self.darksurface.fill((0, 0, 0, 0))
            self.darkstep = 0

        self.mode = mode

        if self.mode == TeamUI.MENU_MODE:
            self.sidebar.set_focus(True)
            self.redraw()
        if self.mode == TeamUI.SQUAD_MODE:
            self.select_unit(self.highlighted, True)
            self.redraw()
        if self.mode == TeamUI.OUT_MODE:
            self.darksurface.fill((0, 0, 0, 1))
            self.darkstep = 0
        if self.mode == TeamUI.IN_MODE:
            self.darksurface.fill((0, 0, 0, 255))
            self.darkstep = 0

    def k_UP(self):
        if self.mode == TeamUI.MENU_MODE:
            self.sidebar.selected = max(self.sidebar.selected - 1, 0)
            self.sidebar.redraw()
            self.redraw()
        elif self.mode == TeamUI.SQUAD_MODE:
            self.select_unit(-2)

    def k_DOWN(self):
        if self.mode == TeamUI.MENU_MODE:
            self.sidebar.selected = min(self.sidebar.selected + 1,
                len(self.sidebar.options) - 1)
            self.sidebar.redraw()
            self.redraw()
        elif self.mode == TeamUI.SQUAD_MODE:
            self.select_unit(2)

    def k_LEFT(self):
        if self.mode == TeamUI.SQUAD_MODE:
            self.select_unit(-1)

    def k_RIGHT(self):
        if self.mode == TeamUI.SQUAD_MODE:
            self.select_unit(1)

    def k_CANCEL(self):
        if self.mode == TeamUI.MENU_MODE:
            self.main.ui_back()  # go back to the previous screen
        elif self.mode == TeamUI.SQUAD_MODE:
            self.set_mode(TeamUI.MENU_MODE)

    def k_OK(self):
        if self.mode == TeamUI.MENU_MODE:
            self.sidebar.k_OK()
        elif self.mode == TeamUI.SQUAD_MODE:
            self.set_mode(TeamUI.OUT_MODE)

    def keep_moving(self):
        if self.mode == TeamUI.OUT_MODE:
            def on_done(to):
                self.units[self.highlighted].loc = to
                self.main.push_ui("unit")
                self.main.ui.set_unit(self.units[self.highlighted])
                self.set_mode(TeamUI.IN_MODE)
            self.fade(True, on_done)
        elif self.mode == TeamUI.IN_MODE:
            def on_done(to):
                self.units[self.highlighted].loc = self.units[self.highlighted].oloc
                self.set_mode(TeamUI.SQUAD_MODE)
            self.fade(False, on_done)

    def fade(self, out, on_done):
        to = 12, 12
        if self.darkstep >= TeamUI.FADE_STEPS:
            on_done(to)
            return
        d = math.cos((math.pi / 2) * self.darkstep / TeamUI.FADE_STEPS)
        if not out:
            d = 1 - d
        self.units[self.highlighted].loc =\
            ((self.units[self.highlighted].oloc[0] - to[0]) * d + to[0],
             (self.units[self.highlighted].oloc[1] - to[1]) * d + to[1])
        self.darksurface.fill((0, 0, 0, 255 - int(d * 255)))
        self.darkstep += 1

    @staticmethod
    def name():
        return "team"


class Sidebar:
    def __init__(self, options):
        self.loc = (MenuUnit.size[0] * 2 + MenuUnit.spacing * 3,
            MenuUnit.spacing)
        self.size = (SCREEN_SIZE[0] - (self.loc[0] + MenuUnit.spacing),
            SCREEN_SIZE[1] - MenuUnit.spacing * 2)

        self.options = options

        self.selected = 0
        self.focused = True
        self.surface = pygame.Surface(self.size)
        self.font = pygame.font.Font(None, 25)
        self.redraw()

    def set_focus(self, focus):
        if self.focused != focus:
            self.focused = focus
            self.redraw()

    def k_OK(self):
        self.options[self.selected][1]()

    def redraw(self):
        color = (0x00, 0x66, 0xFF)
        wordcolor = (0xFF, ) * 3 if self.focused else (0x99, ) * 3
        self.surface.fill(color)
        pygame.draw.rect(self.surface, (0, ) * 3, ((0, 0), self.size), 3)
        for i, (o, _) in enumerate(self.options):
            if i == self.selected:
                o = "> " + o
            self.surface.blit(self.font.render(o, True, wordcolor),
                (7, 7 + 25 * i))

    def reblit(self, screen):
        screen.blit(self.surface, self.loc)
