class LogicalController(object):
    def __init__(self, paddle):
        self.paddle = paddle
        self.speed = 2

    def did_paddle_move(self, event, ball):
        pass

    def did_paddle_move_alone(self, ball):
        if self.paddle.rect.center[1] < ball.rect.center[1]:
            self.paddle.direction = 1
        elif self.paddle.rect.center[1] > ball.rect.center[1]:
            self.paddle.direction = -1

    def should_learn(self, event):
        pass

    def learn(self, data, score):
        pass

    def resign(self):
        pass
