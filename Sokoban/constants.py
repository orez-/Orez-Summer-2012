import random

SCREEN_SIZE = (550, 550)
SCREEN_RADIUS = 5

RS = chr(30)
US = chr(31)

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
