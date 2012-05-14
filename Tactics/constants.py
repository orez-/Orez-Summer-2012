import pygame

SCREEN_SIZE = (1000, 500)

class Config(object):
    """ Keep variables that may change """
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

    @staticmethod
    def _check_key(event, keys):
        s = filter(lambda k: k is not None, keys)
        return event in s or event.key in s

    @staticmethod
    def k_UP(event):
        return Config._check_key(event, (Config.K_UP1, Config.K_UP2))

    @staticmethod
    def k_LEFT(event):
        return Config._check_key(event, (Config.K_LEFT1, Config.K_LEFT2))

    @staticmethod
    def k_RIGHT(event):
        return Config._check_key(event, (Config.K_RIGHT1, Config.K_RIGHT2))

    @staticmethod
    def k_DOWN(event):
        return Config._check_key(event, (Config.K_DOWN1, Config.K_DOWN2))

    @staticmethod
    def k_OK(event):
        return Config._check_key(event, (Config.K_OK1, Config.K_OK2))

    @staticmethod
    def k_CANCEL(event):
        """ User pressed the 'cancel' key """
        return Config._check_key(event, (Config.K_CANCEL1, Config.K_CANCEL2))