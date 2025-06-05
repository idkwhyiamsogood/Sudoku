from . import QVBoxLayout, QSpacerItem, QSizePolicy, QWidget, QHBoxLayout, QLabel, QPixmap, Qt

from components.main_button import MainButton
from core.renderer import renderer


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        # Основной layout
        main_v_layout = QVBoxLayout(self)
        main_v_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        h_layout = QHBoxLayout()
        h_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Виджет с кнопками
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(10)

        btn_names = ["Начать игру", "Настройки", "Статистика", "Выйти из игры"]

        for name in btn_names:
            btn = MainButton(name)
            buttons_layout.addWidget(btn)

            # Привязываем действия к кнопкам
            if name == "Начать игру":
                btn.clicked.connect(self.start_game)
            elif name == "Выйти из игры":
                btn.clicked.connect(self.close_app)
            elif name == "Настройки":
                btn.clicked.connect(self.settings)
            else:
                btn.clicked.connect(self.stats)

        h_layout.addWidget(buttons_widget)
        h_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # Изображение
        image_label = QLabel()
        pixmap = QPixmap("app/public/other/main-window-table.png")
        image_label.setPixmap(pixmap)
        image_label.setFixedSize(600, 600)
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignCenter)

        h_layout.addWidget(image_label)
        h_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_v_layout.addLayout(h_layout)
        main_v_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def start_game(self):
        """Запуск игры"""
        renderer.render('game')

    def close_app(self):
        """Закрытие приложения"""
        renderer.window.close()

    def settings(self):
        renderer.render('settings')

    def stats(self):
        renderer.render('stats')
