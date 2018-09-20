from tkinter import Canvas

# class to hold metadata and to draw tile

class Rectangle:
    def __init__(self, canvas, color, pos, size, cost=1):
        self.canvas = canvas
        self.id = canvas.create_rectangle(pos[0], pos[1], size + pos[0], size + pos[1], fill=color)
        self.cost = cost
        self.distance = 999999
        self.heuristic = 999999

    def updateColor(self, color):
        #self.canvas.after(1, self.updateColor)
        self.canvas.itemconfig(self.id, fill=color)

    def updateOutline(self, color):
        #self.canvas.after(1, self.updateOutline)
        self.canvas.itemconfig(self.id, outline=color)
        self.canvas.itemconfig(self.id, width = 2.0)

    def updateDistance(self, newDistance, parentIndex):
        self.distance = newDistance
        self.parentIndex = parentIndex

    def updateHeuristic(self, newDistance):
        self.heuristic = newDistance

    def getID(self):
        return self.id

    def getCost(self):
        return self.cost

    def getDistance(self):
        return self.distance

    def getParent(self):
        return self.parentIndex

    def getHeuristic(self):
        return self.heuristic

    def getFunctionCost(self):
        return self.heuristic + self.distance
