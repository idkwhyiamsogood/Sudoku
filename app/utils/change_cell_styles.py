from . import QLineEdit

def change_styles(cell: QLineEdit, new_style: str, 
                  old_style: str | None, replace:bool = True) -> None:
    if replace == True:
        cell.setStyleSheet(
            cell.styleSheet().replace(
                old_style, new_style
            )
        )

    else:
        cell.setStyleSheet(
            new_style
        )

def add_style(self, row, col, style: str) -> None:
    self.cells[row][col].setStyleSheet(
        self.cells[row][col].styleSheet() + style
    )

def clear_cell_styles(self) -> None:
    for r in range(9):
            for c in range(9):
                style = self.cells[r][c].styleSheet()
                style = style.replace("background: #90CAF9;", "")\
                            .replace("background: #E0E0E0;", "")  \
                            .replace("background: #FFF9C4;", "")   \
                            # .replace("background: #FFB6C1", "")
                self.cells[r][c].setStyleSheet(style)

def clear_style(self, row, col):
    self.cells[row][col].setStyleSheet("")
