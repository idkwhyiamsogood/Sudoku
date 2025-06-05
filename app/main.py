import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtCore import QSize

from core.renderer import renderer

from pages.main_menu import MainMenu
from pages.game import SudokuGame
from pages.settings import Settings
from pages.stats import Statistics

from utils.JSON import get_value_from_json


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Загрузка стилей
    with open("app/styles/main.qss", "r", encoding="utf-8") as file:
        stylesheet = file.read()
        app.setStyleSheet(stylesheet)
    
    app.setWindowIcon(QIcon("app/public/other/icon.png"))

    # Инициализация главного окна и рендерера
    window = QMainWindow()
    window.setMinimumSize(QSize(1280, 720))  # Установка минимального размера окна
    window.setWindowTitle("Судоку")

    fullscreen = {"full screen": True, "not full screen": False}
    
    if fullscreen.get(get_value_from_json("app/settings.json", "Settings.Screen Mode")):
        window.showFullScreen()

    renderer.initialize(window)
    
    # Регистрация представлений
    renderer.register_view('menu', MainMenu())
    renderer.register_view('game', SudokuGame())
    renderer.register_view('settings', Settings())
    renderer.register_view('stats', Statistics())
    
    # Показ окна
    window.show()
    sys.exit(app.exec())
