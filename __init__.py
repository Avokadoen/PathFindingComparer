from tkinter import *
from board import Board
import random
import time
from pathlib import Path
from functools import partial

# sources:
# tk mainloop: https://stackoverflow.com/a/29158947

def djikstraInit(board, canvas):
    board.runDjikstra(canvas)


def aStarInit(board, canvas):
    board.runAStar(canvas)

def breadthInit(board, canvas):
    board.runBreadthFirst(canvas)

def main():
    tk = Tk()
    tk.title = "search algorithms demo"
    #tk.resizable(0,0)
    tk.wm_attributes("-topmost", 1)

    screenWidth=500

    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()

    board = Board(canvas, "board-2-1.txt")

    # some tk buttons to init the algorithms
    breadthB = Button(tk, text="breadth first", command=partial(breadthInit, board, canvas))
    breadthB.place(anchor="nw", x=100, y=300)
    djikB = Button(tk, text="djikstra's", command=partial(djikstraInit, board, canvas))
    djikB.place(anchor="nw", x=200, y=300)
    aStarB = Button(tk, text="A* ", command=partial(aStarInit, board, canvas))
    aStarB.place(anchor="nw", x=300, y=300)

    menubar = Menu(tk)

    # create a pulldown menu, and add it to the menu bar
    programmenu = Menu(menubar, tearoff=0)
    programmenu.add_command(label="Exit", command=tk.quit)
    menubar.add_cascade(label="Program", menu=programmenu)

    # load each file in boards directory and list them in a meny
    levelsmenu = Menu(menubar, tearoff=0)
    levelFolder = Path("./boards/")
    levelsPaths = list(levelFolder.glob('./board*'))
    loadLevelsFunc = []
    counter = 0
    for path in levelsPaths:
        _, finalPath = str(path).split("/")
        levelsmenu.add_command(label=finalPath, command=partial(board.createCurrentBoard, canvas, finalPath))
    menubar.add_cascade(label="Levels", menu=levelsmenu)

    # display the menu
    tk.config(menu=menubar)

    tk.mainloop()

# application entry point
if __name__ == '__main__':
    main()
