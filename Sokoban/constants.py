import random
from string import lowercase, uppercase
import pygame

SCREEN_SIZE = (550, 550)
SCREEN_RADIUS = 5

RS = chr(30)
US = chr(31)

def get_you_img():
    you_tiles = pygame.image.load("imgs/you.png")
    TS = 50  # MAGICAL
    you_almost = pygame.Surface((TS, TS), pygame.SRCALPHA)
    you_almost.blit(you_tiles, (0, 0), (0, 0, TS, TS))
    you = pygame.Surface((TS, TS))
    you.fill((0xFF, ) * 3)
    you.blit(pygame.transform.flip(you_almost, True, False), (0, 0))
    you.set_colorkey((0xFF, ) * 3)
    return you

def get_me_img():
    me_tiles = pygame.image.load("imgs/me.png")
    TS = 50  # MAGICAL
    me = pygame.Surface((TS, TS))
    me.fill((0xFF, ) * 3)
    me.blit(me_tiles, (0, 0), (0, 0, TS, TS))
    me.set_colorkey((0xFF, ) * 3)
    return me

def valid_file_char(c):
    return c and (c in (" ()" + lowercase + uppercase + ''.join(map(str, range(10)))))

def get_adjective():
    return random.choice(["valiant", "attractive", "helpful",
                    "lovely", "clever", "intelligent", "brave", "noble",
                    "spunky", "stalwart", "worthy", "audacious", "adventurous",
                    "heroic", "fearless", "steadfast", "admirable", "skillful",
                    "top-notch", "peerless", "incomparable", "invaluable",
                    "distinguished", "astute", "apt", "brilliant",
                    "resourceful", "wise", "spirited", "crafty",
                    "second-to-none", "handy", "perspicacious", "inimitable",
                    "indispensable", "dashing"])

def get_noun():
    return random.choice(["teammate", "cohort", "partner-in-crime",
                "partner", "helper", "aide", "ally", "collaborator",
                "colleague", "assistant", "pal", "compatriot", "companion",
                "buddy", "chum", "accomplice", "confederate",
                "sidekick", "consort", "co-conspirator", "friend",
                "compadre"])
