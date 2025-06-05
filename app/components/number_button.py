from . import QPushButton, QSizePolicy

class Button(QPushButton):
    def __init__(self, number, parent=None):
        # Кнопка с цифрой для правого меню
        super().__init__(str(number), parent)
        self.setFixedSize(75, 75)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)