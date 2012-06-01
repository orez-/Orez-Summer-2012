import pygame

from board import Board, Player
from constants import SCREEN_SIZE


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
        self.board = Board()
        self.player1 = Player(self.board)

    def run(self):
        restart = False
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player1.move(y=1)
                    if event.key == pygame.K_UP:
                        self.player1.move(y=-1)
                    if event.key == pygame.K_LEFT:
                        self.player1.move(x=-1)
                    if event.key == pygame.K_RIGHT:
                        self.player1.move(x=1)
                    if event.key == pygame.K_r:
                        self.done = True
                        restart = True
                elif event.type == pygame.KEYUP:
                    pass

            #self.ui.keep_moving()
            self.screen.fill((0, ) * 3)
            self.board.reblit(self.screen)
            self.player1.reblit(self.screen)
            pygame.display.flip()
        if restart:
            return True
        pygame.quit()

if __name__ == "__main__":
    game = Main()
    while game.run():   # ghetto, don't keep.
        game = Main()