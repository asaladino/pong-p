import pygame
from pygame.locals import K_q, K_a

import board
import ball
import score
import paddle
import user_controller
import logical_controller

pygame.init()
pygame.display.set_caption('Pong')

board = board.Board((640, 480))
score = score.Score(board)
ball = ball.Ball(board)
paddle1 = paddle.Paddle(board)
paddle2 = paddle.Paddle(board, left=False)

userPlayer1Controller = user_controller.UserController(paddle1, up=K_q, down=K_a)
# userPlayer1Controller = logical_controller.LogicalController(paddle1)

# userPlayer2Controller = user_controller.UserController(paddle1, up=K_p, down=K_l)
userPlayer2Controller = logical_controller.LogicalController(paddle2)

while True:
    for event in pygame.event.get():
        score.did_reset(event)
        board.game_did_end(event)
        ball.did_restart(event)
        userPlayer1Controller.did_paddle_move(event, ball)
        userPlayer2Controller.did_paddle_move(event, ball)

    userPlayer1Controller.did_paddle_move(None, ball)
    userPlayer2Controller.did_paddle_move(None, ball)

    ball.did_hit(paddle1)
    ball.did_hit(paddle2)

    score.player2 += paddle1.did_miss(ball)
    score.player1 += paddle2.did_miss(ball)

    board.render()
    ball.render()
    paddle1.render()
    paddle2.render()
    score.render()

    pygame.display.flip()
