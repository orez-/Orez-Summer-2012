import ui
from cursor import Cursor
from board import Board


class BattleUI(ui.TacticsUI):
    def __init__(self):
        self.size = (1000, 500)  # gotta find a better way to pass these

        self.cursor = Cursor()
        self.board = Board((20, 20, 30), (40, 20, 10), self.size)
        # TODO: not a fan of the magic numbers

        self.board.set_display_position(*self.cursor.board_pos)

    def redraw(self):
        pass

    def reblit(self, screen):
        self.board.reblit(screen)
        self.cursor.redraw(screen)

    def keydown(self, event):
        if self.cursor.handle_key(event.key, self.board):
            self.board.set_display_position(*self.cursor.board_pos)

    def keep_moving(self):
        if self.cursor.keep_moving():
            self.board.set_display_position(*self.cursor.board_pos)
