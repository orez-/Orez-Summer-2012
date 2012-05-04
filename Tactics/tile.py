import pygame
import math
import random
from unit import *


class Tile:
    top_img = \
        pygame.transform.flip(pygame.image.load("img/top.png"), False, True)
    sqS = ()

    def __init__(self, cx, cy, cz):
        self.selected = False
        self.x = cx
        self.y = cy
        self.z = cz
        self.unit = (Unit("ninja") if random.randint(0, 20) < 4 else None)

    def draw_tile(self, surface, mx, rx=None, ry=None, rz=None):
        if Tile.sqS == ():
            raise Exception("You must define sqS in Tile" +
                "before using any Tiles")
        rx = self.x if rx == None else rx
        ry = self.y if ry == None else ry
        rz = self.z if rz == None else rz

        sqW = Tile.sqS[0]
        sqH = Tile.sqS[1]
        sqD = Tile.sqS[2]

        # vvv COLORS!!! vvv
        step = 255 / max(20, 20)   # size of board
        base = (rx * step / 2, ry * step / 4, 50)
        top = (rx * step, 50, ry * step)
        #base = (128,64,0)
        #top  = (0,128,0)

        size = (sqW, rz * sqD + sqH)
        surf = pygame.Surface(size)
        surf.fill((255, 0, 255))
        surf.set_colorkey((255, 0, 255))  # magenta is see-through

        pygame.draw.polygon(surf, base,
            [(0, sqH / 2), (sqW / 2, 0),
            (sqW, sqH / 2), (sqW, sqD * rz + sqH / 2),
            (0, sqD * rz + sqH / 2)])
        surf.blit(Tile.top_img, (0, sqD * rz + 1))
        if self.selected:
            pygame.draw.polygon(surf, top,
                [(0, sqD * rz + sqH / 2), (sqW / 2, sqD * rz),
                (sqW, sqD * rz + sqH / 2), (sqW / 2, sqD * rz + sqH)])
        surfloc = ((mx - 1) * sqW / 2 - ((rx - ry) * sqW) / 2,
            ((rx + ry - 2) * sqH) / 2)
        surface.blit(surf, surfloc)
        if self.unit != None:
            self.unit.display(surface, (int(surfloc[0] + (size[0] - 25) / 2),
                int(surfloc[1] + size[1] - 12)))
