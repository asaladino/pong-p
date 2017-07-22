import sys

from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QGridLayout
import pygame


# http://zetcode.com/gui/pyqt5/firstprograms/

class SettingsDialog:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.resize(250, 150)
        self.window.setWindowTitle('Settings')
        self.build_ui()

    def build_ui(self):
        title = QLabel('Title')
        author = QLabel('Author')

        title_edit = QLineEdit()
        author_edit = QLineEdit()

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.window.hide)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(title_edit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(author_edit, 2, 1)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(cancel_button)
        h_box.addWidget(ok_button)

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(grid)
        v_box.addLayout(h_box)

        self.window.setLayout(v_box)

    def should_display(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.window.show()
