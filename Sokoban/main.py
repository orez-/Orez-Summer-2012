import pygame

from ui.menu_ui import MenuUI
from ui.game_ui import GameUI
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

    def change_screen(self, which):
        if which == "game":
            self.start_server()
            self.ui = GameUI(self, False)
            self.join_server()
        if which == "join":
            self.ui = GameUI(self, True)
            self.join_server()

    def send_msg(self, msg):
        self.client.send(msg)

    def join_server(self):
        self.client = Client(self)
        self.client.start()

    def stop(self):
        self.done = True
        if self.server is not None:
            self.server.stop()
        if self.client is not None:
            self.client.stop()

    def run(self):
        restart = False
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    self.ui.handle_key(event)
                    if event.key == pygame.K_r:
                        self.ui = GameUI(self)
                elif event.type == pygame.KEYUP:
                    pass

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