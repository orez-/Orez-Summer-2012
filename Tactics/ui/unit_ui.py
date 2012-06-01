import pygame
import math

import ui
from unit import Unit
from equipment import EquipmentItem
from constants import SCREEN_SIZE


class UnitUI(ui.TacticsUI):
    IN_MODE = 1
    ACTIVE_MODE = 2
    OUT_MODE = 3
    EQUIPMENT_MODE = 4

    FADE_STEPS = 18

    def __init__(self, *args, **kwargs):
        super(UnitUI, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.leftsurf = pygame.Surface((470, 450))
        #self.redraw_both()

        self.darksurface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.darksurface.fill((0, 0, 0, 255))
        self.darkstep = 0
        
        self.mode = UnitUI.IN_MODE
        # do not redraw in here i guess; this screen does nothing
        # until set_unit is called.

    def redraw_both(self):
        self.redraw_left(False)
        self.redraw_right(False)

    def redraw_left(self, do_redraw=True):
        self.leftsurf.fill((0, 0x66, 0xFF))
        pygame.draw.rect(self.leftsurf, (0, ) * 3, ((0, 0), (470, 450)), 3)
        if do_redraw:
            self.redraw()

    def redraw_right(self, do_redraw=True):
        self.rightsurf.redraw()
        if do_redraw:
            self.redraw()

    def set_mode(self, mode):
        if self.mode == UnitUI.EQUIPMENT_MODE:
            self.rightsurf.set_show_box(False)
            self.redraw_right()

        self.mode = mode

        if self.mode == UnitUI.EQUIPMENT_MODE:
            self.rightsurf.set_show_box(True)
            self.redraw_right()
        if self.mode == UnitUI.IN_MODE:
            self.darkstep = 0
        if self.mode == UnitUI.OUT_MODE:
            self.darkstep = 0
        if self.mode == UnitUI.ACTIVE_MODE:
            self.darksurface.fill((0, 0, 0, 0))

    def set_unit(self, menuunit):
        self.menu_unit = menuunit
        # FER TESTIN
        self.menu_unit.unit.equip(EquipmentItem())
        self.menu_unit.unit.equip(EquipmentItem("twohand", "2h-sword", "Zweihander"))
        #print "/", self.menu_unit.unit.equipment.equipment["offhand"]
        # END FER TESTIN
        self.rightsurf = EquipmentPage(self.menu_unit.unit)
        self.redraw_both()
        self.redraw()

    def redraw(self):
        self.surface.fill((0, 0x33, 0xCC))
        self.surface.blit(self.leftsurf, (26, 30))
        self.rightsurf.reblit_self()
        self.rightsurf.reblit(self.surface)

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))
        screen.blit(self.darksurface, (0, 0))
        self.menu_unit.reblit(screen)

    def k_OK(self):
        if self.mode == UnitUI.ACTIVE_MODE:
            self.set_mode(UnitUI.EQUIPMENT_MODE)
        elif self.mode == UnitUI.EQUIPMENT_MODE:
            self.rightsurf.k_OK()
            self.redraw()

    def k_UP(self):
        if self.mode == UnitUI.EQUIPMENT_MODE:
            self.rightsurf.k_UP()
            self.redraw()

    def k_DOWN(self):
        if self.mode == UnitUI.EQUIPMENT_MODE:
            self.rightsurf.k_DOWN()
            self.redraw()

    def k_CANCEL(self):
        if self.mode == UnitUI.ACTIVE_MODE:
            self.set_mode(UnitUI.OUT_MODE)
        elif self.mode == UnitUI.EQUIPMENT_MODE:
            self.set_mode(UnitUI.ACTIVE_MODE)

    def keep_moving(self):
        if self.mode == UnitUI.OUT_MODE:
            def on_done():
                self.main.ui_back()
            self.fade(True, on_done)
        elif self.mode == UnitUI.IN_MODE:
            def on_done():
                self.set_mode(UnitUI.ACTIVE_MODE)
            self.fade(False, on_done)

    def fade(self, out, on_done):
        if self.darkstep >= UnitUI.FADE_STEPS:
            on_done()
            return
        d = math.cos((math.pi / 2) * self.darkstep / UnitUI.FADE_STEPS)
        if not out:
            d = 1 - d
        self.darksurface.fill((0, 0, 0, 255 - int(d * 255)))
        self.darkstep += 1

    @staticmethod
    def name():
        return "unit"

