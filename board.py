from rectangle import Rectangle
import math
import queue

# class to hold all of the world state and to compute path

class Board:
    def __init__(self, canvas, boardpath):
        self.rectangle = []
        self.filepath = boardpath
        self.createCurrentBoard(canvas , boardpath)

    def createNoCost(self, canvas, pos, size, color):
        self.rectangle.append(Rectangle(canvas, color, [pos[0]*size, pos[1]*size], size))

    def createCost(self, canvas, pos, size, color, cost):
        self.rectangle.append(Rectangle(canvas, color, [pos[0]*size, pos[1]*size], size, cost=cost))

    # used to travers from endpoint to start and draw path red
    def createFinalPath(self, current, startIndex):
        while current != startIndex:
            self.rectangle[current].updateOutline("red")
            current = self.rectangle[current].getParent()

    # find valid adjucent tiles
    def createNeighbours(self, current):
        neighbours=[]
        if((current % self.width) >= 1):
            neighbours.append(current-1)
        if(current % self.width != self.width-1 or current == 0):
            neighbours.append(current+1)
        if(current / self.width < (self.height-1)):
            neighbours.append(current+self.width)
        if(current / self.width >= 1):
            neighbours.append(current-self.width)
        return neighbours

    # load board from file using board name
    def createCurrentBoard(self, canvas, boardpath):

        del self.rectangle[:]
        canvas.delete("all")
        self.filepath = boardpath
        file = open("boards/" + self.filepath, "r")
        fileContent = file.readlines()

        self.width = len(fileContent[0]) - 1 #TODO: better way than -1?
        self.height = len(fileContent)

        x = 0
        y = 0
        size = 500/self.width

        # loop each character and create a rectangle that will represent said character
        while(y < self.height):
            while(x < self.width):
                if boardpath[6] == "1": # If board doesn't have colored grid
                    if fileContent[y][x] == ".":
                        self.createNoCost(canvas, [x, y], size, "white")
                    elif fileContent[y][x] == "#":
                        self.createNoCost(canvas, [x, y], size, "black")
                    elif fileContent[y][x] == "A":
                        self.createCost(canvas, [x, y], size, "red", 0)
                    elif fileContent[y][x] == "B":
                        self.createCost(canvas, [x, y], size, "#42f456", 0)
                elif boardpath[6] == "2": # If board has colored grid with different costs
                    if fileContent[y][x] == "r":
                        self.createCost(canvas, [x, y], size, "#998834", 1)
                    elif fileContent[y][x] == "g":
                        self.createCost(canvas, [x, y], size, "#81db8a", 5)
                    elif fileContent[y][x] == "f":
                        self.createCost(canvas, [x, y], size, "#2c8235", 10)
                    elif fileContent[y][x] == "m":
                        self.createCost(canvas, [x, y], size, "#9b988a", 50)
                    elif fileContent[y][x] == "w":
                        self.createCost(canvas, [x, y], size, "#5a85e2", 100)
                    elif fileContent[y][x] == "A":
                        self.createCost(canvas, [x, y], size, "red", 0)
                    elif fileContent[y][x] == "B":
                        self.createCost(canvas, [x, y], size, "#42f456", 0)

                x += 1
            x = 0;
            y += 1

    # Source: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # uses the current board state to compute a path with djikstra algorithm
    def runDjikstra(self, canvas):
        self.createCurrentBoard(canvas, self.filepath)
        unvisited = []
        current = 0
        startIndex = 0
        for i in range(len(self.rectangle)):
            if(canvas.itemcget(self.rectangle[i].getID(), "fill") != "black"):
                unvisited.append(i)
            if(canvas.itemcget(self.rectangle[i].getID(), "fill") == "red"):
                self.rectangle[i].updateDistance(0, i)
                current = i
                startIndex = i

        visited = []
        indexWidth = self.width - 1
        indexHeight = self.height - 1

        while canvas.itemcget(self.rectangle[current].getID(), "fill") != "#42f456" and self.rectangle[current].getDistance() < 999999:
            self.rectangle[current].updateOutline("yellow")

            neighbours = self.createNeighbours(current)

            for neighbour in neighbours:
            # if left node is cheaper to travers from current
                if(neighbour in unvisited):
                    if(self.rectangle[neighbour].getDistance() > self.rectangle[neighbour].getCost() + self.rectangle[current].getDistance()):
                        self.rectangle[neighbour].updateDistance(self.rectangle[neighbour].getCost() + self.rectangle[current].getDistance(), current)
                        self.rectangle[neighbour].updateOutline("purple")

            unvisited.remove(current)
            visited.append(current)

            newCurrentCost = 999999
            for i in unvisited:
                if self.rectangle[i].getDistance() < newCurrentCost:
                    newCurrentCost = self.rectangle[i].getDistance()
                    current = i

        self.createFinalPath(current, startIndex)

    # Sources: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
    # uses the current board state to compute a path with a* algorithm
    def runAStar(self, canvas):

        self.createCurrentBoard(canvas, self.filepath)
        illegalTiles = []
        current = 0
        startIndex = 0
        goalIndex = 0
        for i in range(len(self.rectangle)):
            if(canvas.itemcget(self.rectangle[i].getID(), "fill") == "black"):
                illegalTiles.append(i)
            elif(canvas.itemcget(self.rectangle[i].getID(), "fill") == "red"):
                self.rectangle[i].updateDistance(0, i)
                current = i
                startIndex = i
            elif(canvas.itemcget(self.rectangle[i].getID(), "fill") == "#42f456"):
                goalIndex = i

        # foreach rectangle, compute a heuristic
        for i in range(len(self.rectangle)):
            x = goalIndex % self.width - i % self.width
            y = (int)(goalIndex / self.width) - (int)(i / self.width)
            # we use 2.5 as a modifier to make it balanced compared to cost
            self.rectangle[i].updateHeuristic(math.sqrt(math.pow(x, 2) + math.pow(y, 2))*2.5)

        closedTiles = []
        indexWidth = self.width - 1
        indexHeight = self.height - 1
        openTiles = []
        openTiles.append(current)

        while openTiles:
            # record tile we have locked
            self.rectangle[current].updateOutline("yellow")

            newFunctionCost = 999999*2
            for i in openTiles:
                if self.rectangle[i].getFunctionCost() < newFunctionCost:
                    newFunctionCost = self.rectangle[i].getFunctionCost()
                    current = i

            if(current == goalIndex):
                break

            openTiles.remove(current)
            closedTiles.append(current)

            neighbours = self.createNeighbours(current)

            for neighbour in neighbours:
                 if( not (neighbour in illegalTiles or neighbour in closedTiles)):
                         if(not (neighbour in openTiles)):
                             openTiles.append(neighbour)
                             self.rectangle[neighbour].updateOutline("purple")

                         # if new path is cheaper, update path cost and parent
                         if(self.rectangle[neighbour].getDistance() > self.rectangle[current].getDistance() + self.rectangle[neighbour].getCost()):
                             self.rectangle[neighbour].updateDistance(self.rectangle[current].getDistance() + self.rectangle[neighbour].getCost(), current)

        self.createFinalPath(current, startIndex)

    # Soruces: https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
    #uses the current board state to compute a path with breadth first algorithm
    def runBreadthFirst(self, canvas):
        self.createCurrentBoard(canvas, self.filepath)
        closedTiles = []
        current = 0
        startIndex = 0
        goalIndex = 0
        for i in range(len(self.rectangle)):
            if(canvas.itemcget(self.rectangle[i].getID(), "fill") == "black"):
                closedTiles.append(i)
            elif(canvas.itemcget(self.rectangle[i].getID(), "fill") == "red"):
                self.rectangle[i].updateDistance(0, i)
                current = i
                startIndex = i
            elif(canvas.itemcget(self.rectangle[i].getID(), "fill") == "#42f456"):
                goalIndex = i

        openTilesList = []
        openTilesList.append(current)
        while openTilesList:
            current = openTilesList.pop(0)
            self.rectangle[current].updateOutline("yellow")

            if(current == goalIndex):
                break

            neighbours = self.createNeighbours(current)
            for neighbour in neighbours:
                if not neighbour in closedTiles:
                    if not neighbour in openTilesList:
                        openTilesList.append(neighbour)
                    if(self.rectangle[neighbour].getDistance() > self.rectangle[neighbour].getCost() + self.rectangle[current].getDistance()):

                        self.rectangle[neighbour].updateDistance(self.rectangle[neighbour].getCost() + self.rectangle[current].getDistance(), current)
                        self.rectangle[neighbour].updateOutline("purple")

            closedTiles.append(current)

        self.createFinalPath(current, startIndex)
