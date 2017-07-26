class LogicalController(object):
    def __init__(self, paddle):
        self.paddle = paddle
        self.speed = 2

    def did_paddle_move(self, event, ball):
        pass

    def did_paddle_move_alone(self, ball):
        if self.paddle.rect.center[1] < ball.rect.center[1]:
            self.paddle.direction = 1
        else:
            self.paddle.direction = -1

    def learn(self, data, score):
        pass