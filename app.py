import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import Qt

# Импорт моих классов
from UI.widgets.buttons.WhiteButton import WhiteButton
from UI.widgets.buttons.GrayButton import GrayButton
from UI.widgets.buttons.CustomButton import CustomButton

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("My App")

        self.central_widget = QWidget()
        self.main_layout = QGridLayout()
        
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: white;
            }}
        """)

        self.setup_page()

    def setup_page(self) -> None:
        
        btn_start = WhiteButton("Начать игру", (200, 50))
        btn_start.clicked.connect(self.redraw_page)
        self.main_layout.addWidget(btn_start, 1, 1)

    def clear_page(self) -> None:
        
        # Удаляем все виджеты из лэйаута
        while self.main_layout.count():
            widget = self.main_layout.takeAt(0).widget()
            
            if widget:
                widget.deleteLater()

    def redraw_page(self) -> None:
        self.clear_page()
        
        # Создаём игровое поле 9x9
        for i in range(9):
            for j in range(9):
                cell = self.create_button(i, j)
                self.main_layout.addWidget(cell, i, j)
                cell.clicked.connect(lambda _, btn=cell, x=i, y=j: self.btn_clicked(btn, x, y))
        
        for i in range(1, 10):
            self.main_layout.addWidget(CustomButton(text="", 
                                                    active=False), i, 10)
            
            cell = CustomButton(text="",
                                bordercolor="black",
                                border="1px", 
                                padding="10px 20px", 
                                hovercolor="blue",
                                hoverbordercolor="blue",)
            cell.setText(str(i))
            self.main_layout.addWidget(cell, i - 1, 11)

    def create_button(self, i: int, j: int) -> QPushButton:
        #Создаёт кнопку в зависимости от координат.
        
        if (i < 3 or i > 5) and (j < 3 or j > 5) or (3 <= i <= 5 and 3 <= j <= 5):
            return WhiteButton("")
        else:
            return GrayButton("")

    def btn_clicked(self, btn: QPushButton, x: int, y: int) -> None:
        #Обработчик клика по кнопке.

        if btn.text() == "":
            btn.setText(f"{1}")
            
        else:
            btn.setText(f"")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
