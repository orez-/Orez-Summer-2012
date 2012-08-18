from terrain import Room
import pygame

TPS = 3  # Tiles per Square
class Grasslands(Room):
    def __init__(self, load_data=None, **kwargs):
        w, h = 1, 1
        if "width" in kwargs and "height" in kwargs:
            w, h = kwargs["width"], kwargs["height"]
        map_data = self.generate_room(w, h)
        pics = pygame.image.load("imgs/grasslands.png")
        super(Grasslands, self).__init__(map_data, pics)

    def generate_room(self, width, height):
        # return [[(0, 0)] * TPS] * TPS
        return [[(1, 0)] * TPS] + [(
            [(1, 0)] + [(0, 0)] * (TPS - 2) + [(1, 0)]
            )] * (TPS - 2) + [[(1, 0)] * TPS]
