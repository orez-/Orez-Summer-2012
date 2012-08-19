from terrain import Room
import pygame

TILESET = pygame.image.load("imgs/grasslands.png")
class Grasslands(Room):
    def __init__(self, (x, y), load_data=None, **kwargs):
        w, h = 1, 1
        if "width" in kwargs and "height" in kwargs:
            w, h = kwargs["width"], kwargs["height"]
        map_data = self.generate_room(w, h)
        super(Grasslands, self).__init__(map_data, TILESET, (x, y))

    def generate_room(self, width, height):
        width *= Room.TPS
        height *= Room.TPS
        return [[(1, 0)] * width] + [
            [(1, 0)] + [(0, 0)] * (width - 2) + [(1, 0)]
            ] * (height - 2) + [[(1, 0)] * width]
