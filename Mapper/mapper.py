import pygame
import random
SCALE = 5
SCALE_ME = lambda q: q * 2 * SCALE
SCALE_WIDTH = lambda q: (q * 2 - 1) * SCALE
SCREEN_SLOTS = (50, 50)
SCREEN_SIZE = map(SCALE_WIDTH, SCREEN_SLOTS)

COLORS = {(2, 3): ((136, 0, 21), (237, 28, 36)),
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

    def in_bounds(self, (x, y), (w, h)):
        return (0 <= x < SCREEN_SLOTS[0] + 1 - w and
                0 <= y < SCREEN_SLOTS[1] + 1 - h)

    def valid_heights(self, (w, h)):
        pass

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
        """self.draw_room((0, 0), (2, 3))
        self.add_room((1, 3), (2, 2))
        self.add_room((2, 0), (3, 2))
        self.add_room((1, 5), (2, 1))
        self.add_room((3, 2), (1, 2))
        self.add_room((3, 4), (1, 2))
        self.add_room((4, 2), (2, 1))
        self.add_room((4, 3), (2, 3))
        self.add_room((2, 2), (1, 1))"""
        next = set([(0, 0)])
        while next:
            loc = next.pop()
            if not self.map.in_bounds(loc, (1, 1)) or self.map.get_at(loc) is not None:
                continue  # or something
            options = [(2, 3), (3, 2), (2, 2), (1, 2), (2, 1)]
            while 1:
                if not options:
                    shape = (1, 1)
                    self.add_room(loc, shape)
                    break
                shape = random.choice(options)
                if self.map.can_fit(loc, shape):
                    self.add_room(loc, shape)
                    room_locs = set(self.map.room_iter(loc, shape))
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
