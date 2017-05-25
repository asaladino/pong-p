# PongP
Pong for python using pygame and hopefully tensorflow.

![alt text](notes/pong.png "PongP")

## Install pygame
```commandline
pip3 install pygame --user
```

## Run pong
```commandline
python3 pong.py
```

## Game Configuration
```python
import board, score, ball, paddle
import user_controller, logical_controller
from pygame.locals import K_q, K_a, K_p, K_l

# Create a board, score and ball
board = board.Board((640, 480))
score = score.Score(board)
ball = ball.Ball(board)

# Add some paddles
paddle1 = paddle.Paddle(board)
paddle2 = paddle.Paddle(board, left=False)

# Controller Setup
# You can setup a different player for each controller.

# Set player 1 as user controlled
userPlayer1Controller = user_controller.UserController(paddle1, up=K_q, down=K_a)
# Set player 1 to use the logical controller.
userPlayer1Controller = logical_controller.LogicalController(paddle1)

# Set player 2 as user controlled
userPlayer2Controller = user_controller.UserController(paddle1, up=K_p, down=K_l)
# Set player 2 to use the logical controller.
userPlayer2Controller = logical_controller.LogicalController(paddle2)

```