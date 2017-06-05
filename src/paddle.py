import pygame


class Paddle(object):
    def __init__(self, board, left=True):
        self.board = board
        self.height = 100
        self.width = 10
        self.left = left

        if left:
            self.centerX = self.width / 2
        else:
            self.centerX = self.board.size[0] - self.width / 2

        self.centerY = int(self.board.size[1] * 0.5)

        if left:
            self.rect = pygame.Rect(0, self.centerY - int(self.height * 0.5), self.width, self.height)
        else:
            self.rect = pygame.Rect(self.board.size[0] - self.width, self.centerY - int(self.height * 0.5),
                                    self.width, self.height)

        self.color = (255, 255, 255)

        self.speed = 3
        self.direction = 0  # don't want it to move on its own

    def update(self):
        self.centerY += self.direction * self.speed
        self.rect.center = (self.centerX, self.centerY)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.board.size[1] - 1:
            self.rect.bottom = self.board.size[1] - 1

    def render(self):
        self.update()
        pygame.draw.rect(self.board.screen, self.color, self.rect, 0)

    def did_miss(self, ball):
        if self.left and ball.rect.left < 0:
            # ball.start_position()
            return 1
        elif not self.left and ball.rect.right > self.board.size[0]:
            # ball.start_position()
            return 1
        return 0
