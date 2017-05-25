import pygame
from random import randint


class Ball:
    def __init__(self, board, restart_key=pygame.K_SPACE):
        self.rect = pygame.Rect(20, randint(20, board.size[1] - 20), 20, 20)
        self.color = (0, 128, 255)
        self.speed = [0, 0]
        self.board = board
        self.restartKey = restart_key

    def initialize(self):
        self.start_position()
        self.color = (0, 128, 255)
        self.speed = [2, 2]

    def start_position(self):
        self.rect = pygame.Rect(20, randint(20, self.board.size[1] - 20), 20, 20)
        self.speed = [0, 0]

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top < 0 or self.rect.bottom > self.board.size[1]:
            self.speed[1] = -self.speed[1]

    def render(self):
        self.update()
        screen = self.board.screen
        pygame.draw.circle(screen, self.color, (int(self.rect.centerx), int(self.rect.centery)),
                           int(self.rect.width / 2), 0)

    def did_hit(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed[0] = -self.speed[0]

    def did_restart(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.restartKey:
            self.initialize()
