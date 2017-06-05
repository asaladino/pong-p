import pygame
from pygame.locals import K_q, K_a

import ball
import board
import paddle
import score
from controllers import user_controller, logical_controller, neural_network_controller

pygame.init()
pygame.display.set_caption('Pong')

board = board.Board((640, 480))
score = score.Score(board)
ball = ball.Ball(board)
paddle1 = paddle.Paddle(board)
paddle2 = paddle.Paddle(board, left=False)

# userPlayer1Controller = neural_network_controller.NeuralNetworkController(paddle1)
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

    userPlayer1Controller.did_paddle_move_alone(ball)
    userPlayer2Controller.did_paddle_move_alone(ball)

    ball.did_hit(paddle1)
    ball.did_hit(paddle2)

    score.player1 += paddle2.did_miss(ball)
    score.player2 += paddle1.did_miss(ball)

    board.render()
    score.render()
    ball.render()
    paddle1.render()
    paddle2.render()

    pygame.display.flip()

    image_data = pygame.surfarray.array3d(pygame.display.get_surface())

    userPlayer1Controller.learn(image_data, score)
    userPlayer2Controller.learn(image_data, score)
