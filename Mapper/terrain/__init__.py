import pygame


class Tile(object):
    def __init__(self):
        pass


class Room(object):
    def __init__(self, map_data, tile_map):
        self.map = [x[:] for x in map_data]
        self.tile_map = tile_map
        self.surface = pygame.Surface(
            map(self.resize, (len(self.map[0]), len(self.map))))
        self.redraw()

    @staticmethod
    def resize(x):
        return 50 * x

    def reblit(self, surf, (x, y)):
        surf.blit(self.surface, (-x, -y))

    def redraw(self):
        for y, row in enumerate(self.map):
            for x, elem in enumerate(row):
                self.surface.blit(self.tile_map,
                    map(self.resize, (x, y)),
                    (map(self.resize, elem), map(self.resize, (1, 1))))
