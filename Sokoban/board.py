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

    @staticmethod
    def get_tile(tile):
        toR = pygame.Surface((Tile.BLOCKSIZE, ) * 2)
        toR.blit(Tile.TILESET, (0, 0),
            (tile * Tile.BLOCKSIZE, 0, Tile.BLOCKSIZE, Tile.BLOCKSIZE))
        return toR


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
    ITEM_TO_ID = None

    def __init__(self, board):
        self.board = board

    def step(self, stepper=None):
        pass

    def unstep(self):
        pass

    def reblit(self, surf, x, y):
        self.draw(surf, x * Tile.BLOCKSIZE, y * Tile.BLOCKSIZE)

    def draw(self, surf, px, py):
        pass

    @staticmethod
    def build_ids():
        TileFeature.ID_TO_ITEM = {
            1:Snorkel,
            2:Button,
            3:Beartrap,
            4:Walltrap,
            5:Timetrap}
        TileFeature.ITEM_TO_ID = {v:k for k,v in TileFeature.ID_TO_ITEM.items()}

    @staticmethod
    def object_to_id(obj):
        return TileFeature.item_to_id(obj.__class__)

    @staticmethod
    def get_items():
        if TileFeature.ITEM_TO_ID is None:
            TileFeature.build_ids()
        return TileFeature.ITEM_TO_ID

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

    def draw(self, surf, x, y):
        surf.blit(self.img, (x, y), (0, 0, Tile.BLOCKSIZE, Tile.BLOCKSIZE))

class Button(TileFeature):
    def __init__(self, board, activates=None):
        super(Button, self).__init__(board)
        self.activates = activates

    def step(self, stepper=None):
        self.activates.activate()

    def unstep(self):
        self.activates.deactivate()

    def draw(self, surf, x, y):
        pygame.draw.circle(surf, (128, 80, 0),
            map(lambda q: q + Tile.BLOCKSIZE/2, (x, y)), 5)

class Beartrap(TileFeature):
    def __init__(self, board):
        super(Beartrap, self).__init__(board)
        self.active = True

    def activate(self):
        self.active = False
        self.board.redraw()

    def deactivate(self):
        self.active = True
        self.board.redraw()

    def draw(self, surf, x, y):
        color = (128, 80, 0)
        if not self.active:
            color = (80, 128, 0)
        pygame.draw.circle(surf, color, map(lambda q: q + Tile.BLOCKSIZE/2, (x, y)), 20)

class Walltrap(TileFeature):
    def step(self, stepper=None):
        for (y,x), w in self.board.stuff.items():
            if w is self:
                del self.board.stuff[(y,x)]
                self.board.data[y][x] = Tile.WALL
                break
        self.board.redraw()

    def draw(self, surf, x, y):
        color = (0x66, ) * 3
        pygame.draw.circle(surf, color, map(lambda q: q + Tile.BLOCKSIZE/2, (x, y)), 20)

class Timetrap(TileFeature):
    def step(self, stepper=None):
        stepper.time_trapped = not stepper.time_trapped

    def draw(self, surf, x, y):
        circ = map(lambda q: q + Tile.BLOCKSIZE/2, (x, y))
        pygame.draw.circle(surf, (0xEF, 0xE4, 0xB0), circ, 20)
        pygame.draw.circle(surf, (0, ) * 3, circ, 20, 1)
        pygame.draw.line(surf, (0, ) * 3, circ, (circ[0] + 10, circ[1]))
        pygame.draw.line(surf, (0, ) * 3, circ, (circ[0], circ[1] - 15))

