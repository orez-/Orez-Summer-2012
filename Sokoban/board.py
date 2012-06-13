import pygame

from constants import SCREEN_SIZE, SCREEN_RADIUS, TILE_SIZE


class Tile:
    WALL = 0
    OPEN = 1
    BLOCK = 2
    EXIT = 3

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
    def __init__(self, board, teammate=None):
        self.x = 1
        self.y = 1
        lookup = ["me", "you"]
        self.pic = pygame.image.load("imgs/"+lookup[int(teammate is not None)]+".png")
        self.board = board
        self.teammate = teammate
        if self.teammate is not None:
            self.teammate.teammate = self

    def reblit(self, screen, center):
        screen.blit(self.pic, map(lambda (x,y):
            (y-x+SCREEN_RADIUS) * Tile.BLOCKSIZE,
            zip(center, (self.x, self.y))))

    def move(self, x=0, y=0):
        deactivate = None
        if (self.x + x, self.y + y) == (self.teammate.x, self.teammate.y):
            return False

        if (self.y, self.x) in self.board.stuff:
            deactivate = self.board.stuff[(self.y, self.x)]
            if isinstance(deactivate, Beartrap) and deactivate.active:
                return False

        newx = self.x + x
        newy = self.y + y
        if self.board.push_block(self, (x, y)):
            if deactivate is not None:
                deactivate.unstep()

            self.x, self.y = newx, newy

            if (newy, newx) in self.board.stuff:
                stepped = self.board.stuff[(newy, newx)]
                stepped.step()

class Button:
    def __init__(self, board, activates):
        self.board = board
        self.activates = activates

    def step(self):
        #print "Stepped on a button"
        self.activates.activate()

    def unstep(self):
        #print "Got off the button"
        self.activates.deactivate()

    def reblit(self, surf, x, y):
        pygame.draw.circle(surf, (128, 80, 0),
            (int((x + .5) * Tile.BLOCKSIZE), int((y + .5) * Tile.BLOCKSIZE)), 5)

class Beartrap:
    def __init__(self, board):
        self.board = board
        self.active = True

    def step(self):
        #print "stepped on a beartrap"
        pass

    def unstep(self):
        #print "got off a beartrap"
        pass

    def activate(self):
        self.active = False
        self.board.redraw()

    def deactivate(self):
        self.active = True
        self.board.redraw()

    def reblit(self, surf, x, y):
        color = (128, 80, 0)
        if not self.active:
            color = (80, 128, 0)
        pygame.draw.circle(surf, color, (int((x + .5) * Tile.BLOCKSIZE), int((y + .5) * Tile.BLOCKSIZE)), 20)

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

        self.stuff = {}
        x = Beartrap(self)
        self.stuff[(2,2)] = x
        self.stuff[(2,3)] = Button(self, x)
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.redraw()

    def push_block(self, who, (dx, dy)):
        x, y = who.x + dx, who.y + dy
        tile_type = self.data[y][x]
        if tile_type == Tile.WALL:
            return False
        elif tile_type == Tile.OPEN:
            return True
        elif tile_type == Tile.BLOCK:
            if (y, x) in self.stuff:
                if isinstance(self.stuff[(y,x)], Beartrap) and self.stuff[(y,x)].active:
                    return False
            if self.data[y+dy][x+dx] == Tile.OPEN:
                if (who.teammate.x, who.teammate.y) == (x+dx, y+dy):
                    return False    # teammate in the way
                self.data[y+dy][x+dx] = Tile.BLOCK
                self.data[y][x] = Tile.OPEN
                if (y+dy,x+dx) in self.stuff:
                    self.stuff[(y+dy,x+dx)].step()
                self.redraw()
                return True
            return False

    def redraw(self):
        for y, row in enumerate(self.data):
            for x, elem in enumerate(row):
                Tile.draw_tile(elem, self.surface, (x, y))

        for (y,x), v in self.stuff.items():
            v.reblit(self.surface, x, y)

    def reblit(self, surface, center):
        surface.blit(self.surface, map(lambda x: (SCREEN_RADIUS - x) * TILE_SIZE, center))
