import pygame

STEP = .125  # careful with floating point rounding for now
UP, RIGHT, DOWN, LEFT = (2 ** i for i in xrange(4))
DIRECTION = {UP: (0, 1), LEFT: (1, 0),
             DOWN: (0, -1), RIGHT: (-1, 0)}


class Cursor:
    def __init__(self):
        self.board_pos = [0, 0]
        self.moving = 0

    def keep_moving(self):
        if self.moving:
            cx, cy = map(lambda x: STEP * x, DIRECTION[self.moving])
            self.board_pos[0] += cx
            self.board_pos[1] += cy

            if self.board_pos[0] == int(self.board_pos[0]) and\
               self.board_pos[1] == int(self.board_pos[1]):
                self.moving = 0
            return self.board_pos
        return False

    def redraw(self, screen):
        size = (1000, 500)   # TODO: unacceptable
        pygame.draw.polygon(screen, (0xFF, ) * 3,
            [(int((size[0] / 2) - 20), int((size[1] / 2) + 5)),
             (int(size[0] / 2),      int((size[1] / 2) - 5)),
             (int((size[0] / 2) + 20), int((size[1] / 2) + 5)),
             (int(size[0] / 2),      int((size[1] / 2) + 15))], 3)

    def handle_key(self, key, board):
        cx, cy = self.board_pos
        if not self.moving:  # can't go if you ARE moving
            if key == pygame.K_w:
                if cy != board.chunk[1] - 1:
                    self.moving = UP
                    return True
            elif key == pygame.K_a:
                if cx != board.chunk[0] - 1:
                    self.moving = LEFT
                    return True
            elif key == pygame.K_s:
                if cy != 0:
                    self.moving = DOWN
                    return True
            elif key == pygame.K_d:
                if cx != 0:
                    self.moving = RIGHT
                    return True
            elif key == pygame.K_SPACE:
                board.select_square(*self.board_pos)
        return False
