import pygame
from random import randint


class Ball:
    def __init__(self, board, restart_key=pygame.K_SPACE, auto_play_key=pygame.K_c, pause_key=pygame.K_p):
        self.rect = pygame.Rect(20, randint(20, board.size[1] - 20), 20, 20)
        self.color = (0, 128, 255)
        self.colorAutoPlay = (255, 0, 0)
        self.speed = [0, 0]
        self.board = board
        self.restartKey = restart_key
        self.autoPlayKey = auto_play_key
        self.pauseKey = pause_key
        self.autoPlay = False
        self.isPaused = False
        self.pausedSpeed = self.speed

    def initialize(self):
        self.start_position()
        self.color = (0, 128, 255)
        self.speed = [1, 1]

    def start_position(self):
        self.rect = pygame.Rect(20, randint(20, self.board.size[1] - 20), 20, 20)
        self.speed = [0, 0]
        if self.autoPlay:
            self.color = (0, 128, 255)
            self.speed = [1, 1]

    def paddle_missed(self):
        self.speed[0] = -self.speed[0]

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top < 0 or self.rect.bottom > self.board.size[1]:
            self.speed[1] = -self.speed[1]

        if self.autoPlay and (self.rect.left < 0 or self.rect.right > self.board.size[0]):
            self.speed[0] = -self.speed[0]

    def render(self):
        self.update()
        screen = self.board.screen
        pygame.draw.circle(screen, self.ball_color(),
                           (int(self.rect.centerx), int(self.rect.centery)),
                           int(self.rect.width / 2), 0)

    def did_hit(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed[0] = -self.speed[0]
            return 1
        return 0

    def did_pause(self):
        if self.isPaused:
            self.speed = self.pausedSpeed
        else:
            self.pausedSpeed = self.speed
            self.speed = [0, 0]
        self.isPaused = not self.isPaused

    def event_check(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.pauseKey:
            self.did_pause()
        if event.type == pygame.KEYDOWN and event.key == self.restartKey:
            self.initialize()
        if event.type == pygame.KEYDOWN and event.key == self.autoPlayKey:
            self.autoPlay = not self.autoPlay

    def ball_color(self):
        return self.colorAutoPlay if self.autoPlay else self.color
