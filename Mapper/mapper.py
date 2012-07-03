import pygame
import random
SCALE = 1
SCALE_ME = lambda q: q * 2 * SCALE
SCALE_WIDTH = lambda q: (q * 2 - 1) * SCALE
SCREEN_SLOTS = (50, 50)
SCREEN_SIZE = map(SCALE_WIDTH, SCREEN_SLOTS)

COLORS = {(2, 3): ((234, 153, 217), (232, 0, 162)),
          (3, 2): ((181, 230, 29), (34, 177, 76)),
          (2, 2): ((153, 217, 234), (0, 162, 232)),
          (1, 2): ((192, 114, 192), (163, 73, 164)),
          (2, 1): ((112, 146, 190), (63, 72, 204)),
          (1, 1): ((0, 0, 0), (255, 127, 39))}

class MapDS:
    def __init__(self):
        self.all_rooms = {}
        self.room_map = [[None for x in xrange(SCREEN_SLOTS[0])]
                               for y in xrange(SCREEN_SLOTS[1])]

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

    def valid_heights(self, (w, h)):
        pass

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
        for dx in xrange(x, x + w):
            for dy in xrange(y, y + h):
                yield (dx, dy)

    def del_room(self, param):
        try:
            me = self.room_map[param[1]][param[0]]
        except TypeError:  # oops sent the object already
            me = param
        for dx, dy in self.room_iter(self.all_rooms[me]):
            self.room_map[dy][dx] = None
        del self.all_rooms[me]

    def add_room(self, (x, y), (w, h)):
        me = object()
        self.all_rooms[me] = ((x, y), (w, h))
        for dx, dy in self.room_iter((x, y), (w, h)):
            self.room_map[dy][dx] = me

class Main:
    def __init__(self):
        pygame.init()

        d = pygame.display.Info()
        self.desktop_size = (d.current_w, d.current_h)
        self.size = SCREEN_SIZE

        pygame.display.set_caption("Mapper")

        self.done = False
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0xFF, ) * 3)
        self.last = None

        self.clicked = 0

        self.map = MapDS()
        self.expand_room()

    def add_room(self, (x, y), (w, h)):
        self.map.add_room((x, y), (w, h))
        self.draw_room((x, y), (w, h))

    def draw_room(self, (x, y), (w, h)):
        drab, vibr = COLORS[(w, h)]
        px, py = map(SCALE_ME, (x, y))

        self.screen.fill(drab,
            ((px, py), map(SCALE_WIDTH, (w, h))))
        for vx in xrange(w):
            for vy in xrange(h):
                self.screen.fill(vibr, (map(SCALE_ME, (vx + x, vy + y)), (SCALE, SCALE)))

    def expand_room(self, loc=(0, 0)):
        next = set([(0, 0)])
        while next:
            loc = next.pop()
            if (not self.map.in_bounds(loc) or
                    self.map.get_at(loc) is not None):
                continue  # or something
            options = [(2, 3), (3, 2), (2, 2), (1, 2), (2, 1)]
            while 1:
                if not options:
                    shape = (1, 1)
                    self.add_room(loc, shape)
                    break
                shape = random.choice(options)
                fit = self.map.try_fit(loc, shape)
                if fit:
                    self.add_room(fit, shape)
                    room_locs = set(self.map.room_iter(fit, shape))
                    close_locs = set(sum([
                        [(dx-1, dy), (dx+1, dy), (dx, dy-1), (dx, dy+1)]
                        for dx, dy in room_locs], []))
                    next |= close_locs - room_locs
                    break
                del options[options.index(shape)]

    def stop(self):
        self.done = True

    def run(self):
        restart = False
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    pass
                elif event.type == pygame.KEYUP:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                    self.last = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = False
                elif event.type == pygame.MOUSEMOTION:
                    pass

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = Main()
    game.run()
