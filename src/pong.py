import pygame

from models.board import Board
from models.score import Score
from models.paddle import Paddle
from models.ball import Ball
from repositories.settings_repository import SettingsRepository
from ui.settings_dialog import SettingsDialog


class Pong:

    def __init__(self):
        self.settingsRepository = SettingsRepository('settings.bin')
        self.setting = self.settingsRepository.read()
        self.settingsDialog = SettingsDialog(self.setting)

        pygame.init()
        pygame.display.set_caption('Pong')

        self.board = Board((self.setting.boardWidth, self.setting.boardHeight))
        self.score = Score(self.board)
        self.ball = Ball(self.board)
        self.paddle1 = Paddle(self.board)
        self.paddle2 = Paddle(self.board, left=False)

        self.userPlayer1Controller = self.setting.get_controller1(self.paddle1)
        self.userPlayer2Controller = self.setting.get_controller2(self.paddle2)

        self.gameOn = False

    def game_on(self):
        self.gameOn = True
        self.game_loop()

    def game_off(self):
        self.gameOn = False

    def game_loop(self):
        while self.gameOn:
            self.event_check()

            self.userPlayer1Controller.did_paddle_move_alone(self.ball)
            self.userPlayer2Controller.did_paddle_move_alone(self.ball)

            self.ball.did_hit(self.paddle1)
            self.ball.did_hit(self.paddle2)

            self.score.player1 += self.paddle2.did_miss(self.ball)
            self.score.player2 += self.paddle1.did_miss(self.ball)

            self.board.render()
            self.score.render()
            self.ball.render()
            self.paddle1.render()
            self.paddle2.render()

            pygame.display.flip()

            image_data = pygame.surfarray.array3d(pygame.display.get_surface())

            self.userPlayer1Controller.learn(image_data, self.score)
            self.userPlayer2Controller.learn(image_data, self.score)

    def event_check(self):
        for event in pygame.event.get():
            self.score.did_reset(event)
            self.board.game_did_end(event)
            self.ball.did_restart(event)
            self.userPlayer1Controller.did_paddle_move(event, self.ball)
            self.userPlayer2Controller.did_paddle_move(event, self.ball)
            self.settingsDialog.should_display(event, self.setting)


pong = Pong()
pong.game_on()