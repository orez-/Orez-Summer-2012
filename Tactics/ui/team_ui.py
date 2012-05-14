import pygame

import ui
from unit import Unit
from constants import SCREEN_SIZE, Config


class TeamUI(ui.TacticsUI):
    """ Used on the overworld to deal with units/inventory """
    MENU_MODE = 1
    SQUAD_MODE = 2

    def __init__(self):
        super(ui.TacticsUI, self).__init__()
        self.size = SCREEN_SIZE
        self.surface = pygame.Surface(self.size)
        self.units = [MenuUnit(Unit("trainee", name="Orez" + str(i)), i)
            for i in xrange(6)]
        self.highlighted = 0    # the highlighted unit
        self.sidebar = Sidebar()
        self.mode = TeamUI.MENU_MODE

        self.redraw()

    def select_unit(self, amt):
        self.units[self.highlighted].set_selected(False)
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

    def keydown(self, event):
        if self.mode == TeamUI.MENU_MODE:
            if Config.k_UP(event):
                self.sidebar.selected = max(self.sidebar.selected - 1, 0)
                self.sidebar.redraw()
                self.redraw()
            elif Config.k_DOWN(event):
                self.sidebar.selected = min(self.sidebar.selected + 1,
                    len(self.sidebar.options)-1)
                self.sidebar.redraw()
                self.redraw()
        elif self.mode == TeamUI.SQUAD_MODE:
            if Config.k_UP(event):
                self.select_unit(-2)
            elif Config.k_LEFT(event):
                self.select_unit(-1)
            elif Config.k_RIGHT(event):
                self.select_unit(2)
            elif Config.k_DOWN(event):
                self.select_unit(1)

    def keyup(self, event):
        pass

    def keep_moving(self):
        pass


class Sidebar:
    def __init__(self):
        self.loc = (MenuUnit.size[0] * 2 + MenuUnit.spacing * 3,
            MenuUnit.spacing)
        self.size = (SCREEN_SIZE[0] - (self.loc[0] + MenuUnit.spacing),
            SCREEN_SIZE[1] - MenuUnit.spacing * 2)

        self.options = [
            ("Squad", self.nothing),
            ("Inventory", self.nothing),
            ("Options", self.nothing),
            ("Save", self.nothing)]

        self.selected = 0
        self.surface = pygame.Surface(self.size)
        self.font = pygame.font.Font(None, 25)
        self.redraw()

    def nothing(self):
        pass

    def redraw(self):
        color = (0x00, 0x66, 0xFF)
        self.surface.fill(color)
        pygame.draw.rect(self.surface, (0, ) * 3, ((0, 0), self.size), 3)
        for i, (o, _) in enumerate(self.options):
            if i == self.selected:
                o = "> " + o
            self.surface.blit(self.font.render(o, True, (0xFF, ) * 3),
                (7, 7 + 25 * i))

    def reblit(self, screen):
        screen.blit(self.surface, self.loc)


class MenuUnit:
    """ A unit shown in the menu """
    size = (325, 150)
    spacing = 12.5

    def __init__(self, unit, loc):
        self.portrait_size = (136, ) * 2
        self.surface = pygame.Surface(self.size)
        self.font = pygame.font.Font(None, 25)
        self.unit = unit
        spacing = MenuUnit.spacing
        self.loc = (spacing + ((loc % 2) * (MenuUnit.size[0] + spacing)),
            (loc // 2) * (MenuUnit.size[1] + spacing) + spacing
            + ((loc % 2) * 2 - 1) * spacing / 2)
        self.selected = False
        self.redraw()

    def set_selected(self, selected):
        self.selected = selected
        self.redraw()

    def redraw(self):
        color = (0x00, 0x66, 0xFF)
        if self.selected:
            color = (0x66, 0x88, 0xFF)
        self.surface.fill(color)
        pygame.draw.rect(self.surface, (0, ) * 3, ((0, 0), self.size), 3)

        self.surface.fill((0x00, 0x33, 0x33), ((7, 7), self.portrait_size))
        pygame.draw.rect(self.surface, (0, ) * 3, ((7, 7), self.portrait_size),
            2)

        self.surface.blit(self.font.render(self.unit.name, True, (0xFF, ) * 3),
            (164, 6))
        self.surface.blit(self.font.render("HP " + str(self.unit.get_cur_hp())
            + "/" + str(self.unit.get_cur_hp()), True, (0xFF, ) * 3),
            (164, 41))

    def reblit(self, screen):
        screen.blit(self.surface, self.loc)
