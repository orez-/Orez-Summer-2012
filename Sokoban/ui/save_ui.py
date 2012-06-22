import pygame
from string import lowercase, uppercase

from ui import UI
from constants import SCREEN_SIZE
from level_save import LevelSave

pygame.font.init()
BIG_FONT = pygame.font.Font(None, 72)
TOP_TEXT_Y = 20
TEXT_BOX_Y = BIG_FONT.get_linesize() + TOP_TEXT_Y


class SaveUI(UI):
    def __init__(self, main, parent):
        super(SaveUI, self).__init__(main, parent)
        self.board = parent.board
        self.start = parent.start

        self.dx = 0
        self.dy = 0

        self.surface = pygame.Surface(SCREEN_SIZE)
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(BIG_FONT.render("Save your level!", True, (0, ) * 3),
            (20, TOP_TEXT_Y))
        self.font = pygame.font.Font(None, 25)
        self.text = ""
        self.redraw()

    def redraw(self):
        rect = ((20, TEXT_BOX_Y), (300, 25))
        self.surface.fill((0xFF, ) * 3, rect)
        pygame.draw.rect(self.surface, (0, )* 3, rect, 2)
        text = self.font.render(self.text, True, (0, ) * 3)
        self.surface.blit(text, (25, TEXT_BOX_Y + 5),
            ((max(0, text.get_width() - rect[1][0] + 10), 0), (rect[1][0] - 10, rect[1][1])))

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))

    def handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self.main.ui_back()
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            self.redraw()
        if event.key == pygame.K_RETURN:
            self.save_level()
        if event.unicode in (" " + lowercase + uppercase + ''.join(map(str, range(10)))):
            self.text += event.unicode
            self.redraw()

    def save_level(self):
        self.dx, self.dy = self.board.normalize()
        self.start.x -= self.dx
        self.start.y -= self.dy
        text = self.text.replace(" ", "_")
        print "Level saved?: ", LevelSave.save(text, self.board, self.start)
