import pygame
import random

from sprites import Sprite, Animations


class GoblinAI(Sprite):
    def __init__(self, (x, y)):
        def anon():
            delay = 50
            while 1:
                if random.randint(0, 9) < 4:
                    for _ in xrange(3):
                        yield (1, 0, delay)
                        yield (1, 1, delay)
                yield (0, 0, 100 * delay)
                yield (0, 1, 25 * delay)
                yield (0, 2, 50 * delay)
                yield (0, 1, 5 * delay)

        animations = Animations("goblin", (50, 50),
            {"idle": anon}, "idle")
        super(GoblinAI, self).__init__(animations, (x, y))