class TileFeatureDict:
    def __init__(self, stuff={}, (xoff, yoff)=(0, 0)):
        if isinstance(stuff, TileFeatureDict):
            self.stuff = stuff.stuff
            self.xoff = stuff.xoff
            self.yoff = stuff.yoff
        else:
            self.stuff = stuff
            self.xoff = xoff
            self.yoff = yoff

    def normalize(self):
        stuff = {}
        for (y, x), v in self.stuff.items():
            stuff[self.translate((y, x))] = v
        self.stuff = stuff
        self.xoff = 0
        self.yoff = 0

    def shift_offset(self, x=0, y=0):
        self.xoff -= x
        self.yoff -= y

    def reblit(self, surf):
        for (y, x), v in self.stuff.items():
            v.reblit(surf, x + self.xoff, y + self.yoff)

    def translate(self, (y, x)):
        return (self.yoff + y, self.xoff + x)

    def detranslate(self, (y, x)):
        return (y - self.yoff, x - self.xoff)

    def __setitem__(self, (y, x), value):
        self.stuff[self.detranslate((y, x))] = value

    def __getitem__(self, (y, x)):
        return self.stuff[self.translate((y, x))]   # aren't you wrong too?

    def __delitem__(self, (y, x)):
        del self.stuff[self.detranslate((y, x))]

    def __contains__(self, (y, x)):
        return self.detranslate((y, x)) in self.stuff

    def __len__(self):
        return len(self.stuff)

    def items(self):
        return [(self.translate((y, x)), v)
                for (y, x), v in self.stuff.items()]

class Board:
    def __init__(self, tiles=None):
        self.data = tiles

        self.bg = pygame.Surface(SCREEN_SIZE)
        for x in xrange(SCREEN_RADIUS * 2 + 1):
            for y in xrange(SCREEN_RADIUS * 2 + 1):
                Tile.draw_tile(Tile.WALL, self.bg, (x, y))

        self.recreate_surface()

    def add_stuff(self, stuff={}):
        self.stuff = TileFeatureDict(stuff)
        for (y, x), obj in self.stuff.items():
            if isinstance(obj, Button) and self.data[y][x] == Tile.BLOCK:
                obj.step()
        self.redraw()

    def recreate_surface(self):
        width = len(self.data[0])
        height = len(self.data)

        self.surface = pygame.Surface(map(lambda x: x * Tile.BLOCKSIZE, (width, height)))

    def normalize(self):
        #print "\nMap was", self.data
        x_max, y_max, x_min, y_min = [None] * 4
        if self.stuff:
            xs, ys = zip(*[(x, y) for (y, x), _ in self.stuff.items()])
            x_max = max(xs)
            y_max = max(ys)
            x_min = min(xs)
            y_min = min(ys)

        # UP
        for i, row in enumerate(self.data):
            if list(row) != [Tile.WALL] * len(row):
                break
        ycut = i
        if y_min is not None:
            ycut = min(y_min, i)
        self.data = self.data[ycut:]
        self.stuff.shift_offset(y=ycut-1)  # The -1 is for wall_wrap

        #print "After the UPSHIFT:", self.data

        # LEFT
        for i, col in enumerate(zip(*self.data)):
            if list(col) != [Tile.WALL] * len(col):
                break
        xcut = i
        if x_min is not None:
            xcut = min(x_min, i)
        self.data = zip(*zip(*self.data)[xcut:])
        self.stuff.shift_offset(x=xcut-1)

        #print "After the LEFTSHIFT:", self.data

        # DOWN
        for i, row in reversed(list(enumerate(self.data))):
            if list(row) != [Tile.WALL] * len(row):
                break
        cut = i + 1
        if y_max is not None:
            cut = max(y_max, i) + 1
        self.data = self.data[:cut]
        #self.stuff.shift_offset(y=len(self.data) - cut)

        #print "After the DOWNSHIFT:", self.data

        # RIGHT
        for i, col in reversed(list(enumerate(zip(*self.data)))):
            if list(col) != [Tile.WALL] * len(col):
                break
        cut = i + 1
        if x_max is not None:
            cut = max(x_max, i) + 1
        self.data = zip(*zip(*self.data)[:cut])
        #self.stuff.shift_offset(x=len(self.data) - cut)

        #print "After the RIGHTSHIFT:", self.data

        self.wall_wrap()
        self.stuff.normalize()
        return xcut - 1, ycut - 1

    def wall_wrap(self):
        walls = [Tile.WALL] * len(self.data)
        rdata = [walls] + zip(*self.data) + [walls]
        walls = [Tile.WALL] * len(rdata)
        self.data = [walls] + zip(*rdata) + [walls]

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

        self.stuff.reblit(self.surface)
        #for (y,x), v in self.stuff.items():
        #    v.reblit(self.surface, x, y)

    def reblit(self, surface, center):
        surface.blit(self.bg, (0, 0))
        surface.blit(self.surface, map(lambda x: (SCREEN_RADIUS - x) * Tile.BLOCKSIZE, center))
