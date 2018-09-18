from rectangle import Rectangle

class Board:
    def __init__(self, canvas, boardpath):

        self.createCurrentBoard(canvas , boardpath)


    def createNoCost(self, canvas, pos, size, color):
        self.rectangle.append(Rectangle(canvas, color, [pos[0]*size, pos[1]*size], size))

    def createCost(self, canvas, pos, size, color, cost):
        self.rectangle.append(Rectangle(canvas, color, [pos[0]*size, pos[1]*size], size, cost=cost))

    def createCurrentBoard(self, canvas, boardpath):
        file = open(boardpath, "r")
        fileContent = file.readlines()

        self.width = len(fileContent[0]) - 1 #TODO: better way than -1
        self.height = len(fileContent)

        print("{0}, {1}".format(self.width, self.height))
        x = 0
        y = 0
        size = 500/self.width
        self.rectangle = []
        while(y < self.height):
            while(x < self.width):
                if boardpath[6] == "1":
                    if fileContent[y][x] == ".":
                        self.createNoCost(canvas, [x, y], size, "white")
                    elif fileContent[y][x] == "#":
                        self.createNoCost(canvas, [x, y], size, "black")
                    elif fileContent[y][x] == "A":
                        self.createNoCost(canvas, [x, y], size, "red")
                    elif fileContent[y][x] == "B":
                        self.createNoCost(canvas, [x, y], size, "#42f456")
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
                        self.createNoCost(canvas, [x, y], size, "red")
                    elif fileContent[y][x] == "B":
                        self.createNoCost(canvas, [x, y], size, "#42f456")

                x += 1
            x = 0;
            y += 1


    #def runDjikstra
