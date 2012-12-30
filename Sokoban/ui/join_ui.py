import os
import pygame

from ui import UI
from constants import SCREEN_SIZE
from networking import TestConnection

DESCFONT = pygame.font.Font(None, 30)
PADDING = 8
BG_COLOR = (200, 191, 231)
BG_HILITE = (167, 152, 216)
HOSTDATA_SAVE = "data/config/hostdata"


class JoinUI(UI):
    STD_MODE = 0
    SAVE_MODE = 1

    def __init__(self, main, parent):
        super(JoinUI, self).__init__(main, parent)
        self.surface = pygame.Surface((SCREEN_SIZE))
        self.ip_box = Textbox((155, 5), 500)
        self.host_id_box = Textbox((155, 40), 500)
        self.type_buttons = ButtonRow([
                ("Connect", lambda: self.main.change_screen("join ip")),
                ("Save Address", lambda: self.set_mode(JoinUI.SAVE_MODE))
            ], (0, 40))
        self.save_buttons = ButtonRow([
                ("Save", lambda: self.create_hostdata()),
                ("Cancel", lambda: self.set_mode(JoinUI.STD_MODE)),
            ], (0, 75))
        self.base_buttons = ButtonRow([
                ("Delete", lambda: None),
                ("Refresh", lambda: self.refresh()),
                ("Back", lambda: self.go_back())
            ])
        self.base_buttons.bottom = SCREEN_SIZE[1]
        self.hda = HostDataArea(self, self.type_buttons.bottom)
        self.load_hosts()

        self.to_reblit = set([
            self.ip_box, self.type_buttons, self.base_buttons])
        self.mouseable = [
            self.ip_box, self.type_buttons, self.base_buttons,
            self.hda.data]
        self._mode = JoinUI.STD_MODE
        self.redraw()

    def refresh(self):
        for hd in self.hda.data:
            hd.conn.stop()
            hd.conn = TestConnection(hd.conn.ADDR[0], hd.conn.cb)
            hd.conn.start()

    def go_back(self):
        for hd in self.hda.data:
            hd.conn.stop()
        self.main.ui_back()

    def create_hostdata(self):
        self.hda.add(self.ip_box.text, self.host_id_box.text)
        self.set_mode(JoinUI.STD_MODE)
        self.ip_box.text = ""
        self.host_id_box.text = ""
        self.save_hosts()

    def load_hosts(self):
        try:
            with open(HOSTDATA_SAVE, "r") as f:
                self.hda.data[:] = []
                for data in f:
                    addr, _, name = data.partition(chr(30))
                    name = name.rstrip("\n\r")
                    self.hda.add(addr, name)
        except IOError:
            print "Host file not found"

    def save_hosts(self):
        with open(HOSTDATA_SAVE, "w") as f:
            for data in self.hda.data:
                f.write(''.join((data.address, chr(30), data.name, '\n')))

    def set_mode(self, value):
        if self._mode == value:
            return
        self._mode = value
        if self._mode == JoinUI.STD_MODE:
            self.ip_box.disabled = False
            self.to_reblit.discard(self.host_id_box)
            self.to_reblit.discard(self.save_buttons)
            self.mouseable.remove(self.save_buttons)
            self.save_buttons.selected = None
            self.to_reblit.add(self.type_buttons)
            self.mouseable.append(self.type_buttons)
            self.hda._top = self.type_buttons.bottom
        elif self._mode == JoinUI.SAVE_MODE:
            self.ip_box.disabled = True
            self.to_reblit.add(self.host_id_box)
            self.to_reblit.add(self.save_buttons)
            self.mouseable.append(self.save_buttons)
            self.to_reblit.discard(self.type_buttons)
            self.mouseable.remove(self.type_buttons)
            self.type_buttons.selected = None
            self.hda._top = self.save_buttons.bottom
        self.redraw()

    mode = property(lambda self: self._mode, set_mode)

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        self.hda.reblit(surf)
        for x in self.to_reblit:
            x.reblit(surf)
        #self.ip_box.reblit(surf)
        #if self.mode == JoinUI.SAVE_MODE:
        #    self.host_id_box.reblit(surf)
        #self.type_buttons.reblit(surf)

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.fill((200, 191, 231), ((0, 0), (SCREEN_SIZE[0], 80)))
        self.surface.blit(DESCFONT.render("Host Address", True, (0, ) * 3),
            (PADDING, PADDING))

        if self.mode == JoinUI.SAVE_MODE:
            self.surface.blit(DESCFONT.render("Host's Name", True, (0, ) * 3),
                (PADDING, PADDING + 30 + PADDING))

        #self.surface.fill((0, ) * 3, ((400, 400), (100, 100)))

        #surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        #surf.fill((206, 206, 206, 104))
        #self.surface.blit(surf, (350, 350))

    def handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self.main.ui_back()
        if self.mode == JoinUI.STD_MODE:
            res = self.ip_box.handle_key(event)
            if res == Textbox.ENTER:
                self.main.change_screen("join ip")
            if res == Textbox.TAB:
                self.mode = JoinUI.SAVE_MODE
        elif self.mode == JoinUI.SAVE_MODE:
            res = self.host_id_box.handle_key(event)
            if res == Textbox.ENTER:
                pass
            if res == Textbox.TAB:
                self.mode = JoinUI.STD_MODE

    def handle_motion(self, event, mouseable=None):
        if mouseable is None:
            mouseable = self.mouseable
        for elem in mouseable:
            x, y = event.pos
            try:
                self.handle_motion(event, elem)
            except TypeError:
                pass
            try:
                elem.top
            except:
                pass
            else:
                if elem.top < y < elem.bottom and elem.left < x < elem.right:
                    elem.handle_motion(event)
                else:
                    elem.selected = None

    def handle_click(self, event, mouseable=None):
        if mouseable is None:
            mouseable = self.mouseable
        for elem in mouseable:
            try:
                if self.handle_click(event, elem):
                    return True
            except TypeError:
                pass
            try:
                elem.top
            except:
                pass
            else:
                if elem.handle_click(event):
                    return True


