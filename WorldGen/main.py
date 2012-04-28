import pygame
import random
import os

from unit import Unit
from planet import Planet

class Main():
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        
        self.size = (600,600)
        self.screen = pygame.display.set_mode(self.size)    # pygame.RESIZABLE)
        
        pygame.display.set_caption("Game Name goes Here")
        self.done = False
        self.clock = pygame.time.Clock()
        
        self.planet = Planet(self.size)
        #self.unit = Unit()
        
    def redraw(self):
        self.screen.fill((0xFF,)*3)
        self.screen.blit(*self.planet.blit_params())
        #self.screen.blit(*self.unit.blit_params())
        
    def run(self):
        self.redraw()
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 0:
                        pass
                elif event.type == pygame.KEYDOWN:
                    pass
                elif event.type == pygame.KEYUP:
                    pass
                elif event.type == pygame.VIDEORESIZE:
                    pass
            
            #self.unit.move()
            self.redraw()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    m = Main()
    m.run()