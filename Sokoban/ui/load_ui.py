import pygame
from os import listdir
from os.path import isfile, join

from ui import UI
from constants import SCREEN_SIZE, valid_file_char, get_me_img, get_you_img
from level_save import LevelLoad

SMALL_FONT = pygame.font.Font(None, 25)
WIDTH = 250
HEIGHT = SCREEN_SIZE[1] - 70
SPACER = 5

BOX_X = (SCREEN_SIZE[0] - WIDTH) // 2
BOX_Y = 10
#BOX_Y = (SCREEN_SIZE[1] - HEIGHT) // 2

TAB_OVERFLOW = 10  # on each side
TAB_HEIGHT = SMALL_FONT.get_linesize() + SPACER * 2

I_WIDTH = WIDTH - SPACER * 2
I_HEIGHT = SMALL_FONT.get_linesize() + SPACER * 2

R_WIDTH = WIDTH - SPACER * 2
R_HEIGHT = HEIGHT - SPACER * 3 - TAB_HEIGHT - I_HEIGHT

HILITE_COLOR = (0x00, 0x80, 0xFF)


class LoadEditorUI(UI):
    def __init__(self, main, parent):
        super(LoadEditorUI, self).__init__(main, parent)
        self.load_box = LoadBox(
            [["Maps", (0xD6, ) * 3, "maps"],
             ["Drafts", (0xBB, ) * 3, "draft"]])
        self.surface = pygame.Surface(SCREEN_SIZE)

        self.redraw()

    def redraw(self):
        self.surface.fill((0xEE, ) * 3)

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        self.load_box.reblit(surf)

    def handle_key(self, event):
        if event.key == pygame.K_TAB:
            self.load_box.cur_tab ^= 1
            self.load_box.reload_files()
            self.load_box.redraw()
        if valid_file_char(event.unicode):
            self.load_box.add_char(event.unicode)
        if event.key == pygame.K_BACKSPACE:
            self.load_box.del_char()
        if event.key == pygame.K_UP:
            self.load_box.up_key()
        if event.key == pygame.K_DOWN:
            self.load_box.down_key()
        if event.key == pygame.K_RETURN:
            filename = self.load_box.load_results.files[
                self.load_box.load_results.selection]
            full_filename = self.load_box.tab_data[2] + "/" + filename + ".skb"
            start, board = LevelLoad.load(full_filename)
            board.stuff.show_numbers = True
            board.redraw()
            self.parent.set_start(start)
            self.parent.board = board
            self.parent.view[:] = start
            self.dx, self.dy = (0, 0)
            self.main.ui_back()


