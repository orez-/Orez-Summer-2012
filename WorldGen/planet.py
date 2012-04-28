import pygame
import random

X_RANGE = (100,500)
Y_RANGE = (100,500)
NUM_POINTS_RANGE = (50,100)
PIXEL_SIZE = 4
class Planet:
    def __init__(self, (w,h)):
        self.size = (w,h)
        self.image = pygame.Surface((w,h), pygame.SRCALPHA)
        self.generate_points()
        self.lines = []
        comp = set(self.points[:])
        while comp:
            comp.difference_update(self.gift_wrap(list(comp)))
        self.redraw()
    
    def complement(self, points):
        return filter(lambda x:x not in points, self.points)
    
    def generate_points(self):
        self.points = [(random.randint(*X_RANGE), random.randint(*Y_RANGE))
                    for _ in xrange(random.randint(*NUM_POINTS_RANGE))]
    
    def on_left(self, ((x1,y1),(x2,y2)), (px,py)):
        return sum([(dx1-dx2)*(dy1+dy2) for (dx1, dy1), (dx2, dy2) in (((x1,y1),(x2,y2)), ((x2,y2),(px,py)), ((px,py),(x1,y1)))]) > 0
    
    def polypoints(self, points):
        return zip(points, points[1:]+[points[0]])
    
    def gift_wrap(self, points):
        np = len(points)
        if np <= 2: # too few points to wrap
            if np == 2:
                self.lines += [tuple(points)]
            return points
        hull_pt = min(points, key=lambda x:x[0])   # leftmost point
        toR = []    # the points we're wrapping on
        endpoint = None # the final point
        while endpoint is None or endpoint != toR[0]:
            toR.append(hull_pt)
            endpoint = points[0]
            for j in points[1:]:
                if endpoint == hull_pt or self.on_left((hull_pt, endpoint), j):
                    endpoint = j
            hull_pt = endpoint
        self.lines += self.polypoints(toR)
        return toR
    
    def redraw(self):
        self.image.fill((0,)*4) # clear the screen
        for px, py in self.points:
            self.image.fill((0xFF,0,0), (px-PIXEL_SIZE/2,py-PIXEL_SIZE/2,PIXEL_SIZE,PIXEL_SIZE))
        for pt1, pt2 in self.lines:
            pygame.draw.line(self.image, (0,)*3, pt1, pt2, 2)
    
    def blit_params(self):
        return (self.image, (0,0))
