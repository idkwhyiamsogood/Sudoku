from PyQt6 import QtGui
from PyQt6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self, text: str, 
                 active : bool = True,
                 textdecoration: str = "none",
                 padding: str = "10px 20px",
                 color:str = "black", 
                 bgcolor:str = "white",
                 bordercolor: str = "none",
                 hovercolor: str = "none",
                 hoverbgcolor: str = "none",
                 hoverbordercolor: str = "none",
                 pressedcolor: str = "none",
                 pressedbgcolor: str = "none",
                 pressedbordercolor: str = "none",
                 border: str = "none",
                 fontsize: int = 16, 
                 fontfamily: list[str] = ["Times New Roman"],
                 size: tuple = (100,50)) -> None:
        super().__init__()
        
        if len(text) == 0:
            size = (50,50)
            
        self.setEnabled(active)
        
        self.setText(f"{text}")
        self.setFixedSize(*size)
        
        self.setStyleSheet(f"""
                           QPushButton {{
                               padding: {padding};
                               color: {color};
                               background-color: {bgcolor};
                               border: {border} solid {bordercolor};
                               text-decoration: {textdecoration};   
                           }}
                           
                           QPushButton:hover {{
                               color: {hovercolor};
                               background-color: {hoverbgcolor};
                               border: {border} solid {hoverbordercolor};
                           }}
                           
                           QPushButton:hover:pressed {{
                               color: {pressedcolor};
                               background-color: {pressedbgcolor};
                               border: {border} solid {pressedbordercolor}
                           }}
                           """)
        
        self.setFont(QtGui.QFont(*fontfamily, fontsize))