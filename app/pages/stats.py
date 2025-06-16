
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QSizePolicy,  QHBoxLayout
)
from PySide6.QtCore import Qt

from components.back_move import BackMove
from components.main_button import MainButton
from widgets.stats_table import StatisticsTable
from utils.JSON import change_json_value

STATS_FILE = "app/stats.json"

class StatisticsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Основной вертикальный лейаут
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        # Верхний лейаут с кнопкой назад
        top_layout = QHBoxLayout()
        back_btn = BackMove("menu_back.svg")
        back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_layout.addWidget(back_btn, alignment=Qt.AlignLeft | Qt.AlignTop)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        main_layout.addStretch()

        center_layout = QVBoxLayout()
        center_layout.setSpacing(30)
        self.table = StatisticsTable()
        center_layout.addWidget(self.table, alignment=Qt.AlignHCenter)

        clear_btn = MainButton("Очистить", (300, 75))
        clear_btn.clicked.connect(self.clear_table)
        center_layout.addWidget(clear_btn, alignment=Qt.AlignHCenter)

        main_layout.addLayout(center_layout)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def clear_table(self):
        change_json_value(STATS_FILE, "total_games", "0")
        change_json_value(STATS_FILE, "total_wins", "0")
        change_json_value(STATS_FILE, "total_losses", "0")
        for level in ["easy", "medium", "hard"]:
            change_json_value(STATS_FILE, f"difficulty_levels.{level}.games_played", "0")
            change_json_value(STATS_FILE, f"difficulty_levels.{level}.wins", "0")
            change_json_value(STATS_FILE, f"difficulty_levels.{level}.losses", "0")

        for row_cells in self.table.cells:
            for lbl in row_cells:
                lbl.setText("0 (0%)")
