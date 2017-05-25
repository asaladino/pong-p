class LogicalController(object):
    def __init__(self, paddle):
        self.paddle = paddle
        self.speed = 2

    def did_paddle_move(self, event, ball):
        if event is not None:
            return
        if self.paddle.rect.center[1] < ball.rect.center[1]:
            self.paddle.direction = 1
        else:
            self.paddle.direction = -1
