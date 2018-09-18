from tkinter import Canvas

class Rectangle:
    def __init__(self, canvas, color, pos, size, cost=10):
        self.canvas = canvas
        self.id = canvas.create_rectangle(pos[0], pos[1], size + pos[0], size + pos[1], fill=color)
        self.cost = cost

    def updateColor(self, color):
        self.canvas.after(1, self.updateColor)
        self.canvas.itemconfig(self.id, fill=color)
