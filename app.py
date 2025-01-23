import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

# Импорт моих классов
from UI.widgets.buttons.WhiteButton import WhiteButton
from UI.widgets.buttons.GrayButton import GrayButton

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.central_widget = QWidget()
        self.main_layout = QGridLayout()
        
        self.main_layout.setSpacing(0)  
        self.main_layout.setHorizontalSpacing(0)
        self.main_layout.setVerticalSpacing(0)
            
        self.central_widget.setFixedSize(50 * 9 + 20, 50 * 9 + 20)
        
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
        
        self.main_layout.addWidget(btn_start, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    def redraw_page(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        
        for i in range(9):
            for j in range(9):
                if i < 3 or i > 5:
                    if (j < 3 or j > 5):
                        cell = WhiteButton("")

                    else:
                        cell = GrayButton("")
                
                else:
                    if (j < 3 or j > 5):
                        cell = GrayButton("")
                        
                    else:
                        cell = WhiteButton("")
                
                self.main_layout.addWidget(cell, i, j)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()