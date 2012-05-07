import pygame

from unit import Unit
import ui


class TeamUI(ui.TacticsUI):
    """ Used on the overworld to deal with units/inventory """
    def __init__(self):
        super(ui.TacticsUI, self).__init__()
        self.size = (1000, 500)
        self.surface = pygame.Surface(self.size)
        self.units = [MenuUnit(Unit("trainee", name="Orez"+str(i)), i) for i in xrange(6)]

        self.redraw()

    def redraw(self):
        self.surface.fill((0x00, 0x33, 0x99))
        for u in self.units:
            u.reblit(self.surface)

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))

    def keydown(self, event):
        pass

    def keyup(self, event):
        pass

    def keep_moving(self):
        pass

class MenuUnit:
    """ A unit shown in the menu """
    def __init__(self, unit, loc):
        self.size = (325, 150)
        self.portrait_size = (136, ) * 2
        self.surface = pygame.Surface(self.size)
        self.font = pygame.font.Font(None, 25)
        self.unit = unit
        spacing = 12.5
        self.loc = (spacing + ((loc % 2) * (self.size[0] + spacing)),
            (loc // 2) * (self.size[1] + spacing) + spacing)
        self.redraw()

    def redraw(self):
        self.surface.fill((0x00, 0x66, 0xFF))
        pygame.draw.rect(self.surface, (0, ) * 3, ((0, 0), self.size), 3)

        self.surface.fill((0x00, 0x33, 0x33), ((7, 7), self.portrait_size))
        pygame.draw.rect(self.surface, (0, ) * 3, ((7, 7), self.portrait_size), 2)

        self.surface.blit(self.font.render(self.unit.name, True, (0xFF, ) * 3),
            (164, 6))
        self.surface.blit(self.font.render("HP "+str(self.unit.get_cur_hp())+"/"+
            str(self.unit.get_cur_hp()), True, (0xFF, ) * 3), (164, 41))

    def reblit(self, screen):
        screen.blit(self.surface, self.loc)
