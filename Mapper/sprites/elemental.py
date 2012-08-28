import pygame
import random

from sprites import Sprite, Animations


class ElementalAI(Sprite):
    def __init__(self, (x, y)):
        def anon():
            last = -1
            next = 0
            while 1:
                while next == last:
                    next = random.randint(0, 4)
                yield (0, next, 50)
                last = next

        animations = Animations("elemental", (50, 50),
            {("", "idle"): anon}, ("", "idle"))
        super(ElementalAI, self).__init__(animations, (x, y))

    def move(self, room, x=0, y=0):
        self.x += x * 5
        self.y += y * 5

    def act(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
