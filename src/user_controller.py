from pygame.locals import KEYDOWN, K_DOWN, K_UP, KEYUP


class UserController(object):
    def __init__(self, paddle, up=K_UP, down=K_DOWN):
        self.paddle = paddle
        self.up = up
        self.down = down

    def did_paddle_move(self, event, ball):
        if event is None:
            return

        if event.type == KEYDOWN:
            if event.key == self.up:
                self.paddle.direction = -1
            elif event.key == self.down:
                self.paddle.direction = 1

        if event.type == KEYUP:
            if event.key == self.up and self.paddle.direction == -1 or \
                                    event.key == self.down and self.paddle.direction == 1:
                self.paddle.direction = 0
