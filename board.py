from rectangle import Rectangle
import math

class Board:
    def __init__(self, canvas, boardpath):
        self.rectangle = []
        self.filepath = boardpath
        self.createCurrentBoard(canvas , boardpath)


    def createNoCost(self, canvas, pos, size, color):
        self.rectangle.append(Rectangle(canvas, color, [pos[0]*size, pos[1]*size], size))

    def createCost(self, canvas, pos, size, color, cost):
        self.rectangle.append(Rectangle(canvas, color, [pos[0]*size, pos[1]*size], size, cost=cost))

    def createCurrentBoard(self, canvas, boardpath):

        del self.rectangle[:]
        canvas.delete("all")
        self.filepath = boardpath
        file = open("boards/" + self.filepath, "r")
        fileContent = file.readlines()

        self.width = len(fileContent[0]) - 1 #TODO: better way than -1?
        self.height = len(fileContent)

        print("{0}, {1}".format(self.width, self.height))
        x = 0
        y = 0
        size = 500/self.width

        while(y < self.height):
            while(x < self.width):
                if boardpath[6] == "1":
                    if fileContent[y][x] == ".":
                        self.createNoCost(canvas, [x, y], size, "white")
                    elif fileContent[y][x] == "#":
                        self.createNoCost(canvas, [x, y], size, "black")
                    elif fileContent[y][x] == "A":
                        self.createCost(canvas, [x, y], size, "red", 0)
                    elif fileContent[y][x] == "B":
                        self.createCost(canvas, [x, y], size, "#42f456", 0)
                elif boardpath[6] == "2":
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

    '''
    source: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    - Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set.
    - Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all other nodes. Set the initial node as current.
    - For the current node, consider all of its unvisited neighbors and calculate their tentative distances through the current node.
    Compare the newly calculated tentative distance to the current assigned value and assign the smaller one. For example, if the current node A is marked with a distance of 6, and the edge connecting it with a neighbor B has length 2, then the distance to B through A will be 6 + 2 = 8. If B was previously marked with a distance greater than 8 then change it to 8. Otherwise, keep the current value.
    - When we are done considering all of the unvisited neighbors of the current node, mark the current node as visited and remove it from the unvisited set. A visited node will never be checked again.
    - If the destination node has been marked visited (when planning a route between two specific nodes) or if the smallest tentative distance among the nodes in the unvisited set is infinity (when planning a complete traversal; occurs when there is no connection between the initial node and remaining unvisited nodes), then stop. The algorithm has finished.
    - Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the new "current node", and go back to step 3.
    '''
    def runDjikstra(self, canvas):
        self.createCurrentBoard(canvas, self.filepath)
        unvisited = []
        current = 0
        startIndex = 0
        print(len(self.rectangle))
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

            # if left node is cheaper to travers from current
            if(current-1 in unvisited):
                if(((current % self.width) >= 1) and
                    (self.rectangle[current-1].getDistance() > self.rectangle[current-1].getCost() + self.rectangle[current].getDistance())):

                    self.rectangle[current-1].updateDistance(self.rectangle[current-1].getCost() + self.rectangle[current].getDistance(), current)
                    print("left true")

            # if right node is cheaper to travers from current
            if(current+1 in unvisited):
                if((current % self.width != indexWidth or current == 0) and
                    (self.rectangle[current+1].getDistance() > self.rectangle[current+1].getCost() + self.rectangle[current].getDistance())):

                    self.rectangle[current+1].updateDistance(self.rectangle[current+1].getCost() + self.rectangle[current].getDistance(),current)
                    print("right true")

            # if down node is cheaper to travers from current
            if(current+self.width in unvisited):
                if((current / self.width <= indexHeight) and
                    (self.rectangle[current+self.width].getDistance() > self.rectangle[current+self.width].getCost() + self.rectangle[current].getDistance())):

                    self.rectangle[current+self.width].updateDistance(self.rectangle[current+self.width].getCost() + self.rectangle[current].getDistance(), current)
                    print("down true")

            # if up node is cheaper to travers from current
            if(current-self.width in unvisited):
                if((current / self.width >= 1) and
                    (self.rectangle[current-self.width].getDistance() > self.rectangle[current-self.width].getCost() + self.rectangle[current].getDistance())):

                    self.rectangle[current-self.width].updateDistance(self.rectangle[current-self.width].getCost() + self.rectangle[current].getDistance(), current)
                    print("up true")

            unvisited.remove(current)
            visited.append(current)

            newCurrentCost = 999999
            for i in unvisited:
                if self.rectangle[i].getDistance() < newCurrentCost:
                    newCurrentCost = self.rectangle[i].getDistance()
                    current = i

        while current != startIndex:
            self.rectangle[current].updateOutline("red")
            current = self.rectangle[current].getParent()

    def runAStar(self, canvas):

        self.createCurrentBoard(canvas, self.filepath)
        illegalTiles = []
        current = 0
        startIndex = 0
        goalIndex = 0
        print(len(self.rectangle))
        for i in range(len(self.rectangle)):
            if(canvas.itemcget(self.rectangle[i].getID(), "fill") == "black"):
                illegalTiles.append(i)
            elif(canvas.itemcget(self.rectangle[i].getID(), "fill") == "red"):
                self.rectangle[i].updateDistance(0, i)
                current = i
                startIndex = i
            elif(canvas.itemcget(self.rectangle[i].getID(), "fill") == "#42f456"):
                goalIndex = i

        for i in range(len(self.rectangle)):
            x = goalIndex % self.width - i % self.width
            y = (int)(goalIndex / self.width) - (int)(i / self.width)
            self.rectangle[i].updateHeuristic(math.sqrt(math.pow(x, 2) + math.pow(y, 2)))

        closedTiles = []
        indexWidth = self.width - 1
        indexHeight = self.height - 1

        openTiles = []
        openTiles.append(current)

        while openTiles:
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

            neighbours = []

            if((current % self.width) >= 1):
                neighbours.append(current-1)
            if(current % self.width != indexWidth or current == 0):
                neighbours.append(current+1)
            if(current / self.width <= indexHeight):
                neighbours.append(current+self.width)
            if(current / self.width >= 1):
                neighbours.append(current-self.width)

            for neighbour in neighbours:
                 if( not (neighbour in illegalTiles or neighbour in closedTiles)):
                         if(not (neighbour in openTiles)):
                             openTiles.append(neighbour)
                             self.rectangle[current].updateOutline("purple")
                         if(self.rectangle[neighbour].getDistance() > self.rectangle[current].getDistance() + self.rectangle[neighbour].getCost()):
                             self.rectangle[neighbour].updateDistance(self.rectangle[current].getDistance() + self.rectangle[neighbour].getCost(), current)

        while current != startIndex:
            self.rectangle[current].updateOutline("red")
            current = self.rectangle[current].getParent()
