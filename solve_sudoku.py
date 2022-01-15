import math
import sys

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

small_boxes = {
    "11": [],
    "12": [],
    "13": [],
    "21": [],
    "22": [],
    "23": [],
    "31": [],
    "32": [],
    "33": [],
}

#Split the 9x9 puzzle into the 3x3 squares
def make_small_boxes(): 

    for row in range(1, 10):
        arg1 = math.ceil(row/3)

        for column in range(1, 10):

            arg2 = math.ceil(column/3)
            args = str(arg1) + str(arg2)
            small_boxes[args].append(board[row-1][column-1])

#Get empty box
def empty(board):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if(board[row][column] == 0):
                return(row, column)

    return None

#Check if puzzle is valid
def is_valid(board, number, position):

    for i in range(9):
        if((i != position[1]) and (number == board[position[0]][i])):
            return False
        elif((i != position[0]) and (number == board[i][position[1]])):
            return False

    args = str(math.floor(position[0]/3)+1)+str(math.floor(position[1]/3)+1)

    if(number in small_boxes[args]):
        return False

    return True

def solve(puzzle):

    print("-"*100)
    display_board(puzzle)
    empty_position = empty(puzzle)

    if not empty_position:
        return True
    else:
        row, column = empty(puzzle)

    for i in range(1, 10):

        if(is_valid(puzzle, i, (row, column))):
            puzzle[row][column] = i

            if solve(puzzle):
                return True

            puzzle[row][column] = 0

    board=puzzle
    return False
        
                
def display_board(board):
    for row in board:
        print(row)

if __name__ == '__main__':

    if(len(board) != 9):
        sys.exit()

    for row in range(len(board)):

        if(len(board[row]) != 9):
            sys.exit()

    make_small_boxes()
    solve(board)
