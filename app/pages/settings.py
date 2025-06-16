from . import QWidget, QVBoxLayout, QHBoxLayout

from components.main_button import MainButton
from components.back_move import BackMove

from core.renderer import renderer

from utils.JSON import change_json_value, get_value_from_json

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Списки названий для каждой кнопки
        self.name_lists = [
            ["Уровень сложности: легкий", "Уровень сложности: средний", "Уровень сложности: сложный"],   
            ["Режим экрана: \n полноэкранный", "Режим экрана: оконный"],   
            ["Сбор статистики: вкл", "Сбор статистики: выкл"],    
            ["Количество подсказок: 3", "Количество подсказок: 5", "Количество подсказок: 7", "Количество подсказок: 9"],  
        ]
        
        self.current_indices = [0, 0, 0, 0]
        
        self.buttons = []

        self.adrs_list = {0: "Difficulty Level", 1: "Screen Mode", 2: "Collect Statistics", 3: "Number of Hints"}

        self.items_list = {"легкий": "easy", "средний": "medium", "сложный": "hard", "полноэкранный": "full screen", 
                           "оконный": "not full screen", "вкл": True, "выкл": False, "3": 3, "5": 5, "7": 7, "9": 9}

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(BackMove("menu_back.svg"))
        main_layout.addStretch()

        for idx in range(4):
            json_value = get_value_from_json("app/settings.json", f"Settings.{self.adrs_list.get(idx)}")

            name_list = self.name_lists[idx]
            display_value = None
            for name in name_list:
                if self.items_list.get(name.split(" ")[-1]) == json_value:
                    display_value = name
                    break

            if display_value is None:
                display_value = name_list[0]

            current_index = name_list.index(display_value)
            self.current_indices[idx] = current_index

            btn = MainButton(display_value, parent=self)
            btn.clicked.connect(lambda checked, i=idx: self.on_button_clicked(i))
            self.buttons.append(btn)

            h_layout = QHBoxLayout()
            h_layout.setContentsMargins(15, 15, 15, 15)
            h_layout.addWidget(btn)

            main_layout.addLayout(h_layout)

        main_layout.addStretch()
        self.setLayout(main_layout)


    def on_button_clicked(self, button_index: int):
        """
        Обработчик нажатия на кнопку с номером button_index.
        Меняет текст кнопки на следующий элемент из её списка.
        """
        current = self.current_indices[button_index]
        next_idx = (current + 1) % len(self.name_lists[button_index])
        new_text = self.name_lists[button_index][next_idx]
        self.buttons[button_index].setText(new_text)
        self.current_indices[button_index] = next_idx

        change_json_value("app/settings.json", f"Settings.{self.adrs_list.get(button_index)}", self.items_list.get(new_text.split(" ")[-1]))
