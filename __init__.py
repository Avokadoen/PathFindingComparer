from tkinter import *
from board import Board
import random
import time
from pathlib import Path

# sources:
# tk mainloop: https://stackoverflow.com/a/29158947

def callback():
    print ("click!")


def hello():
    print ("hello!")

def main():
    tk = Tk()
    tk.title = "Game"
    #tk.resizable(0,0)
    tk.wm_attributes("-topmost", 1)

    screenWidth=500

    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()

    board = Board(canvas, "boards/board-2-1.txt")

    djikB = Button(tk, text="djikstra's", command=callback)
    djikB.place(anchor="nw", x=screenWidth/3, y=300)
    aStarB = Button(tk, text="A* ", command=callback)
    aStarB.place(anchor="nw", x=300, y=300)


    menubar = Menu(tk)

    # create a pulldown menu, and add it to the menu bar
    programmenu = Menu(menubar, tearoff=0)
    programmenu.add_command(label="Exit", command=tk.quit)
    menubar.add_cascade(label="Program", menu=programmenu)

    levelsmenu = Menu(menubar, tearoff=0)
    levelFolder = Path("./boards")
    levelsPaths = list(levelFolder.glob('./board*'))
    for path in levelsPaths:
        print(str(path))
        levelsmenu.add_command(label=path, command= lambda: board.createCurrentBoard(canvas, str(path)))
    menubar.add_cascade(label="Levels", menu=levelsmenu)

    # display the menu
    tk.config(menu=menubar)

    tk.mainloop()

if __name__ == '__main__':
    main()
