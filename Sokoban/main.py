import pygame

from ui.menu_ui import MenuUI
from ui.game_ui import GameUI
from ui.wait_ui import WaitUI
from ui.editor_ui import EditorUI
from ui.save_ui import SaveUI
from constants import SCREEN_SIZE
from networking import Server, Client


class Main:
    def __init__(self):
        pygame.init()

        d = pygame.display.Info()
        self.desktop_size = (d.current_w, d.current_h)
        self.size = SCREEN_SIZE

        pygame.display.set_caption("Sokorez")

        self.done = False
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.size)

        self.ui = MenuUI(self)
        self.server = None
        self.client = None

    def start_server(self):
        self.server = Server()
        self.server.start()

    def restart(self):
        self.ui = self.ui.reload_level()

    def change_screen(self, which, **kwargs):
        if which == "editor":
            self.ui = EditorUI(self)
        if which == "game":
            self.ui = GameUI(self, self.ui.player2)  # oh dis is bad.
        if which == "host":
            self.start_server()
            self.ui = WaitUI(self, False)
            self.join_server()
        if which == "join":
            self.ui = WaitUI(self, True)
            self.join_server()
        if which == "no connect":
            self.ui = MenuUI(self, "Couldn't connect")
            self.client = None
        if which == "main":
            self.stop_multiplayer()
            self.ui = MenuUI(self)
        if which == "save":
            self.ui = SaveUI(self, kwargs["board"], kwargs["start"])

    def send_msg(self, msg):
        self.client.send(msg)

    def join_server(self):
        self.client = Client(self)
        self.client.start()

    def stop_multiplayer(self):
        if self.server is not None:
            self.server.stop()
        if self.client is not None:
            self.client.stop()

    def stop(self):
        self.done = True
        self.stop_multiplayer()

    def run(self):
        restart = False
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    self.ui.handle_key(event)
                elif event.type == pygame.KEYUP:
                    self.ui.handle_key_up(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.ui.handle_click(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.ui.handle_motion(event)

            #self.ui.keep_moving()
            self.screen.fill((0, ) * 3)
            #self.board.reblit(self.screen)
            #self.player1.reblit(self.screen)
            self.ui.reblit(self.screen)
            pygame.display.flip()
        if restart:
            return True
        pygame.quit()

if __name__ == "__main__":
    game = Main()
    game.run()