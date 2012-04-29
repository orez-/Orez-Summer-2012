import pygame


class Unit:
    def __init__(self):
        self.image = pygame.image.load("img/dude.png")
        self.loc = [0, 0]
        self.velocity = [0, 0]

    def move(self):
        self.loc = map(sum, zip(self.loc, self.velocity))

    def blit_params(self):
        return (self.image, self.loc)

    def _handle_key(self, key, mult):
        if key == pygame.K_DOWN:
            self.velocity[1] += 5 * mult
        if key == pygame.K_RIGHT:
            self.velocity[0] += 5 * mult
        if key == pygame.K_UP:
            self.velocity[1] -= 5 * mult
        if key == pygame.K_LEFT:
            self.velocity[0] -= 5 * mult

    def handle_key_down(self, key):
        self._handle_key(key, 1)

    def handle_key_up(self, key):
        self._handle_key(key, -1)
