import pygame
import math
import random

class Stats:
    # TODO: figure out what stats are used in this friggin game.
    def __init__(self,attack,defense,hp,mp,**args):
        self.attack  = attack
        self.defense = defense
        self.hp = hp
        self.mp = mp

class ElementalDamage():
    pass

class Unit:
    # TODO: late step: this loads all class's images whether they're needed or not.
    jobs = {"ninja":{"sprite":pygame.image.load("img/idle.png"),\
                     "basestats":Stats(5,5,5,5),\
                     "statgrowth":Stats(5,5,5,5)}}
    def __init__(self, job):
        if job.lower() not in Unit.jobs:
            raise ValueError("'job' must be a valid job")
        self.job = job.lower()
    def display(self,screen,size):
        unitimg = pygame.transform.flip(Unit.jobs[self.job]["sprite"], False, True)
        screen.blit(unitimg,size)
