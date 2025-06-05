from components.icon_button import IconButton
from PySide6.QtCore import Signal

from core.renderer import renderer


class BackMove(IconButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(icon_path, parent)
        self.clicked.connect(self.back_to_menu)

    def back_to_menu(self):
        renderer.render('menu')
