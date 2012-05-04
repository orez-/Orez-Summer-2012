import pygame


class Stats:
    # TODO: figure out what stats are used in this friggin game.
    def __init__(self, attack, defense, hp, mp, **args):
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.mp = mp


class ElementalDamage():
    pass


class Unit:
    # TODO: late step: this loads all class's images
    # whether they're needed or not.
    def __init__(self, job):
        self.job = Job(job)
        #self.skills = SkillWeb

    def display(self, screen, size):
        unitimg = pygame.transform.flip(self.job.sprite, False, True)
        screen.blit(unitimg, size)


class Job(object):
    NINJA = 1
    TRAINEE = 2

    token = {"ninja": NINJA, "trainee": TRAINEE}
    sprite = {k: pygame.image.load("img/" + v + ".png") for k, v in
        [(NINJA, "idle"),
         (TRAINEE, "idle")]}  # FIXME: don't preload?
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
