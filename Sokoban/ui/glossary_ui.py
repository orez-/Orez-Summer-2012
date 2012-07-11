import pygame

from ui import UI
from constants import SCREEN_SIZE, get_me_img, get_you_img
from board import Tile, TileFeature, Button, Beartrap, Snorkel, Timetrap, Walltrap, Helptrap, LaunchSpring, LaunchTarget

DATA = [
         ["Our Heroes",
           [(get_me_img(), "This is player 1. I clearly have a lot to say about him, which is why this line of text is so long."),
            (get_you_img(), "This is player 2")
           ]
         ],
         ["Tiles",
           [(Tile.get_tile(Tile.WALL), "Wall"),
            (Tile.get_tile(Tile.OPEN), "Floor"),
            (Tile.get_tile(Tile.BLOCK), "Block"),
            (Tile.get_tile(Tile.EXIT), "Exit"),
            (Tile.get_tile(Tile.WATER), "Water"),
            (Tile.get_tile(Tile.GRAVEL), "Gravel"),
            (Tile.get_tile(Tile.ICE), "Ice")
           ]
         ],
         ["Features",
           [(Button(None), "Button"),
            (Beartrap(None), "Beartrap"),
            (Snorkel(None), "Snorkel"),
            (Timetrap(None), "Timetrap"),
            (Walltrap(None), "Walltrap"),
            (Helptrap(None), "Help"),
            (LaunchSpring(None), "Spring"),
            (LaunchTarget(None), "Target")
           ]
         ]
       ]

H2 = pygame.font.Font(None, 40)
H3 = pygame.font.Font(None, 30)
H4 = pygame.font.Font(None, 24)

P_SPACER = 5
SPACER = 10
SCROLL_DIST = 30

class GlossaryUI(UI):
    def __init__(self, main, parent):
        super(GlossaryUI, self).__init__(main, parent)
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.scroll = 0

        self.redraw()

    def redraw(self):
        self.surface.fill((0xFF, ) * 3)
        y = SPACER
        for title, section in DATA:
            txt = H2.render(title, True, (0, ) * 3)
            self.double_surface(y + H2.get_linesize())
            self.surface.blit(txt, (SPACER, y))
            y += H2.get_linesize()
            for pic, elem in section:
                wid = SCREEN_SIZE[0] - SPACER * 2
                dx = 0
                if pic is not None:
                    dx = SPACER + 50
                    wid -= dx

                dy, surf = self.draw_text(elem, H4, wid)

                if pic is not None:
                    dy = max(50, dy)
                    self.double_surface(y + dy + P_SPACER)
                    if isinstance(pic, TileFeature):
                        pic.draw(self.surface, SPACER, y)
                    else:
                        self.surface.blit(pic, (SPACER, y))
                self.double_surface(y + dy + P_SPACER)

                self.surface.blit(surf, (SPACER + dx, y))
                y += dy + P_SPACER
        self.max_scroll = (y - SCREEN_SIZE[1]) // SCROLL_DIST

    def double_surface(self, y):
        if y > self.surface.get_height():
            surface = pygame.Surface((SCREEN_SIZE[0], self.surface.get_height() * 2))
            surface.fill((0xFF, ) * 3)
            surface.blit(self.surface, (0, 0))
            self.surface = surface

    @staticmethod
    def draw_text(text, font, width):
        linesize = font.get_linesize()
        lines = []
        buff = ""
        for word in text.split():
            if font.size(buff + word)[0] > width:  # overflow
                lines.append(buff)
                buff = ""
            buff += word + " "
        lines.append(buff)
        height = linesize * len(lines)
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        for i, line in enumerate(lines):
            surf.blit(font.render(line, True, (0, ) * 3), (0, linesize * i))
        return height, surf

    def reblit(self, surf):
        surf.fill((0xFF, ) * 3)
        surf.blit(self.surface, (0, -self.scroll * SCROLL_DIST))

    def handle_key(self, event):
        if event.key == pygame.K_UP:
            if self.scroll > 0:
                self.scroll -= 1
        if event.key == pygame.K_DOWN:
            if self.scroll <= self.max_scroll:
                self.scroll += 1
        if event.key == pygame.K_ESCAPE:
            self.main.ui_back()


class AlignedImage:
    def __init__(self, img):
        pass
