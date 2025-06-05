from . import QWidget, Signal, QPushButton, QIcon, QSize, QLabel, Qt


class Hint(QWidget):
    clicked = Signal()

    def __init__(self, icon_path: str, parent=None):
        super().__init__(parent)

        self.setFixedSize(50, 50)

        # Кнопка подсказки
        self.button = QPushButton(self)
        self.button.setIcon(QIcon("app/public/svg/" + icon_path))
        self.button.setIconSize(QSize(50, 50))
        self.button.setFixedSize(50, 50)
        self.button.setFlat(True)
        self.button.clicked.connect(self.clicked)

        # Лейбл-счётчик
        self.counter_label = QLabel("", self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("""
            background-color: #FFDE73;
            color: black;
            border-radius: 10px;
            min-width: 20px;
            min-height: 20px;
            font-size: 16px;
            font-weight: 600;
        """)
        self.counter_label.move(30, 0)  # позиция в правом верхнем углу
        self.counter_label.raise_()  # поверх кнопки

    def set_count(self, count: int):
        self.counter_label.setText(str(count))
        self.counter_label.setVisible(count > 0)