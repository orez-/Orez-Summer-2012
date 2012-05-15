# THIS FILE IS TERRBILE
import ui
from board import Board
from unit import Unit
from cursor import Cursor
from constants import SCREEN_SIZE

class Stupid:
    pass

class OverworldUI(ui.TacticsUI):
    def __init__(self, *args, **kwargs):
        super(OverworldUI, self).__init__(*args, **kwargs)
        self.size = SCREEN_SIZE

        self.board = Board((20, 20, 30), (40, 20, 10), self.size)
        player = Unit("trainee")
        self.cursor = Cursor(player)
        self.board.set_unit(0, 0, player)
        self.board.redraw()

        self.board.set_display_position(*self.cursor.board_pos)
        self.keys = set()

    def redraw(self):
        pass

    def reblit(self, screen):
        self.board.reblit(screen)

    def keydown(self, event):
        if self.cursor.handle_key(event.key, self.board):
            self.board.set_display_position(*self.cursor.board_pos)
            self.board.redraw()
            self.keys.add(event.key)

    def keyup(self, event):
        self.keys.discard(event.key)

    def keep_moving(self):
        if self.cursor.keep_moving():
            self.board.set_display_position(*self.cursor.board_pos)
        elif self.cursor.unit.tile is None:
            self.board.set_unit(*self.cursor.set_unit_here())
            self.board.redraw()
            try:
                e = self.keys.pop()
                self.keys.add(e)
                x = Stupid()
                x.key = e
                self.keydown(x)
            except KeyError:
                print "no key"

    @staticmethod
    def name():
        return "overworld"