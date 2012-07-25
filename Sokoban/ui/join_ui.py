import pygame

from ui import UI
from constants import SCREEN_SIZE

DESCFONT = pygame.font.Font(None, 30)
PADDING = 8


class JoinUI(UI):
    STD_MODE = 0
    SAVE_MODE = 1

    def __init__(self, main, parent):
        super(JoinUI, self).__init__(main, parent)
        self.surface = pygame.Surface((SCREEN_SIZE))
        self.ip_box = Textbox((155, 5), 500)
        self._mode = JoinUI.STD_MODE
        self.redraw()

    def set_mode(self, value):
        self._mode = value
        if self._mode == JoinUI.STD_MODE:
            self.ip_box.disabled = False
        elif self._mode == JoinUI.SAVE_MODE:
            self.ip_box.disabled = True
            self.host_id_box = Textbox((155, 40), 500)
        self.redraw()

    mode = property(lambda self: self._mode, set_mode)

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        self.ip_box.reblit(surf)
        if self.mode == JoinUI.SAVE_MODE:
            self.host_id_box.reblit(surf)

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(DESCFONT.render("Host Address", True, (0, ) * 3), (PADDING, PADDING))

        if self.mode == JoinUI.SAVE_MODE:
            self.surface.blit(DESCFONT.render("Host's Name", True, (0, ) * 3), (PADDING, PADDING + 30 + PADDING))

        #self.surface.fill((0, ) * 3, ((400, 400), (100, 100)))

        #surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        #surf.fill((206, 206, 206, 104))
        #self.surface.blit(surf, (350, 350))

    def handle_key(self, event):
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


class Textbox(object):
    ENTER = object()
    TAB = object()

    def __init__(self, (x, y), width, fontheight=30):
        self.padding = 3
        self.text = ""
        self.font = pygame.font.Font(None, fontheight)
        self.surface = pygame.Surface((width, self.padding * 2 + self.font.get_linesize()))
        self.border = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        self.pos = (x, y)
        self._disabled = False
        self.redraw_text()
        self.redraw_border()

    def set_disabled(self, value):
        self._disabled = value
        self.redraw_border()

    disabled = property(lambda self: self._disabled, set_disabled)

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
        self.redraw_text()
