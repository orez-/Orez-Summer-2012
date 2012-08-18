from terrain import Room
import pygame


class Grasslands(Room):
    def __init__(self, load_data=None):
        map_data = [[(0, 0)] * 12] * 9
        pics = pygame.image.load("imgs/grasslands.png")
        super(Grasslands, self).__init__(map_data, pics)
