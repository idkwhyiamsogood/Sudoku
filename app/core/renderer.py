from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt


class Renderer:
    def __init__(self):
        self._window = None
        self._stack = None
        self._current_view = None
        self._views = {}

    def initialize(self, window: QMainWindow):
        """Инициализация рендерера с главным окном"""
        self._window = window
        self._stack = QStackedWidget()
        
        # Настройка главного окна
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)
        
        window.setCentralWidget(central_widget)
        window.setWindowTitle("Судоку")

    def get_view(self, name: str) -> QWidget:
        if name not in self._views:
            raise ValueError(f"Страница '{name}' не зарегестрирована")
        return self._views[name]

    def register_view(self, name: str, view: QWidget):
        """Регистрация нового представления"""
        self._views[name] = view
        self._stack.addWidget(view)
        
        # Если это первое представление, показываем его
        if len(self._views) == 1:
            self.render(name)

    def render(self, view_name: str):
        """Переключение на указанное представление"""
        if view_name not in self._views:
            raise ValueError(f"Страница '{view_name}' не зарегестрирована")
        
        view = self._views[view_name]
        self._stack.setCurrentWidget(view)
        self._current_view = view_name

    @property
    def window(self) -> QMainWindow:
        """Получение главного окна"""
        return self._window


# Глобальный экземпляр рендерера
renderer = Renderer() 