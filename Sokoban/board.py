import pygame

from constants import SCREEN_SIZE, SCREEN_RADIUS


class Tile:
    WALL = 0
    OPEN = 1
    BLOCK = 2
    EXIT = 3
    WATER = 4
    GRAVEL = 5
    ICE = 6

    BLOCKSIZE = 50

    TILESET = pygame.image.load("imgs/tileset.png")

    def __init__(self):
        raise TypeError("The Tile type cannot be instantiated.")

    @staticmethod
    def draw_tile(tile, surf, (x, y)):
        surf.blit(Tile.TILESET, (x * Tile.BLOCKSIZE, y * Tile.BLOCKSIZE),
            (tile * Tile.BLOCKSIZE, 0, Tile.BLOCKSIZE,
            Tile.BLOCKSIZE))


class Player:
    us_pic = pygame.image.load("imgs/us.png")
    def __init__(self, board, (x, y), teammate=None):
        self.x = x
        self.y = y
        lookup = ["me", "you"]
        self.pic = pygame.image.load("imgs/"+lookup[int(teammate is not None)]+".png")
        self.board = board
        self.teammate = teammate
        if self.teammate is not None:
            self.teammate.teammate = self

        self.time_trapped = False
        self.snorkel = False
        self.ice_dir = None

    def reblit(self, screen, center):
        if self.board.data[self.y][self.x] == Tile.ICE:
            self.x, self.y = self.x + self.ice_dir[0], self.y + self.ice_dir[1]
        loc = map(lambda (x,y):
            (y-x+SCREEN_RADIUS) * Tile.BLOCKSIZE,
            zip(center, (self.x, self.y)))
        if (self.teammate.x, self.teammate.y) == (self.x, self.y):
            screen.blit(Player.us_pic, loc)
        else:
            num = (self.time_trapped + self.snorkel * 2 +
                (self.board.data[self.y][self.x] == Tile.WATER) * 4) * Tile.BLOCKSIZE
            section = (num, 0, Tile.BLOCKSIZE, Tile.BLOCKSIZE)
            screen.blit(self.pic, loc, section)

    def move(self, x=0, y=0):
        deactivate = None

        if (self.y, self.x) in self.board.stuff:
            deactivate = self.board.stuff[(self.y, self.x)]
            if not self.time_trapped and isinstance(deactivate, Beartrap) and deactivate.active:
                return False

        newx = self.x + x
        newy = self.y + y
        if self.board.move_player(self, (x, y)):
            if deactivate is not None and self.board.data[self.y][self.x] != Tile.BLOCK:
                deactivate.unstep()

            self.x, self.y = newx, newy

            if (newy, newx) in self.board.stuff:
                stepped = self.board.stuff[(newy, newx)]
                stepped.step(self)

class TileFeature(object):
    ID_TO_ITEM = None

    def __init__(self, board):
        self.board = board

    def step(self, stepper=None):
        pass

    def unstep(self):
        pass

    def reblit(self, surf, x, y):
        pass

    @staticmethod
    def build_ids():
        TileFeature.ID_TO_ITEM = {
            1:Snorkel,
            2:Button,
            3:Beartrap,
            4:Walltrap,
            5:Timetrap}
        ITEM_TO_ID = {v:k for k,v in TileFeature.ID_TO_ITEM.items()}

    @staticmethod
    def id_to_item(idd):
        if TileFeature.ID_TO_ITEM is None:
            TileFeature.build_ids()
        return TileFeature.ID_TO_ITEM[idd]

    @staticmethod
    def item_to_id(item):
        if TileFeature.ID_TO_ITEM is None:
            TileFeature.build_ids()
        return TileFeature.ITEM_TO_ID[item]


class Snorkel(TileFeature):
    def __init__(self, board):
        super(Snorkel, self).__init__(board)
        self.img = pygame.image.load("imgs/tools.png")

    def step(self, stepper=None):
        if stepper is not None:
            for (y,x), w in self.board.stuff.items():
                if w is self:
                    del self.board.stuff[(y, x)]
                    self.board.redraw()
                    break
            stepper.snorkel = True

    def reblit(self, surf, x, y):
        surf.blit(self.img, (x * Tile.BLOCKSIZE, y * Tile.BLOCKSIZE),
            (0, 0, Tile.BLOCKSIZE, Tile.BLOCKSIZE))

class Button(TileFeature):
    def __init__(self, board, activates):
        self.board = board
        self.activates = activates

    def step(self, stepper=None):
        #print "Stepped on a button"
        self.activates.activate()

    def unstep(self):
        #print "Got off the button"
        self.activates.deactivate()

    def reblit(self, surf, x, y):
        pygame.draw.circle(surf, (128, 80, 0),
            (int((x + .5) * Tile.BLOCKSIZE), int((y + .5) * Tile.BLOCKSIZE)), 5)

class Beartrap(TileFeature):
    def __init__(self, board):
        self.board = board
        self.active = True

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

