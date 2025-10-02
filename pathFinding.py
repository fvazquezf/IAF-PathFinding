from collections import deque
import heapq

# read map from txt file following predetermined pattern
def parseExample(path):
    with open(path, newline='') as f:
        lines = f.readlines()
        size = list(map(int, lines[0].split(sep=' ')))
        coordinates =  [[] for i in range(size[0])]
        for line, x in zip(lines[1:size[0]+1], range(size[1])):
            values = list(map(int, line.split(sep=' ')))
            coordinates[x] = values
        start = list(map(int, lines[size[0]+1].split(sep=' '))) 
        end = list(map(int, lines[size[0]+2].split(sep=' ')))
        return miningMap(start, end, coordinates)

class position:
    # values for each direction for printing output
    directions = {
     0: "North",
     1: "NorthEast",
     2: "East",
     3: "SouthEast",
     4: "South",
     5: "SouthWest",
     6: "West",
     7: "NorthWest",
     8: "NOP",
    }
    
    def __init__(self, x, y, orientation, cost=0):
        self.cost = cost
        self.x = x  
        self.y = y  
        self.orientation = orientation  

    def __lt__(self, node):
        return self.cost < node.cost

    def __eq__(self, other):
        return isinstance(other, position) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = "(" + str(self.x) + ":" + str(self.y) + ") " + self.directions[self.orientation] + " | Cost: " + str(self.cost)
        return output

# generate new position based on direction the robot is facing
def calculatePosition(currentPosition, direction):
    match direction:
        case 0: 
            return position(currentPosition.x+1, currentPosition.y, 0)
        case 1: 
            return position(currentPosition.x+1, currentPosition.y+1, 1)
        case 2: 
            return position(currentPosition.x, currentPosition.y+1, 2)
        case 3: 
            return position(currentPosition.x-1, currentPosition.y+1, 3)
        case 4: 
            return position(currentPosition.x-1, currentPosition.y, 4)
        case 5: 
            return position(currentPosition.x-1, currentPosition.y-1, 5)
        case 6: 
            return position(currentPosition.x, currentPosition.y-1, 6)
        case 7: 
            return position(currentPosition.x+1, currentPosition.y-1, 7)


class miningMap:
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    def __init__(self, initial, end, coordinates):
        self.coordinates = coordinates
        self.current = position(initial[0], initial[1], initial[2])
        self.end = position(end[0], end[1], end[2])

    # generate copy of current miningMap
    def copy(self):
        initial = [self.current.x, self.current.y, self.current.orientation]
        end = [self.end.x, self.end.y, self.end.orientation]
        return miningMap(initial, end, self.coordinates)

    def __str__(self):
        output = "Current: " + str(self.current) + '\n'
        output += "Destination: " + str(self.end) + '\n'

        output += "Map:\n"
        output += "  x|y: " + " ".join(f"{j}" for j in range(len(self.coordinates[0]))) + '\n\n'
        for i, row in enumerate(self.coordinates):
            row_str = [f"{i:3}:  "] 
            for j, x in enumerate(row):
                if (i, j) == (self.current.x, self.current.y):
                    row_str.append(f"{self.GREEN}{x}{self.RESET}")
                elif (i, j) == (self.end.x, self.end.y):
                    row_str.append(f"{self.RED}{x}{self.RESET}")
                else:
                    row_str.append(str(x))
            output += (" ".join(row_str)) + '\n'
        return output

    # _private_ function for calculating the next position of the robot based on a direction 
    def calculate(self, direction):
        difference = abs(self.current.orientation - direction)
        partialCost = difference if difference < 4 else abs(8-difference)
        newPosition = calculatePosition(self.current, direction)
        if newPosition.x > len(self.coordinates) or newPosition.x < 0:
            raise Exception("InvalidMovement")
        if newPosition.y > len(self.coordinates[0]) or newPosition.y < 0:
            raise Exception("InvalidMovement")
        partialCost += self.coordinates[newPosition.x][newPosition.y]
        newPosition = position(newPosition.x, newPosition.y, direction, partialCost)
        return position(newPosition.x, newPosition.y, direction, partialCost)
    
    # update current position based on the desired direction 
    def move(self, direction):
        newPosition = self.calculate(direction)
        newPosition.cost += self.current.cost 
        self.current = newPosition
        # moving south implies going lower in the y axis

    # calculate the cost for the next movements based on the current position
    def expand(self):
        results = []
        for x in range(8):
            try:
                results.append(self.calculate(x))
            except:
                continue
        return results

