import pygame


class Tile(object):
    def __init__(self):
        pass


class Room(object):
    TPS = 15  # Tiles per Square

    def __init__(self, map_data, tile_map, (x, y)):
        self.map = [d[:] for d in map_data]
        self.tile_map = tile_map
        self.surface = pygame.Surface(
            map(self.resize, (len(self.map[0]), len(self.map))))
        self.x, self.y = x, y  # these are invariant
        self.redraw()

    @staticmethod
    def resize(x):
        return 50 * x

    def reblit(self, surf, (vx, vy), (tlrx, tlry)):
        surf.blit(self.surface,
            ((self.x - tlrx) * 50 * Room.TPS - vx,
             (self.y - tlry) * 50 * Room.TPS - vy))

    def redraw(self):
        for y, row in enumerate(self.map):
            for x, elem in enumerate(row):
                self.surface.blit(self.tile_map,
                    map(self.resize, (x, y)),
                    (map(self.resize, elem), map(self.resize, (1, 1))))

    def __repr__(self):
        return "Room: " + str(self.x) + ", " + str(self.y)
