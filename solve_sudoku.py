import math
from generate_random import generate

global solution
solution = None

#Split the 9x9 puzzle into the 3x3 squares
def make_small_boxes(current_board):

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

    for row in range(1, 10):
        arg1 = math.ceil(row/3)

        for column in range(1, 10):

            arg2 = math.ceil(column/3)
            args = str(arg1) + str(arg2)
            small_boxes[args].append(current_board[row-1][column-1])

    return small_boxes

#Get empty box
def empty(board):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if(board[row][column] == 0):
                return(row, column)

    return None

#Check if puzzle is valid
def is_position_valid(board, small_boxes, number, position):

    for i in range(9):
        if((i != position[1]) and (number == board[position[0]][i])):
            return False
        elif((i != position[0]) and (number == board[i][position[1]])):
            return False

    args = str(math.floor(position[0]/3)+1)+str(math.floor(position[1]/3)+1)

    if(number in small_boxes[args]):
        return False

    return True

def solve(puzzle, small_boxes):

    print("/"*100)
    display_board(puzzle)
    empty_position = empty(puzzle)

    if not empty_position:
        return True
    else:
        row, column = empty(puzzle)

    for i in range(1, 10):

        if(is_position_valid(puzzle, small_boxes, i, (row, column))):
            puzzle[row][column] = i
            small_boxes = make_small_boxes(puzzle)

            if solve(puzzle, small_boxes):
                return True

            puzzle[row][column] = 0

    solution = puzzle

    return False
                
def display_board(board):
    global solution
    solution = board
    for row in board:
        print("—"*38)
        for element in row:
            if element == 0:
                element = "◼"
            print(" | " + str(element), end="")
        print(" |")

if __name__ == '__main__':

    '''
    board = [
        [7,8,0,4,0,0,1,2,0],
        [6,0,0,0,7,5,0,0,9],
        [0,0,0,6,0,1,0,7,8],
        [0,0,7,0,4,0,2,6,0],
        [0,0,1,0,5,0,9,3,0],
        [9,0,4,0,6,0,0,0,5],
        [0,7,0,3,0,0,0,1,2],
        [1,2,0,0,0,7,4,0,0],
        [5,4,9,2,0,6,0,0,7]
    ]

    small_boxes = make_small_boxes(board)
    solve(board, small_boxes)
    print("&"*100)
    display_board(solution)
    '''

    problem = generate(1, make_small_boxes)
    display_board(problem)
    small_boxes = make_small_boxes(problem)
    solve(problem, small_boxes)




















