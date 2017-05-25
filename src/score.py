import pygame


class Score(object):
    def __init__(self, board, reset_key=pygame.K_r):
        self.defaultFont = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.defaultFont, 50)

        self.resetKey = reset_key
        self.player1 = 0
        self.player2 = 0

        self.board = board

    def render(self):
        message = self.font.render(str(self.player1) + "  |  " + str(self.player2), True, (255, 255, 255))
        x = message.get_rect().width
        self.board.screen.blit(message, (int(self.board.size[0] / 2) - int(x / 2), 0))

    def did_reset(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.resetKey:
            self.player1 = 0
            self.player2 = 0
