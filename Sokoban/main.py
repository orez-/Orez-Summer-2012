import pygame

from ui.menu_ui import MenuUI
from ui.game_ui import GameUI
from ui.wait_ui import WaitUI
from ui.editor_ui import EditorUI
from ui.save_ui import SaveUI
from ui.load_ui import LoadUI
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

        self.ui = MenuUI(self, None)
        self.server = None
        self.client = None

        self.clicked = 0

    def start_server(self):
        self.server = Server()
        self.server.start()

    def restart(self):
        self.ui = self.ui.reload_level()

    def ui_back(self):
        """ Set the current ui-view to its parent, discarding the current """
        if self.ui.parent is not None:
            child = self.ui
            self.ui = self.ui.parent
            self.ui.on_reentry(child)

    def push_ui(self, cls, *args, **kwargs):
        """ Push the new UI onto the old one. """
        self.ui = cls(self, self.ui, *args, **kwargs)

    def change_screen(self, which, **kwargs):
        if which == "editor":
            self.push_ui(EditorUI)
        elif which == "game":
            self.push_ui(GameUI)
            #self.ui = GameUI(self, self.ui.player2)  # oh dis is bad.
        elif which == "host":
            self.start_server()
            self.push_ui(WaitUI, False)
            self.join_server()
        elif which == "join":
            self.push_ui(LoadUI)
            #self.push_ui(WaitUI, True)
            #self.join_server()
        elif which == "no connect":
            self.ui_back()
            self.ui.set_message("Couldn't connect")
        elif which == "save":
            self.push_ui(SaveUI)
        else:
            raise ValueError("I don't know the class "+str(which))

    def send_msg(self, msg):
        self.client.send(msg)

    def join_server(self):
        self.client = Client(self)
        self.client.start()

    def stop_multiplayer(self):
        if self.server is not None:
            self.server.stop()
            self.server = None
        if self.client is not None:
            self.client.stop()
            self.client = None

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
                    self.clicked = True
                    self.ui.handle_click(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = False
                    self.ui.handle_click_up(event)
                elif event.type == pygame.MOUSEMOTION:
                    if self.clicked:
                        self.ui.handle_drag(event)
                    else:
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