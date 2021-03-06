import pygame

import ui
from ui.map_ui import MapUI
from terrain import Room
from terrain.rooms import *
from sprites.slime import SlimeAI
from sprites.goblin import GoblinAI
from sprites.elemental import ElementalAI

SCREEN_SIZE = (600, 450)


class OverworldUI(ui.UI):
    def __init__(self, main, parent):
        super(OverworldUI, self).__init__(main, parent)
        self.slime = SlimeAI((50, 50))

        self.terrain = []
        self.load_rooms_around((25, 25))

        self.redraw()

    def load_rooms_around(self, (px, py)):
        (rx, ry), (w, h) = self.main.map.get_at((px, py)).get_rect()
        for x, y in self.main.map.surround_iter((rx, ry), (w, h)):
            self.load_room((x, y))
        try:
            self.room_data.entities.discard(self.slime)
        except AttributeError:
            pass
        self.room_data = self.load_room((rx, ry))
        self.room_data.entities.add(self.slime)

    def load_room(self, (x, y)):
        room = self.main.map.get_at((x, y))
        if room is None:
            print "Could not load room at (", x, ", ", y, ")"
            return False
        (x, y), (w, h) = room.get_rect()

        for i, item in enumerate(self.terrain):
            if (x, y) == (item.x, item.y):
                del self.terrain[i]
                self.terrain.append(item)
                return item

        if (x - 25) ** 2 + (y - 25) ** 2 < 625:
            room_obj = Grasslands(room)
        else:
            room_obj = Ocean(room)
        self.terrain.append(room_obj)
        self.terrain = self.terrain[-16:]  # limit the list to 16 elements
        return room_obj

    def redraw(self):
        pass

    def reblit(self, surf, time_passed):
        super(OverworldUI, self).reblit(surf, time_passed)
        center = self.slime.centerx - 300, self.slime.centery - 225
        for t in self.terrain:
            t.reblit(surf, time_passed, center, self.room_data.pos)

    def handle_key(self, event):
        if event.key == pygame.K_m:
            self.main.ui_push(MapUI)

    def update(self):
        xoff, yoff = 0, 0
        if self.main.keys & set((pygame.K_a, pygame.K_LEFT)):
            xoff -= 1
        if self.main.keys & set((pygame.K_d, pygame.K_RIGHT)):
            xoff += 1
        if self.main.keys & set((pygame.K_w, pygame.K_UP)):
            yoff -= 1
        if self.main.keys & set((pygame.K_s, pygame.K_DOWN)):
            yoff += 1
        if not (xoff == yoff == 0):  # there is movement
            ret = self.slime.move(self.room_data, xoff, yoff)
            if ret == "room":
                self.room_data.entities.discard(self.slime)
                self.room_data = Inside(self.room_data.pos, self.slime.pos)
                self.room_data.entities.add(self.slime)
                self.terrain = [self.room_data]
                self.slime.pos = (50, 360)
                return
            elif ret == "out":
                self.slime.pos = self.room_data.player_toR
                self.load_rooms_around(self.room_data.room_toR)

            newx = int(self.slime.x // (Room.TPS * 50))
            newy = int(self.slime.y // (Room.TPS * 50))
            if not (0 <= newx < self.room_data.w and
                    0 <= newy < self.room_data.h):
                x, y = self.room_data.pos  # keep the current room's position
                self.load_rooms_around((newx + self.room_data.x,
                        newy + self.room_data.y))
                # readjust for the new room
                self.slime.x += (x - self.room_data.x) * Room.TPS * 50
                self.slime.y += (y - self.room_data.y) * Room.TPS * 50
        elif self.slime.animations.name[1] != "idle":
            self.slime.animations.cur_animation = (
                self.slime.animations.name[0], "idle")