class LoadUI(UI):
    def __init__(self, main, parent):
        super(LoadUI, self).__init__(main, parent)
        self.load_box = LoadBox(
            [["Maps", (0xD6, ) * 3, "maps"]])
        self.surface = pygame.Surface(SCREEN_SIZE)

        self.suggest_text = ""
        self.suggest_surf = pygame.Surface((SCREEN_SIZE[0], SMALL_FONT.get_linesize()))
        self.suggest_data = None

        self.me = get_me_img()
        self.you = get_you_img()
        self.redraw_suggest()
        self.redraw()

    def redraw(self):
        self.surface.fill((0xEE, ) * 3)
        self.surface.blit(self.me, (50, 300))
        self.surface.blit(self.you, (450, 300))

    def reblit(self, surf):
        surf.blit(self.surface, (0, 0))
        self.load_box.reblit(surf)
        self.surface.blit(self.suggest_surf, (5, 520))

    def redraw_suggest(self):
        self.suggest_surf.fill((0xEE, ) * 3)
        self.suggest_surf.blit(
            SMALL_FONT.render(self.suggest_text, True, (0, ) * 3), (0, 0))

    def handle_key(self, event):
        #if event.key == pygame.K_TAB:
        #    self.load_box.cur_tab ^= 1
        #    self.load_box.reload_files()
        #    self.load_box.redraw()
        if valid_file_char(event.unicode):
            self.load_box.add_char(event.unicode)
        elif event.key == pygame.K_BACKSPACE:
            self.load_box.del_char()
        elif event.key == pygame.K_UP:
            self.load_box.up_key()
        elif event.key == pygame.K_DOWN:
            self.load_box.down_key()
        elif event.key == pygame.K_RETURN:
            filename = self.load_box.load_results.files[
                self.load_box.load_results.selection]
            dec_filename = "maps/" + filename + ".skb"
            self.main.send_msg("LEVELOFF " + filename + " " +
                LevelLoad.check_hash(dec_filename))
        elif event.key == pygame.K_TAB:
            print self.suggest_data
            if self.suggest_data is not None:  # accept the suggestion
                self.main.send_msg("LEVELACC " + ' '.join(self.suggest_data))

    def set_suggestion(self, filename, hashh):
        self.suggest_data = ("0", filename, hashh)
        dec_filename = "maps/" + filename + ".skb"
        print "BEFORE", filename
        _filename = filename.replace("_", " ")
        print "AFTER", filename
        self.suggest_text = "How about '" + _filename + "'"
        if LevelLoad.file_exists(dec_filename):  # I have this file...
            if not LevelLoad.check_hash(dec_filename, hashh):  # and it's not the same
                self.suggest_data = ("1", filename, hashh)
                self.suggest_text = "How about my version of '" + _filename + "'"
        else:
            self.suggest_data = ("1", filename, hashh)
        print "!", self.suggest_data
        self.redraw_suggest()
        print "?", self.suggest_data
        print "-", self.suggest_text


class LoadBox(object):
    def __init__(self, tabs):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.tabs = tabs
        self._cur_tab = 0
        self.tab_data = self.tabs[self._cur_tab]

        TAB_WIDTH = (WIDTH - TAB_OVERFLOW * (len(self.tabs) + 1)) // len(self.tabs) - 2
        self.tab_shape = [(0, TAB_HEIGHT), (0, TAB_OVERFLOW),
            (TAB_OVERFLOW, 0), (TAB_WIDTH + TAB_OVERFLOW, 0),
            (TAB_WIDTH + TAB_OVERFLOW * 2, TAB_OVERFLOW),
            (TAB_WIDTH + TAB_OVERFLOW * 2, TAB_HEIGHT)]
        self.TAB_WIDTH = TAB_WIDTH + 2  # only the meat

        self.load_results = LoadResults()
        self.load_input = LoadInput()
        self.redraw()

    def down_key(self):
        if self.load_results.selection < len(self.load_results.files) - 1:
            self.load_results.selection += 1

    def up_key(self):
        if self.load_results.selection > 0:
            self.load_results.selection -= 1

    def add_char(self, char):
        self.load_input.text += char
        self.load_results.prefix = self.load_input.text
        self.set_to_prefix()

    def del_char(self):
        self.load_input.text = self.load_input.text[:-1]
        self.load_results.prefix = self.load_input.text

    def set_curtab(self, value):
        self._cur_tab = value
        self.tab_data = self.tabs[self._cur_tab]

    cur_tab = property(lambda self: self._cur_tab, set_curtab)

    def reload_files(self):
        self.load_results.get_files(self.tab_data[2])
        self.load_results.selection = 0
        self.set_to_prefix()

    def set_to_prefix(self):
        top, bot = self.load_results.letter_limits
        if not (top < self.load_results.selection < bot):
            self.load_results.selection = self.load_results.letter_limits[0]

    def draw_tab(self, surf, which):
        x = (self.TAB_WIDTH + TAB_OVERFLOW) * which
        y = 0
        shape = map(lambda (tx, ty): (tx + x, ty + y), self.tab_shape)
        pygame.draw.polygon(surf, self.tabs[which][1], shape)
        pygame.draw.lines(surf, (0, ) * 3, which != self._cur_tab, shape, 2)

        text = SMALL_FONT.render(self.tabs[which][0], True, (0, ) * 3)
        #tx = x + TAB_OVERFLOW + SPACER  # left justified
        tx = x + TAB_OVERFLOW + (self.TAB_WIDTH - text.get_width()) // 2  # centered
        surf.blit(text, (tx, y + SPACER))

    def redraw_base(self):
        self.surface.fill((0xEE, ) * 3)
        for i, x in enumerate(self.tabs):
            if i != self.cur_tab:
                self.draw_tab(self.surface, i)
        self.draw_tab(self.surface, self.cur_tab)  # I go last.
        self.surface.fill(self.tab_data[1],
            ((0, TAB_HEIGHT + 1), (WIDTH, HEIGHT - TAB_HEIGHT - 1)))
        pygame.draw.lines(self.surface, (0, ) * 3, False,
            [(0, TAB_HEIGHT), (0, HEIGHT - 2),
             (WIDTH - 2, HEIGHT - 2), (WIDTH - 2, TAB_HEIGHT)], 2)

    def redraw(self):
        self.redraw_base()

    def reblit(self, surf):
        surf.blit(self.surface, (BOX_X, BOX_Y))
        self.load_results.reblit(surf)
        self.load_input.reblit(surf)


