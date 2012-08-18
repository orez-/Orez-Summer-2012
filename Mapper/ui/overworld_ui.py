import pygame

import ui
from ui.map_ui import MapUI
from terrain.rooms import Grasslands
from sprites.slime import SlimeAI

SCREEN_SIZE = (600, 450)


class OverworldUI(ui.UI):
    def __init__(self, main, parent):
        super(OverworldUI, self).__init__(main, parent)
        #self.surface = pygame.Surface(SCREEN_SIZE)
        self.slime = SlimeAI((0, 0))
        self.terrain = Grasslands()
        self.redraw()

    def redraw(self):
        pass
        #self.surface.fill((0xFF, ) * 3)

    def reblit(self, surf, time_passed):
        super(OverworldUI, self).reblit(surf, time_passed)
        center = self.slime.centerx - 300, self.slime.centery - 225
        self.terrain.reblit(surf, center)
        self.slime.reblit(surf, time_passed, center)

    def handle_key(self, event):
        if event.key == pygame.K_m:
            self.main.ui_push(MapUI)

    def update(self):
        xoff, yoff = 0, 0
        if self.main.keys & set((pygame.K_a, pygame.K_LEFT)):
            xoff -= 1
        if self.main.keys & set((pygame.K_d, pygame.K_RIGHT)):
            xoff += 1
        if self.main.keys & set((pygame.K_w, pygame.K_UP)):
            yoff -= 1
        if self.main.keys & set((pygame.K_s, pygame.K_DOWN)):
            yoff += 1
        if not (xoff == yoff == 0):  # there is movement
            self.slime.move(xoff, yoff)
        elif self.slime.animations.name[1] != "idle":
            self.slime.animations.cur_animation = (
                self.slime.animations.name[0], "idle")

