import pygame
import time
import re

from constants import SCREEN_SIZE, RS, US

pygame.font.init()
CHAT_BUFFER = 1024
CHAT_EDGE = 10
CHAT_WIDTH = SCREEN_SIZE[0] - CHAT_EDGE * 2
CHAT_HEIGHT = 100
CHAT_FONT = pygame.font.Font(None, 16)
CHAT_FONT_HEIGHT = CHAT_FONT.get_linesize()
INPUT_Y = SCREEN_SIZE[1] - CHAT_FONT_HEIGHT - CHAT_EDGE * 3 / 2
CHAT_Y = INPUT_Y - CHAT_HEIGHT - CHAT_EDGE

CHAT_LINGER = 3


class Inputbox:
    def __init__(self):
        self.bg_surface = pygame.Surface((CHAT_WIDTH, CHAT_FONT_HEIGHT + CHAT_EDGE))
        self.bg_surface.set_alpha(192)
        self.text_surface = pygame.Surface((CHAT_WIDTH - CHAT_EDGE, CHAT_FONT_HEIGHT), pygame.SRCALPHA)
        self.text = ""

    def reblit(self, surf):
        surf.blit(self.bg_surface, (CHAT_EDGE, INPUT_Y - CHAT_EDGE / 2))
        surf.blit(self.text_surface, (CHAT_EDGE * 3 / 2, INPUT_Y))

    def redraw(self):
        self.text_surface.fill((0, ) * 4)
        words = CHAT_FONT.render(self.text, True, (0xFF, ) * 3)
        self.text_surface.blit(words, (0, 0),
            ((max(words.get_width() - (CHAT_WIDTH - CHAT_EDGE), 0), 0),
             (CHAT_WIDTH, CHAT_FONT_HEIGHT)))

    def submit(self, client):
        if self.text:
            self.text = self.text.replace(RS, "")   # strip bad characters
            client.send("MSG " + self.text)
            self.text = ""
            self.redraw()


class Chatbox:
    def __init__(self):
        self.bg_color = (0, ) * 4
        self.text_surface = pygame.Surface((CHAT_WIDTH, CHAT_BUFFER), pygame.SRCALPHA)
        self.text_surface.fill(self.bg_color)
        self.bg_surface = pygame.Surface((CHAT_WIDTH, CHAT_HEIGHT))
        self.bg_surface.fill((0, ) * 3)
        self.bg_surface.set_alpha(192)

        self.hide_time = 0
        #self.surface = pygame.Surface((CHAT_WIDTH, CHAT_HEIGHT))
        #self.surface.set_alpha(64)
        self.input_box = Inputbox()

    def reblit(self, surf):
        if self.hide_time is not None:
            if self.hide_time is not True and self.hide_time < time.time():
                self.hide_time = None
            surf.blit(self.bg_surface, (CHAT_EDGE, CHAT_Y))
            surf.blit(self.text_surface,
                (CHAT_EDGE / 2, CHAT_Y + CHAT_EDGE / 2),
                ((0, CHAT_BUFFER - CHAT_HEIGHT + CHAT_EDGE),
                 (CHAT_WIDTH, CHAT_HEIGHT - CHAT_EDGE / 2)))
            if self.hide_time is True:
                self.input_box.reblit(surf)

    def message(self, player2, msg):
        COLORS = {0: (0x00, 0xA2, 0xE8),
                  1: (0xC0, 0x55, 0xDF),
                  2: (0x99, 0x99, 0x99),
                  3: (0xFF, 0xD7, 0x00)}
        color = COLORS[int(player2)]
        keep_color = color
        lines = self.split_message(msg)
        bunp = -len(lines) * CHAT_FONT_HEIGHT
        self.text_surface.scroll(0, bunp)
        self.text_surface.fill(self.bg_color,
            ((0, CHAT_BUFFER + bunp), (CHAT_WIDTH, -bunp)))

        for i, x in enumerate(lines):
            wid = 0
            while US in x:  # different colors
                loc = x.find(US)
                next_color = COLORS[int(x[loc + 1: loc + 3], 16)]
                text, x = x[:loc], x[loc + 3:]

                text = CHAT_FONT.render(text, True, color)
                self.text_surface.blit(text,
                    (CHAT_EDGE + wid, CHAT_BUFFER + bunp + i * CHAT_FONT_HEIGHT))
                wid += text.get_width()
                color = next_color
            text = CHAT_FONT.render(x, True, color)
            self.text_surface.blit(text,
                (CHAT_EDGE + wid, CHAT_BUFFER + bunp + i * CHAT_FONT_HEIGHT))

        hide_time = time.time() + CHAT_LINGER * len(lines)
        if self.hide_time is None or (self.hide_time is not True and
            hide_time > self.hide_time):  # don't LOWER the time on the clock, and
            self.hide_time = hide_time    # don't close my window if i'm typing too
        #self.view.fill((0,0,0,64))
        #self.view.blit(self.surface, (0, self.view.get_height()-self.surface.get_height()))
        # TODO: maybe make it keep track of scroll (instead of scrolling to the bottom)

    def split_message(self, msg):
        wid = 0
        toR = []
        screenwid = CHAT_WIDTH - CHAT_EDGE
        msg = msg.split(' ')
        line = ""
        while msg:
            last_index = 0
            while US in msg[0][last_index:]:  # different colors
                loc = msg[0].find(US, last_index)
                last_index = loc + 1
                raw_num = msg[0][loc + 1: loc + 3]
                try:
                    if len(raw_num) != 2:
                        raise ValueError
                    num = int(raw_num, 16)  # hex num
                except ValueError:  # not valid input
                    msg[0] = msg[0][:loc] + msg[0][loc + 1:]  # strip the US
                    last_index -= 1  # what if some idiot did USUS03
                                     # (or worse USUSbad)
            colorless = re.sub(US + r"\d\d", "", msg[0])
            word_width = CHAT_FONT.size(colorless)[0]
            if word_width + wid > screenwid:  # nextline
                wid = 0
                toR += [line]
                line = ""
                if word_width > screenwid:  # nextline too long!?
                    for i, c in enumerate(msg[0]):  # go character by character
                        if c == US:
                            line += msg[0][i: i + 3]
                            continue
                        if CHAT_FONT.size(re.sub(US + r"\d\d", "", line) + c)[0] > screenwid:
                            toR += [line]
                            line = ""
                        line += c
                    line += " "
                    wid += CHAT_FONT.size(re.sub(US + r"\d\d", "", line + " "))[0]
                    msg = msg[1:]
                    continue
            wid += CHAT_FONT.size(colorless + " ")[0]
            line += msg[0] + " "
            msg = msg[1:]
        toR += [line]
        return toR

    def add_string(self, other):
        self.input_box.text += other
        self.input_box.redraw()

    def remove_chars(self, other=1):
        self.input_box.text = self.input_box.text[:-other]
        self.input_box.redraw()
