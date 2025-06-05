from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGridLayout
)
from PySide6.QtGui import QColor, QPalette
import sys

from components.back_move import BackMove
from utils.JSON import get_file


class Statistics(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Верхняя кнопка "Назад"
        layout.addWidget(BackMove("menu_back.svg"))

        # Табличка на QWidget + QGridLayout
        table_widget = QWidget()
        self.grid = QGridLayout(table_widget)

        headers = ["Всего игр", "Победы", "Поражения"]
        modes = ["Легкий режим", "Средний режим", "Сложный режим", "Всего"]

        # Заголовки столбцов
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold; padding: 4px;")
            self.grid.addWidget(label, 0, col + 1)

        # Заголовки строк
        for row, mode in enumerate(modes):
            label = QLabel(mode)
            label.setStyleSheet("font-weight: bold; padding: 4px;")
            self.grid.addWidget(label, row + 1, 0)

        # Заполняем ячейки
        data = get_file("app/stats.json")

        self.cells = []  # для доступа при очистке

        for row in range(len(modes)):
            row_cells = []
            for col in range(len(headers)):
                cell = QLabel(f"{row + 1}, {col + 1}")
                cell.setStyleSheet("padding: 4px; border: 1px solid #ccc;")
                self.grid.addWidget(cell, row + 1, col + 1)
                row_cells.append(cell)
            self.cells.append(row_cells)

        # Красим первую строку
        top_color = "background-color: rgb(200, 230, 255);"
        for col in range(len(headers)):
            self.cells[0][col].setStyleSheet(f"padding: 4px; border: 1px solid #ccc; {top_color}")

        # Красим последнюю строку
        bottom_color = "background-color: rgb(255, 230, 200);"
        bottom_row = len(modes) - 1
        for col in range(len(headers)):
            self.cells[bottom_row][col].setStyleSheet(f"padding: 4px; border: 1px solid #ccc; {bottom_color}")

        layout.addWidget(table_widget)

        # Кнопка очистки
        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_table)
        layout.addWidget(clear_button)

        self.setLayout(layout)

    def clear_table(self):
        for row_cells in self.cells:
            for cell in row_cells:
                cell.setText("")

        # Вернем цвета первой и последней строки
        top_color = "background-color: rgb(200, 230, 255);"
        bottom_color = "background-color: rgb(255, 230, 200);"
        for col in range(len(self.cells[0])):
            self.cells[0][col].setStyleSheet(f"padding: 4px; border: 1px solid #ccc; {top_color}")
            self.cells[-1][col].setStyleSheet(f"padding: 4px; border: 1px solid #ccc; {bottom_color}")
