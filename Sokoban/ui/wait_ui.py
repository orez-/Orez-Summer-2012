import pygame
import random

from constants import SCREEN_SIZE, get_noun, get_adjective

class WaitUI:
    def __init__(self, main, player2):
        self.main = main
        self.player2 = player2
        self.surface = pygame.Surface((SCREEN_SIZE))
        self.smaller_font = pygame.font.Font(None, 28)
        self.larger_font = pygame.font.Font(None, 108)

        you_tiles = pygame.image.load("imgs/you.png")
        TS = 50  # MAGICAL
        you = pygame.Surface((TS, TS), pygame.SRCALPHA)
        you.blit(you_tiles, (0, 0), (0, 0, TS, TS))
        self.you = pygame.Surface((TS, TS))
        self.you.fill((0xFF, ) * 3)
        self.you.blit(pygame.transform.flip(you, True, False), (0, 0))

        me_tiles = pygame.image.load("imgs/me.png")
        self.me = pygame.Surface((TS, TS))
        self.me.fill((0xFF, ) * 3)
        self.me.blit(me_tiles, (0, 0), (0, 0, TS, TS))

        self.adjective = get_adjective()
        self.noun = get_noun()

        self.redraw_teammate_words()
        self.redraw_join_words()

        self.redraw()

    def redraw_join_words(self):
        if self.player2:
            first_line = self.smaller_font.render("You will join your", True, (0, ) * 3)
            second_line = self.smaller_font.render("teammate shortly", True, (0, ) * 3)
        else:
            first_line = self.smaller_font.render("Your teammate", True, (0, ) * 3)
            second_line = self.smaller_font.render("will join you shortly", True, (0, ) * 3)
        text_width = max(map(lambda x: x.get_width(), (first_line, second_line)))
        self.join_words = pygame.Surface((text_width,
            sum(map(lambda x: x.get_height(), 
            (first_line, second_line)))))
        self.join_words.fill((0xFF, ) * 3)
        self.join_words.blit(first_line, ((text_width - first_line.get_width()) / 2, 0))
        self.join_words.blit(second_line, ((text_width - second_line.get_width()) / 2, first_line.get_height()))

        self.join_words_pos = ((SCREEN_SIZE[0] - text_width) / 2, 250)

    def redraw_teammate_words(self):
        first_line = self.smaller_font.render("your "+self.adjective,
            True, (0, ) * 3)
        second_line = self.smaller_font.render(self.noun, True, (0, ) * 3)
        text_width = max(map(lambda x: x.get_width(), (first_line, second_line)))
        self.teammate_text = pygame.Surface((text_width,
            sum(map(lambda x: x.get_height(), 
            (first_line, second_line)))))
        self.teammate_text.fill((0xFF, ) * 3)
        if self.player2:
            self.teammate_text.blit(first_line,
                (max(0, text_width / 2 - first_line.get_width()), 0))
            self.teammate_text.blit(second_line,
                (max(0, text_width / 2 - second_line.get_width()),
                first_line.get_height()))

            self.teammate_text_pos = (5, 350)
            self.my_text_pos = (SCREEN_SIZE[0] - 70, 350)
        else:
            self.teammate_text.blit(first_line,
                (min(text_width - first_line.get_width(), text_width / 2), 0))
            self.teammate_text.blit(second_line,
                (min(text_width - second_line.get_width(), text_width / 2),
                first_line.get_height()))

            self.teammate_text_pos = (SCREEN_SIZE[0] - text_width - 5, 350)
            self.my_text_pos = (30, 350)

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(self.larger_font.render("Please Wait", True, (0, ) * 3), (60, 150))
        self.surface.blit(self.join_words, self.join_words_pos)
        self.surface.blit(self.me, (30, 300))
        self.surface.blit(self.smaller_font.render("you", True, (0, ) * 3),
            self.my_text_pos)
        self.surface.blit(self.teammate_text, self.teammate_text_pos)
        self.surface.blit(self.you, (470, 300))

    def reblit(self, screen):
        screen.blit(self.surface, (0, 0))

    def handle_key(self, event):
        pass

    def handle_key_up(self, event):
        pass