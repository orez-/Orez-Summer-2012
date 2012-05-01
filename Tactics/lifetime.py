class LifetimeStats:
    """ Refer to stats that do not help in battle, but of which maybe you want
    to keep track? For example: number of shots fired, favorite weapon, steps
    taken, etc """

    def __init__(self):
        self.weapons = {}
        self.weapon_types = {}

    def use_weapon(self, weapon):
        """ When you use a weapon there's a handful of relevant stats to keep
        track of, such as which weapon you used, what type it was, its element,
        etc. """
        self._incr(self.weapons, weapon)
        self._incr(self.weapon_types, weapon.wtype)

    def _incr(self, dic, field, amt=1):
        """ Increment stat in the dictionary, defaulting to 0 if nonexistant"""
        if field not in dic:
            dic[field] = 0
        dic[field] += amt

if __name__ == "__main__":
    help(LifetimeStats)
