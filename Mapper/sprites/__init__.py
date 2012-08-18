import pygame


class Sprite(pygame.sprite.DirtySprite):
    """ The sprite class assumes """
    def __init__(self, animations, (x, y)=(0, 0)):
        self.animations = animations

        self.x, self.y = (x, y)

    def set_xy(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    width = property(lambda self: self.size[0])
    height = property(lambda self: self.size[1])
    size = property(lambda self: self.animations.size)
    pos = property(lambda self: (self.x, self.y),
        lambda self, (x, y): set_xy(x=x, y=y))
    center = property(lambda self: (self.centerx, self.centery),
        lambda self, (x, y):
        self.set_xy(x=x - self.width // 2, y=y - self.height // 2))
    centerx = property(lambda self: self.x + self.width // 2,
        lambda self, value: self.set_xy(x=value - self.width // 2))
    centery = property(lambda self: self.y + self.height // 2,
        lambda self, value: self.set_xy(y=value - self.height // 2))
    left = property(lambda self: self.x,
        lambda self, value: self.set_xy(x=value))
    right = property(lambda self: self.x + self.width,
        lambda self, value: self.set_xy(x=value - self.width))
    top = property(lambda self: self.y,
        lambda self, value: self.set_xy(y=value))
    bottom = property(lambda self: self.y + self.height,
        lambda self, value: self.set_xy(y=value - self.height))

    def reblit(self, surf, time_passed, (viewx, viewy)):
        self.animations.pass_time(time_passed)
        self.animations.reblit(surf, (self.x - viewx, self.y - viewy))

    def redraw(self):
        pass


class Animations(object):
    def __init__(self, img_name, size, animations, start):
        self.img = pygame.image.load("imgs/" + img_name + ".png")
        self.size = tuple(size[:])
        self.animations = {k: v for k, v in animations.iteritems()}
        self.set_animation(start)
        self.time = 0

    def set_animation(self, name):
        self.name = name
        self._cur_animation = self.animations[name]()
        self.cur_frame = self._cur_animation.next()

    def set_frame(self, (x, y, t)):
        self._cur_frame = (x * self.size[0], y * self.size[1], t)

    src = property(lambda self: self.cur_frame[:2])
    run_time = property(lambda self: self.cur_frame[2])
    cur_animation = property(lambda self: self._cur_animation, set_animation)
    cur_frame = property(lambda self: self._cur_frame, set_frame)

    def next(self):
        self.cur_frame = self.cur_animation.next()
        while isinstance(self.cur_frame, basestring):
            self.cur_animation = self.cur_frame

    def pass_time(self, time_passed):
        self.time += time_passed
        while self.time >= self.run_time:
            self.time -= self.run_time
            self.next()

    def reblit(self, surf, pos):
        surf.blit(self.img, pos, (self.src, self.size))
