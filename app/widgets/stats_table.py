from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QGridLayout, QSizePolicy, QFrame, 
)
from PySide6.QtCore import Qt, Signal

from utils.JSON import get_value_from_json

STATS_FILE = "app/stats.json"

class StatisticsTable(QWidget):
    stats_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(960, 360)
        self.cells = []
        self.init_ui()
        self.load_stats()

    def init_ui(self):
        container = QFrame(self)
        container.setFrameShape(QFrame.NoFrame)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

        self.grid = QGridLayout(container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        headers = ["Всего игр", "Победы", "Поражения"]
        modes = ["Легкий", "Средний", "Сложный", "Всего"]

        header_style = (
            "font-weight: 600; font-size: 18px; padding: 12px;"
            " background-color: #90CAF9; color: #333;"
        )
        row_style = (
            "padding: 12px; font-size: 18px; background-color: #f0f0f0;"
        )
        footer_style = (
            "font-weight: bold; padding: 12px; font-size: 18px; background-color: #FFDE73;"
        )

        first = QLabel("")
        first.setStyleSheet(header_style + "border-top-left-radius:20px;")
        first.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(first, 0, 0)

        for col, text in enumerate(headers, 1):
            lbl = QLabel(text)
            style = header_style + ("border-top-right-radius:20px;" if col == len(headers) else "")
            lbl.setStyleSheet(style)
            lbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(lbl, 0, col)

        for row, mode in enumerate(modes, 1):
            style = footer_style if row == len(modes) else row_style
            name_label = QLabel(mode.capitalize())
            name_label.setStyleSheet(style + ("border-bottom-left-radius:20px;" if row == len(modes) else ""))
            name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.grid.addWidget(name_label, row, 0)

            row_cells = []
            for col in range(1, len(headers) + 1):
                lbl = QLabel()
                cell_style = style + ("border-bottom-right-radius:20px;" if row == len(modes) and col == len(headers) else "")
                lbl.setStyleSheet(cell_style)
                lbl.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(lbl, row, col)
                row_cells.append(lbl)
            self.cells.append(row_cells)

    def load_stats(self):
        values = {}
        for key in ["total_games", "total_wins", "total_losses"]:
            values[key] = get_value_from_json(STATS_FILE, key)

        for level in ["easy", "medium", "hard"]:
            for stat in ["games_played", "wins", "losses"]:
                path = f"difficulty_levels.{level}.{stat}"
                values[path] = get_value_from_json(STATS_FILE, path)

        order = ["easy", "medium", "hard", "total"]

        for i, mode in enumerate(order):
            if mode == "total":
                stats = [values["total_games"], values["total_wins"], values["total_losses"]]
            else:
                stats = [
                    values.get(f"difficulty_levels.{mode}.games_played", 0),
                    values.get(f"difficulty_levels.{mode}.wins", 0),
                    values.get(f"difficulty_levels.{mode}.losses", 0),
                ]

            total = int(stats[0]) if str(stats[0]).isdigit() else 0
            for j, val in enumerate(stats):
                val_int = int(val) if str(val).isdigit() else 0
                pct = (val_int / total * 100) if total else 0
                text = f"{val_int} ({pct:.0f}%)"
                self.cells[i][j].setText(text)

    def update_stats(self):
        """Обновляет данные таблицы из JSON."""
        self.load_stats()
        self.stats_updated.emit()