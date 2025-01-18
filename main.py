import random

def generate_board():
    board = [[0 for _ in range(9)] for _ in range(9)]

    def fill_board(board):
        
        for col in range(9):
            numbers = list(range(1,10))
            print(numbers)
            print("-------------------------------")
            for row in range(9):
                if board[col][row] == 0:
                    board[col][row] = 
            
        return board
    
    fill_board(board)
    for i in range(9):
        print(board[i])

generate_board()