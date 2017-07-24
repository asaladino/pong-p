import pygame

from models import score, ball, board, paddle, setting
from ui import settings_dialog

setting = setting.Setting()
settingsDialog = settings_dialog.SettingsDialog()

pygame.init()
pygame.display.set_caption('Pong')

board = board.Board((setting.boardWidth, setting.boardHeight))
score = score.Score(board)
ball = ball.Ball(board)
paddle1 = paddle.Paddle(board)
paddle2 = paddle.Paddle(board, left=False)

userPlayer1Controller = setting.get_controller1(paddle1)
userPlayer2Controller = setting.get_controller2(paddle2)

while True:
    for event in pygame.event.get():
        score.did_reset(event)
        board.game_did_end(event)
        ball.did_restart(event)
        userPlayer1Controller.did_paddle_move(event, ball)
        userPlayer2Controller.did_paddle_move(event, ball)
        settingsDialog.should_display(event)

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
