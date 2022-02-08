'''
#Last Updated: 08/02/2022 20:40pm
#Last Updated by: Sarthak S Kumar
    * Pending:
        # Yet to add the functionality to enable user solve the maze manually
        # Functionality to check whether the user solution is correct or not
        # Exit Screens, and refining a few parts in the application
    * Done:
        # Added Welcome Screen, User Entry Screen, and Maze UI Screen
        # Show the randomly generated maze
        # Show the solution for the randomly generated maze
'''

import numpy as np
import random
import time
import copy
from tkinter import *
from tkinter import ttk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

"""Tkinter Initialisation"""
master = Tk()
master.title("Rat in a Maze")
master.geometry("1920x1080")
master.configure(bg="#ffffff")
master.attributes('-fullscreen', True)

""" Welcome Screen """
intro = Frame(master)

bg = PhotoImage(file=r"Code\Assets\1st_Screen.png")
canvas1 = Canvas(intro, height=1080, width=2000)

intro.place(anchor="nw")

canvas1.pack()
canvas1.create_image(0, 0, image=bg, anchor="nw")

intro.after(3000, intro.destroy)
intro.wait_window(intro)

"""User Entry Screen"""

user_entry = Frame(master, background="#ffffff")
user_entry.pack()

bg = PhotoImage(file=r"Code\Assets\back_4.png")
canvas1 = Canvas(user_entry, height=1080, width=2000)
canvas1.pack()
canvas1.create_image(0, 0, image=bg, anchor="nw")

username = Label(user_entry, text="Your Name: ",
                 font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
username.place(anchor='e', x=800, y=450)

sizebox = Entry(user_entry, font=(r"HK Grotesk", 20),
                fg="#000000", bg="#ffffff")
sizebox.place(anchor='w', x=960, y=450)

sizelabel = Label(user_entry, text="Maze Size: ",
                  font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
sizelabel.place(anchor='e', x=800, y=540)

clicked = StringVar()
clicked.set("Select one")
gridsizes = [
    "2 x 2",
    "3 x 3",
    "4 x 4",
    "5 x 5",
    "6 x 6",
    "7 x 7",
    "8 x 8",
    "9 x 9",
    "10 x 10"
]
drop = OptionMenu(user_entry, clicked, *gridsizes)
drop.place(anchor='w', x=960, y=540)
drop.config(font=(r'HK Grotesk', (20)), bg='#ffffff', fg="#000000")


def movenext():
    global N, username, x
    username = sizebox.get()  # Maze Size Variable
    x = clicked.get().split()
    N = int(x[0])
    user_entry.after(1000, user_entry.destroy)


submit = Button(user_entry, text="Submit", command=movenext,
                bg="#4d1354", font=(r'HK Grotesk', (25)), fg="white")
submit.place(anchor='c', x=960, y=900)

user_entry.wait_window(user_entry)

""" Maze Initialisation and Solution Finding"""
sol_maze = []
while True:
    global maze
    maze = np.random.randint(2, size=(N, N))

    def MAZE(maze):
        global sol
        sol = copy.deepcopy(maze)

        if BACKTRACKING_ALGORITHM(maze, 0, 0, sol) == False:
            return False

        return True

    def BACKTRACKING_ALGORITHM(maze, x, y, sol):

        if x == N-1 and y == N-1:
            sol[x][y] = 5
            return True

        if check(maze, x, y) == True:
            sol[x][y] = 5

            if BACKTRACKING_ALGORITHM(maze, x+1, y, sol) == True:
                return True

            if BACKTRACKING_ALGORITHM(maze, x, y+1, sol) == True:
                return True

            sol[x][y] = 0
            return False

    def check(maze, x, y):
        if x >= 0 and x < N and y >= 0 and y < N and maze[x][y] == 1:
            return True

    if MAZE(maze) == False or maze[N-1][N-1] == 0 or maze[0][0] == 0:
        continue
    break

"""Maze Display UI"""

squaresize = int(60/N + 60)
tile_color = " "
rectbox_coordinates = [0, 0, squaresize, squaresize]

maze_UI = Frame(master, background="#fffceb")
maze_UI.pack()

bg2 = PhotoImage(file=r"Code\Assets\back_5.png")
canvas2 = Canvas(maze_UI, height=1080, width=2000)
canvas2.pack()
canvas2.create_image(0, 0, image=bg2, anchor="nw")

greet = Label(maze_UI, text=f"Hello {username}. Your {tile_color.join(x)} maze is here. Go Ahead! Solve it",
              font=(r"HK Grotesk", 25), fg="#000000", bg="#ffffff")
greet.place(anchor='c', x=960, y=150)

question_canvas = Canvas(master, height=(N*squaresize + (N)),
                         width=(N*squaresize + (N)), bg='#ffffff')
question_canvas.place(anchor='w', x=200, y=540)

solution_canvas = Canvas(master, height=(N*squaresize + (N)),
                         width=(N*squaresize + (N)), bg='#ffffff')

for i in maze:
    for j in i:
        if j == 1:
            color = "white"
        else:
            color = "grey"
        square = question_canvas.create_rectangle(rectbox_coordinates[0], rectbox_coordinates[1],
                                                  rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=1)
        rectbox_coordinates[0] += squaresize
        rectbox_coordinates[2] += squaresize

    rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
    rectbox_coordinates[1] += squaresize
    rectbox_coordinates[3] += squaresize


def somefunc():
    print("cde")  # to check user solution


def nextstep():
    Next = Tk()
    Next.geometry("1500x300")
    Next.title("Solving the Maze")
    Next.configure(bg="#ffffff", border=1)
    message = Label(Next, text=f"Wanna solve another maze?",
                    font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
    message.place(anchor='c', x=750, y=100)

    yes = Button(Next, text="Yeah", command=start,
                 bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
    yes.place(anchor='c', x=1000, y=270)
    no = Button(Next, text="Nah", command=exit,
                bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
    no.place(anchor='c', x=1250, y=270)


def solve():
    confirm = Tk()
    confirm.geometry("1500x300")
    confirm.title("Solving the Maze")
    confirm.configure(bg="#ffffff", border=1)
    message = Label(confirm, text=f"Solution coming up! Please Wait",
                    font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
    message.place(anchor='c', x=750, y=100)

    confirm.after(3000, confirm.destroy)
    confirm.wait_window(confirm)

    rectbox_coordinates = [0, 0, squaresize, squaresize]
    solution_canvas.place(anchor='e', x=1720, y=540)
    for i in sol:
        for j in i:
            if j == 5:
                color = "green"
            elif j == 1:
                color = "white"
            else:
                color = "grey"
            square = solution_canvas.create_rectangle(rectbox_coordinates[0], rectbox_coordinates[1],
                                                      rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=1)
            rectbox_coordinates[0] += squaresize
            rectbox_coordinates[2] += squaresize

        rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
        rectbox_coordinates[1] += squaresize
        rectbox_coordinates[3] += squaresize

    greet.configure(text="You gave up so quick! Better Luck Next Time 🦾")
    comp_solve.destroy()
    check_sol.destroy()

    nextb = Button(maze_UI, text="Next", command=nextstep,
                   bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
    nextb.place(anchor='c', x=960, y=950)


comp_solve = Button(maze_UI, text="Solve Maze", command=solve,
                    bg="#4d1354", font=(r'HK Grotesk', (15)), fg="white")
comp_solve.place(anchor='c', x=1390, y=950)

check_sol = Button(maze_UI, text="Check", command=somefunc,
                   bg="#4d1354", font=(r'HK Grotesk', (15)), fg="white")
check_sol.place(anchor='c', x=530, y=950)


mainloop()
