import pygame

from constants import SCREEN_SIZE


class Tile:
    WALL = 0
    OPEN = 1
    BLOCK = 2

    BLOCKSIZE = 50

    TILESET = pygame.image.load("imgs/tileset.png")

    def __init__(self):
        raise TypeError("The Tile type cannot be instantiated.")

    @staticmethod
    def draw_tile(tile, surf, (x, y)):
        surf.blit(Tile.TILESET, (x * Tile.BLOCKSIZE, y * Tile.BLOCKSIZE),
            (tile * Tile.BLOCKSIZE, 0, (tile + 1) * Tile.BLOCKSIZE,
            Tile.BLOCKSIZE))


class Player:
    def __init__(self, board):
        self.x = 1
        self.y = 1
        self.pic = pygame.image.load("imgs/me.png")
        self.board = board

    def reblit(self, screen):
        screen.blit(self.pic, map(lambda x: x * Tile.BLOCKSIZE, (self.x, self.y)))

    def move(self, x=0, y=0):
        newx = self.x + x
        newy = self.y + y
        if self.board.push_block((newx, newy), (x, y)):
            self.x, self.y = newx, newy


class Board:
    def __init__(self):
        self.width = 10
        self.height = 10
        
        self.data = (
            [[Tile.WALL] * self.width] +
            [[Tile.WALL] + [Tile.OPEN]*(self.width-2) + [Tile.WALL] for _ in xrange(self.height-2)] +
            [[Tile.WALL] * self.width])
        self.data[3][3] = Tile.BLOCK
        self.data[3][5] = Tile.BLOCK
        self.data[5][5] = Tile.BLOCK
        self.data[5][3] = Tile.BLOCK

        self.surface = pygame.Surface(SCREEN_SIZE)
        self.redraw()

    def push_block(self, (x, y), (dx, dy)):
        tile_type = self.data[y][x]
        if tile_type == Tile.WALL:
            return False
        elif tile_type == Tile.OPEN:
            return True
        elif tile_type == Tile.BLOCK:
            if self.data[y+dy][x+dx] == Tile.OPEN:
                self.data[y+dy][x+dx] = Tile.BLOCK
                self.data[y][x] = Tile.OPEN
                self.redraw()
                return True
            return False

    def redraw(self):
        for y, row in enumerate(self.data):
            for x, elem in enumerate(row):
                Tile.draw_tile(elem, self.surface, (x, y))

    def reblit(self, surface):
        surface.blit(self.surface, (0, 0))