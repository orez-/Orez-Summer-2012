import pygame
from math import ceil

from tile import Tile


class Board:
    def __init__(self, chunk_size, square_size, screen_size):
        self.assert_type(chunk_size,  tuple, 3, name="chunk_size")
        self.assert_type(square_size, tuple, 3, name="square_size")
        self.assert_type(screen_size, tuple, 2, name="screen_size")
        self.sqS = square_size
        self.chunk = chunk_size
        self.ssize = screen_size
        Tile.sqS = self.sqS
        self.board_size = ((self.chunk[0] + self.chunk[1]) * self.sqS[0] / 2,
                           (self.chunk[0] + self.chunk[1]) * self.sqS[1] / 2,
                           (self.chunk[2] * self.sqS[2]))
        self.board_data = [[Tile(x + 1, y + 1, min(self.chunk[2],
                                int(((y + 1) ** 2 + (x + 1) ** 2) ** .5)))\
                                for y in xrange(self.chunk[1])]\
                                    for x in xrange(self.chunk[0])]
        self.board_image = pygame.Surface(
            (self.board_size[0], self.board_size[1] + self.board_size[2]))
        self.dx = 0
        self.dy = 0
        self.build_display()

    def set_display_position(self, cx, cy):
        """ Set the display position based on player coordinates. Accepts
        fractional values for one coordinate (never both), for a frame in a
        transition """
        if cx == int(cx) and cy == int(cy):   # you are ON a square
            zOffset = self.board_data[int(cx)][int(cy)].z
        else:  # you are between squares
            fx = cx - int(cx)
            fy = cy - int(cy)
            if fx and fy:
                raise TypeError("You may only move the display in one cardinal"+
                    "direction at a time.")
            zOffset = self.board_data[int(cx)][int(cy)].z * (1 - max(fx, fy))
            zOffset += self.board_data[int(ceil(cx))][int(ceil(cy))].z *\
                    max(fx, fy)
            # linear average of the two

        self.dx = (cx - cy) * self.sqS[0] / 2 + (self.ssize[0] - self.board_size[0]) / 2
        self.dy = (cx + cy) * self.sqS[1] / 2 + zOffset * self.sqS[2] + (self.ssize[1] / 2 - (self.board_size[1] + self.board_size[2])) + 18

    def select_square(self, cx, cy):
        cx = int(cx)
        cy = int(cy)
        self.board_data[int(cx)][int(cy)].selected ^= True
        self.build_display()

    def build_display(self):
        self.board_image.fill((0, 0, 0))
        for x in xrange(self.chunk[0] - 1, -1, -1):
            for y in xrange(self.chunk[1] - 1, -1, -1):
                self.board_data[x][y].draw_tile(self.board_image, self.chunk[0])
        self.board_image = pygame.transform.flip(self.board_image, False, True)

    def reblit(self, screen):
        screen.blit(self.board_image, (self.dx, self.dy))

    def assert_type(self, checkitem, checkType, size=-1, **args):
        name = ""
        if "name" in args:
            name = " for " + args["name"]
        if not (isinstance(checkitem, checkType) and\
        (size == -1 or len(checkitem) == size)):
            size = str(size)
            if isinstance(checkitem, checkType):
                raise TypeError("You must pass a tuple of size " + size + name\
                    + " (passed tuple of size " + str(len(checkitem)) + ")")
            raise TypeError("You must pass a tuple" + ("" if size == "-1" else\
                " of size " + size) + name + " (passed " + str(type(checkitem))\
                + ")")
