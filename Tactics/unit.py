import pygame

from equipment import EquipmentSet


class Stats(object):
    # TODO: figure out what stats are used in this friggin game.
    def __init__(self, attack, defense, hp, mp, **args):
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.cur_hp = hp
        self.mp = mp

    def get_hp(self):
        return self.hp

    def get_cur_hp(self):
        return self.cur_hp

    def get_hp_frac(self):
        return float(self.cur_hp)/self.hp


class Unit(Stats):
    # TODO: late step: this loads all class's images
    # whether they're needed or not.
    def __init__(self, job, tile=None, **kwargs):
        super(Unit, self).__init__(4, 5, 6, 7)
        self.job = Job(job)
        self.tile = tile
        self.name = "Orez"
        self.equipment = EquipmentSet()
        self.__dict__.update(kwargs)
        #self.skills = SkillWeb

    def display(self, screen, size):
        unitimg = pygame.transform.flip(self.job.sprite, False, True)
        screen.blit(unitimg, size)

    def get_accessories(self):
        return self.equipment.equipment["accessories"]

    def get_equip(self, slot, acc_slot=None):
        slot = slot.lower()
        if slot == "accessories":
            return self.equipment.equipment[slot][acc_slot]
        item = self.equipment.equipment[slot]
        #if item is True and slot == "offhand":
        #    return self.equipment.equipment["mainhand"]
        return self.equipment.equipment[slot]

    def equip(self, item, slot=None):
        self.equipment.equip(item, slot)


class Job(object):
    NINJA = 1
    TRAINEE = 2

    token = {"ninja": NINJA, "trainee": TRAINEE}
    sprite = {k: pygame.image.load("img/" + v + ".png") for k, v in
        [(NINJA, "idle"),
         (TRAINEE, "hero")]}  # FIXME: don't preload?
    basestats = {NINJA: Stats(5, 5, 5, 5),
                 TRAINEE: Stats(5, 5, 5, 5)}  # FIXME: do I even want to do
    statgrowth = {NINJA: Stats(5, 5, 5, 5),
                  TRAINEE: Stats(5, 5, 5, 5)}  # it this way?
    instances = {}

    def __new__(cls, job, *args, **kwargs):
        token = Job.token[job.lower()]
        if token not in Job.instances:
            Job.instances[token] = \
                super(Job, cls).__new__(cls, *args, **kwargs)
            Job.instances[token].__init(token)
        return Job.instances[token]

    def __init(self, job_token):
        self.sprite = Job.sprite[job_token]
        self.basestats = Job.basestats[job_token]
        self.statgrowth = Job.statgrowth[job_token]

if __name__ == "__main__":
    j = Job("ninja")
    k = Job("ninja")
    t = Job("trainee")
    print j is k
    print j is t
