import pygame

from sprites import Sprite, Animations


class GoblinAI(Sprite):
    def __init__(self, (x, y)):
        def anon():
            delay = 50
            while 1:
                yield (0, 0, 100 * delay)
                yield (0, 1, 25 * delay)
                yield (0, 2, 50 * delay)
                yield (0, 1, 10 * delay)

        animations = Animations("goblin", (50, 50),
            {"idle": anon}, "idle")
        super(GoblinAI, self).__init__(animations, (x, y))
