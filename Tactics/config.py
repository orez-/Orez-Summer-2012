import pygame


class Config(object):
    CONTROLLER_MODE = 1
    KEYBOARD_MODE = 2

    def __init__(self):
        self.keymode = Config.CONTROLLER_MODE

        K_UP1 = pygame.K_UP
        K_UP2 = pygame.K_w

        K_LEFT1 = pygame.K_LEFT
        K_LEFT2 = pygame.K_a

        K_RIGHT1 = pygame.K_RIGHT
        K_RIGHT2 = pygame.K_d

        K_DOWN1 = pygame.K_DOWN
        K_DOWN2 = pygame.K_s

        K_OK1 = pygame.K_z
        K_OK2 = pygame.K_SPACE

        K_CANCEL1 = pygame.K_x
        K_CANCEL2 = None

        K_PAUSE1 = pygame.K_RETURN
        K_PAUSE2 = None

        self.keys = {"up": (K_UP1, K_UP2),
                "left": (K_LEFT1, K_LEFT2),
                "right": (K_RIGHT1, K_RIGHT2),
                "down": (K_DOWN1, K_DOWN2),
                "ok": (K_OK1, K_OK2),
                "cancel": (K_CANCEL1, K_CANCEL2),
                "pause": (K_PAUSE1, K_PAUSE2)}

    def clear_key(self, name, num):
        self.set_key(name, num, None)

    def set_key(self, name, num, newkey):
        name = name.lower()
        one, two = self.keys[name]
        if newkey is None:
            if two is None:  # either we're setting None to None or we're
                return       # trying to remove the key entirely
            if not num:
                self.keys[name] = (two, None)
                return
        elif newkey == self.keys[name][not num]:  # if you chose
            self.keys[name] = (two, one)    # swap em
            return
        elif newkey in [i for _, v in self.keys.items() for i in v]:
            return  # already bound
        self.keys[name] = (one, newkey) if num else (newkey, two)

    def get_keys(self, name):
        return self.keys[name.lower()]

    def _check_key(self, event, keyname):
        s = filter(lambda k: k is not None, self.get_keys(keyname))
        return event in s or event.key in s

    def k_UP(self, event):
        return self._check_key(event, "up")

    def k_LEFT(self, event):
        return self._check_key(event, "left")

    def k_RIGHT(self, event):
        return self._check_key(event, "right")

    def k_DOWN(self, event):
        return self._check_key(event, "down")

    def k_OK(self, event):
        return self._check_key(event, "ok")

    def k_CANCEL(self, event):
        """ User pressed the 'cancel' key """
        return self._check_key(event, "cancel")

    def k_PAUSE(self, event):
        """ User pressed the 'pause' key """
        return self._check_key(event, "pause")

    def handle_key(self, event, ui):
        if self.keymode == Config.CONTROLLER_MODE:
            self._handle_controller(event, ui)
        elif self.keymode == Config.KEYBOARD_MODE:
            self._handle_keyboard(event, ui)

    def _handle_controller(self, event, ui):
        if self.k_UP(event):
            ui.k_UP()
        if self.k_DOWN(event):
            ui.k_DOWN()
        if self.k_LEFT(event):
            ui.k_LEFT()
        if self.k_RIGHT(event):
            ui.k_RIGHT()
        if self.k_OK(event):
            ui.k_OK()
        if self.k_CANCEL(event):
            ui.k_CANCEL()
        if self.k_PAUSE(event):
            ui.k_PAUSE()

    def _handle_keyboard(self, event, ui):
        ui.keydown(event)