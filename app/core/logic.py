import random

from utils.JSON import get_value_from_json

class SudokuLogic:
    def __init__(self):
        self.board = None
        self.solved = None
        self.puzzle = None

    def generate_solved_sudoku(self):
        # Генерирует полностью решенное поле Судоку
        board = [[0]*9 for _ in range(9)]
        for box in range(0, 9, 3):  
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box+i][box+j] = nums.pop()
        self.solve_sudoku(board)
        return board

    def solve_sudoku(self, board):
        # Решает Судоку рекурсивно с помощью бэктрекинга
        empty = self.find_empty(board)
        if not empty: 
            return True
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty(self, board):
        # Ищет первую пустую ячейку на поле
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        # Проверяет, можно ли поставить число num в позицию pos
        if num in board[pos[0]]:
            return False
        if num in [board[i][pos[1]] for i in range(9)]:
            return False
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if board[i][j] == num and (i,j) != pos:
                    return False
        return True
    
    holes = {"easy": 30, "medium": 40, "hard": 50}

    def create_puzzle(self, solved, holes=holes.get(get_value_from_json("app/settings.json", "Settings.Difficulty Level"))):
        # Удаляет заданное количество цифр для создания головоломки
        board = [row.copy() for row in solved]
        for _ in range(holes):
            row, col = random.randint(0,8), random.randint(0,8)
            while board[row][col] == 0:
                row, col = random.randint(0,8), random.randint(0,8)
            board[row][col] = 0
        return board

    def is_board_valid(self, board):
        # Проверяет валидность полного поля по строкам, столбцам и квадратам
        for row in board:
            if sorted(row) != list(range(1,10)):
                return False
        for col in range(9):
            if sorted([board[row][col] for row in range(9)]) != list(range(1,10)):
                return False
        for box in range(9):
            x = (box % 3) * 3
            y = (box // 3) * 3
            square = [board[y+i][x+j] for i in range(3) for j in range(3)]
            if sorted(square) != list(range(1,10)):
                return False
        return True

    def check_cell_valid(self, number, row, col, current_board):
        # Проверяет, нарушает ли number в ячейке правила Судоку
        for c in range(9):
            if c != col and current_board[row][c] == str(number):
                return False
        for r in range(9):
            if r != row and current_board[r][col] == str(number):
                return False
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and current_board[r][c] == str(number):
                    return False
        return True

    def new_game(self):
        # Генерирует новую игру
        self.solved = self.generate_solved_sudoku()
        self.puzzle = self.create_puzzle(self.solved)
        return self.puzzle, self.solved
