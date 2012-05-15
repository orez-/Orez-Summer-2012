import ui
from cursor import Cursor
from board import Board


class BattleUI(ui.TacticsUI):
    def __init__(self, *args, **kwargs):
        super(BattleUI, self).__init__(*args, **kwargs)
        self.size = (1000, 500)  # gotta find a better way to pass these

        self.cursor = Cursor()
        self.board = Board((20, 20, 30), (40, 20, 10), self.size)
        # TODO: not a fan of the magic numbers

        self.board.set_display_position(*self.cursor.board_pos)

    def redraw(self):
        pass

    def reblit(self, screen):
        self.board.reblit(screen)
        self.cursor.reblit(screen)

    def keydown(self, event):
        if self.cursor.handle_key(event.key, self.board):
            self.board.set_display_position(*self.cursor.board_pos)

    def k_UP(self):
        if self.cursor.k_UP(self.board):
            self.board.set_display_position(*self.cursor.board_pos)

    def k_DOWN(self):
        if self.cursor.k_DOWN(self.board):
            self.board.set_display_position(*self.cursor.board_pos)

    def k_LEFT(self):
        if self.cursor.k_LEFT(self.board):
            self.board.set_display_position(*self.cursor.board_pos)

    def k_RIGHT(self):
        if self.cursor.k_RIGHT(self.board):
            self.board.set_display_position(*self.cursor.board_pos)

    def k_CANCEL(self):
        pass

    def k_OK(self):
        pass

    def k_PAUSE(self):
        self.main.push_ui("team")

    def keep_moving(self):
        if self.cursor.keep_moving():
            self.board.set_display_position(*self.cursor.board_pos)

    @staticmethod
    def name():
        return "battle"