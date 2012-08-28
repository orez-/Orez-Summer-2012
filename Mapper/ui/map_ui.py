import random
import pygame

import ui

SCALE = 4
SCREEN_SLOTS = (50, 50)

COLORS = {(2, 3): ((234, 153, 217), (232, 0, 162)),
          (3, 2): ((181, 230, 29), (34, 177, 76)),
          (2, 2): ((153, 217, 234), (0, 162, 232)),
          (1, 2): ((192, 114, 192), (163, 73, 164)),
          (2, 1): ((44, 86, 255), (63, 72, 204)),
          (1, 1): ((0, 0, 0), (255, 127, 39))}

UP, RIGHT, DOWN, LEFT = [2 ** x for x in xrange(4)]


class RoomDS(object):
    def __init__(self, (x, y), (w, h)):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.paths = set()

    def get_rect(self):
        return (self.x, self.y), (self.w, self.h)

    def add_path(self, (x, y), dr):
        self.paths.add((x, y, dr))

    def paths_iter(self):
        for x, y, dr in self.paths:
            yield (x - self.x, y - self.y, dr)


class MapUI(ui.UI):
    FRAMES = 10

    def __init__(self, main, parent):
        super(MapUI, self).__init__(main, parent)
        self.spacing = 1
        self.surface = pygame.Surface(map(self.scale_coord_width, SCREEN_SLOTS))
        self.surface.fill((0xFF, ) * 3)

        self.size = map(self.scale_coord_width, SCREEN_SLOTS)

        self.map = main.map  # MapDS()
        # self.expand_room()
        self.preload_expansion()

        self.dir = 0
        self.last_dir = 1
        self.frame = MapUI.FRAMES

        self.hilite_loc = map(sum, zip(map(lambda q: (q // (15 * 50)),
            self.parent.slime.center), self.parent.room_data.pos))
        self.dot_counter = 0

    def scale_coord(self, q):
        return int(q * (self.spacing + 1) * SCALE)

    def scale_coord_width(self, q):
        return int((q * (self.spacing + 1) - self.spacing) * SCALE)

    def draw_room(self, (x, y), (w, h)):
        SCALE_ME = self.scale_coord
        SCALE_WIDTH = self.scale_coord_width
        drab, vibr = COLORS[(w, h)]
        px, py = map(SCALE_ME, (x, y))

        self.surface.fill(drab, ((px, py), map(SCALE_WIDTH, (w, h))))
        for vx in xrange(w):
            for vy in xrange(h):
                self.surface.fill(vibr,
                        (map(SCALE_ME, (vx + x, vy + y)), (SCALE, SCALE)))

    def draw_path(self, (x, y), horiz):
        SCALE_ME = self.scale_coord
        SCALE_WIDTH = self.scale_coord_width
        path_color = (0xAA, ) * 3
        if horiz:
            loc = SCALE_ME(x) + SCALE, SCALE_ME(y)
            size = self.spacing * SCALE, SCALE
        else:
            loc = SCALE_ME(x), SCALE_ME(y) + SCALE
            size = SCALE, self.spacing * SCALE
        self.surface.fill(path_color, (loc, size))

    def preload_expansion(self):
        FRAMES = MapUI.FRAMES
        temp_surf = self.surface
        spacing = self.spacing

        self.animation_surfs = []
        for i in xrange(FRAMES + 1):
            self.spacing = (float(i) / FRAMES)
            self.surface = pygame.Surface(self.size)
            self.redraw()
            self.animation_surfs.append(self.surface)

        self.spacing = spacing
        self.surface = temp_surf

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        for room in self.map.all_rooms:
            self.draw_room(*room.get_rect())

        for x, y, horiz in self.map.all_paths:
            self.draw_path((x, y), horiz)

    def reblit(self, surf, time_passed):
        if 0 <= self.frame + self.dir <= MapUI.FRAMES:
            self.frame += self.dir
        else:
            self.dir = 0
        surf.blit(self.animation_surfs[self.frame], (0, 0))

        if self.dot_counter > 25:
            spacing = int(self.frame * SCALE // MapUI.FRAMES)
            pygame.draw.rect(surf, (0xFF, 0, 0),
                (map(lambda q: q * (SCALE + spacing) - spacing // 2,
                    self.hilite_loc),
                (SCALE + spacing, SCALE + spacing)))
        self.dot_counter = (self.dot_counter + 1) % 50

    def screen_size(self):
        return map(self.scale_coord_width, SCREEN_SLOTS)

    def handle_click(self, event):
        self.last_dir *= -1
        self.dir = self.last_dir

    def handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self.main.ui_pop()


class MapDS:
    def __init__(self):
        self.all_rooms = set()
        self.room_map = [[None for x in xrange(SCREEN_SLOTS[0])]
                               for y in xrange(SCREEN_SLOTS[1])]  # 2d list maps coordinates to room_objects
        self.all_paths = set()

        self.expand_room()

    def get_at(self, (x, y)):
        return self.room_map[y][x]

    def can_fit(self, (x, y), (w, h)):
        if not self.in_bounds((x, y), (w, h)):
            return False
        for dx, dy in self.room_iter((x, y), (w, h)):
            if self.get_at((dx, dy)) is not None:
                return False
        return True

    def in_bounds(self, (x, y), (w, h)=(1, 1)):
        return (0 <= x < SCREEN_SLOTS[0] + 1 - w and
                0 <= y < SCREEN_SLOTS[1] + 1 - h)

    def try_fit(self, (x, y), (w, h)):
        """ Some part of this figure must be on (x, y) """
        left_clamp = x
        for left_clamp in xrange(x - 1, x - w, -1):
            if not (self.in_bounds((left_clamp, y)) and not self.get_at((left_clamp, y))):
                left_clamp += 1
                break

        right_clamp = x + 1
        for right_clamp in xrange(x + 1, x + w):
            if not (self.in_bounds((right_clamp, y)) and not self.get_at((right_clamp, y))):
                break
        right_clamp -= w

        top_clamp = y
        for top_clamp in xrange(y - 1, y - h, -1):
            if not (self.in_bounds((x, top_clamp)) and not self.get_at((x, top_clamp))):
                top_clamp += 1
                break

        bot_clamp = y + 1
        for bot_clamp in xrange(y + 1, y + h):
            if not (self.in_bounds((x, bot_clamp)) and not self.get_at((x, bot_clamp))):
                break
        bot_clamp -= h

        possible_spots = self.room_iter((right_clamp, bot_clamp),
            (left_clamp - right_clamp + 1, top_clamp - bot_clamp + 1))

        final_cut = []
        for spot in possible_spots:
            if self.can_fit(spot, (w, h)):
                final_cut.append(spot)

        if not final_cut:
            return None

        return random.choice(final_cut)

    def room_iter(self, (x, y), (w, h)):
        """ Given a rectangular room at location x, y of dimensions w, h,
        generate all the points within the room. """
        for dx in xrange(x, x + w):
            for dy in xrange(y, y + h):
                yield (dx, dy)

    def surround_iter(self, (x, y), (w, h)):
        for dx in xrange(x - 1, x + w + 1):
            if self.in_bounds((dx, y - 1)):
                yield (dx, y - 1)
            if self.in_bounds((dx, y + h)):
                yield (dx, y + h)
        for dy in xrange(y, y + h):
            if self.in_bounds((x - 1, dy)):
                yield (x - 1, dy)
            if self.in_bounds((x + w, dy)):
                yield (x + w, dy)

    def expand_room(self):
        next = {(0, 0): 0}  # coordinate location cannot overlap: direction irrelevant
        while next:
            loc, dr = next.popitem()  # get a random location and direction for a path
            if (not self.in_bounds(loc) or
                    self.get_at(loc) is not None):  # this one isn't valid.
                continue  # or something
            self.add_path(loc, dr)
            options = [(2, 3), (3, 2), (2, 2), (1, 2), (2, 1)]  # all different room sizes
            while 1:
                if not options:  # nothing fit...
                    shape = (1, 1)  # only then can you fill the area
                    self.add_room(loc, shape)
                    break
                shape = random.choice(options)  # pick a random shape
                fit = self.try_fit(loc, shape)  # see if it can fit in that area
                if fit:  # also selects a valid configuration for you.
                    self.add_room(fit, shape)
                    room_locs = set(self.room_iter(fit, shape))  # get each location on the new room

                    dictlist = ({(dx - 1, dy): LEFT, (dx + 1, dy): RIGHT,
                                 (dx, dy - 1): UP, (dx, dy + 1): DOWN}
                                 for dx, dy in room_locs)  # get every direction off of these points (for a path)

                    close_locs = {}
                    for d in dictlist:
                        close_locs.update(d)  # combine each direction into one dic

                    for loc in room_locs:  # close_locs -= room_locs
                        close_locs.pop(loc, None)  # remove yourself from the adjacency

                    next.update(close_locs)  # everything that remains is fair game as a path
                    break
                del options[options.index(shape)]
        self.fill_paths()

    def del_room(self, param):
        try:
            me = self.room_map[param[1]][param[0]]
        except TypeError:  # oops sent the object already
            me = param
        for dx, dy in self.room_iter(self.all_rooms[me]):
            self.room_map[dy][dx] = None
        # probably gotta fix the paths
        self.all_rooms.remove(me)

    def add_room(self, (x, y), (w, h)):
        me = RoomDS((x, y), (w, h))
        self.all_rooms.add(me)
        for dx, dy in self.room_iter((x, y), (w, h)):
            self.room_map[dy][dx] = me

    def add_path(self, (x, y), dr):
        if dr == UP:
            x, y, horiz = x, y, 0
        elif dr == RIGHT:
            x, y, horiz = x - 1, y, 1
        elif dr == DOWN:
            x, y, horiz = x, y - 1, 0
        elif dr == LEFT:
            x, y, horiz = x, y, 1
        else:
            return
        self.all_paths.add((x, y, horiz))

    def fill_paths(self):
        for x, y, horiz in self.all_paths:
            self.get_at((x, y)).add_path((x, y), RIGHT if horiz else DOWN)
            loc = (x + horiz, y + (not horiz))
            self.get_at(loc).add_path(loc, LEFT if horiz else UP)
