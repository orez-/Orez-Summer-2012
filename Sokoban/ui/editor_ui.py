import pygame

from constants import SCREEN_SIZE, SCREEN_RADIUS
from board import Tile, Board, TileFeature
from ui import UI

TS_SPACER = 10
TS_ACROSS = 3
TS_WIDTH = TS_SPACER * (TS_ACROSS + 1) + Tile.BLOCKSIZE * TS_ACROSS
TS_X = SCREEN_SIZE[0] - TS_WIDTH

RECT_CURVE = min(Tile.BLOCKSIZE / 2, 15)
HILITE_COLOR = (0xFF, 0xFF, 0x00, 0x40)


class EditorUI(UI):
    def __init__(self, main, parent):
        super(EditorUI, self).__init__(main, parent)
        self.view = [0, 0]
        self.board = Board([[Tile.WALL]])
        self.board.add_stuff()
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.highlight_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        self.tile_select = TileSelect()
        self.start = None

        self.select_rect = None
        self.move_select = MoveChunk()

    def reblit(self, surf, hide_side=False):
        self.board.reblit(surf, self.view)
        if self.start is not None:
            self.start.reblit(surf)

        self.redraw_highlight()
        surf.blit(self.highlight_surface, (0, 0))

        self.move_select.reblit(surf)

        if not hide_side:
            self.tile_select.reblit(surf)

    def redraw_highlight(self):
        self.highlight_surface.fill((0, ) * 4)
        if self.select_rect is not None:
            (x_min, y_min), (x_max, y_max) = self.fix_rect(self.select_rect)

            self.draw_curved_highlight((x_min, y_min), (x_max, y_max))

            #self.highlight_surface.fill(HILITE_COLOR,
            #    map(lambda q: map(lambda r: r * Tile.BLOCKSIZE, q),
            #    ((x_min, y_min), (x_max, y_max))))

    def draw_curved_highlight(self, (x_min, y_min), (x_max, y_max)):
        px_min, py_min = map(lambda q: q * Tile.BLOCKSIZE + RECT_CURVE, (x_min, y_min))
        px_max, py_max = map(lambda q: (q + 1) * Tile.BLOCKSIZE - RECT_CURVE, (x_max, y_max))

        for x, y in ((px_min, py_min), (px_max, py_min),
                (px_min, py_max), (px_max, py_max)):
            pygame.draw.circle(self.highlight_surface, HILITE_COLOR,
                (x, y), RECT_CURVE)

        x_max -= x_min - 1
        y_max -= y_min - 1

        self.highlight_surface.fill(HILITE_COLOR,
            ((x_min * Tile.BLOCKSIZE + RECT_CURVE, y_min * Tile.BLOCKSIZE),
             (x_max * Tile.BLOCKSIZE - RECT_CURVE * 2, y_max * Tile.BLOCKSIZE)))
        self.highlight_surface.fill(HILITE_COLOR,
            ((x_min * Tile.BLOCKSIZE, y_min * Tile.BLOCKSIZE + RECT_CURVE),
             (x_max * Tile.BLOCKSIZE, y_max * Tile.BLOCKSIZE - RECT_CURVE * 2)))

    @staticmethod
    def grid_coords(x, y):
        return map(lambda q: q // Tile.BLOCKSIZE * Tile.BLOCKSIZE, (x, y))

    def handle_motion(self, event):
        ex, ey = event.pos
        if ex < TS_X:
            self.tile_select.sel_loc = self.grid_coords(ex, ey)
        else:
            self.tile_select.sel_loc = None

    def handle_click(self, event):
        ex, ey = event.pos
        if ex > TS_X:   # stuff-bar
            click_x = ex - TS_SPACER - TS_X
            select = 0
            self.select_rect = None
            self.redraw_highlight()
            if click_x % (Tile.BLOCKSIZE + TS_SPACER) < Tile.BLOCKSIZE:
                select += click_x // (Tile.BLOCKSIZE + TS_SPACER)
                if ey % (Tile.BLOCKSIZE + TS_SPACER) > TS_SPACER:
                    select += (ey // (Tile.BLOCKSIZE + TS_SPACER)) * TS_ACROSS
                    if len(self.tile_select.click_lookup) > select:
                        self.tile_select.selected = None
                        if self.tile_select.click_lookup[select] is not None:
                            self.tile_select.selected = self.tile_select.click_lookup[select][:]
                        print self.tile_select.selected, select
                        return
            self.tile_select.selected = None
        else:   # map proper
            if self.select_rect is not None:
                ax, ay = self.get_click_abs_coord((ex, ey))
                (x1, y1), (x2, y2) = self.fix_rect(self.select_rect)
                if x1 <= ax <= x2 and y1 <= ay <= y2:
                    self.move_select.set_chunk(((x1, y1), (x2, y2)), (ax, ay), self)
                    return
                else:
                    self.select_rect = [[ax, ay], [ax, ay]]
            self.set_something(ex, ey)  # hey

    def get_click_abs_coord(self, (ex, ey)):
        return map(lambda q: q // Tile.BLOCKSIZE, (ex, ey))

    def get_click_board_coord(self, (ex, ey), skip=False):  # pixels -> coords
        x, y = ex, ey
        if not skip:
            x, y = self.get_click_abs_coord((ex, ey))
        return map(sum, zip((x - SCREEN_RADIUS, y - SCREEN_RADIUS), self.view))

    @staticmethod
    def fix_rect(rect):
        transpose = zip(*rect)
        x_min, y_min = map(min, transpose)
        x_max, y_max = map(max, transpose)
        return [[x_min, y_min], [x_max, y_max]]

    def set_something(self, ex, ey):
        if self.tile_select.sel_loc is None:
            return
        x, y = self.get_click_board_coord(self.tile_select.sel_loc)
        if self.tile_select.selected is not None:
            if self.tile_select.selected[0] == 0:    # tiles
                self.set_tile((x, y), self.tile_select.selected[1])
            elif self.tile_select.selected[0] == 1:  # stuff
                self.set_feature((x, y), self.tile_select.selected[1])
                self.tile_select.selected = None
            elif self.tile_select.selected[0] == 2:  # player start
                print x, y
                self.set_start((x, y))
                self.tile_select.selected = None
            elif self.tile_select.selected[0] == 3:  # connector tool
                if (y, x) not in self.board.stuff:
                    self.tile_select.selected = None
                    print "There's nothing there."
                    return
                item1 = self.board.stuff[(y, x)]
                if self.tile_select.selected[1] is None:  # haven't connected
                    self.tile_select.selected[1] = item1
                    print "Connected to a", item1
                else:   # one connection in place
                    item2 = self.tile_select.selected[1]
                    if item2.__class__ in item1.CAN_LINK:
                        item1, item2 = item2, item1
                    elif item1.__class__ not in item2.CAN_LINK:
                        print "Man you can't link those things."
                        self.tile_select.selected = None
                        return
                    # item2 can link to item1
                    dirty = item2.set_linked(item1)
                    self.board.stuff.update_nums(dirty)
                    self.tile_select.selected = None
                    self.board.redraw()
                    print "Linked a", item2, "to a", item1

        #else:
        #    if self.select_rect is None:
        #        self.select_rect = [[x, y]]

    def handle_click_up(self, event):
        if self.move_select.active():  # put it down!
            self.move_select.release(self)

    def handle_drag(self, event):
        self.handle_motion(event)

        if self.tile_select.sel_loc is None:
            return False
        x, y = self.get_click_abs_coord(self.tile_select.sel_loc)
        if (self.tile_select.selected is None and self.select_rect is None and
                not self.move_select.active()):
            self.select_rect = [[x, y], [x, y]]  # not placing and no rect
        else:
            if self.move_select.active():
                self.move_select.move_to((x, y))
                return
            if self.select_rect is not None:  # uh
                self.select_rect[1] = [x, y]
                return
            x, y = self.get_click_board_coord(self.tile_select.sel_loc)
            try:
                if (y >= 0 and x >= 0 and
                        self.board.data[y][x] == self.tile_select.selected[1]):
                    return False
            except IndexError:
                pass
            self.set_something(*event.pos)
        return True

    def resize_board(self, x, y):
        """ We're placing a new item at (x, y): do we need to
        stretch the board? """
        resized = False
        if x < 0:  # need more columns
            for i, row in enumerate(self.board.data):
                self.board.data[i] = [Tile.WALL for _ in xrange(-x)] + list(row)
            self.board.stuff.shift_offset(x=x)  # all of our features are off
            self.scroll(x=-x)
            if self.start is not None:
                self.start.x -= x
            x = 0
            resized = True

        if y < 0:  # need more rows
            wid = len(self.board.data[0])
            self.board.data = [[Tile.WALL for _ in xrange(wid)]
                          for _ in xrange(-y)] + self.board.data
            self.board.stuff.shift_offset(y=y)  # all of our features are off
            self.scroll(y=-y)
            if self.start is not None:
                self.start.y -= y
            y = 0
            resized = True

        ydiff = y - len(self.board.data) + 1
        if ydiff > 0:
            wid = len(self.board.data[0])
            self.board.data += [[Tile.WALL for _ in xrange(wid)] for _ in xrange(ydiff)]
            resized = True

        xdiff = x - len(self.board.data[0]) + 1
        if xdiff > 0:
            for i, row in enumerate(self.board.data):
                self.board.data[i] += [Tile.WALL for _ in xrange(xdiff)]
            resized = True

        if resized:
            self.board.recreate_surface()
        return (x, y)

    def set_feature(self, (x, y), feature_class):
        feature = feature_class
        if feature_class.__class__ == type:  # if you're actually a class
            feature = feature_class(self.board)  # make one of me
        x, y = self.resize_board(x, y)
        if self.start is not None and (x, y) == (self.start.x, self.start.y):
            self.start = None
        if (y, x) in self.board.stuff:
            dirty = set()
            d = self.board.stuff[(y, x)]
            if d.linked is not None:
                dirty.add(d)
            if d.linkee is not None:
                dirty.add(d.linkee)
            self.board.stuff.remove_nums(dirty)
        self.board.stuff[(y, x)] = feature
        self.board.redraw()

    def set_tile(self, (x, y), tile):
        x, y = self.resize_board(x, y)
        self.board.data[y][x] = tile
        self.board.redraw()

    def set_start(self, (x, y)):
        self.start = PlayerStart(x, y, self.view)
        if (y, x) in self.board.stuff:
            dirty = set()
            d = self.board.stuff[(y, x)]
            if d.linked is not None: 
                dirty.add(d)
            if d.linkee is not None:
                dirty.add(d.linkee)
            self.board.stuff.remove_nums(dirty)
            del self.board.stuff[(y, x)]
            self.board.redraw()

    def get_tile(self, (x, y)):
        if x < 0 or y < 0:
            return Tile.WALL
        try:
            return self.board.data[y][x]
        except IndexError:
            return Tile.WALL

    def scroll(self, x=0, y=0):
        self.view[0] += x
        self.view[1] += y
        if self.select_rect is not None:
            self.select_rect[0] = map(sum, zip(self.select_rect[0], (-x, -y)))
            self.redraw_highlight()

    def handle_key(self, event):
        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
            if event.key == pygame.K_UP:
                self.scroll(y=-1)
            if event.key == pygame.K_DOWN:
                self.scroll(y=1)
            if event.key == pygame.K_RIGHT:
                self.scroll(x=1)
            if event.key == pygame.K_LEFT:
                self.scroll(x=-1)
            if self.main.clicked and self.tile_select.selected is not None:
                self.set_tile(self.get_click_board_coord(self.tile_select.sel_loc),
                    self.tile_select.selected[1])

        if event.key == pygame.K_ESCAPE:
            self.main.ui_back()

        if (event.key == pygame.K_s and
                pygame.key.get_mods() | pygame.KMOD_CTRL):
            if self.start is not None:
                self.main.change_screen("save", board=self.board,
                    start=self.start)
            else:  # let them know they need a start zone.
                print "You must have a startpoint on the board before you can save."

    def on_reentry(self, save):
        self.scroll(-save.dx, -save.dy)


class PlayerStart(TileFeature):
    img = pygame.image.load("imgs/us.png")
    def __init__(self, x, y, view):
        self.x = x
        self.y = y
        self.view = view  # this is a reference. Do not overwrite!

    def reblit(self, surf):
        super(PlayerStart, self).reblit(surf, self.x, self.y)

    def draw(self, surf, x, y):
        surf.blit(PlayerStart.img, map(lambda (q1, q2):
            (q1 - (q2 - SCREEN_RADIUS) * Tile.BLOCKSIZE), zip((x, y), self.view)))


class TileSelect:
    def __init__(self):
        self.back_surface = pygame.Surface((TS_WIDTH, SCREEN_SIZE[1]))
        self.back_surface.fill((0, ) * 3)
        self.back_surface.set_alpha(192)

        self.click_lookup = []
        self.selected = None
        self.sel_loc = None

        self.tile_surface = pygame.Surface((TS_WIDTH, SCREEN_SIZE[1]), pygame.SRCALPHA)
        for i, tile in enumerate((Tile.WALL, Tile.OPEN, Tile.BLOCK, Tile.EXIT,
                                  Tile.WATER, Tile.GRAVEL, Tile.ICE)):
            t_img = Tile.get_tile(tile)
            self.click_lookup.append((0, tile, t_img))
            self.set_tile(t_img, i)

        skip, clicks = self.skip_line(i)
        self.click_lookup += clicks

        for i, obj in enumerate((TileFeature.get_items()), i + skip):
            s = pygame.Surface((Tile.BLOCKSIZE, ) * 2, pygame.SRCALPHA)
            obj(None).draw(s, 0, 0)
            self.click_lookup.append((1, obj, s))
            self.set_tile(s, i)

        skip, clicks = self.skip_line(i)
        self.click_lookup += clicks

        img = PlayerStart.img
        self.click_lookup.append((2, None, img))
        self.set_tile(img, i + 1)

        img = pygame.image.load("imgs/connector.png")
        self.click_lookup.append([3, None, img])
        self.set_tile(img, i + 2)

    def skip_line(self, i):
        skip = TS_ACROSS - (i % TS_ACROSS)
        return skip, [None] * (skip - 1)

    def set_tile(self, img, i):
        self.tile_surface.blit(img,
                map(lambda x: TS_SPACER + (TS_SPACER + Tile.BLOCKSIZE) * x, 
                ((i % TS_ACROSS), (i // TS_ACROSS))))

    def reblit(self, surf):
        if self.sel_loc is not None and self.selected is not None:
            surf.blit(self.selected[2], self.sel_loc)
        surf.blit(self.back_surface, (TS_X, 0))
        surf.blit(self.tile_surface, (TS_X, 0))


class MoveChunk:
    """ The selected bit that we've selected and are moving around.
    It's complex enough to warrant its own data structure :( """
    def __init__(self):
        self.move_rect = None
        self.move_surf = None
        self.move_data = None
        self.move_stuff = None
        self.move_start = None

        self._juggler = pygame.Surface(SCREEN_SIZE)

    def active(self):
        return self.move_rect is not None

    def reblit(self, surf):
        if self.active():
            surf.blit(self.move_surf, map(sum, zip(*self.move_rect)))

    def set_chunk(self, ((x1, y1), (x2, y2)), (ax, ay), editor):
        bx, by = editor.get_click_board_coord((x1, y1), True)
        w, h = (x2 - x1 + 1, y2 - y1 + 1)
        px, py = map(lambda q: q * Tile.BLOCKSIZE, (x1, y1))
        pw, ph = map(lambda q: q * Tile.BLOCKSIZE, (w, h))
        self.move_surf = pygame.Surface((pw, ph))
        editor.reblit(self._juggler, True)
        self.move_surf.blit(self._juggler, (0, 0), ((px, py), (pw, ph)))
        self.move_rect = [[ax * Tile.BLOCKSIZE, ay * Tile.BLOCKSIZE],
            map(lambda q: q * Tile.BLOCKSIZE, [x1 - ax, y1 - ay])]
        editor.select_rect = None
        self.move_data = [[editor.get_tile((x, y)) for x in xrange(bx, bx + w)]
                for y in xrange(by, by + h)]

        self.move_stuff = {}
        for (y, x), v in editor.board.stuff.items():
            fx, fy = x - bx, y - by
            if 0 <= fx < w and 0 <= fy < h:  # in bounds
                self.move_stuff[(fy, fx)] = v
                del editor.board.stuff[(y, x)]

        if editor.start is not None:
            sx, sy = editor.start.x - bx, editor.start.y - by
            if 0 <= sx < w and 0 <= sy < h:
                self.move_start = (sx, sy)
                editor.start = None

        if True:  # IF YOU WANT TO DELETE THE OLD TILES
            editor.resize_board(bx, by)
            bx = max(bx, 0)
            by = max(by, 0)
            for y in xrange(by, by + h):
                for x in xrange(bx, bx + w):
                    editor.set_tile((x, y), Tile.WALL)

    def move_to(self, (x, y)):
        self.move_rect[0] = map(lambda q: q * Tile.BLOCKSIZE, (x, y))

    def release(self, editor):
        x, y = editor.get_click_abs_coord(editor.tile_select.sel_loc)  # uh oh
        bx, by = editor.get_click_board_coord(editor.tile_select.sel_loc)
        bx += self.move_rect[1][0] // Tile.BLOCKSIZE
        by += self.move_rect[1][1] // Tile.BLOCKSIZE
        editor.resize_board(bx, by)
        bx, by = map(lambda q: max(0, q), (bx, by))
        for r, row in enumerate(self.move_data):
            for c, elem in enumerate(row):
                editor.set_tile((c + bx, r + by), elem)

        if self.move_start is not None:
            editor.set_start((self.move_start[0] + bx, self.move_start[1] + by))
            self.move_start = None

        for (y, x), v in self.move_stuff.items():
            editor.set_feature((x + bx, y + by), v)
        self.move_rect = None
        self.move_data = None
        self.move_surf = None
        self.move_stuff = None
