from terrain import Room
import pygame

TILESET = pygame.image.load("imgs/grasslands.png")


class Grasslands(Room):
    def __init__(self, room):
        map_data = self.generate_room(room)
        super(Grasslands, self).__init__(map_data, TILESET, room)

    def generate_room(self, room):
        width = room.w * Room.TPS
        height = room.h * Room.TPS
        toR = [[(1, 0)] * width] + [
            [(1, 0)] + [(0, 0)] * (width - 2) + [(1, 0)]
            for _ in xrange(height - 2)] + [[(1, 0)] * width]

        for x, y, dr in room.paths_iter():
            if (room.x, room.y) == (0, 0):
                print x, y, dr
            x = int((x + .5) * Room.TPS)
            y = int((y + .5) * Room.TPS)
            if dr == 1:
                toR[0][x - 1] = (0, 0)
                toR[0][x] = (0, 0)
                toR[0][x + 1] = (0, 0)
            elif dr == 2:
                toR[y - 1][-1] = (0, 0)
                toR[y][-1] = (0, 0)
                toR[y + 1][-1] = (0, 0)
            elif dr == 4:
                toR[-1][x - 1] = (0, 0)
                toR[-1][x] = (0, 0)
                toR[-1][x + 1] = (0, 0)
            elif dr == 8:
                toR[y - 1][0] = (0, 0)
                toR[y][0] = (0, 0)
                toR[y + 1][0] = (0, 0)
        return toR
