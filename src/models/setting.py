from enum import Enum

from pygame.constants import K_q, K_a

from controllers import user_controller, neural_network_controller, logical_controller


class ControllerTypes(Enum):
    USER = "User"
    LOGICAL_AI = "Logical AI"
    LEARNING_AI = "Learning AI"


class Setting:
    def __init__(self):
        self.boardWidth = 80
        self.boardHeight = 80

        self.controller1 = ControllerTypes.USER
        self.controller1Up = K_q
        self.controller1Down = K_a

        self.controller2 = ControllerTypes.LOGICAL_AI
        self.controller2Up = K_q
        self.controller2Down = K_a

    def get_controller1(self, paddle):
        if self.controller1 is ControllerTypes.USER:
            return user_controller.UserController(paddle, up=self.controller1Up, down=self.controller1Down)
        if self.controller1 is ControllerTypes.LEARNING_AI:
            return neural_network_controller.NeuralNetworkController(paddle)
        return logical_controller.LogicalController(paddle)

    def get_controller2(self, paddle):
        if self.controller2 is ControllerTypes.USER:
            return user_controller.UserController(paddle, up=self.controller2Up, down=self.controller2Down)
        if self.controller2 is ControllerTypes.LEARNING_AI:
            return neural_network_controller.NeuralNetworkController(paddle)
        return logical_controller.LogicalController(paddle)
