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
        if (self.x + x, self.y + y) == (self.teammate.x, self.teammate.y):
            return False

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

    def step(self, stepper):
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
        """
        # 1,1
        width = 10
        height = 10
        
        self.data = (
            [[Tile.WALL] * width] +
            [[Tile.WALL] + [Tile.OPEN]*(width-2) + [Tile.WALL] for _ in xrange(height-2)] +
            [[Tile.WALL] * width])
        self.data[3][3] = Tile.BLOCK
        self.data[3][5] = Tile.BLOCK
        self.data[5][5] = Tile.BLOCK
        self.data[5][3] = Tile.BLOCK
        self.data[4][4] = Tile.WATER

        self.stuff = {}
        x = Beartrap(self)
        self.stuff[(2,2)] = x
        self.stuff[(2,3)] = Button(self, x)"""

        """
        # 4, 7
        width = 9
        height = 10
        self.data = [[0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,1,0,0,0,0],
                     [0,0,1,2,1,0,0,0,0],
                     [0,0,1,0,1,0,0,0,0],
                     [0,0,1,1,1,1,0,0,0],
                     [0,0,1,0,0,0,0,0,0],
                     [0,5,1,1,1,1,0,0,0],
                     [0,5,1,1,1,1,4,3,0],
                     [0,5,1,1,1,1,0,0,0],
                     [0,0,0,0,0,0,0,0,0]]
        self.stuff = {}"""

        """
        # 4, 17
        self.data = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,1,1,2,1,1,1,1,1,1,1,2,1,0,0,0,0],
                     [0,1,1,1,1,1,1,1,1,2,1,1,1,0,0,0,0],
                     [0,1,1,1,1,2,1,1,1,1,1,1,1,0,0,0,0],
                     [0,1,1,1,2,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,1,2,1,1,1,1,1,1,1,2,1,1,0,0,0,0],
                     [0,1,1,1,1,1,1,1,2,1,1,1,1,1,1,3,0],
                     [0,0,0,0,0,0,5,1,0,0,0,0,0,0,1,1,0],
                     [0,0,0,0,0,0,4,1,4,1,1,1,1,1,1,1,0],
                     [0,0,0,0,0,0,4,1,0,0,0,0,0,0,1,1,0],
                     [0,0,0,0,0,0,4,1,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,4,1,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,4,1,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,4,1,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,4,1,0,0,0,0,0,0,0,0,0],
                     [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
                     [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
                     [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

        self.stuff = {}
        for i, (y,x) in enumerate(((6,2), (2,3), (5,4), (4,5), (7,8), (3,9), (6,10), (2,11))):
            b = Beartrap(self)
            self.stuff[(8+i, 7)] = b
            self.stuff[(y, x)] = Button(self, b)
        b = Beartrap(self)
        self.stuff[(7, 13)] = b
        self.stuff[(10, 14)] = Button(self, b)"""

        """
        # 15, 5
        self.data = map(lambda x: map(lambda y: int(y), x),
                       ["0000000000000000000000000000000",
                        "0002121121211110111111000000000",
                        "0001121122211111111211000000000",
                        "0002221111111110111112000000000",
                        "0001111111111010101111000000000",
                        "0001111111111011101111000000000",
                        "0004050000001000001111000000000",
                        "0114050011101000001111000010000",
                        "0104411010101001421111111111110",
                        "0200411110111001004444444111110",
                        "0100400000000002000444444150000",
                        "0000100000000000004404000000000",
                        "0000000000001000121004000000000",
                        "0000000000001110000001000000000",
                        "0000000000312111111111000000000",
                        "0000000000000000000000000000000"])
        self.stuff = {}

        self.stuff[(5, 14)] = Walltrap(self)
        self.stuff[(5, 16)] = Walltrap(self)
        self.stuff[(3, 14)] = Walltrap(self)
        self.stuff[(3, 16)] = Walltrap(self)
        self.stuff[(4, 16)] = Timetrap(self)
        self.stuff[(7, 26)] = Timetrap(self)
        self.stuff[(11, 4)] = Snorkel(self)

        b = Beartrap(self)  # 1
        self.stuff[(2, 15)] = b
        self.stuff[(9, 15)] = Button(self, b)

        b = Beartrap(self)  # 2
        self.stuff[(14, 12)] = b
        self.stuff[(13, 13)] = Button(self, b)

        for i in xrange(4):
            b = Beartrap(self)  # 3-6
            self.stuff[(8, 22+i)] = b
            self.stuff[(7, 18+i)] = Button(self, b)

        b = Beartrap(self)  # 7
        self.stuff[(14, 16)] = b
        self.stuff[(12, 16)] = Button(self, b)

        b = Beartrap(self)  # 8
        self.stuff[(8, 15)] = b
        self.stuff[(10, 1)] = Button(self, b)"""

        """
        # 5, 1
        self.data = map(lambda x: map(lambda y: int(y), x),
                    ["0000000000000000",
                     "0000110000000000",
                     "0200110000010000",
                     "0111111115114130",
                     "0111111111110000",
                     "0000000100000000",
                     "0000000000000000"])

        self.stuff = {}
        self.stuff[(1, 4)] = Timetrap(self)
        self.stuff[(2, 4)] = Walltrap(self)
        self.stuff[(2, 5)] = Walltrap(self)
        b = Beartrap(self)
        self.stuff[(5, 7)] = b
        self.stuff[(4, 1)] = Button(self, b)
        b = Beartrap(self)
        self.stuff[(2, 11)] = b
        self.stuff[(3, 10)] = Button(self, b)
        """

        """# 5, 10
        self.data = map(lambda x: map(lambda y: int(y), x),
                    ["0000000000000000",
                     "0000000001000000",
                     "0000000001210000",
                     "0000041301110000",
                     "0000010001120000",
                     "0000111011110000",
                     "0010010000011110",
                     "0011161111110020",
                     "0011161111110110",
                     "0011161111110010",
                     "0111111111111000",
                     "0111111111111000",
                     "0110000000000000",
                     "0000000000000000"])

        self.stuff = {}
        b = Beartrap(self)  # 1
        self.stuff[(6, 11)] = b
        self.stuff[(4, 5)] = Button(self, b)

        b = Beartrap(self)  # 2
        self.stuff[(3, 6)] = b
        self.stuff[(5, 6)] = Button(self, b)

        b = Beartrap(self)  # 3
        self.stuff[(5, 4)] = b
        self.stuff[(8, 13)] = Button(self, b)

        b = Beartrap(self)  # 4
        self.stuff[(10, 4)] = b
        self.stuff[(6, 2)] = Button(self, b)

        b = Beartrap(self)  # 5
        self.stuff[(10, 12)] = b
        self.stuff[(6, 12)] = Button(self, b)

        b = Beartrap(self)  # 6
        self.stuff[(10, 6)] = b
        self.stuff[(8, 14)] = Button(self, b)

        self.stuff[(12, 1)] = Walltrap(self)
        self.stuff[(12, 2)] = Walltrap(self)
        """
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
                return False    # teammate in the way
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
