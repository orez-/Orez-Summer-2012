from math import pi
from skills import SkillHelix
import pygame

import ui


class SkillUI(ui.TacticsUI):
    def __init__(self):
        self.skills = SkillHelix()

    def redraw(self):
        self.skills.redraw()

    def reblit(self, screen):
        self.skills.reblit(screen)

    def keydown(self, event):
        if event.key == pygame.K_UP:
            self.skills.move(-1)
        if event.key == pygame.K_DOWN:
            self.skills.move(1)
        try:
            self.skills.set_viewangle(int(event.unicode)*10)
        except:
            pass

    def keep_moving(self):
        self.skills.keep_moving()
