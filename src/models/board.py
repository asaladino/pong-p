import pygame


class Board(object):

    def __init__(self, size):
        """
        Create a new game board.
        :param size: 
        """
        self.size = size
        self.screen = pygame.display.set_mode(self.size)

    def render(self):
        """
        Draws the board on the screen black.
        """
        self.screen.fill((0, 0, 0))

    @staticmethod
    def game_did_end(event):
        """
        Check if the game quit and the app closed.
        :param event: 
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
