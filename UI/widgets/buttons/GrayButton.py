from PyQt6 import QtGui
from PyQt6.QtWidgets import QPushButton

class GrayButton(QPushButton):
    def __init__(self, text: str, 
                 size: tuple = (100, 50)) -> None:
        super().__init__()

        if len(text) == 0:
            size = (50, 50)

        elif len(text) > 6 and size == (100, 50):
            size = ((len(text) - 6) * 12 + 100, 50)  

        self.setText(f"{text}")
        self.setFixedSize(*size)
        self.setObjectName("QPushButton-gray")

        self.setStyleSheet(f"""
            #QPushButton-gray {{
                padding: 10px 20px;
                text-decoration: none;
                border: 1px solid black;
                background-color: #BDBBBB;
            }}
            
            #QPushButton-gray:hover {{
                color: blue;
                border: 1px solid blue;
            }}
            
            #QPushButton-gray:hover:pressed {{
                color: #BDBBBB;
                border: 1px solid #BDBBBB;
            }}
        """)

        # Установка шрифта
        self.setFont(QtGui.QFont("Times New Roman", 16))
        