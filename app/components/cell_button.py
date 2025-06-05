from . import QLineEdit, QSizePolicy, QMouseEvent, Signal, QSize, Qt

class SudokuCell(QLineEdit):
    clicked = Signal(int, int)
    
    def __init__(self, row, col, parent=None):
        # Инициализирует ячейку с заданными координатами
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
    def mousePressEvent(self, event: QMouseEvent):
        # Обрабатывает клик по ячейке и генерирует сигнал clicked
        self.clicked.emit(self.row, self.col)
        super().mousePressEvent(event)
        
    def sizeHint(self):
        # Возвращает рекомендуемый размер ячейки
        return QSize(49, 49)