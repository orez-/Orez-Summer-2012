import pygame
import random
from math import pi

from ui.skill_ui import SkillUI
from ui.battle_ui import BattleUI
from ui.overworld_ui import OverworldUI


class Main:
    def __init__(self):
        pygame.init()   # Initialize the game engine

        self.size = (1000, 500)
        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Orez Tactics")

        self.done = False
        self.clock = pygame.time.Clock()

        self.screen.fill((0, ) * 3)

        #self.ui = SkillUI()
        self.ui = OverworldUI()
        self.mousedown = False

    def run(self):
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.ui.keydown(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousedown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mousedown = False
                elif event.type == pygame.MOUSEMOTION:
                    pass

            self.ui.keep_moving()
            self.screen.fill((0, ) * 3)
            self.ui.reblit(self.screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    m = Main()
    m.run()
