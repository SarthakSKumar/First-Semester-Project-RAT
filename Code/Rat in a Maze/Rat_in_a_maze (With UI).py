'''
#Last Updated: 22/02/2022 21:47
#Last Updated by: Sarthak S Kumar
#Changelog:
    22/02/2022 21:47
        #Added Functionality to let the user solve the maze manually
        #Comments and Decluttering

    21/02/2022 11:40
        #Added the new try, prompt window (Exit Screen)
        #Fixed Username not displaying while using main()

    08/02/2022 20:40
        # Added Welcome Screen, User Entry Screen, and Maze UI Screen
        # Show the randomly generated maze
        # Show the solution for the randomly generated maze
#Pending:
        # Functionality to check whether the user solution is correct or not
        # Refining a few parts in the application
'''

# MODULES
import numpy as np
import random
import time
import copy
from tkinter import *
from tkinter import ttk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

# Program execution begins from here


def main():
    """Tkinter Window Initialisation"""
    master = Tk()
    master.title("Rat in a Maze")
    master.geometry("1920x1080")
    master.configure(bg="#ffffff")
    master.attributes('-fullscreen', True)

    """ Welcome Screen """
    intro = Frame(master)

    bg = PhotoImage(file=r"Code\Rat in a Maze\Assets\1st_Screen.png")
    canvas1 = Canvas(intro, height=1080, width=2000)

    intro.place(anchor="nw")

    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    intro.after(3000, intro.destroy)
    intro.wait_window(intro)

    """User Entry Screen"""

    user_entry = Frame(master, background="#ffffff")
    user_entry.pack()

    bg = PhotoImage(file=r"Code\Rat in a Maze\Assets\back_4.png")
    canvas1 = Canvas(user_entry, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    user = Label(user_entry, text="Your Name: ", font=(
        r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
    user.place(anchor='e', x=800, y=450)

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

    """ Maze Initialisation and Solution Generation (Backtracking)"""
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

    """Maze UI"""

    squaresize = int(60/N + 60)  # Dynamically changes with the maze size
    tile_color = " "
    rectbox_coordinates = [0, 0, squaresize, squaresize]
    forbidden = []  # To store co-ordinates of obstacle boxes in maze grid

    maze_UI = Frame(master, background="#fffceb")
    maze_UI.pack()

    bg2 = PhotoImage(file=r"Code\Rat in a Maze\Assets\back_5.png")
    canvas2 = Canvas(maze_UI, height=1080, width=2000)
    canvas2.pack()
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    greet = Label(maze_UI, text=f"Hello {username}. Your {tile_color.join(x)} maze is here. Go Ahead! Solve it",
                  font=(r"HK Grotesk", 25), fg="#000000", bg="#ffffff")
    greet.place(anchor='c', x=960, y=150)

    # Canvas to display Maze to be solved
    question_canvas = Canvas(maze_UI, height=(N*squaresize + (N)),
                             width=(N*squaresize + (N)), bg='#ffffff')
    question_canvas.place(anchor='w', x=200, y=540)

    # drawing the maze to be solved in the question canvas
    for i in maze:
        for j in i:
            if j == 1:
                color = "white"

            else:
                color = "grey"
                forbidden.append((rectbox_coordinates[0], rectbox_coordinates[1],
                                  rectbox_coordinates[2], rectbox_coordinates[3]))

            square = question_canvas.create_rectangle(rectbox_coordinates[0], rectbox_coordinates[1],
                                                      rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=1)
            rectbox_coordinates[0] += squaresize
            rectbox_coordinates[2] += squaresize

        rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
        rectbox_coordinates[1] += squaresize
        rectbox_coordinates[3] += squaresize

    # Rat Object to Traverse through the maze
    rat = question_canvas.create_rectangle(
        0, 0, squaresize, squaresize, fill="green", width=1)

    # Keybind Events
    def left(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[0] > 0:
            x = -squaresize
            y = 0
            if (rat_xy[0]+x, rat_xy[1], rat_xy[2]+x, rat_xy[3]) not in forbidden:
                question_canvas.move(rat, x, y)
        else:
            pass

    def right(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[2] <= N*squaresize-1:
            x = squaresize
            y = 0
            if (rat_xy[0]+x, rat_xy[1], rat_xy[2]+x, rat_xy[3]) not in forbidden:
                question_canvas.move(rat, x, y)
        else:
            pass

    def up(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[1] > 0:
            x = 0
            y = -squaresize
            if (rat_xy[0], rat_xy[1]+y, rat_xy[2], rat_xy[3]+y) not in forbidden:
                question_canvas.move(rat, x, y)
        else:
            pass

    def down(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[3] <= N*squaresize-1:
            x = 0
            y = squaresize
            if (rat_xy[0], rat_xy[1]+y, rat_xy[2], rat_xy[3]+y) not in forbidden:
                question_canvas.move(rat, x, y)
        else:
            pass

    master.bind("<Left>", left)
    master.bind("<Right>", right)
    master.bind("<Up>", up)
    master.bind("<Down>", down)

    def checksolution():
        print("cde")  # to check user solution

    check_sol = Button(maze_UI, text="Check", command=checksolution,
                       bg="#4d1354", font=(r'HK Grotesk', (15)), fg="white")
    check_sol.place(anchor='c', x=530, y=950)

    # To Display the Solution Maze

    solution_canvas = Canvas(maze_UI, height=(N*squaresize + (N)),
                             width=(N*squaresize + (N)), bg='#ffffff')

    # Displays Confirmation Window on clicking next
    def nextstep():
        Next = Tk()
        Next.geometry("1500x300")
        Next.title("Solving the Maze")
        Next.configure(bg="#ffffff", border=1)
        message = Label(Next, text=f"Wanna solve another maze?",
                        font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
        message.place(anchor='c', x=750, y=100)

        def restart():
            Next.destroy()
            master.destroy()
            main()

        yes = Button(Next, text="Yeah", command=restart,
                     bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        yes.place(anchor='e', x=750, y=200)
        no = Button(Next, text="Nah", command=exit,
                    bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        no.place(anchor='w', x=850, y=200)

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

    # Button to let computer display the solution
    comp_solve = Button(maze_UI, text="Solve Maze", command=solve,
                        bg="#4d1354", font=(r'HK Grotesk', (15)), fg="white")
    comp_solve.place(anchor='c', x=1390, y=950)

    mainloop()


if __name__ == "__main__":
    main()
