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


class Player(object):
    us_pic = pygame.image.load("imgs/us.png")

    def __init__(self, board, (x, y), me, teammate=None):
        self.x = x
        self.y = y
        lookup = ["me", "you"]
        self.player2 = teammate is not None
        self.me = me
        self.pic = pygame.image.load("imgs/" + lookup[int(self.player2)] + ".png")
        self.board = board
        self.teammate = teammate
        if self.teammate is not None:
            self.teammate.teammate = self

        self.time_trapped = False
        self.snorkel = False
        self.ice_dir = None

    def _set_pos(self, (x, y)):
        self.x = x
        self.y = y

    pos = property(lambda self: (self.x, self.y), _set_pos)

    def reblit(self, screen, center):
        if self.board.data[self.y][self.x] == Tile.ICE and self.ice_dir is not None:
            print "\nGonna slide from", self.x, self.y
            if self.board.can_move(self, self.ice_dir):
                self.x, self.y = self.x + self.ice_dir[0], self.y + self.ice_dir[1]
                print "sliding", self.x, self.y
            else:
                self.ice_dir = None
        loc = map(lambda (x, y):
            (y - x + SCREEN_RADIUS) * Tile.BLOCKSIZE,
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
            return True
        return False


class TileFeature(object):
    ID_TO_ITEM = None
    ITEM_TO_ID = None
    CAN_LINK = []

    def __init__(self, board, pos=None):
        assert(board is not None or pos is None)
        self.board = board
        self.pos = None if pos is None else tuple(pos)
        self.linkee = None
        self.linked = None

    def step(self, stepper=None):
        pass

    def unstep(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def on_linked(self):
        pass

    def on_linkee(self):
        pass

    def reblit(self, surf, pos=None):
        x, y = pos or self.pos
        self.draw(surf, x * Tile.BLOCKSIZE, y * Tile.BLOCKSIZE)

    def draw(self, surf, px, py):
        pass

    def set_linked(self, linked):
        dirty = set([self])
        if self.linked is not None:  # if the button has a beartrap
            #dirty.add(self.linked)
            self.linked.linkee = None  # the old beartrap has no button
            self.linked.on_linkee()
        self.linked = linked  # the button has a new beartrap
        if linked.linkee is not None:  # if the new beartrap has a button
            dirty.add(linked.linkee)
            linked.linkee.linked = None  # the new beartrap's old button has no beartrap
            linked.linkee.on_linked()
        linked.linkee = self  # the new beartrap's button is me!
        self.on_linked()
        linked.on_linkee()
        return dirty

    @staticmethod
    def build_ids():
        TileFeature.ID_TO_ITEM = {
            1: Snorkel,
            2: Button,
            3: Beartrap,
            4: Walltrap,
            5: Timetrap,
            6: Helptrap,
            7: LaunchSpring,
            8: LaunchTarget}
        TileFeature.ITEM_TO_ID = {v: k for k, v in
            TileFeature.ID_TO_ITEM.items()}

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
    def __init__(self, board, xy=None):
        super(Snorkel, self).__init__(board, xy)
        self.img = pygame.image.load("imgs/tools.png")

    def step(self, stepper=None):
        if stepper is not None:
            x, y = self.pos
            del self.board.stuff[(y, x)]
            self.board.dirty.add((x, y))
            stepper.snorkel = True

    def draw(self, surf, x, y):
        surf.blit(self.img, (x, y), (0, 0, Tile.BLOCKSIZE, Tile.BLOCKSIZE))


class LaunchTarget(TileFeature):
    def __init__(self, board, xy=None):
        super(LaunchTarget, self).__init__(board, xy)
        self.img = pygame.image.load("imgs/target.png")
        self.open = True

    def step(self, stepper=None):
        self.open = False

    def unstep(self):
        self.open = True

    def draw(self, surf, x, y):
        surf.blit(self.img, (x, y))


class LaunchSpring(TileFeature):
    CAN_LINK = [LaunchTarget]

    def __init__(self, board, xy=None, activates=None):
        super(LaunchSpring, self).__init__(board, xy)
        self.img = pygame.image.load("imgs/spring.png")
        self.launch_me = None
        if activates is not None:
            self.set_linked(activates)

    def step(self, stepper=None):
        if stepper is None:
            self.launch_me = Tile.BLOCK
        else:
            self.launch_me = stepper

    def unstep(self):
        self.launch_me = None

    def activate(self):
        if self.launch_me is not None and self.linked.open:  # gonna launch something
            tx, ty = self.linked.pos
            if self.launch_me == Tile.BLOCK:  # launching a block
                x, y = self.pos
                self.board.set_tile((x, y), Tile.OPEN)
                self.board.set_tile((tx, ty), Tile.BLOCK)
            elif self.launch_me is not None:
                self.launch_me.x, self.launch_me.y = tx, ty
            self.linked.step()
            self.launch_me = None

    def draw(self, surf, x, y):
        surf.blit(self.img, (x, y))


class Beartrap(TileFeature):
    def __init__(self, board, xy=None):
        super(Beartrap, self).__init__(board, xy)
        self._active = True

    def _set_active(self, value):
        if value != self._active:
            self._active = value
            if self.pos:
                self.board.dirty.add(self.pos)
            else:
                print "no board"

    active = property(lambda self: self._active, _set_active)

    def activate(self):
        self.active = False

    def deactivate(self):
        self.active = True

    def draw(self, surf, x, y):
        color = (128, 80, 0)
        if not self.active:
            color = (80, 128, 0)
        pygame.draw.circle(surf, color, map(lambda q: q + Tile.BLOCKSIZE / 2, (x, y)), 20)


class Button(TileFeature):
    CAN_LINK = [Beartrap, LaunchSpring]

    def __init__(self, board, xy=None, activates=None):
        super(Button, self).__init__(board, xy)
        self.color = (0xCC, ) * 3
        if activates is not None:
            self.set_linked(activates)

    def set_color(self, connector):
        colors = {Beartrap: (128, 80, 0),
                  LaunchSpring: (255, 247, 0),
                  None: (0xCC, 0xCC, 0xCC)
                 }
        if connector not in colors:
            connector = connector.__class__
        self.color = colors[connector]

    def step(self, stepper=None):
        if self.linked is not None:
            self.linked.activate()

    def unstep(self):
        if self.linked is not None:
            self.linked.deactivate()

    def on_linked(self):
        self.set_color(self.linked)

    def draw(self, surf, x, y):
        pygame.draw.circle(surf, self.color,
            map(lambda q: q + Tile.BLOCKSIZE / 2, (x, y)), 5)
        pygame.draw.circle(surf, (0, ) * 3,
            map(lambda q: q + Tile.BLOCKSIZE / 2, (x, y)), 5, 1)


class Walltrap(TileFeature):
    def step(self, stepper=None):
        x, y = self.pos
        del self.board.stuff[(y, x)]
        self.board.set_tile((x, y), Tile.WALL)

    def draw(self, surf, x, y):
        color = (0x66, ) * 3
        pygame.draw.circle(surf, color, map(lambda q: q + Tile.BLOCKSIZE / 2, (x, y)), 20)


class Timetrap(TileFeature):
    def step(self, stepper=None):
        if stepper is not None:
            stepper.time_trapped = not stepper.time_trapped

    def draw(self, surf, x, y):
        circ = map(lambda q: q + Tile.BLOCKSIZE / 2, (x, y))
        pygame.draw.circle(surf, (0xEF, 0xE4, 0xB0), circ, 20)
        pygame.draw.circle(surf, (0, ) * 3, circ, 20, 1)
        pygame.draw.line(surf, (0, ) * 3, circ, (circ[0] + 10, circ[1]))
        pygame.draw.line(surf, (0, ) * 3, circ, (circ[0], circ[1] - 15))


class Helptrap(TileFeature):
    def __init__(self, board, xy=None, text="--default--"):
        super(Helptrap, self).__init__(board, xy)
        self.text = str(text)

    def step(self, stepper=None):
        if stepper is not None and stepper.me:
            if self.board.client is not None:
                self.board.client.send("HELP " + str(int(stepper.player2)) +
                    " " + self.text)

    def draw(self, surf, x, y):
        circ = map(lambda q: q + Tile.BLOCKSIZE / 2, (x, y))
        pygame.draw.circle(surf, (0xFF, 0xD7, 0x00), circ, 20)
        pygame.draw.circle(surf, (0, ) * 3, circ, 20, 2)
        surf.blit(pygame.font.Font(None, 40).render("?", True, (0, ) * 3), (x + 16, y + 12))


class TileFeatureDict(object):
    def __init__(self, stuff={}, (xoff, yoff)=(0, 0)):
        self.show_numbers = False
        self.font = pygame.font.Font(None, 24)
        self.nums = []  # buttons
        if isinstance(stuff, TileFeatureDict):
            self.show_numbers = stuff.show_numbers
            self.stuff = {k: v for k, v in stuff.items()}
            self.xoff = stuff.xoff
            self.yoff = stuff.yoff
            self.nums = stuff.nums[:]
        else:
            self.stuff = {k: v for k, v in stuff.iteritems()}
            self.xoff = xoff
            self.yoff = yoff

    def normalize(self):
        stuff = {}  # let's not do it in-place to avoid stepping on any toes
        for (y, x), v in self.stuff.items():
            y, x = self.translate((y, x))
            stuff[(y, x)] = v
            v.pos = (x, y)
        self.stuff = stuff
        self.xoff = 0
        self.yoff = 0

    def shift_offset(self, x=0, y=0):
        self.xoff -= x
        self.yoff -= y

    def remove_nums(self, dirty):
        for d in dirty:
            if d in self.nums:
                self.nums[self.nums.index(d)] = None

    def update_nums(self, dirty):
        self.remove_nums(dirty)
        for d in dirty:
            if d.linked is not None:
                self.add_to_nums(d)

    def add_to_nums(self, thing):
        if None in self.nums:
            i = self.nums.index(None)
            self.nums[i] = thing
        else:
            self.nums.append(thing)

    def reblit_item(self, surf, (x, y), v):
        v.reblit(surf, reversed(self.translate((y, x))))
        if self.show_numbers:
            if v.linked and (v in self.nums):
                i = self.nums.index(v)
                surf.blit(self.font.render(str(i), True, (0x41, 0x69, 0xE1)),
                    map(lambda q: q * Tile.BLOCKSIZE, (x + self.xoff, y + self.yoff)))
            if v.linkee and (v.linkee in self.nums):
                i = self.nums.index(v.linkee)
                surf.blit(self.font.render(str(i), True, (0x41, 0x69, 0xE1)),
                    (Tile.BLOCKSIZE * (x + self.xoff),
                     Tile.BLOCKSIZE * (y + self.yoff) + 35))

    def reblit(self, surf):
        for (y, x), v in self.stuff.items():
            self.reblit_item(surf, (x, y), v)

    def translate(self, (y, x)):
        return (self.yoff + y, self.xoff + x)

    def detranslate(self, (y, x)):
        return (y - self.yoff, x - self.xoff)

    def __setitem__(self, (y, x), value):
        self.stuff[self.detranslate((y, x))] = value
        #self.nums.append(value)

    def __getitem__(self, (y, x)):
        return self.stuff[self.detranslate((y, x))]

    def __delitem__(self, (y, x)):
        key = self.detranslate((y, x))
        del self.stuff[key]

    def __contains__(self, (y, x)):
        return self.detranslate((y, x)) in self.stuff

    def __len__(self):
        return len(self.stuff)

    def items(self):
        return [(self.translate((y, x)), v)
                for (y, x), v in self.stuff.items()]

    def __str__(self):
        count = {}
        for v in self.stuff.itervalues():
            v = v.__class__.__name__
            if v not in count:
                count[v] = 0
            count[v] += 1
        toR = ', '.join([str(v) + " " + k + "s" for k, v in count.items()])
        toR += " (" + ("N" if self.show_numbers else "No n") + "umbers shown, "
        toR += "roughly " + str(len(self.nums)) + " connections"
        if not (self.xoff == self.yoff == 0):
            toR += ", offset:" + str(tuple(map(str, (self.xoff, self.yoff))))
        return toR + ")"

    def clear(self):
        self.nums = []
        self.stuff = {}
        self.xoff, self.yoff = 0, 0
        # you probably want a full redraw after this

    def clone(self, board):
        toR = {}  # my new data
        updater = {}  # old_items -> new_items
        for (y, x), v in self.items():
            toR[(y, x)] = v.__class__(board, (x, y))  # make a new one
            toR[(y, x)].__dict__.update(v.__dict__)  # make it identical
            toR[(y, x)].board = board  # it needs the new board
            updater[v] = toR[(y, x)]  # and the updater needs to bookkeep
        for v in toR.itervalues():
            if v.linked is not None:  # update all the linkeds
                updater[v.linked].linkee = v
                v.linked = updater[v.linked]
        tfd = TileFeatureDict(toR)
        tfd.show_numbers = True
        return tfd


class Board:
    def __init__(self, tiles=None):
        self.data = tiles

        self.bg = pygame.Surface(SCREEN_SIZE)   # Background of walls
        for x in xrange(SCREEN_RADIUS * 2 + 1):
            for y in xrange(SCREEN_RADIUS * 2 + 1):
                Tile.draw_tile(Tile.WALL, self.bg, (x, y))

        self.dirty = set()
        self.recreate_surface()

    def add_stuff(self, stuff={}):
        self.stuff = TileFeatureDict(stuff)
        for (y, x), obj in self.stuff.items():
            if isinstance(obj, Button) and self.data[y][x] == Tile.BLOCK:
                obj.step()
        self.full_redraw()

    def add_client(self, client):
        self.client = client

    def set_tile(self, (x, y), tile):
        self.dirty.add((x, y))
        self.data[y][x] = tile

    def recreate_surface(self):
        width = len(self.data[0])
        height = len(self.data)

        self.surface = pygame.Surface(map(lambda x: x * Tile.BLOCKSIZE, (width, height)))

    def normalize(self):
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
        self.stuff.shift_offset(y=ycut - 1)  # The -1 is for wall_wrap

        #print "After the UPSHIFT:", self.data

        # LEFT
        for i, col in enumerate(zip(*self.data)):
            if list(col) != [Tile.WALL] * len(col):
                break
        xcut = i
        if x_min is not None:
            xcut = min(x_min, i)
        self.data = zip(*zip(*self.data)[xcut:])
        self.stuff.shift_offset(x=xcut - 1)

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
        self.data = map(list, self.data)  # zip makes tuples: unacceptable
        self.stuff.normalize()
        self.recreate_surface()
        self.full_redraw()
        return xcut - 1, ycut - 1

    def wall_wrap(self):
        walls = [Tile.WALL] * len(self.data)
        rdata = [walls] + zip(*self.data) + [walls]
        walls = [Tile.WALL] * len(rdata)
        self.data = [walls] + zip(*rdata) + [walls]

    def move_player(self, who, (dx, dy)):
        tile_type = self.data[who.y][who.x]
        if tile_type == Tile.ICE and who.ice_dir is not None:
            return False
        x = self.can_move(who, (dx, dy))
        if x is True:
            if who.time_trapped:
                if ((who.y + dy, who.x + dx) in self.stuff and
                    isinstance(self.stuff[(who.y + dy, who.x + dx)], Beartrap)
                    and self.stuff[(who.y + dy, who.x + dx)].active):
                    return False
                return self.pull_block(who, (dx, dy))
            return True
        elif x is False:
            return False
        elif x is Tile.BLOCK:
            if who.time_trapped:
                return False
            return self.push_block(who, (dx, dy))

    def can_move(self, who, (dx, dy)):
        # What you're moving towards
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
                self.set_tile((bx, by), Tile.OPEN)
                self.set_tile((who.x, who.y), Tile.BLOCK)
                if (by, bx) in self.stuff:
                    self.stuff[(by, bx)].unstep()
        return True

    def push_block(self, who, (dx, dy)):
        """ Assumes you're moving into a block (that is, not called frivolously)"""
        x, y = who.x + dx, who.y + dy
        if (y, x) in self.stuff:
            if isinstance(self.stuff[(y, x)], Beartrap) and self.stuff[(y, x)].active:
                return False
        if (y + dy, x + dx) in self.stuff:
            if isinstance(self.stuff[(y + dy, x + dx)], Walltrap):
                return False
        if self.data[y + dy][x + dx] == Tile.OPEN:
            if (who.teammate.x, who.teammate.y) == (x + dx, y + dy):
                return False    # teammate in the way of the block
            self.set_tile((x + dx, y + dy), Tile.BLOCK)
            self.set_tile((x, y), Tile.OPEN)
            if (y + dy, x + dx) in self.stuff:
                self.stuff[(y + dy, x + dx)].step()
            return True
        if self.data[y + dy][x + dx] == Tile.WATER:
            if (who.teammate.x, who.teammate.y) == (x + dx, y + dy):
                return False    # teammate in the way (snorkel logic!)
            self.set_tile((x + dx, y + dy), Tile.OPEN)  # maybe dirt someday
            self.set_tile((x, y), Tile.OPEN)
            return True
        return False

    def full_redraw(self):
        for y, row in enumerate(self.data):
            for x, elem in enumerate(row):
                Tile.draw_tile(elem, self.surface, (x, y))

        self.stuff.reblit(self.surface)

    def redraw(self):
        if self.dirty:
            for x, y in self.dirty:
                Tile.draw_tile(self.data[y][x], self.surface, (x, y))
                if (y, x) in self.stuff:
                    self.stuff.reblit_item(self.surface,
                            (x - self.stuff.xoff, y - self.stuff.yoff),
                            self.stuff[(y, x)])
            self.dirty.clear()

    def reblit(self, surface, center):
        self.redraw()
        surface.blit(self.bg, (0, 0))
        surface.blit(self.surface, map(lambda x: (SCREEN_RADIUS - x) * Tile.BLOCKSIZE, center))

    def clone(self):
        toR = Board([x[:] for x in self.data])
        toR.add_stuff(self.stuff.clone(toR))
        return toR
