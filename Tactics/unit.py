import pygame


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


class EquipmentItem:
    """ Currently just an example. """
    def __init__(self):
        self.equip_slot = "head"
        self.item_type = "hat"
        self.name = "Stylish Beret"


class EquipmentSet:
    def __init__(self):
        self.equipment = {
            "head":None,
            "armor":None,
            "mainhand":None,
            "offhand":None,
            "accessories":[]
        }

    def equip(self, item, slot=None):
        """ slot is unnecessary except for mainhand vs offhand """
        if item.equip_slot not in self.equipment:
            return False
        if item.equip_slot == "accessories":  # special case.
            alike = 0
            for i, it in enumerate(self.equipment["accessories"]):
                if i != slot and it.item_type == item.item_type:
                    alike += 1
            if alike >= (2 if it.item_type == "ring" else 1):
                return False  # ^ not the best
            if slot is not None:    # overwriting old accessory
                self._unequip_accessory(slot)
                self.equipment["accessories"][slot] = item
            else:   # adding new accessory
                slot = len(self.equipment["accessories"])
                self.equipment["accessories"].append(item)
        else:   # not an accessory
            if item.equip_slot in ("mainhand", "offhand"):
                if item.hands == 1:  # slot is important
                    if slot not in ("mainhand", "offhand"):
                        return False
                else:  # slot not important: takes both hands
                    slot = "mainhand"
                    self.unequip("offhand")
                    self.equipment["offhand"] = True
            else:
                slot = item.equip_slot
            self.unequip(slot)
            self.equipment[slot] = item
        # TODO: recalculate stats (based on item)

    def _unequip_accessory(self, index):
        """ Unequips the accessory at slot 'index', but does not shift
        later elements back """
        item = self.equipment["accessories"][index]
        if item is not None:
            # TODO: put back in your inventory
            self.equipment["accessories"][index] = None
            # TODO: recalculate stats (based on item)

    def unequip(self, slot, acc_slot=None):
        if slot in self.equipment:
            if slot == "accessories":
                self._unequip_accessory(acc_slot)
                del self.equipment["accessory"][acc_slot]
                return
            if slot in ("mainhand", "offhand"):
                if self.equipment["offhand"] is True:  # currently a two-hander
                    self.equipment["offhand"] = None
                    self.unequip("mainhand")
            item = self.equipment[slot]
            if item is not None:
                # TODO: put it back in your inventory
                self.equipment[slot] = None
                # TODO: recalculate stats (based on item)


class Unit(Stats):
    # TODO: late step: this loads all class's images
    # whether they're needed or not.
    def __init__(self, job, tile=None, **kwargs):
        super(Unit, self).__init__(4, 5, 6, 7)
        self.job = Job(job)
        self.tile = tile
        self.name = "Orez"
        self.__dict__.update(kwargs)
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