class HostDataArea(object):
    SPACING = 5
    def __init__(self, parent, top):
        self.parent = parent
        self.surface = pygame.Surface((SCREEN_SIZE[0], 550))
        self.data = []
        self.dirty = set()
        self._top = top
        self.redraw()

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        for i, _ in enumerate(self.data):
            self.redraw_hd(i)

    def redraw_hd(self, i):
        elem = self.data[i]
        self.surface.blit(elem,
            (HostDataArea.SPACING, elem.y))

    def reblit(self, surf):
        if self.dirty:
            for i in self.dirty:
                self.redraw_hd(i)
        surf.blit(self.surface, (0, self._top))

    def add(self, address, name):
        num = len(self.data)
        self.dirty.add(num)
        self.data.append(HostData(self, HostDataArea.SPACING +
                (HostDataArea.SPACING + HostData.HEIGHT) * num, address, name))


class HostData(pygame.Surface):
    HEIGHT = 80
    def __init__(self, parent, y, address, name):
        super(HostData, self).__init__((SCREEN_SIZE[0] - HostDataArea.SPACING * 2,
            HostData.HEIGHT))
        self.parent = parent
        self.address = str(address)
        self.name = str(name)
        self.font = pygame.font.Font(None, 24)
        self._selected = None

        self.y = y
        self.conn = TestConnection(self.address, self.handle_result)

        self.handle_result("POLLING")
        self.redraw()
        self.conn.start()

    def set_selected(self, value):
        self._selected = value
        self.redraw()

    top = property(lambda self: self.parent._top + self.y)
    left = property(lambda self: HostDataArea.SPACING)
    right = property(lambda self: SCREEN_SIZE[0] - HostDataArea.SPACING)
    bottom = property(lambda self: self.top + HostData.HEIGHT)
    selected = property(lambda self: self._selected, set_selected)

    def handle_result(self, result):
        if result == "BAD":
            self.status = "Server unavailable"
            self.color = (0xCC, 0, 0)
        elif result == "SOKOPONG":  # This is the guy we like
            self.status = "Available!"
            self.color = (0, 0x99, 0)
        elif result == "FULL":
            self.status = "Game in progress"
            self.color = (0x66, 0, 0)
        elif result == "POLLING":
            self.color = (0x66, ) * 3
            self.status = "Polling"
        else:
            print "wat"
        self.redraw()
        if self in self.parent.data:
            self.parent.dirty.add(self.parent.data.index(self))

    def handle_motion(self, event):
        self.selected = True

    def redraw(self):
        self.fill((0xFF, 0xDD, 0xEE) if self.selected else (0xEE, 0xDD, 0xFF))
        self.blit(self.font.render(self.name, True, (0, ) * 3), (10, 10))
        self.blit(self.font.render(self.address, True, (0x99, ) * 3), (10, 30))
        self.blit(self.font.render(self.status, True, self.color), (10, 50))

    def handle_click(self, event):
        if self.selected:
            ui = self.parent.parent
            ui.set_mode(JoinUI.STD_MODE)
            ui.ip_box.text = self.address
            print self.address, self.name


