import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QGridLayout, QComboBox, QTabWidget
import pygame

# http://zetcode.com/gui/pyqt5/firstprograms/
from models.setting import ControllerTypes


class SettingsDialog:
    def __init__(self, setting, pong):
        self.app = QApplication(sys.argv)
        # noinspection PyArgumentList
        self.window = QWidget()
        self.window.resize(250, 150)
        self.window.setWindowTitle('Settings')
        self.setting = setting
        self.pong = pong

        tabs = QTabWidget()
        # noinspection PyArgumentList
        options_tab = QWidget()
        # noinspection PyArgumentList
        controller1_tab = QWidget()
        # noinspection PyArgumentList
        controller2_tab = QWidget()
        tabs.resize(300, 200)

        # Add tabs
        tabs.addTab(options_tab, "Options")
        tabs.addTab(controller1_tab, "Player 1")
        tabs.addTab(controller2_tab, "Player 2")

        board_height_label = QLabel('Board Height')
        board_width_label = QLabel('Board Width')

        controllers_player1_label = QLabel("Controller")
        controllers_player2_label = QLabel("Controller")

        controllers_player1_up_label = QLabel("Key Up")
        controllers_player1_down_label = QLabel("Key Down")

        controllers_player2_up_label = QLabel("Key Up")
        controllers_player2_down_label = QLabel("Key Down")

        self.board_height_edit = QLineEdit()
        self.board_width_edit = QLineEdit()

        self.controllers_player1_combo = QComboBox()
        self.controllers_player2_combo = QComboBox()

        self.controllers_player1_up_edit = QLineEdit()
        self.controllers_player1_down_edit = QLineEdit()

        self.controllers_player2_up_edit = QLineEdit()
        self.controllers_player2_down_edit = QLineEdit()

        for controller in ControllerTypes:
            self.controllers_player1_combo.addItem(controller.value)
            self.controllers_player2_combo.addItem(controller.value)

        ok_button = QPushButton("Save")
        # noinspection PyUnresolvedReferences
        ok_button.clicked.connect(self.save)
        cancel_button = QPushButton("Cancel")
        # noinspection PyUnresolvedReferences
        cancel_button.clicked.connect(self.window.hide)

        # Options
        options_grid = QGridLayout()
        options_grid.setSpacing(10)

        # noinspection PyArgumentList
        options_grid.addWidget(board_height_label, 1, 0)
        # noinspection PyArgumentList
        options_grid.addWidget(self.board_height_edit, 1, 1)

        # noinspection PyArgumentList
        options_grid.addWidget(board_width_label, 2, 0)
        # noinspection PyArgumentList
        options_grid.addWidget(self.board_width_edit, 2, 1)

        options_v_box = QVBoxLayout()
        options_v_box.addStretch(1)
        options_v_box.addLayout(options_grid)
        options_tab.setLayout(options_v_box)

        # Controller 1
        controller1_grid = QGridLayout()
        controller1_grid.setSpacing(10)

        # noinspection PyArgumentList
        controller1_grid.addWidget(controllers_player1_label, 1, 0)
        # noinspection PyArgumentList
        controller1_grid.addWidget(self.controllers_player1_combo, 1, 1)
        # noinspection PyArgumentList
        controller1_grid.addWidget(controllers_player1_up_label, 2, 0)
        # noinspection PyArgumentList
        controller1_grid.addWidget(self.controllers_player1_up_edit, 2, 1)
        # noinspection PyArgumentList
        controller1_grid.addWidget(controllers_player1_down_label, 3, 0)
        # noinspection PyArgumentList
        controller1_grid.addWidget(self.controllers_player1_down_edit, 3, 1)

        controller1_v_box = QVBoxLayout()
        controller1_v_box.addStretch(1)
        controller1_v_box.addLayout(controller1_grid)
        controller1_tab.setLayout(controller1_v_box)

        # Controller 2
        controller2_grid = QGridLayout()
        controller2_grid.setSpacing(10)

        # noinspection PyArgumentList
        controller2_grid.addWidget(controllers_player2_label, 1, 0)
        # noinspection PyArgumentList
        controller2_grid.addWidget(self.controllers_player2_combo, 1, 1)
        # noinspection PyArgumentList
        controller2_grid.addWidget(controllers_player2_up_label, 2, 0)
        # noinspection PyArgumentList
        controller2_grid.addWidget(self.controllers_player2_up_edit, 2, 1)
        # noinspection PyArgumentList
        controller2_grid.addWidget(controllers_player2_down_label, 3, 0)
        # noinspection PyArgumentList
        controller2_grid.addWidget(self.controllers_player2_down_edit, 3, 1)

        controller2_v_box = QVBoxLayout()
        controller2_v_box.addStretch(1)
        controller2_v_box.addLayout(controller2_grid)
        controller2_tab.setLayout(controller2_v_box)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        # noinspection PyArgumentList
        h_box.addWidget(cancel_button)
        # noinspection PyArgumentList
        h_box.addWidget(ok_button)

        v_box = QVBoxLayout()
        v_box.addStretch(1)

        # noinspection PyArgumentList
        v_box.addWidget(tabs)
        v_box.addLayout(h_box)

        self.window.setLayout(v_box)

    def should_display(self, event, setting):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.setting = setting
            self.update_setting()
            self.window.show()

    def update_setting(self):
        self.board_height_edit.setText(str(self.setting.boardHeight))
        self.board_width_edit.setText(str(self.setting.boardWidth))

        self.controllers_player1_combo.setCurrentText(self.setting.controller1.value)
        self.controllers_player2_combo.setCurrentText(self.setting.controller2.value)

        self.controllers_player1_up_edit.setText(str(self.setting.controller1Up))
        self.controllers_player1_down_edit.setText(str(self.setting.controller1Down))

        self.controllers_player2_up_edit.setText(str(self.setting.controller2Up))
        self.controllers_player2_down_edit.setText(str(self.setting.controller2Down))

    def save(self):
        self.setting.boardHeight = int(self.board_height_edit.text())
        self.setting.boardWidth = int(self.board_width_edit.text())

        if self.controllers_player1_combo.currentText() == ControllerTypes.USER.value:
            self.setting.controller1 = ControllerTypes.USER
        if self.controllers_player1_combo.currentText() == ControllerTypes.LEARNING_AI.value:
            self.setting.controller1 = ControllerTypes.LEARNING_AI
        if self.controllers_player1_combo.currentText() == ControllerTypes.LOGICAL_AI.value:
            self.setting.controller1 = ControllerTypes.LOGICAL_AI

        if self.controllers_player2_combo.currentText() == ControllerTypes.USER.value:
            self.setting.controller2 = ControllerTypes.USER
        if self.controllers_player2_combo.currentText() == ControllerTypes.LEARNING_AI.value:
            self.setting.controller2 = ControllerTypes.LEARNING_AI
        if self.controllers_player2_combo.currentText() == ControllerTypes.LOGICAL_AI.value:
            self.setting.controller2 = ControllerTypes.LOGICAL_AI

        self.setting.controller1Up = int(self.controllers_player1_up_edit.text())
        self.setting.controller1Down = int(self.controllers_player1_down_edit.text())

        self.setting.controller2Up = int(self.controllers_player2_up_edit.text())
        self.setting.controller2Down = int(self.controllers_player2_down_edit.text())

        self.pong.save_setting(self.setting)
        self.window.hide()