# generate the path for arriving to the position in others
def buildPath(previous, others):
    result = []
    for node in others:
        parcial = previous.copy()
        if node in previous or node == position(0, 0, 0): # ignoring origin, can generalize this
            continue
        parcial.append(node)
        result.append(parcial)
    return result

# generate tuple with the cost to arriving to the last position in the path and the whole path.
def buildPathWithWeights(previous, others):
    result = []
    for node in others:
        partial = previous.copy()
        if node in previous or node == position(0, 0, 0): # ignoring origin, can generalize this
            continue
        partial.append(node)
        cost = 0
        for nodePath in partial:
            cost += nodePath.cost
        partial = (cost, partial)
        result.append(partial)
    return result

def breathFirstSearch(path):
    testMap = parseExample(path)
    print(testMap)

    following = testMap.expand()
    following = buildPath([], following)

    frontier = deque(following)  # FIFO queue
    count = 0
    while frontier:
        count += 1
        node = frontier.popleft()

        print("Simulating path: " )
        print(node)
        print()

        testing = testMap.copy()
        for step in node: 
            testing.move(step.orientation)

        print("Current path position: ")
        print(testing)
        print()
        if (node[-1] == testMap.end):
            print("finish\nPath found: ")
            print(node)
            print("with total cost: " + str(testing.current.cost))
            print("paths left in the frontier: " + str(len(frontier)))
            print("ammount of nodes explored: " + str(count))
            break
        temp = testing.expand()
        following = buildPath(node, temp)
        print("new paths added to frontier: ")
        print(following)
        print()
        frontier.extend(following)
    return

def depthFirstSearch(path):
    testMap = parseExample(path)
    print(testMap)

    following = testMap.expand()
    following = buildPath([], following)

    frontier = list(following[::-1])  # FIFO queue
    count = 0
    while frontier:
        count += 1
        node = frontier.pop()

        print("Simulating path: " )
        print(node)
        print()

        testing = testMap.copy()
        for step in node: 
            testing.move(step.orientation)

        print("Current path position: ")
        print(testing)
        print()
        if (node[-1] == testMap.end):
            print("finish\nPath found: ")
            print(node)
            print("with total cost: " + str(testing.current.cost))
            print("paths left in the frontier: " + str(len(frontier)))
            print("ammount of nodes explored: " + str(count))
            break

        temp = testing.expand()
        following = buildPath(node, temp)
        print("new paths added to frontier: ")
        print(following)
        print()
        frontier.extend(following)
    return

def aStarSearch(path):
    testMap = parseExample(path)
    print(testMap)

    following = testMap.expand()
    following = buildPathWithWeights([], following)
    heapq.heapify(following)
    frontier = following  # priority queue
    count = 0
    while frontier:
        count += 1
        node = heapq.heappop(frontier)
        node = node[1]
        print("Simulating path: " )
        print(node)
        print()

        testing = testMap.copy()
        for step in node: 
            testing.move(step.orientation)

        print("Current path position: ")
        print(testing)
        print()
        if (node[-1] == testMap.end):
            print("finish\nPath found: ")
            print(node)
            print("with total cost: " + str(testing.current.cost))
            print("paths left in the frontier: " + str(len(frontier)))
            print("ammount of nodes explored: " + str(count))
            break
        temp = testing.expand()
        following = buildPathWithWeights(node, temp)
        print("new paths added to frontier: ")
        print(following)
        print()
        for value in following:
            heapq.heappush(frontier, value)
    return


aStarSearch("./exampleMap.txt")