class Walltrap(TileFeature):
    def __init__(self, board):
        self.board = board

    def step(self, stepper=None):
        for (y,x), w in self.board.stuff.items():
            if w is self:
                del self.board.stuff[(y,x)]
                self.board.data[y][x] = Tile.WALL
                break
        self.board.redraw()

    def reblit(self, surf, x, y):
        color = (0x66, ) * 3
        pygame.draw.circle(surf, color, (int((x + .5) * Tile.BLOCKSIZE), int((y + .5) * Tile.BLOCKSIZE)), 20)

class Timetrap(TileFeature):
    def __init__(self, board):
        self.board = board

    def step(self, stepper=None):
        stepper.time_trapped = not stepper.time_trapped

    def reblit(self, surf, x, y):
        circ = (int((x + .5) * Tile.BLOCKSIZE), int((y + .5) * Tile.BLOCKSIZE))
        pygame.draw.circle(surf, (0xEF, 0xE4, 0xB0), circ, 20)
        pygame.draw.circle(surf, (0, ) * 3, circ, 20, 1)
        pygame.draw.line(surf, (0, ) * 3, circ, (circ[0] + 10, circ[1]))
        pygame.draw.line(surf, (0, ) * 3, circ, (circ[0], circ[1] - 15))

class Board:
    def __init__(self, tiles=None):
        self.data = tiles

        width = len(self.data[0])
        height = len(self.data)

        self.surface = pygame.Surface(map(lambda x: x * Tile.BLOCKSIZE, (width, height)))

    def add_stuff(self, stuff):
        self.stuff = stuff
        for (y,x), obj in self.stuff.items():
            if isinstance(obj, Button) and self.data[y][x] == Tile.BLOCK:
                obj.step()
        self.redraw()

    def move_player(self, who, (dx, dy)):
        x = self.can_move(who, (dx, dy))
        if x is True:
            if who.time_trapped:
                if ((who.y+dy, who.x+dx) in self.stuff and
                    isinstance(self.stuff[(who.y+dy, who.x+dx)], Beartrap) and
                    self.stuff[(who.y+dy, who.x+dx)].active):
                    return False
                return self.pull_block(who, (dx, dy))
            return True
        if x is False:
            return False
        if x is Tile.BLOCK:
            if who.time_trapped:
                return False
            return self.push_block(who, (dx, dy))

    def can_move(self, who, (dx, dy)):
        x, y = who.x + dx, who.y + dy
        tile_type = self.data[y][x]
        if (x, y) == (who.teammate.x, who.teammate.y):
            return tile_type == Tile.EXIT

        if tile_type == Tile.WALL:
            return False
        elif tile_type == Tile.WATER:
            return who.snorkel
        elif tile_type in (Tile.OPEN, Tile.GRAVEL):
            return True
        elif tile_type == Tile.BLOCK:
            return Tile.BLOCK
        elif tile_type == Tile.ICE:
            who.ice_dir = (dx, dy)
            return True
        elif tile_type == Tile.EXIT:
            return True

    def pull_block(self, who, (dx, dy)):
        """ Can be used at any time """
        x, y = who.x + dx, who.y + dy
        bx, by = who.x - dx, who.y - dy
        if self.data[by][bx] == Tile.BLOCK:
            if self.data[who.y][who.x] != Tile.GRAVEL:
                self.data[by][bx] = Tile.OPEN
                self.data[who.y][who.x] = Tile.BLOCK
                if (by, bx) in self.stuff:
                    self.stuff[(by, bx)].unstep()
                self.redraw()
        return True

    def push_block(self, who, (dx, dy)):
        """ Assumes you're moving into a block (that is, not called frivolously)"""
        x, y = who.x + dx, who.y + dy
        if (y, x) in self.stuff:
            if isinstance(self.stuff[(y,x)], Beartrap) and self.stuff[(y,x)].active:
                return False
        if (y+dy, x+dx) in self.stuff:
            if isinstance(self.stuff[(y+dy, x+dx)], Walltrap):
                return False
        if self.data[y+dy][x+dx] == Tile.OPEN:
            if (who.teammate.x, who.teammate.y) == (x+dx, y+dy):
                return False    # teammate in the way of the block
            self.data[y+dy][x+dx] = Tile.BLOCK
            self.data[y][x] = Tile.OPEN
            if (y+dy,x+dx) in self.stuff:
                self.stuff[(y+dy,x+dx)].step()
            self.redraw()
            return True
        if self.data[y+dy][x+dx] == Tile.WATER:
            if (who.teammate.x, who.teammate.y) == (x+dx, y+dy):
                return False    # teammate in the way (snorkel logic!)
            self.data[y+dy][x+dx] = Tile.OPEN   # maybe dirt someday
            self.data[y][x] = Tile.OPEN
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
        surface.blit(self.surface, map(lambda x: (SCREEN_RADIUS - x) * Tile.BLOCKSIZE, center))