class LoadResults(object):
    def __init__(self):
        self.surface = pygame.Surface((R_WIDTH, R_HEIGHT))
        self.files = []
        # self.limited_files = []
        self._prefix = ""
        self.selection = 0

        self.letter_limits = []

        self.hilite = pygame.Surface((R_WIDTH - SPACER + 1, SMALL_FONT.get_linesize() + SPACER - 2))
        self.hilite.fill(HILITE_COLOR)
        self.hilite.set_alpha(64)
        self.get_files("maps")

    def set_prefix(self, value):
        self._prefix = value.lower()  #.replace(" ", "_")
        self.redraw()

    prefix = property(lambda self: self._prefix, set_prefix)

    def get_files(self, mypath):
        #self.selection = 0
        #self.files = filter(lambda f: f[-4:] == ".skb" and isfile(join(mypath, f)), listdir(mypath))
        self.files = [f[:-4] for f in listdir(mypath)
                        if f[-4:] == ".skb" and isfile(join(mypath, f))]
        self.redraw()

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        pygame.draw.rect(self.surface, (0, ) * 3,
            ((0, 0), (R_WIDTH, R_HEIGHT)), 3)

        top = None
        bot = None
        for i, txt in enumerate(self.files):
            txt = txt.replace("_", " ")
            if txt[:len(self.prefix)].lower() == self._prefix:
                if top is None:
                    top = i
                color = (0, ) * 3
            else:
                if top is not None and bot is None:
                    bot = i
                color = (0x99, ) * 3
            self.surface.blit(SMALL_FONT.render(txt, True, color),
                (SPACER, SPACER + i * SMALL_FONT.get_linesize()))

        if top is None:
            top = 0

        if bot is None:
            bot = len(self.files) - 1
        self.letter_limits = [top, bot]

    def reblit(self, surf):
        surf.blit(self.surface, (SPACER + BOX_X, TAB_HEIGHT + SPACER + BOX_Y))
        surf.blit(self.hilite, (2 + BOX_X + SPACER,
            2 + BOX_Y + SPACER + TAB_HEIGHT + self.selection * SMALL_FONT.get_linesize()))


class LoadInput(object):
    def __init__(self):
        self.surface = pygame.Surface((R_WIDTH, TAB_HEIGHT))
        self._text = ""

        self.redraw()

    def set_text(self, value):
        self._text = value
        self.redraw()

    text = property(lambda self: self._text, set_text)

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        pygame.draw.rect(self.surface, (0, ) * 3,
            ((0, 0), (I_WIDTH, I_HEIGHT)), 3)
        self.surface.blit(SMALL_FONT.render(self._text, True, (0, ) * 3),
            (SPACER, SPACER))

    def reblit(self, surf):
        surf.blit(self.surface,
            (SPACER + BOX_X, HEIGHT - I_HEIGHT - SPACER + BOX_Y))
