import sys

from . import QWidget, Signal, QVBoxLayout, QHBoxLayout, QSizePolicy, QSize, QGridLayout, QPushButton, QMessageBox, QIcon

from utils.change_cell_styles import change_styles, add_style, clear_cell_styles
from utils.JSON import get_value_from_json
from utils.scanarios import user_loss, user_win

from components.cell_button import SudokuCell
from components.back_move import BackMove
from components.message_box import CustomMessageDialog
from components.main_button import MainButton

from widgets.right_menu import RightMenu

from core.logic import SudokuLogic

class SudokuGame(QWidget):
    game_won = Signal(False)

    def __init__(self):
        super().__init__()

        self.message_box = CustomMessageDialog(self)

        self.selected_cell = None
        self.pencil_mode = False
        self.errorsCells = ()
        self.move_history = []
        self.hint_count = get_value_from_json('app/settings.json', 'Settings.Number of Hints')
        self.error_count = 3
        self.start = False
        
        # Инициализация игровой логики
        self.game_logic = SudokuLogic()
        
        # Настройка основного layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
          
        self.back_move = BackMove("menu_back.svg")
        self.main_layout.addWidget(self.back_move)

        self.game_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.game_layout)
        self.main_layout.addLayout(self.button_layout)

        # Создание панели с сеткой
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        
        cell_size = 60  # размер одной ячейки
        
        # Инициализация ячеек 9x9
        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = SudokuCell(row, col)
                cell.setFixedSize(QSize(cell_size, cell_size))
                cell.setProperty("deletable", False)
                borders = []
                if row % 3 == 0:
                    borders.append("border-top: 3px solid black;")
                if col % 3 == 0:
                    borders.append("border-left: 3px solid black;")
                if col == 8:
                    borders.append("border-right: 3px solid black;")
                if row == 8:
                    borders.append("border-bottom: 3px solid black;")
                cell.setStyleSheet("".join(borders))
                cell.clicked.connect(self.cell_clicked)
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        left_layout.addLayout(self.grid_layout)
        
        # Инициализация правого меню и привязка сигналов
        self.right_menu = RightMenu()
        self.right_menu.hint_btn.set_count(self.hint_count)
        self.right_menu.number_clicked.connect(self.number_button_clicked)
        self.right_menu.back_move_btn.clicked.connect(self.handle_back_move)
        self.right_menu.hint_btn.button.clicked.connect(self.handle_hint)
        self.right_menu.eraser_btn.clicked.connect(self.handle_eraser)
        self.right_menu.pencil_btn.pressed.connect(self.handle_pencil)
        
        self.game_layout.addWidget(left_panel)
        self.game_layout.addWidget(self.right_menu)
    
        self.new_game_btn = MainButton("Новая игра", (300, 75))
        self.new_game_btn.clicked.connect(self.new_game)
        self.button_layout.addWidget(self.new_game_btn)
        
        # Запуск новой игры
        self.new_game()
        self.game_won.connect(self.show_new_game_button)
        self.game_won.emit()

    def new_game(self):
        clear_cell_styles(self)

        for row in range(9):
            for col in range(9):
                change_styles(self.cells[row][col], "color: black;", "color: gray;")
                self.cells[row][col].setProperty("countable", False)
                self.cells[row][col].setProperty("deletable", False)

        self.selected_cell = None
        self.pencil_mode = False
        icon_path = "app/public/svg/pencil_active.svg" if self.pencil_mode else "app/public/svg/pencil_inactive.svg"
        self.right_menu.pencil_btn.setIcon(QIcon(icon_path))
        self.errorsCells = ()
        self.move_history = []
        self.hint_count = get_value_from_json('app/settings.json', 'Settings.Number of Hints')
        self.right_menu.hint_btn.set_count(self.hint_count)
        self.error_count = 3
        self.start = False
        self.new_game_btn.show()  # Показываем кнопку при новой игре

        for i in range(self.right_menu.number_grid.count()):
            widget = self.right_menu.number_grid.itemAt(i).widget()
            if isinstance(widget, QPushButton):  # Ищем кнопки
                widget.blockSignals(False)

        self.right_menu.hint_btn.button.blockSignals(False)

        self.selected_cell = None
        for row in self.cells:
            for cell in row:
                cell.setText("")
                cell.setStyleSheet(cell.styleSheet().replace("background: #FFB6C1;", ""))
        
        # Получаем новую головоломку от игровой логики
        self.puzzle, self.solved = self.game_logic.new_game()
        
        # Заполняет ячейки начальными значениями
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] != 0:
                    self.cells[row][col].setText(str(self.puzzle[row][col]))
                    self.cells[row][col].setProperty("countable", True)
                else:
                    self.cells[row][col].setProperty("deletable", True)

    def cell_clicked(self, row, col):
        # Обработка выбора ячейки: подсветка и сброс предыдущих конфликтов

        self.selected_cell = (row, col)

        selected_text = self.cells[row][col].text()

        clear_cell_styles(self)
        
        # Подсветка строки и столбца
        for i in range(9):
            add_style(self, row, i, "background: #E0E0E0;")
            add_style(self, i, col, "background: #E0E0E0;")
        
        # Подсветка 3x3 квадрата
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                add_style(self, r, c, "background: #FFF9C4;")
        
        # Подсветка выбранной ячейки и одинаковых чисел
        add_style(self, row, col, "background: #90CAF9;")
        if selected_text:
            for r in range(9):
                for c in range(9):
                    if (r, c) == (row, col):
                        continue
                    if self.cells[r][c].text() == selected_text:
                        add_style(self, r, c, "background: #90CAF9;")

    def number_button_clicked(self, number):
        if not self.selected_cell:
            self.message_box.show_message("Ошибка", "Выберите ячейку!") 
            return   

        if not self.start:
            self.start = True
            self.new_game_btn.hide()  # Скрываем кнопку при первом действии  

        row, col = self.selected_cell
        change_styles(self.cells[row][col], "color: black;" ,"color: gray;")

        previous_value = self.cells[row][col].text()
        self.move_history.append((row, col, previous_value))

        self.clear_conflicts_highlight(previous_value, row, col)

        if self.pencil_mode:
            self.cells[row][col].setText(str(number))
            add_style(self, row, col, "color: gray;")
            self.cells[row][col].setProperty("countable", False)
        else:
            # Создаем текущее состояние доски для проверки
            current_board = [[self.cells[r][c].text() for c in range(9)] for r in range(9)]
            if self.game_logic.check_cell_valid(number, row, col, current_board):
                self.cells[row][col].setText(str(number))
                self.cells[row][col].setProperty("countable", True)
                self.check_victory()
            else:
                self.cells[row][col].setText(str(number))
                self.errorsCells = (row, col)
                self.highlight_conflicts(number, row, col)

                if self.error_count == 1:
                    self.handle_lose()
                else:
                    self.error_count -= 1

    def handle_pencil(self):
        # Переключает режим заметок (карандаш)
        self.pencil_mode = not self.pencil_mode
        icon_path = "app/public/svg/pencil_active.svg" if self.pencil_mode else "app/public/svg/pencil_inactive.svg"
        self.right_menu.pencil_btn.setIcon(QIcon(icon_path))

    def handle_back_move(self):
        if self.start == False:
            return

        # Отменяет последнее действие пользователя
        if self.move_history:
            row, col, prev_value = self.move_history.pop()

            self.clear_conflicts_highlight(self.cells[row][col].text(), row, col)
            self.highlight_conflicts(prev_value, row, col) if prev_value != "" else None
            self.cells[row][col].setText(prev_value)

            if self.selected_cell == (row, col):
                self.cell_clicked(row, col)

    def handle_hint(self):
        row, col = self.selected_cell

        if not self.cells[row][col].text() == "":
            return

        if not self.start:
            self.start = True
            self.new_game_btn.hide()  # Скрываем кнопку при первом действии  

        if self.hint_count == 0:
            return
        
        self.move_history = [item for item in self.move_history if item[:2] != self.selected_cell]

        self.clear_conflicts_highlight(self.cells[row][col].text(), row, col)

        right_number = str(self.solved[row][col])
        
        if not self.selected_cell:
            return
        if self.pencil_mode == True:
            change_styles(self.cells[row][col], "color: black;", "color: gray;")

        self.cells[row][col].setText(right_number)
        self.cells[row][col].setProperty("countable", True)
        self.cells[row][col].setProperty("deletable", False)
        self.hint_count -= 1
        self.right_menu.hint_btn.set_count(self.hint_count)
        self.check_victory()

    def handle_eraser(self):
        # Удаляет введенное число, если ячейка разрешает удаление
        if self.selected_cell:  
            row, col = self.selected_cell

            if self.cells[row][col].property("deletable"):
                self.clear_conflicts_highlight(self.cells[row][col].text(), row, col)
                previous_value = self.cells[row][col].text()
                self.move_history.append((row, col, previous_value))
                self.cells[row][col].setText("")
                change_styles(self.cells[row][col], "color: black;", "color: gray;")
            else:
                self.message_box.show_message("Ошибка", "Нельзя удалить значение в этой ячейке")
        else:
            self.message_box.show_message("Ошибка", "Сначала выберите ячейку")

    def check_victory(self):
        # Проверяем заполненность и свойство countable
        for row in range(9):
            for col in range(9):
                text = self.cells[row][col].text()
                countable = self.cells[row][col].property("countable")
                if not text or not countable if countable is not None else False:
                    return  # Пустая ячейка или несчитаемое значение — выходим
        
        # Формируем текущую доску
        try:    
            board = []
            for row in range(9):
                current_row = []
                for col in range(9):
                    current_row.append(int(self.cells[row][col].text()))
                board.append(current_row)

        except ValueError: return
        
        # Проверяем на корректность
        if self.game_logic.is_board_valid(board):
            self.message_box.show_message("Поздравляем", "Вы успешно решили судоку!")
            self.game_won.emit()
            user_win()

    def handle_lose(self):
        self.start = False

        for i in range(self.right_menu.number_grid.count()):
            widget = self.right_menu.number_grid.itemAt(i).widget()
            if isinstance(widget, QPushButton):  # Ищем кнопки
                widget.blockSignals(True)

        self.right_menu.hint_btn.button.blockSignals(True)

        self.message_box.show_message("Очень жаль", "Вы проиграли!")
        self.game_won.emit()
        user_loss()

    def show_new_game_button(self):
        # При победе показываем кнопку новой игры
        self.new_game_btn.show()

    def highlight_conflicts(self, number, row, col):
        # Подсвечивает ячейку и все конфликтующие
        add_style(self, row, col, "background: #FFB6C1;")
        for c in range(9):
            if c != col and self.cells[row][c].text() == str(number):
                add_style(self, row, c, "background: #FFB6C1;")
        for r in range(9):
            if r != row and self.cells[r][col].text() == str(number):
                add_style(self, r, col, "background: #FFB6C1;")
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and self.cells[r][c].text() == str(number):
                    add_style(self, r, c, "background: #FFB6C1;")

    def clear_conflicts_highlight(self, number, row, col):
        change_styles(self.cells[row][col], "background: white;", "background: #FFB6C1;")

        for c in range(9):
            if c != col and self.cells[row][c].text() == str(number):
                change_styles(self.cells[row][c], "background: white;", "background: #FFB6C1;")
        for r in range(9):
            if r != row and self.cells[r][col].text() == str(number):
                change_styles(self.cells[r][col], "background: white;", "background: #FFB6C1;")
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and self.cells[r][c].text() == str(number):
                    change_styles(self.cells[r][c], "background: white;", "background: #FFB6C1;")