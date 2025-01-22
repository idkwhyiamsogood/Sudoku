import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from Buttons.Buttons import WhiteButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        button1 = WhiteButton(1, "Button", (150, 50))
        button2 = WhiteButton(2, "Button", (200, 60))
        button3 = WhiteButton(3, "Click Me", (180, 40))
        
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()