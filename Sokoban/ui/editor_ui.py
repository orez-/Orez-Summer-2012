import pygame

from constants import SCREEN_SIZE, SCREEN_RADIUS
from board import Tile, Board, TileFeature
from ui import UI

TS_SPACER = 10
TS_ACROSS = 3
TS_WIDTH = TS_SPACER * (TS_ACROSS + 1) + Tile.BLOCKSIZE * TS_ACROSS
TS_X = SCREEN_SIZE[0] - TS_WIDTH


class EditorUI(UI):
    def __init__(self, main):
        super(EditorUI, self).__init__(main)
        self.view = [0, 0]
        self.board = Board([[Tile.WALL]])
        self.board.add_stuff()
        self.surface = pygame.Surface(SCREEN_SIZE)

        self.tile_select = TileSelect()
        self.start = None

    def reblit(self, surf):
        self.board.reblit(surf, self.view)
        if self.start is not None:
            self.start.reblit(surf)
        self.tile_select.reblit(surf)

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
        if ex > TS_X:
            click_x = ex - TS_SPACER - TS_X
            select = 0
            if click_x % (Tile.BLOCKSIZE + TS_SPACER) < Tile.BLOCKSIZE:
                select += click_x // (Tile.BLOCKSIZE + TS_SPACER)
                if ey % (Tile.BLOCKSIZE + TS_SPACER) > TS_SPACER:
                    select += (ey // (Tile.BLOCKSIZE + TS_SPACER)) * TS_ACROSS
                    if len(self.tile_select.click_lookup) > select:
                        self.tile_select.selected = self.tile_select.click_lookup[select]
                        print self.tile_select.selected, select
                        return
            self.tile_select.selected = None
        else:
            if self.tile_select.selected is not None:
                x, y = map(lambda q: q // Tile.BLOCKSIZE, self.tile_select.sel_loc)
                x += self.view[0] - SCREEN_RADIUS
                y += self.view[1] - SCREEN_RADIUS
                if self.tile_select.selected[0] == 0:    # tiles
                    self.set_tile((x, y), self.tile_select.selected[1])
                elif self.tile_select.selected[0] == 1:  # stuff
                    if self.start is not None and (self.start.x, self.start.y) == (x, y):
                        self.start = None
                    self.set_feature((x, y), self.tile_select.selected[1])
                    self.tile_select.selected = None
                elif self.tile_select.selected[0] == 2:  # player start
                    self.start = PlayerStart(x, y, self.view)
                    if (y, x) in self.board.stuff:
                        del self.board.stuff[(y, x)]
                        self.board.redraw()
                    self.tile_select.selected = None

    def resize_board(self, x, y):
        resized = False
        if x < 0:  # need more columns
            for i, row in enumerate(self.board.data):
                self.board.data[i] = [Tile.WALL for _ in xrange(-x)] + row
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
        x, y = self.resize_board(x, y)
        self.board.stuff[(y, x)] = feature_class(self.board)
        self.board.redraw()

    def set_tile(self, (x, y), tile):
        x, y = self.resize_board(x, y)
        self.board.data[y][x] = tile
        self.board.redraw()

    def scroll(self, x=0, y=0):
        self.view[0] += x
        self.view[1] += y

    def handle_key(self, event):
        if event.key == pygame.K_UP:
            self.scroll(y=-1)
        if event.key == pygame.K_DOWN:
            self.scroll(y=1)
        if event.key == pygame.K_RIGHT:
            self.scroll(x=1)
        if event.key == pygame.K_LEFT:
            self.scroll(x=-1)
        if (event.key == pygame.K_s and
                pygame.key.get_mods() | pygame.KMOD_CTRL):
            if self.start is not None:
                self.main.change_screen("save", board=self.board,
                    start=self.start)
            else:  # let them know they need a start zone.
                pass


class PlayerStart(TileFeature):
    img = pygame.image.load("imgs/us.png")
    def __init__(self, x, y, view):
        self.x = x
        self.y = y
        self.view = view

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

        skip = TS_ACROSS - (i % TS_ACROSS)
        print skip
        self.click_lookup += [None] * (skip - 1)

        for i, obj in enumerate((TileFeature.get_items()), i + skip):
            s = pygame.Surface((Tile.BLOCKSIZE, ) * 2, pygame.SRCALPHA)
            obj(None).draw(s, 0, 0)
            self.click_lookup.append((1, obj, s))
            self.set_tile(s, i)

        img = PlayerStart.img
        self.click_lookup.append((2, None, img))
        self.set_tile(img, i + 1)

    def set_tile(self, img, i):
        self.tile_surface.blit(img,
                map(lambda x: TS_SPACER + (TS_SPACER + Tile.BLOCKSIZE) * x, 
                ((i % TS_ACROSS), (i // TS_ACROSS))))

    def reblit(self, surf):
        if self.sel_loc is not None and self.selected is not None:
            surf.blit(self.selected[2], self.sel_loc)
        surf.blit(self.back_surface, (TS_X, 0))
        surf.blit(self.tile_surface, (TS_X, 0))
