import pygame
import random
import sys
from string import lowercase as alphabet
from math import cos, sin, pi

try:
    seed = int(sys.argv[1])
except:
    seed = random.randint(0, 2 ** 32 - 1)
random.seed(seed)
print seed

vowel = "aeiou"
consonant = ''.join(filter(lambda x: x not in vowel, alphabet))
SKILL_RADIUS = 12
DNA_RADIUS = 70
DNA_STEP = 50
DNA_TWIST = pi / 8

"""
UP, RIGHT, DOWN, LEFT, IN = (2 ** i for i in xrange(5))
data = {"One": {"next": {UP:"Two"}, "pos":(50, 50)},
        "Two": {"next": {LEFT|IN: "One"}, "pos":(200, 200)}}
"""

def random_word(length=8):
    toR = random.choice(consonant)
    while len(toR) < length:
        toR += random.choice(vowel)
        eh = random.randint(1, 3)
        if eh == 1:
            toR += random.choice(vowel)
        toR += random.choice(consonant)
        if eh == 3:
            toR += toR[-1]
    return toR[:length].title()

def arc(surface, color, rect, start_angle, end_angle, width):
    while start_angle > end_angle:
        end_angle += 2 * pi
    pygame.draw.arc(surface, color, rect, -end_angle, -start_angle, width)

class SkillHelix:
    def __init__(self):
        self.moving = 0
        self.cur_y = 0
        self.viewangle = 0
        names = list(set(random_word() for _ in xrange(20)))
        self.skills = {n: {"next": [] if i % 2 else names[i + 1: i + 3], "color": tuple(random.randint(0, 0xFF) for _ in xrange(3))} for i, n in enumerate(names)}
        self.orbsurface = pygame.Surface((1000, 500), pygame.SRCALPHA)  # size might be wrong
        self.linesurface = pygame.Surface((1000, 500))
        self.init_skills(names[0])
        self.redraw()

    def keep_moving(self):
        if self.moving:
            if int(self.cur_y) != int(self.cur_y + self.moving) or self.cur_y * (self.cur_y + self.moving) <= 0:
                self.cur_y = int(round(self.cur_y+self.moving))
                self.moving = 0
            else:
                self.cur_y += self.moving
            self.redraw()

    def set_viewangle(self, degrees):
        self.viewangle = degrees * pi / 180
        self.redraw()

    def move(self, direction):
        if abs(direction) != 1:
            raise ValueError("Directional values only")
        self.moving = direction * .125
        self.cur_y += self.moving

    def init_skills(self, job, pos=(-1, 0)):
        self.skills[job]["pos"] = pos
        self.skills[job]["angle"] = (DNA_TWIST * pos[1]) % (2 * pi)
        self.skills[job]["done"] = True

        up = False
        for next in self.skills[job]["next"]:
            self.init_skills(next, (pos[0] * (up * 2 - 1), pos[1] + up))
            up = True

    def draw_orb(self, orb):
        for color, wid in ((orb["color"], 0), ((0, ) * 3, 2)):
            if orb["done"]:
                orb["curpos"] = map(int, (orb["pos"][0] * DNA_RADIUS * cos(orb["angle"] - (DNA_TWIST * self.cur_y) % (2 * pi)) + 500,
                    sin(self.viewangle) * orb["pos"][0] * DNA_RADIUS * sin(orb["angle"] - (DNA_TWIST * self.cur_y) % (2 * pi)) + 250 + cos(self.viewangle) * (orb["pos"][1] - self.cur_y) * DNA_STEP))
                #(orb["pos"][1]-self.cur_y)*DNA_STEP+250))
                #_y = cy+Math.sin(angle+mod-Math.PI/2-fullstep)*spinradius*Math.sin(viewangle) + cz*Math.cos(viewangle);
                pygame.draw.circle(self.orbsurface, color, orb["curpos"], SKILL_RADIUS, wid)

    def redraw(self):
        self.linesurface.fill((0xFF, )*3)
        self.orbsurface.fill((0, )*4)
        for skill in self.skills:
            self.draw_orb(self.skills[skill])
        for skill in self.skills:
            for next in self.skills[skill]["next"]:
                pygame.draw.line(self.linesurface, (0, ) * 3 ,
                    self.skills[skill]["curpos"],
                    self.skills[next]["curpos"], 2)

    def reblit(self, screen):
        screen.blit(self.linesurface, (0,0))
        screen.blit(self.orbsurface, (0,0))


