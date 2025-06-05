from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class CustomMessageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #FAFAFA;
                border: 2px solid #90CAF9;
                border-radius: 15px;
            }
            QLabel {
                color: #333;
                font-size: 18px;
            }
            QPushButton {
                background-color: #90CAF9;
                border: none;
                padding: 8px 16px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

    def show_message(self, title, message):
        self.setWindowTitle(title)
        self.label.setText(message)
        self.exec()
