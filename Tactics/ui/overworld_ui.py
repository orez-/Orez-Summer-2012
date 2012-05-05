import ui
from board import Board
from unit import Unit
from cursor import Cursor


class OverworldUI(ui.TacticsUI):
    def __init__(self):
        self.size = (1000, 500)

        self.board = Board((20, 20, 30), (40, 20, 10), self.size)
        player = Unit("trainee")
        self.cursor = Cursor(player)
        self.board.set_unit(0, 0, player)
        self.board.redraw()

        self.board.set_display_position(*self.cursor.board_pos)

    def redraw(self):
        pass

    def reblit(self, screen):
        self.board.reblit(screen)

    def keydown(self, event):
        if self.cursor.handle_key(event.key, self.board):
            self.board.set_display_position(*self.cursor.board_pos)
            self.board.redraw()

    def keep_moving(self):
        if self.cursor.keep_moving():
            self.board.set_display_position(*self.cursor.board_pos)
        elif self.cursor.unit.tile is None:
            self.board.set_unit(*self.cursor.set_unit_here())
            self.board.redraw()
