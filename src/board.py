import pygame


class Board(object):
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(self.size)

    def render(self):
        self.screen.fill((0, 0, 0))

    @staticmethod
    def game_did_end(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
