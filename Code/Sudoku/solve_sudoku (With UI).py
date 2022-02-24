'''
#Project Name: Rat in a maze
#Last Updated: 24/02/2022 22:59
#Last Updated by: Sarthak S Kumar

#Changelog:
    24/02/2022 22:59 Sarthak S Kumar
        # Added Welcome Screen, User Entry Screen, and Maze UI Screen
        # Show the randomly generated sudoku puzzle
        # Added Navigator/Selector functionality
    
    24/02/2022 18:47 Varun Chandrashekar
        # Algorithm to solve sudoku puzzles using Backtracking
        # Command line running of the program with output
#Pending:
    --Cleared
'''
# Modules
import math
import time
from generate_random import generate
from tkinter import *
from tkinter import ttk
from ctypes import windll
from PIL import Image
from PIL import ImageTk

windll.shcore.SetProcessDpiAwareness(1)

# Global Functions


def make_small_boxes(current_board):  # Split the 9x9 puzzle into the 3x3 squares

    small_boxes = {"11": [], "12": [], "13": [], "21": [], "22": [], "23": [], "31": [], "32": [], "33": [], }

    for row in range(1, 10):
        arg1 = math.ceil(row/3)

        for column in range(1, 10):

            arg2 = math.ceil(column/3)
            args = str(arg1) + str(arg2)
            small_boxes[args].append(current_board[row-1][column-1])

    return small_boxes


def empty(board):  # Get empty position in the puzzle
    for row in range(len(board)):
        for column in range(len(board[row])):
            if(board[row][column] == 0):
                return(row, column)

    return None


def is_position_valid(board, small_boxes, number, position):  # Check whether board is valid if number is inserted in given position

    for i in range(9):
        if((i != position[1]) and (number == board[position[0]][i])):  # Check in the same row
            return "r"
        elif((i != position[0]) and (number == board[i][position[1]])):  # Check in the same column
            return "c"

    args = str(math.floor(position[0]/3)+1)+str(math.floor(position[1]/3)+1)

    if(number in small_boxes[args]):  # Check in the small 3x3 boxes
        return "b"

    return ""


def solve(puzzle, small_boxes):  # Solves the Sudoku puzzle

    print("/"*100)
    display_board(puzzle)
    empty_position = empty(puzzle)

    if not empty_position:
        return True  # Return if there is no empty position
    else:
        row, column = empty_position

    for i in range(1, 10):

        if(not is_position_valid(puzzle, small_boxes, i, (row, column))):  # If a valid number is found put it in the puzzle
            puzzle[row][column] = i
            small_boxes = make_small_boxes(puzzle)

            if solve(puzzle, small_boxes):
                return True

            puzzle[row][column] = 0  # Backtrack

    return False


def display_board(board):
    for row in board:
        print("—"*38)
        for element in row:
            if element == 0:
                element = "◼"
            print(" | " + str(element), end="")
        print(" |")


def main():  # Program execution begins from here.
    """Tkinter Window Initialisation"""
    master = Tk()
    master.title("Sudoku")
    master.geometry("1900x1080")
    master.configure(bg="#4d1354")

    """ Welcome Screen """
    intro = Frame(master)
    intro.place(anchor="nw")

    bg = PhotoImage(file=r"Code\Sudoku\Assets\intro.png")
    canvas1 = Canvas(intro, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    intro.after(3000, intro.destroy)
    intro.wait_window(intro)

    """User Entry Screen"""
    user_entry = Frame(master, background="#4d1354")
    user_entry.pack()

    bg = PhotoImage(file=r"Code\Sudoku\Assets\user_entry.png")
    canvas1 = Canvas(user_entry, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    Label(user_entry, text="Welcome", font=(r"HK Grotesk", 50), fg="#ffffff", bg="#4d1354").place(anchor='c', x=960, y=275)

    Label(user_entry, text="Your Name: ", font=(r"HK Grotesk", 25), fg="#ffffff", bg="#4d1354").place(anchor='e', x=800, y=450)

    sizebox = Entry(user_entry, font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354")
    sizebox.place(anchor='w', x=960, y=450)

    def movenext():
        global username
        username = sizebox.get()
        user_entry.after(1000, user_entry.destroy)

    submit = Button(user_entry, text="Submit", command=movenext, bg="#ffffff", font=(r'HK Grotesk', (25)), fg="#4d1354").place(anchor='c', x=960, y=800)
    user_entry.wait_window(user_entry)

    """Sudoku UI"""
    sudoku_UI = Frame(master, background="#4d1354")
    sudoku_UI.pack()

    bg2 = PhotoImage(file=r"Code\Sudoku\Assets\sudoku_UI.png")
    canvas2 = Canvas(sudoku_UI, height=1080, width=2000)
    canvas2.pack()
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    headline = Label(sudoku_UI, text=f"Hello {username}\n Your Sudoku is here. Go Ahead, Solve it", font=(r"HK Grotesk", 30), fg="#ffffff", bg="#4d1354")
    headline.place(anchor='center', x=1390, y=375)

    question_canvas = Canvas(sudoku_UI, height=720, width=720, bg='#4d1354', bd=0, highlightthickness=0, relief='ridge')
    question_canvas.place(anchor='center', x=500, y=512)

    for i in (0, 3, 6, 9):
        question_canvas.create_line(0, 80*i, 730, 80*i, width=5, fill="#ffffff")
        question_canvas.create_line(80*i, 0, 80*i, 730, width=5, fill="#ffffff")

    for i in range(11):
        question_canvas.create_line(80*i, 0, 80*i, 730, width=2, fill="#ffffff")
        question_canvas.create_line(0, 80*i, 730, 80*i, width=2, fill="#ffffff")

    problem = generate(1, make_small_boxes)
    y_coord, x_coord, p, q = 40, 40, 0, 0
    allowed_squares = []
    for i in problem:
        for j in i:
            if j == 0:
                j = ""
                allowed_squares.append((x_coord-40, y_coord-40, x_coord+40, y_coord+40))
            question_canvas.create_text(x_coord, y_coord, font=(r"HK Grotesk", 30), fill="#ffffff", text=j)
            x_coord += 80
            p += 1
        p = 0
        x_coord = 40
        y_coord += 80
        q += 1

    pos = allowed_squares[1]
    selector = question_canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill="#4d1354", width=3, outline="#35668f")

    def left(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[0] > 0:
            x = -80
            y = 0
            question_canvas.move(selector, x, y)
            if (selector_xy[0] + x, selector_xy[1], selector_xy[2] + x, selector_xy[3]) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    def right(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[2] <= 719:
            x = 80
            y = 0
            question_canvas.move(selector, x, y)
            if (selector_xy[0] + x, selector_xy[1], selector_xy[2] + x, selector_xy[3]) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    def up(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[1] > 0:
            x = 0
            y = -80
            question_canvas.move(selector, x, y)
            if (selector_xy[0], selector_xy[1] + y, selector_xy[2], selector_xy[3] + y) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    def down(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[3] <= 719:
            x = 0
            y = 80
            question_canvas.move(selector, x, y)
            if (selector_xy[0], selector_xy[1] + y, selector_xy[2], selector_xy[3] + y) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    master.bind("<Left>", left)
    master.bind("<Right>", right)
    master.bind("<Up>", up)
    master.bind("<Down>", down)

    comp_solve = Button(sudoku_UI, text="Give Up!", command=None,
                        bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
    comp_solve.place(anchor='center', x=1490, y=800)
    #solve(problem, make_small_boxes(problem))

    sudoku_UI.wait_window(sudoku_UI)


if __name__ == '__main__':
    main()