class UnitPages(pygame.Surface):
    """ Nominally abstract """
    def __init__(self, unit):  # probably want to send the unit too
        super(UnitPages, self).__init__((470, 450))
        self.tabwidth = 33

    def reblit(self, surf):
        surf.blit(self, (514, 30))

    def redraw(self, tabnum, alt=None):
        if alt is None:
            alt = self
        alt.fill((0, 0x66, 0xFF))
        pygame.draw.lines(alt, (0, ) * 3, False,
            ((tabnum * self.tabwidth, 0), (0, 0), (0, 450),
             (470, 450), (470, 0), ((tabnum + 1) * self.tabwidth, 0)), 3)


class EquipmentPage(UnitPages):
    def __init__(self, unit):
        super(EquipmentPage, self).__init__(unit)
        self.unit = unit
        self.font = pygame.font.Font(None, 40)
        self.slots = ["Head", "Armor", "Mainhand", "Offhand", "Accessories"]
        self.item_widths = []
        self.slot_width = max(map(lambda x: self.font.size(x)[0], self.slots))
        self.slotheight = self.font.get_height() + 5

        self.selected = 0
        self.selected_box = pygame.Surface((470, self.slotheight),
            pygame.SRCALPHA)
        self.show_box = False
        self.selected_box.fill((0, 0, 0, 64))
        self.most_surface = pygame.Surface(self.get_size())

    def set_show_box(self, val):
        if self.show_box != val:
            self.show_box = val
            self.resize_box()

    def k_OK(self):
        acc_slot = self.selected - len(self.slots) + 1
        if acc_slot >= 0:
            self.unit.equip(EquipmentItem("accessories", "ring",
                "Buttstank Ring"), acc_slot)
        else:
            slot = self.slots[self.selected].lower()
            if slot in ("mainhand", "offhand"):
                self.unit.equip(EquipmentItem(slot,
                    "mystery", "Buttstank"), slot)
            else:
                self.unit.equip(EquipmentItem(slot,
                    "mystery", "Buttstank"))
        self.redraw()
        self.resize_box()

    def k_UP(self):
        if self.selected > 0:
            self.selected -= 1
            if (self.unit.get_equip("offhand") is True and
                self.selected == self.slots.index("Offhand")):
                self.selected -= 1
            self.resize_box()
            #self.reblit_self()

    def k_DOWN(self):
        if self.selected + 1 < len(self.item_widths):
            self.selected += 1
            if (self.unit.get_equip("offhand") is True and
                self.selected == self.slots.index("Offhand")):
                self.selected += 1
            self.resize_box()
            #self.reblit_self()

    def reblit_self(self):
        self.blit(self.most_surface, (0, 0))
        if self.show_box:
            if (self.unit.get_equip("offhand") is True and
                self.selected == self.slots.index("Mainhand")):
                self.selected += .5
            self.blit(self.selected_box, (self.slot_width + 20,
                                          self.slotheight * self.selected + 2))
            self.selected = int(self.selected)

    def resize_box(self, width=None):
        if width is None:
            width = self.item_widths[self.selected]
        self.selected_box.fill((0, ) * 4)
        self.selected_box.fill((0, 0, 0, 64),
            ((0, 0), (width + 20, self.slotheight)))
        self.reblit_self()

    def redraw(self):
        super(EquipmentPage, self).redraw(0, self.most_surface)
        self.item_widths = []
        for i, slot in enumerate(self.slots):
            slot_text = self.font.render(slot, True, (0xFF, ) * 3)
            y = i * self.slotheight + 5
            self.most_surface.blit(slot_text,
                (self.slot_width - slot_text.get_size()[0] + 5, y))
            if slot.lower() != "accessories":
                item_name = self.unit.get_equip(slot)
                color = (0xEE, ) * 3
                if item_name is None:
                    item_name = "<None>"
                    color = (0x99, ) * 3
                else:
                    if self.unit.get_equip("offhand") is True:  # 2h weapon
                        if slot.lower() == "mainhand":
                            y += .5 * self.slotheight
                        if slot.lower() == "offhand":
                            self.item_widths.append(0)
                            continue
                    item_name = item_name.name
                item_text = self.font.render(item_name, True, color)
                self.item_widths.append(item_text.get_width())
                self.most_surface.blit(item_text, (self.slot_width + 30, y))
            else:
                for j, acc in enumerate(self.unit.get_accessories() + [None]):
                    y = (j + i) *self.slotheight + 5
                    if acc is None:
                        acc = "<None>"
                        color = (0x99, ) * 3
                    else:
                        acc = acc.name
                        color = (0xEE, ) * 3
                    acc_text = self.font.render(acc, True, color)
                    self.item_widths.append(acc_text.get_width())
                    self.most_surface.blit(acc_text, (self.slot_width + 30, y))
