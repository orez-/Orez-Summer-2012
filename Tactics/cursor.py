import pygame

STEP = .125  # careful with floating point rounding for now
UP, RIGHT, DOWN, LEFT = (2 ** i for i in xrange(4))
DIRECTION = {UP: (0, 1), LEFT: (1, 0),
             DOWN: (0, -1), RIGHT: (-1, 0)}


class Cursor:
    def __init__(self, unit=None):
        self.unit = unit
        self.board_pos = [0, 0]
        self.moving = 0

    def keep_moving(self):
        if self.moving:
            cx, cy = map(lambda x: STEP * x, DIRECTION[self.moving])

            if ((int(self.board_pos[0]) != int(self.board_pos[0] + cx) or (cx and self.board_pos[0] * (self.board_pos[0] + cx) <= 0)) or
                (int(self.board_pos[1]) != int(self.board_pos[1] + cy) or (cy and self.board_pos[1] * (self.board_pos[1] + cy) <= 0))):
            #if ((int(self.board_pos[0]) != int(self.board_pos[0] + cx)) or
            #    (int(self.board_pos[1]) != int(self.board_pos[1] + cy))):
            #if map(int, self.board_pos) == self.board_pos:
                self.moving = 0
                self.board_pos[0] = int(round(self.board_pos[0] + cx))
                self.board_pos[1] = int(round(self.board_pos[1] + cy))
                return False
            else:
                self.board_pos[0] += cx
                self.board_pos[1] += cy
            return self.board_pos
        return False

    def set_unit_here(self):
        return self.board_pos + [self.unit]

    def reblit(self, screen):
        size = (1000, 500)   # TODO: unacceptable
        pygame.draw.polygon(screen, (0xFF, ) * 3,
            [(int((size[0] / 2) - 20), int((size[1] / 2) + 5)),
             (int(size[0] / 2),      int((size[1] / 2) - 5)),
             (int((size[0] / 2) + 20), int((size[1] / 2) + 5)),
             (int(size[0] / 2),      int((size[1] / 2) + 15))], 3)

    def set_moving(self, direction):
        self.moving = direction
        cx, cy = map(lambda x: STEP * x, DIRECTION[self.moving])
        self.board_pos[0] += cx
        self.board_pos[1] += cy
        if self.unit is not None:
            self.unit.tile.unit = None
            self.unit.tile = None

    def handle_key(self, key, board):
        cx, cy = self.board_pos
        if not self.moving:  # can't go if you ARE moving
            if key == pygame.K_w:
                if cy != board.chunk[1] - 1:
                    self.set_moving(UP)
                    return True
            elif key == pygame.K_a:
                if cx != board.chunk[0] - 1:
                    self.set_moving(LEFT)
                    return True
            elif key == pygame.K_s:
                if cy != 0:
                    self.set_moving(DOWN)
                    return True
            elif key == pygame.K_d:
                if cx != 0:
                    self.set_moving(RIGHT)
                    return True
            elif key == pygame.K_SPACE:
                board.select_square(*self.board_pos)
        return False
