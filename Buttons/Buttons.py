import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton

class WhiteButton(QPushButton):
   def __init__(self, num, text, size):                 
        super().__init__()
        
        self.setText(f"{text} {num}")
        self.setFixedSize(*size)
        
        self.setStyleSheet(f"""
                           QPushButton {{
                               color: white;
                               
                           }}
                           QPushButton:hover {{
                               color: blue
                           }}
                           
                           QPushButtons:touched {{
                               color: black
                           }}
                           
                        """)
        
        self.setFont(QtGui.QFont("Times New Roman", 14))