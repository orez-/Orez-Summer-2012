import pygame
import random
from math import pi

from cursor import Cursor
from board import Board
from skills import SkillHelix


class Main:
    def __init__(self):
        pygame.init()   # Initialize the game engine

        self.size = (1000, 500)
        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Orez Tactics")

        self.done = False
        self.clock = pygame.time.Clock()

        self.cursor = Cursor()
        self.board = Board((20, 20, 30), (40, 20, 10), self.size)
        # TODO: not a fan of the magic numbers
        self.skills = SkillHelix()
        self.screen.fill((0, ) * 3)
        self.board.set_display_position(*self.cursor.board_pos)

    def run(self):
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.skills.move(-1)
                    if event.key == pygame.K_DOWN:
                        self.skills.move(1)
                    #if self.cursor.handle_key(event.key, self.board):
                    #    self.board.set_display_position(*self.cursor.board_pos)

            self.skills.keep_moving()
            if self.cursor.keep_moving():
                self.board.set_display_position(*self.cursor.board_pos)
            self.screen.fill((0, ) * 3)
            self.skills.reblit(self.screen)
            #self.board.reblit(self.screen)
            #self.cursor.redraw(self.screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    m = Main()
    m.run()