class ButtonRow(object):
    def __init__(self, name_actions, (x, y)=(0, 0),
            width=SCREEN_SIZE[0], font_height=30):
        self.padding = 10
        self.bg_color = BG_COLOR
        self.bg_hilite = BG_HILITE
        self.font = pygame.font.Font(None, font_height)

        ln = len(name_actions)
        self.step = width // (ln)
        self.hstep = self.step // 2

        self.x, self.y = (x, y)
        self.name_actions = name_actions[:]
        self.surface = pygame.Surface(
            (width, self.font.get_linesize() + self.padding * 2))
        self._selected = None
        self.redraw()

    def set_pos(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def set_selected(self, value):
        newsel = min(value, len(self.name_actions) - 1)
        if self._selected != newsel:
            self._selected = newsel
            self.redraw()

    pos = property(lambda self: (self.x, self.y),
        lambda self, value: self.set_pos(*value))

    selected = property(lambda self: self._selected, set_selected)

    top = property(lambda self: self.y,
        lambda self, value: self.set_pos(y=value))
    bottom = property(lambda self: self.y + self.surface.get_height(),
        lambda self, value: self.set_pos(y=value - self.surface.get_height()))
    left = property(lambda self: self.x,
        lambda self, value: self.set_pos(x=value))
    right = property(lambda self: self.x + self.surface.get_width(),
        lambda self, value: self.set_pos(x=value - self.surface.get_width()))

    def redraw(self):
        self.surface.fill(self.bg_color)
        if self.selected is not None:
            self.surface.fill(self.bg_hilite, ((self.selected * self.step, 0),
                (self.step, self.surface.get_height())))
        for i, (name, _) in enumerate(self.name_actions):
            text = self.font.render(name, True, (0, ) * 3)
            offset = text.get_width() // 2
            self.surface.blit(text,
                (i * self.step + self.hstep - offset, self.padding))

    def reblit(self, surf):
        surf.blit(self.surface, self.pos)

    def handle_motion(self, event):
        self.selected = event.pos[0] // self.step

    def handle_click(self, event):
        if self.selected is not None:
            self.name_actions[self.selected][1]()
            return True
        return False


class Textbox(object):
    ENTER = object()
    TAB = object()

    def __init__(self, (x, y), width, fontheight=30):
        self.padding = 3
        self._text = ""
        self.font = pygame.font.Font(None, fontheight)
        self.surface = pygame.Surface((width,
            self.padding * 2 + self.font.get_linesize()))
        self.border = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        self.pos = (x, y)
        self._disabled = False
        self.redraw_text()
        self.redraw_border()

    def set_text(self, value):
        if self._disabled:
            return False
        self._text = str(value)
        self.redraw_text()
        return True

    def set_disabled(self, value):
        self._disabled = value
        self.redraw_border()

    disabled = property(lambda self: self._disabled, set_disabled)
    text = property(lambda self: self._text, set_text)

    def redraw_text(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(self.font.render(self.text, True, (0, ) * 3),
            (self.padding, ) * 2)

    def redraw_border(self):
        alpha = 104 if self.disabled else 0
        self.border.fill((206, 206, 206, alpha))
        pygame.draw.rect(self.border, (171, 173, 179),
            ((0, 0), self.surface.get_size()), 1)

    def reblit(self, surf):
        surf.blit(self.surface, self.pos)
        surf.blit(self.border, self.pos)

    def handle_key(self, event):
        if self.disabled:
            return False
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return Textbox.ENTER
        elif event.key == pygame.K_TAB:
            return Textbox.TAB
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.unicode:
            self.text += event.unicode
        else:
            return None
