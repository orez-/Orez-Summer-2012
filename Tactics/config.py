import pygame


class Config(object):
    CONTROLLER_MODE = 1
    KEYBOARD_MODE = 2
    def __init__(self):
        self.keymode = Config.CONTROLLER_MODE

        self.K_UP1 = pygame.K_UP
        self.K_UP2 = pygame.K_w

        self.K_LEFT1 = pygame.K_LEFT
        self.K_LEFT2 = pygame.K_a

        self.K_RIGHT1 = pygame.K_RIGHT
        self.K_RIGHT2 = pygame.K_d

        self.K_DOWN1 = pygame.K_DOWN
        self.K_DOWN2 = pygame.K_s

        self.K_OK1 = pygame.K_z
        self.K_OK2 = pygame.K_SPACE

        self.K_CANCEL1 = pygame.K_x
        self.K_CANCEL2 = None

        self.K_PAUSE1 = pygame.K_RETURN
        self.K_PAUSE2 = None

    def _check_key(self, event, keys):
        s = filter(lambda k: k is not None, keys)
        return event in s or event.key in s

    def k_UP(self, event):
        return self._check_key(event, (self.K_UP1, self.K_UP2))

    def k_LEFT(self, event):
        return self._check_key(event, (self.K_LEFT1, self.K_LEFT2))

    def k_RIGHT(self, event):
        return self._check_key(event, (self.K_RIGHT1, self.K_RIGHT2))

    def k_DOWN(self, event):
        return self._check_key(event, (self.K_DOWN1, self.K_DOWN2))

    def k_OK(self, event):
        return self._check_key(event, (self.K_OK1, self.K_OK2))

    def k_CANCEL(self, event):
        """ User pressed the 'cancel' key """
        return self._check_key(event, (self.K_CANCEL1, self.K_CANCEL2))

    def k_PAUSE(self, event):
        """ User pressed the 'pause' key """
        return self._check_key(event, (self.K_PAUSE1, self.K_PAUSE2))

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
        pass