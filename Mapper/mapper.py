import pygame

from ui.map_ui import MapUI
from ui.overworld_ui import OverworldUI


class Main:
    def __init__(self):
        pygame.init()

        d = pygame.display.Info()
        self.desktop_size = (d.current_w, d.current_h)
        self.ui = OverworldUI(self, None)
        self.size = (600, 450)  # self.ui.screen_size()

        pygame.display.set_caption("Mapper")

        self.done = False
        self.clock = pygame.time.Clock()
        self.keys = set()

        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0xFF, ) * 3)
        self.last = None

        self.clicked = 0

    def ui_push(self, cls):
        self.ui = cls(self, self.ui)

    def ui_pop(self):
        self.ui = self.ui.parent

    def stop(self):
        self.done = True

    def run(self):
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    self.keys.add(event.key)
                    self.ui.handle_key(event)
                elif event.type == pygame.KEYUP:
                    self.keys.discard(event.key)
                    self.ui.handle_key_up(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicked = True
                        self.ui.handle_click(event)
                    elif event.button in (4, 5):  # scrollin!
                        event.scroll_dir = event.button * 2 - 9
                        self.ui.handle_scroll(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicked = False
                        self.ui.handle_click_up(event)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                        self.ui.handle_drag(event)
                    else:
                        self.ui.handle_motion(event)

            self.screen.fill((0, ) * 3)
            self.ui.update()
            self.ui.reblit(self.screen, self.clock.get_time())
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = Main()
    game.run()