class SkillWeb:
    def __init__(self):
        self.view_pos = [0,0]
        self.orbsurface = pygame.Surface((1000, 500), pygame.SRCALPHA)  # size might be wrong
        self.linesurface = pygame.Surface((1000, 500))
        self.linesurface.fill((0xFF, ) * 3)
        
        self.skills = {}
        names = list(set(random_word() for _ in xrange(20)))
        self.job = names[0]
        for name in names:
            self.skills[name] = {"next":[random.choice(names[len(self.skills):]) for x in xrange(int(random.randint(4,8)/4))] if len(self.skills)-len(names) else [],
                "color":(random.randint(0,255), random.randint(0,255), random.randint(0,255)),
                "done":False}
        self.init_skills(self.job)
        self.redraw()

    def circle_radius(self, circle_num):
        return SKILL_RADIUS * circle_num * 5

    def init_skills(self, job, circle=0, last_angle=None, direction=None):
        if not self.skills[job]["done"]:
            if last_angle is None:
                last_angle = random.randint(0, 7)
            if direction is None:
                direction = random.randint(0, 1) * 2 - 1
            self.skills[job].update({
                "circle":circle,
                "angle":last_angle,
                "pos":(int(cos(pi * last_angle / 4) * self.circle_radius(circle)) + 500,
                       int(sin(pi * last_angle / 4) * self.circle_radius(circle)) + 250),
                "done":True
            })
            for next in self.skills[job]["next"]:
                maybe_angle = (last_angle + direction + 8) % 8
                if not circle or filter(lambda x:x[1]["done"] and x[1]["circle"] == circle and x[1]["angle"] == maybe_angle, self.skills.items()):
                    pos = self.init_skills(next, circle+1, last_angle, random.randint(0,1) * 2 - 1)[0]
                    pygame.draw.line(self.linesurface, (0, ) * 3, self.skills[job]["pos"], pos, 2)
                else:
                    pos, ang = self.init_skills(next, circle, maybe_angle, direction)
                    r = self.circle_radius(circle)
                    #pygame.draw.line(self.linesurface, self.skills[job]["color"], self.skills[job]["pos"], pos, 2)
                    arc(self.linesurface, self.skills[job]["color"], (-r+500, -r+250, 2 * r, 2 * r), last_angle * pi / 4, ang * pi / 4, 2)
                    pygame.draw.line(self.linesurface, self.skills[job]["color"],
                        (int(cos(pi * ang / 4) * self.circle_radius(circle)) + 500,
                         int(sin(pi * ang / 4) * self.circle_radius(circle)) + 250), pos, 2)

        return self.skills[job]["pos"], self.skills[job]["angle"]

    def draw_orb(self, orb):
        for color, wid in ((orb["color"], 0), ((0, ) * 3, 2)):
            if orb["done"]:
                pygame.draw.circle(self.orbsurface, color, orb["pos"], SKILL_RADIUS, wid)

    def redraw(self):
        self.orbsurface.fill((0, )*4)
        for skill in self.skills:
            self.draw_orb(self.skills[skill])

    def reblit(self, screen):
        screen.blit(self.linesurface, (0, 0), (self.view_pos[0], self.view_pos[1], 1000, 500))
        screen.blit(self.orbsurface, (0, 0), (self.view_pos[0], self.view_pos[1], 1000, 500))
