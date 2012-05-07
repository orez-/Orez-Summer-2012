import pygame
import random
from math import pi

from ui.skill_ui import SkillUI
from ui.battle_ui import BattleUI
from ui.overworld_ui import OverworldUI
from ui.team_ui import TeamUI


class Main:
    def __init__(self):
        pygame.init()   # Initialize the game engine

        d = pygame.display.Info()
        self.desktop_size = (d.current_w, d.current_h)
        self.size = (1000, 500)
        self.ssize = self.size
        self.blit_offset = (0, 0)

        self.prescreen = pygame.Surface(self.size)
        self.screen = pygame.display.set_mode(self.size)
        self.fullscreen = False

        pygame.display.set_caption("Orez Tactics")

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps_font = pygame.font.Font(None, 16)

        self.screen.fill((0, ) * 3)

        self.ui = TeamUI()
        self.mousedown = False

    def draw_fps(self):
        self.screen.blit(
            self.fps_font.render(str(self.clock.get_fps()),
                False, (0xFF, 0, 0)),
            (0, 0))

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size)
            self.ssize = self.size
            self.blit_offset = (0, 0)
        else:
            self.screen = pygame.display.set_mode(self.desktop_size,
                pygame.FULLSCREEN | pygame.HWSURFACE)
            scale = min((float(ds) / s) for ds, s in
                zip(self.desktop_size, self.size))
            self.ssize = map(lambda x:int(x*scale), self.size)
            self.blit_offset = tuple((ds - (scale * s)) / 2 for ds, s in
                zip(self.desktop_size, self.size))
        self.fullscreen ^= True

    def run(self):
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    if event.key == pygame.K_F1:
                        self.toggle_fullscreen()
                    self.ui.keydown(event)
                elif event.type == pygame.KEYUP:
                    self.ui.keyup(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousedown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mousedown = False
                elif event.type == pygame.MOUSEMOTION:
                    pass

            self.ui.keep_moving()
            self.screen.fill((0, ) * 3)
            self.prescreen.fill((0, ) * 3)
            self.ui.reblit(self.prescreen)
            self.screen.blit(
                pygame.transform.smoothscale(self.prescreen, self.ssize),
                self.blit_offset)
            self.draw_fps()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    m = Main()
    m.run()
