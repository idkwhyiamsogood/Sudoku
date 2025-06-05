from . import QPushButton, QIcon, QSize

class IconButton(QPushButton):
    def __init__(self, icon_path: str, parent=None):
        # Кнопка с иконкой из заданного пути
        super().__init__(parent)
        self.setIcon(QIcon("app/public/svg/" + icon_path))
        self.setIconSize(QSize(50, 50))
        self.setFixedSize(50, 50)
        self.setFlat(True)