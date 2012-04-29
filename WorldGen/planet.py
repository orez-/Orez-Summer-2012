import pygame
import random
from math import sin, cos, pi

from noise import Noise

POINTS_RADIUS = 200
NUM_POINTS_RANGE = (50, 100)
PIXEL_SIZE = 4


class Planet:
    def __init__(self, (w, h)):
        self.size = (w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.points = []
        self.lines = []
        self.polygons = []
        self.squiggles = []
        self.generate_points()
        #self.gift_wrap(self.points)
        self.concentric_polygons()
        self.redraw()

    def complement(self, points):
        return filter(lambda x: x not in points, self.points)

    def random_point(self):
        t = 2 * pi * random.random()
        u = random.random() + random.random()   # buh?
        r = 2 - u if u > 1 else u
        return (r * cos(t) * POINTS_RADIUS + self.size[0] / 2,
                r * sin(t) * POINTS_RADIUS + self.size[1] / 2)

    def generate_points(self):
        self.points = [self.random_point()
            for _ in xrange(random.randint(*NUM_POINTS_RANGE))]

    def on_left(self, ((x1, y1), (x2, y2)), (px, py)):
        return sum([(dx1 - dx2) * (dy1 + dy2) for (dx1, dy1), (dx2, dy2) in
                    (((x1, y1), (x2, y2)),
                     ((x2, y2), (px, py)),
                     ((px, py), (x1, y1)))]) > 0

    def concentric_polygons(self):
        comp = set(self.points)
        while comp:
            comp.difference_update(self.gift_wrap(list(comp)))

    def polypoints(self, points):
        return zip(points, points[1:] + [points[0]])

    def gift_wrap(self, points):
        np = len(points)
        if np <= 2:         # too few points to wrap
            if np == 2:
                self.lines += [tuple(points)]
            return points
        hull_pt = min(points, key=lambda x: x[0])   # leftmost point
        toR = []            # the points we're wrapping on
        endpoint = None     # the final point
        while endpoint is None or endpoint != toR[0]:
            toR.append(hull_pt)
            endpoint = points[0]
            for j in points[1:]:
                if endpoint == hull_pt or self.on_left((hull_pt, endpoint), j):
                    endpoint = j
            hull_pt = endpoint

        n = Noise("butts")
        self.squiggles += [n.noisy_line(c1, c2) for c1, c2 in
                            self.polypoints(toR)]
        self.polygons.append(toR)
        return toR

    def redraw(self, lines=True, points=True):
        self.image.fill((0, ) * 4)  # clear the screen
        if points:
            for px, py in self.points:
                self.image.fill((0xFF, 0, 0),
                    (px - PIXEL_SIZE / 2, py - PIXEL_SIZE / 2,
                     PIXEL_SIZE, PIXEL_SIZE))
        if lines:
            #for pt1, pt2 in self.lines:
            #    pygame.draw.line(self.image, (0, ) * 3, pt1, pt2, 2)
            #for polygon in self.polygons:
            #    pygame.draw.polygon(self.image, (0, )*3, polygon, 2)
            for x in self.squiggles:
                pygame.draw.lines(self.image, (0, ) * 3, False, x, 1)

    def blit_params(self):
        return (self.image, (0, 0))
