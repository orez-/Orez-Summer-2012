import pygame


class TacticsUI(object):
    def __init__(self, main, parent=None):
        self.main = main
        self.parent = parent

    def redraw(self):
        pass

    def reblit(self, screen):
        pass

    def keydown(self, event):
        pass

    def keyup(self, event):
        pass

    def keep_moving(self):
        """ Called every frame: should probably be renamed. """
        pass

    def k_UP(self):
        """ Called when the user presses a key marked as 'up' """
        pass

    def k_DOWN(self):
        """ Called when the user presses a key marked as 'down' """
        pass

    def k_LEFT(self):
        """ Called when the user presses a key marked as 'left' """
        pass

    def k_RIGHT(self):
        """ Called when the user presses a key marked as 'right' """
        pass

    def k_CANCEL(self):
        pass

    def k_OK(self):
        pass

    def k_PAUSE(self):
        pass

    @staticmethod
    def name():
        raise NotImplementedError


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
        self.oloc = self.loc
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
