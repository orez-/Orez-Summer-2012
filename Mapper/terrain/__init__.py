import pygame


class Tile(object):
    def __init__(self):
        pass


class Room(object):
    TPS = 15  # Tiles per Square

    def __init__(self, map_data, (tile_map, impassible), roomds):
        self.map = [d[:] for d in map_data]
        self.tile_map = tile_map
        self.surface = pygame.Surface(
            map(self.resize, (len(self.map[0]), len(self.map))))
        self.impassible = impassible
        self.roomds = roomds
        self.entities = set()
        self.redraw()

    pos = property(lambda self: (self.roomds.x, self.roomds.y))
    x = property(lambda self: self.roomds.x)
    y = property(lambda self: self.roomds.y)
    w = property(lambda self: self.roomds.w)
    h = property(lambda self: self.roomds.h)

    @staticmethod
    def resize(x):
        return 50 * x

    def get_at(self, (x, y)):
        """ In terms of character tile position from the top left of this room """
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[int(y)]):
            return self.map[int(y)][int(x)]
        return None

    def get_abs(self, (x, y)):
        """ In terms of character tile position from the top left room """
        return self.get_at((x - self.x * Room.TPS, y - self.y * Room.TPS))

    def reblit(self, surf, time_passed, (vx, vy), (tlrx, tlry)):
        surf.blit(self.surface,
            ((self.x - tlrx) * 50 * Room.TPS - vx,
             (self.y - tlry) * 50 * Room.TPS - vy))
        for e in self.entities:
            e.reblit(surf, time_passed, (vx, vy))

    def redraw(self):
        for y, row in enumerate(self.map):
            for x, elem in enumerate(row):
                self.surface.blit(self.tile_map,
                    map(self.resize, (x, y)),
                    (map(self.resize, elem), map(self.resize, (1, 1))))

    def __repr__(self):
        return "Room: " + str(self.x) + ", " + str(self.y)
