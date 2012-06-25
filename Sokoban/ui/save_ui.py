import pygame

from ui import UI
from constants import SCREEN_SIZE, valid_file_char
from level_save import LevelSave

pygame.font.init()
BIG_FONT = pygame.font.Font(None, 72)
SMALL_FONT = pygame.font.Font(None, 25)
TOP_TEXT_Y = 20
TEXT_BOX_Y = BIG_FONT.get_linesize() + TOP_TEXT_Y
BUTTON_TEXT_SPACER = 5
BUTTON_SPACER = 5
BUTTON_X = BUTTON_SPACER * 5
BUTTON_Y = 150
BUTTONS_ACROSS = 2

SUCCESS_COLOR = (0x32, 0xCD, 0x32)
FAILURE_COLOR = (0xFF, 0x24, 0x00)


class SaveUI(UI):
    def __init__(self, main, parent):
        super(SaveUI, self).__init__(main, parent)
        self.board = parent.board
        self.start = parent.start

        self.dx = 0
        self.dy = 0

        self.surface = pygame.Surface(SCREEN_SIZE)
        self.text = ""

        def to_menu():
            self.main.ui_back()
            self.main.ui_back()

        def to_test():
            self.normalize()
            self.main.ui_back()
            self.main.change_screen("test")

        self.options = [("Save as Draft", self.save_level(True)),
                        ("Save as Finished", self.save_level(False)),
                        ("Back to Editor", self.main.ui_back),
                        ("Back to Menu", to_menu),
                        ("Test Map", to_test)]
        self.button_size = max(map(lambda (t, _): SMALL_FONT.size(t)[0], self.options))
        self.w = self.button_size + BUTTON_TEXT_SPACER * 2
        self.h = SMALL_FONT.get_linesize() + BUTTON_TEXT_SPACER * 2

        self._save_success = None
        self.save_surf = pygame.Surface((SCREEN_SIZE[0], SMALL_FONT.get_linesize()))

        self.redraw_success()
        self.redraw()

    def set_success(self, value):
        if self._save_success is not value:
            self._save_success = value
            self.redraw_success()

    save_success = property(lambda self: self._save_success, set_success)

    def redraw_text(self):
        rect = ((20, TEXT_BOX_Y), (300, 25))
        self.surface.fill((0xFF, ) * 3, rect)
        pygame.draw.rect(self.surface, (0, )* 3, rect, 2)
        text = SMALL_FONT.render(self.text, True, (0, ) * 3)
        self.surface.blit(text, (25, TEXT_BOX_Y + 5),
            ((max(0, text.get_width() - rect[1][0] + 10), 0), (rect[1][0] - 10, rect[1][1])))

    def redraw_success(self):
        self.save_surf.fill((0xFF, ) * 3)
        if self.save_success is not None:
            if self.save_success:
                words = "Level saved!"
                color = SUCCESS_COLOR
            else:
                words = "Invalid level name"
                color = FAILURE_COLOR
            self.save_surf.blit(SMALL_FONT.render(words, True, color), (0, 0))

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        self.surface.blit(BIG_FONT.render("Save your level!", True, (0, ) * 3),
            (20, TOP_TEXT_Y))
        for i, (x, _) in enumerate(self.options):
            self.draw_button(x, (i % BUTTONS_ACROSS, i // BUTTONS_ACROSS))
        self.redraw_text()

    def draw_button(self, words, (x, y)):
        txt = SMALL_FONT.render(words, True, (0, ) * 3)
        center = (self.w - txt.get_width()) // 2
        px = BUTTON_X + x * (self.w + BUTTON_SPACER)
        py = BUTTON_Y + y * (self.h + BUTTON_SPACER)
        rect = ((px, py), (self.w, self.h))
        self.surface.fill((0xEE, ) * 3, rect)
        pygame.draw.rect(self.surface, (0, ) * 3, rect, 2)
        self.surface.blit(txt, (center + px, BUTTON_TEXT_SPACER + py))

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        surf.blit(self.save_surf, (15, 100))

    def handle_click(self, event):
        self.save_success = None
        ex, ey = event.pos
        px = ex - BUTTON_X
        py = ey - BUTTON_Y
        count = 0
        if 0 <= px % (self.w + BUTTON_SPACER) < self.w:
            q = px // (self.w + BUTTON_SPACER)
            if q >= BUTTONS_ACROSS:
                return
            count += q
            if 0 <= py % (self.h + BUTTON_SPACER) < self.h:
                count += BUTTONS_ACROSS * (py // (self.h + BUTTON_SPACER))
                if 0 <= count < len(self.options):
                    self.options[count][1]()

    def handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self.main.ui_back()
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            self.save_success = None
            self.redraw_text()
        if valid_file_char(event.unicode):
            self.text += event.unicode
            self.save_success = None
            self.redraw_text()

    def normalize(self):
        self.dx, self.dy = self.board.normalize()
        self.start.x -= self.dx
        self.start.y -= self.dy

    def save_level(self, draft=False):
        def anon():
            self.normalize()
            text = self.text.replace(" ", "_")
            if draft:
                self.save_success = LevelSave.save_draft(text, self.board, self.start)
            else:
                self.save_success = LevelSave.save_level(text, self.board, self.start)
            self.redraw()
        return anon
