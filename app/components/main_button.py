from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize


class MainButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setText(text)
        self.setFixedSize(QSize(300, 125))
        self.setStyleSheet("font-size: 20px; background: #90CAF9; border-radius: 37px; border: 2px solid black; font: bold;")