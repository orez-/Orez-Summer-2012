import unittest


class EquipmentItem:
    """ Currently just an example. """
    def __init__(self, slot="head", itype="hat", name="Stylish Beret"):
        self.equip_slot = slot
        self.item_type = itype
        self.name = name


class EquipmentSet:
    def __init__(self):
        self.equipment = {
            "head":None,
            "armor":None,
            "mainhand":None,
            "offhand":None,
            "accessories":[],
            "twohand":None
        }

    def equip(self, item, slot=None):
        """ slot is unnecessary except for mainhand vs offhand """
        if item.equip_slot not in self.equipment:
            print "No such slot"
            return False
        if item.equip_slot == "accessories":  # special case.
            alike = 0
            for i, it in enumerate(self.equipment["accessories"]):
                if i != slot and it.item_type == item.item_type:
                    alike += 1
            if alike >= (2 if item.item_type == "ring" else 1):
                print "Too many of that accessory"
                return False  # ^ not the best
            if (slot is not None and
                    slot < len(self.equipment["accessories"])):  # overwriting old accessory
                self._unequip_accessory(slot)
                self.equipment["accessories"][slot] = item
            else:   # adding new accessory
                slot = len(self.equipment["accessories"])
                self.equipment["accessories"].append(item)
        else:   # not an accessory
            if item.equip_slot in ("mainhand", "offhand"):  # slot is important
                if slot not in ("mainhand", "offhand"):
                    print "Must specify which hand."
                    return False
            elif item.equip_slot == "twohand":  # slot not important: takes both hands
                slot = "mainhand"
                self.unequip("mainhand")
                self.unequip("offhand")
                self.equipment["offhand"] = True
                self.equipment["mainhand"] = item
                # TODO: recalculate stats (based on item)
                return
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

    def get_all(self):
        return [v for k, v in self.equipment.items() if k != "accessories"
            and v is not None] + self.equipment["accessories"]
