import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

# Импорт моих классов
from UI.widgets.buttons.WhiteButton import WhiteButton

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.central_widget = QWidget()
        self.main_layout = QGridLayout()  
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.setup_page()

        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)

    def setup_page(self):

        btn_start = WhiteButton("Начать игру", (200, 50))
        btn_start.clicked.connect(self.redraw_page)  
        self.main_layout.addWidget(btn_start, 0, 0)  

    def redraw_page(self):
        
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        for i in range(9):
            for j in range(9):
                cell = WhiteButton("")
                self.main_layout.addWidget(cell, i, j)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
