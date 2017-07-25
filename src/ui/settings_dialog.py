import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QGridLayout, QComboBox, QTabWidget
import pygame


# http://zetcode.com/gui/pyqt5/firstprograms/
from models.setting import ControllerTypes


class SettingsDialog:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.resize(250, 150)
        self.window.setWindowTitle('Settings')
        self.build_ui()

    def build_ui(self):
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

        board_height_edit = QLineEdit()
        board_width_edit = QLineEdit()

        controllers_player1_combo = QComboBox()
        controllers_player2_combo = QComboBox()

        for controller in ControllerTypes:
            controllers_player1_combo.addItem(controller.value)
            controllers_player2_combo.addItem(controller.value)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.window.hide)

        # Options
        options_grid = QGridLayout()
        options_grid.setSpacing(10)

        options_grid.addWidget(board_height_label, 1, 0)
        options_grid.addWidget(board_height_edit, 1, 1)

        options_grid.addWidget(board_width_label, 2, 0)
        options_grid.addWidget(board_width_edit, 2, 1)

        options_v_box = QVBoxLayout()
        options_v_box.addStretch(1)
        options_v_box.addLayout(options_grid)
        options_tab.setLayout(options_v_box)

        # Controller 1
        controller1_grid = QGridLayout()
        controller1_grid.setSpacing(10)

        controller1_grid.addWidget(controllers_player1_label, 1, 0)
        controller1_grid.addWidget(controllers_player1_combo, 1, 1)

        controller1_v_box = QVBoxLayout()
        controller1_v_box.addStretch(1)
        controller1_v_box.addLayout(controller1_grid)
        controller1_tab.setLayout(controller1_v_box)

        # Controller 2
        controller2_grid = QGridLayout()
        controller2_grid.setSpacing(10)

        controller2_grid.addWidget(controllers_player2_label, 1, 0)
        controller2_grid.addWidget(controllers_player2_combo, 1, 1)

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

    def should_display(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.window.show()
