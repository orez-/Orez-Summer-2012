import random
import pygame

from terrain import Room
from ui.map_ui import RoomDS
from sprites.goblin import GoblinAI
from sprites.elemental import ElementalAI

TILESET = pygame.image.load("imgs/grasslands.png")


class Grasslands(Room):
    def __init__(self, room):
        map_data = self.generate_room(room)
        impassible = tuple((x, y) for x in xrange(6) for y in xrange(4) if (x, y) not in ((0, 0), (4, 3), (4, 2)))
        super(Grasslands, self).__init__(map_data, (TILESET, impassible), room)
        self.entities.add(ElementalAI(
            (random.randint(1, room.w * Room.TPS - 10) * 50,
            random.randint(1, room.h * Room.TPS) * 50)))
        self.transitions = {(4, 3): "room"}

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
        self.build_house(toR)
        return toR

    def build_house(self, toR):
        toR[1][-2] = (5, 1)
        toR[2][-2] = (5, 2)
        toR[3][-2] = (5, 3)

        toR[1][-3] = (4, 1)
        toR[2][-3] = (4, 2)
        toR[3][-3] = (4, 3)

        toR[1][-4] = (1, 1)
        toR[2][-4] = (1, 2)
        toR[3][-4] = (1, 3)

        toR[1][-5] = (0, 1)
        toR[2][-5] = (0, 2)
        toR[3][-5] = (0, 3)

TILESET2 = pygame.image.load("imgs/inside.png")


class Inside(Room):
    def __init__(self, room_toR, player_toR):
        self.room_toR = room_toR
        self.player_toR = player_toR
        room = RoomDS((0, 0), (1, 1))
        map_data = self.generate_room(room)
        impassible = ((0, 0), (1, 0), (3, 0), (0, 1), (3, 1), (0, 2), (2, 2), (3, 2))
        super(Inside, self).__init__(map_data, (TILESET2, impassible), room)
        self.entities.add(GoblinAI((200, 50)))
        self.transitions = {(2, 1): "out"}

    def generate_room(self, room):
        width = room.w * 12
        height = room.h * 9
        toR = [[(0, 0)] + [(1, 0)] * (width - 2) + [(3, 0)]] + [
            [(0, 1)] + [(1, 1)] * (width - 2) + [(3, 1)]
            for _ in xrange(height - 2)] + [
            [(0, 2), (1, 2)] + [(2, 2)] * (width - 3) + [(3, 2)]] + [
            [(2, 0), (2, 1)] + [(2, 0)] * (width - 2)]

        return toR

TILESET3 = pygame.image.load("imgs/ocean.png")


class Ocean(Room):
    def __init__(self, room):
        map_data = self.generate_room(room)
        impassible = ((1, 0), )
        super(Ocean, self).__init__(map_data, (TILESET3, impassible), room)

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
