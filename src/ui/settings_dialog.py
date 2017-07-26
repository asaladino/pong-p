import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QGridLayout, QComboBox, QTabWidget
import pygame

# http://zetcode.com/gui/pyqt5/firstprograms/
from models.setting import ControllerTypes


class SettingsDialog:
    def __init__(self, setting):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.resize(250, 150)
        self.window.setWindowTitle('Settings')
        self.setting = setting

        tabs = QTabWidget()
        options_tab = QWidget()
        controller1_tab = QWidget()
        controller2_tab = QWidget()
        tabs.resize(300, 200)

        # Add tabs
        tabs.addTab(options_tab, "Options")
        tabs.addTab(controller1_tab, "Player 1")
        tabs.addTab(controller2_tab, "Player 2")

        board_height_label = QLabel('Board Height')
        board_width_label = QLabel('Board Width')
        controllers_player1_label = QLabel("Controllers")
        controllers_player2_label = QLabel("Controllers")

        self.board_height_edit = QLineEdit()
        self.board_width_edit = QLineEdit()

        self.controllers_player1_combo = QComboBox()
        self.controllers_player2_combo = QComboBox()

        for controller in ControllerTypes:
            self.controllers_player1_combo.addItem(controller.value)
            self.controllers_player2_combo.addItem(controller.value)

        ok_button = QPushButton("Save")
        ok_button.clicked.connect(self.save)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.window.hide)

        # Options
        options_grid = QGridLayout()
        options_grid.setSpacing(10)

        options_grid.addWidget(board_height_label, 1, 0)
        options_grid.addWidget(self.board_height_edit, 1, 1)

        options_grid.addWidget(board_width_label, 2, 0)
        options_grid.addWidget(self.board_width_edit, 2, 1)

        options_v_box = QVBoxLayout()
        options_v_box.addStretch(1)
        options_v_box.addLayout(options_grid)
        options_tab.setLayout(options_v_box)

        # Controller 1
        controller1_grid = QGridLayout()
        controller1_grid.setSpacing(10)

        controller1_grid.addWidget(controllers_player1_label, 1, 0)
        controller1_grid.addWidget(self.controllers_player1_combo, 1, 1)

        controller1_v_box = QVBoxLayout()
        controller1_v_box.addStretch(1)
        controller1_v_box.addLayout(controller1_grid)
        controller1_tab.setLayout(controller1_v_box)

        # Controller 2
        controller2_grid = QGridLayout()
        controller2_grid.setSpacing(10)

        controller2_grid.addWidget(controllers_player2_label, 1, 0)
        controller2_grid.addWidget(self.controllers_player2_combo, 1, 1)

        controller2_v_box = QVBoxLayout()
        controller2_v_box.addStretch(1)
        controller2_v_box.addLayout(controller2_grid)
        controller2_tab.setLayout(controller2_v_box)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(cancel_button)
        h_box.addWidget(ok_button)

        v_box = QVBoxLayout()
        v_box.addStretch(1)

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

    def save(self):
        self.setting.boardHeight = int(self.board_height_edit.text())
        self.setting.boardWidth = int(self.board_width_edit.text())

        if self.controllers_player1_combo.currentText() is ControllerTypes.USER:
            self.setting.controller1 = ControllerTypes.USER
        if self.controllers_player1_combo.currentText() is ControllerTypes.LEARNING_AI:
            self.setting.controller1 = ControllerTypes.LEARNING_AI
        if self.controllers_player1_combo.currentText() is ControllerTypes.LOGICAL_AI:
            self.setting.controller1 = ControllerTypes.LOGICAL_AI

        if self.controllers_player2_combo.currentText() is ControllerTypes.USER:
            self.setting.controller2 = ControllerTypes.USER
        if self.controllers_player2_combo.currentText() is ControllerTypes.LEARNING_AI:
            self.setting.controller2 = ControllerTypes.LEARNING_AI
        if self.controllers_player2_combo.currentText() is ControllerTypes.LOGICAL_AI:
            self.setting.controller2 = ControllerTypes.LOGICAL_AI

        self.window.hide()
