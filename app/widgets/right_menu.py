from . import Signal, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, Qt

from components.hint import Hint
from components.number_button import Button
from components.icon_button import IconButton


class RightMenu(QWidget):
    number_clicked = Signal(int)
    
    def __init__(self, parent=None):
        # Инициализация бокового меню с кнопками и цифрами
        super().__init__(parent)
        self.setFixedWidth(400)
        self.init_ui()
        
    def init_ui(self):
        # Создает интерфейс бокового меню
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 135, 0, 0)
        self.setLayout(layout)

        # Панель основных действий
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 6)
        buttons_layout.setSpacing(25)

        self.back_move_btn = IconButton("back.svg")
        buttons_layout.addWidget(self.back_move_btn)

        self.hint_btn = Hint("hint.svg")
        buttons_layout.addWidget(self.hint_btn)

        self.eraser_btn = IconButton("eraser.svg")
        buttons_layout.addWidget(self.eraser_btn)

        self.pencil_btn = IconButton("pencil_inactive.svg")
        buttons_layout.addWidget(self.pencil_btn)

        layout.addLayout(buttons_layout)
        
        # Кнопки цифр 1-9
        self.number_grid = QGridLayout()
        self.number_grid.setAlignment(Qt.AlignCenter)
        positions = [(i, j) for i in range(3) for j in range(3)]
        for index, (row, col) in enumerate(positions):
            btn = Button(index + 1)
            btn.clicked.connect(lambda _, n=index+1: self.number_clicked.emit(n))
            self.number_grid.addWidget(btn, row, col, Qt.AlignCenter)
        
        layout.addLayout(self.number_grid)
