import math
from generate_random import generate
from pynput import keyboard
import multiprocessing
import threading
import time
import sys

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

#Check whether board is valid if number is inserted in given position
def is_position_valid(board, small_boxes, number, position):

    if(board[position[0]][position[1]] != 0):
        return False

    for i in range(9):
        if((i != position[1]) and (number == board[position[0]][i])):
            return False
        elif((i != position[0]) and (number == board[i][position[1]])):
            return False

    args = str(math.floor(position[0]/3)+1)+str(math.floor(position[1]/3)+1)

    if(number in small_boxes[args]):
        return False

    return True

#Solving algorithm
def solve(puzzle, small_boxes):

    print("/"*100)
    display_board(puzzle)
    empty_position = empty(puzzle)

    if not empty_position:
        return True
    else:
        row, column = empty_position

    for i in range(1, 10):

        if(is_position_valid(puzzle, small_boxes, i, (row, column))):
            puzzle[row][column] = i
            small_boxes = make_small_boxes(puzzle)

            if solve(puzzle, small_boxes):
                return True

            puzzle[row][column] = 0

    return False

def user_solution(puzzle):
    while empty(puzzle):

        try:
            number = int(input("Enter a number: ").strip())
            row = int(input("Enter the row: ").strip())
            column = int(input("Enter the column: ").strip())

        except ValueError:
            print("Wrong Input")
            continue
        except EOFError:
            continue

        if(is_position_valid(puzzle, make_small_boxes(puzzle), number, (row, column))):
            puzzle[row][column] = number
            display_board(puzzle)
        else:
            print(f"You can't put {number} there!\n\n")

    print("You completed the solution!")

def start(puzzle):

    display_board(puzzle)
    print("\n\nPress 'y' to solve the puzzle, or try to solve it yourself!\n\n")

    #user_solve = multiprocessing.Process(target=user_solution, args=(puzzle,))
    #user_solve.start()

    user_solve = threading.Thread(target=start, args=(problem,))
    user_solve.start()

    def solve_for_me(key):
        if key.char == 'y':
            user_solve.join()
            solve(puzzle, make_small_boxes(puzzle))
            listener.stop()
            viewed_solution = True

    listener = keyboard.Listener(on_press=solve_for_me)
    listener.start()

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

    problem = generate(1, make_small_boxes)
    #user_solve = threading.Thread(target=start, args=(problem,))
    #user_solve.start()
    start(problem)
    #small_boxes = make_small_boxes(problem)
    #solve(problem, small_boxes)









