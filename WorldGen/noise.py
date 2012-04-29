import random
from math import pi, cos


class Noise:
    def __init__(self, seed):
        self.seed = seed

    def random(self, seed):
        random.seed(self.seed + str(seed))
        return (random.random() * 2) - 1

    def linear_interpolate(self, a, b, x):
        return a * (1 - x) + (b * x)

    def cosine_interpolate(self, a, b, x):
        ft = x * pi
        f = (1 - cos(ft)) * .5
        return self.linear_interpolate(a, b, f)

    def noisy_line(self, (x1, y1), (x2, y2)):
        """ Takes in a line and returns a pointlist of a fuzzier line """
        toR = []
        vector = ((x2 - x1), (y2 - y1))
        dist = ((vector[0] * vector[0]) + (vector[1] * vector[1])) ** .5
        normal = (-vector[1] / dist, vector[0] / dist)    # this is only one of
        # the normals, but this is acceptable as long as it's consitent
        subdivisions = 100
        for d in xrange(subdivisions):
            progress = float(d) / subdivisions
            offset = map(lambda x: x * progress, vector)
            pt = self.perlin_pt(d)
            toR.append((pt * normal[0] + offset[0] + x1,
                        pt * normal[1] + offset[1] + y1))
        return toR

    def perlin_pt(self, x):
        start_amp = 3
        total = 0
        p = .1  # persistence
        n = 4  # number of octaves - 1
        for i in xrange(n):  # for each octave
            freq = 2 ** i
            amp = (p ** i) * start_amp

            bx = x * freq   # i don't know i needed a name
            ix = int(bx)
            fx = bx - ix
            v1 = self.random((i, ix))
            v2 = self.random((i, ix + 1))
            total += self.cosine_interpolate(v1, v2, fx) * amp
        return total
