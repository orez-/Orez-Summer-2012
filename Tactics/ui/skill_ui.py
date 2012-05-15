from math import pi
from skills import SkillHelix
import pygame

import ui


class SkillUI(ui.TacticsUI):
    def __init__(self, *args, **kwargs):
        super(SkillUI, self).__init__(*args, **kwargs)
        self.skills = SkillHelix()

    def redraw(self):
        self.skills.redraw()

    def reblit(self, screen):
        self.skills.reblit(screen)

    def k_UP(self):
        self.skills.move(-1)
        
    def k_DOWN(self):
        self.skills.move(1)
        
        try:
            self.skills.set_viewangle(int(event.unicode)*10)
        except:
            pass

    def keep_moving(self):
        self.skills.keep_moving()

    @staticmethod
    def name():
        return "skill"