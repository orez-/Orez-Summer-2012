import pygame
import random

NUM_POINTS_RANGE = (50,100)
PIXEL_SIZE = 4
class Planet:
    def __init__(self, (w,h)):
        self.size = (w,h)
        self.image = pygame.Surface((w,h), pygame.SRCALPHA)
        self.generate_points()
        self.gift_wrap()
        #self.generate_delaunay()
        
        self.triangles = []
        self.redraw()
    
    def generate_points(self):
        self.points = [(random.randint(0,self.size[0]-PIXEL_SIZE), random.randint(0,self.size[1]-PIXEL_SIZE))
                    for _ in xrange(random.randint(*NUM_POINTS_RANGE))]
    
    def generate_delaunay(self):
        triangles = []
        edge = []
        fstpt = self.points[0]
        lstpt = self.points[0]
        self.lines = []
        for px, py in self.points[1:]:
            self.lines.append((fstpt, (px,py)))
            if fstpt != lstpt:
                self.lines.append((lstpt, (px,py)))
            lstpt = (px,py)
    
    def dt_place_point(self, (x,y)):
        Triangle t = self.dt_locate((x,y))
        cavity = self.dt_get_cavity((x,y), t)
        self.dt_update((x,y), cavity)
    
    #def dt_is_outside((x,y), triangle):
        #return on_
    
    def dt_neighbor_opposite(self, (x,y), triangle):
        for neighbor in self.triangles: # TODO: improve me
            if (x,y) not in neighbor:
                return neighbor
        return None
    
    def dt_get_cavity(self, (x,y), triangle):
        encroached = set()
        willcheck = [triangle]
        marked = set([triangle])
        while willcheck:
            t = willcheck.pop(0)
            if 
                continue
            encroached.add(t)
            for 
    
    def dt_locate(self, (x,y)):
        visited = []
        triangle = []
        while triangle != None:
            if triangle in visited: # this should never happen
                print "Locate loop!"
                break;
            visited.add(triangle)
            corner = self.dt_is_outside((x,y), triangle)
            if corner is None:
                return triangle
            triangle = self.dt_neighbor_opposite(corner, triangle)
        # No luck, try brute force
        print "Warning: checking all triangles for",(x,y)
        for tri in self.triangles:
            if self.dt_is_outside((x,y), tri) is None:
                return tri
        print "Warning: No triangle holds",(x,y)
        return None
    
    def on_left(self, ((x1,y1),(x2,y2)), (px,py)):
        return sum([(dx1-dx2)*(dy1+dy2) for (dx1, dy1), (dx2, dy2) in (((x1,y1),(x2,y2)), ((x2,y2),(px,py)), ((px,py),(x1,y1)))]) > 0
    
    def gift_wrap(self):
        points = self.points[:]
        hull_pt = min(self.points, key=lambda x:x[0])   # leftmost
        toR = []
        endpoint = None
        while endpoint is None or endpoint != toR[0]:
            toR.append(hull_pt)
            endpoint = points[0]
            for j in points[1:]:
                if endpoint == hull_pt or self.on_left((hull_pt, endpoint), j):
                    endpoint = j
            hull_pt = endpoint
        self.lines = zip(toR, toR[1:]+[toR[0]])
    
    def redraw(self):
        self.image.fill((0,)*4)
        for px, py in self.points:
            self.image.fill((0xFF,0,0), (px,py,PIXEL_SIZE,PIXEL_SIZE))
        for pt1, pt2 in self.lines:
            pygame.draw.line(self.image, (0,)*3, pt1, pt2, 2)
    
    def blit_params(self):
        return (self.image, (0,0))
    
class Triangle:
    def __init__(self, (x1,y1), (x2,y2), (x3,y3)):
        self.points = [(x1,y1), (x2,y2), (x3,y3)]
        
    def __contains__(self, (x,y)):
        return (x,y) in self.points
