from queue import PriorityQueue


def rushHour(heuristic, startBoard):
    startState = State(startBoard, 0, None, heuristic)
    stateExplored = 0   # number of states were explored
    visited = []        # list of states that were visited
    generatedList = []  # list of states that were generated during the process
    numMoves = 0        # number of possible moves
    q = PriorityQueue() # frontier list

    q.put((startState.f_n, startState))

    while not q.empty():
        # pop the front of the frontier
        currState = q.get()[1]
        stateExplored += 1

        # check if reach goal
        if not isGoal(currState):
            # add currState to the path
            visited.append(currState.board)
            # generate new states
            newStates = currState.generateNewStates()

            # add new state to frontier
            for state in newStates:
                if state.board not in generatedList and state.board not in visited:
                    generatedList.append(state.board)
                    q.put((state.f_n, state))
        else:
            break

    path = findPath(currState)
    numMoves = len(path) - 1
    displayPath(path)
    displayMoves(numMoves)
    displayStateExplored(stateExplored)


#find the path to current state
def findPath(currState):
    path = []
    while(currState):
        path.append(currState)
        currState = currState.parent
    return path[::-1]


# display path
def displayPath(path):
    for state in path:
        state.printBoard()
        print()

# display number of moves
def displayMoves(numMoves):
    print("Total moves: {}".format(numMoves))


# display number of state explored
def displayStateExplored(stateExplored):
    print("Total states explored: {}".format(stateExplored))


# check if we reach the goal
def isGoal(currState):
    XX_head = currState.carCollection['X']
    XX_pos = currState.findCarPos('X', XX_head)
    # check if XX car is in the 3rd row and at position 4 and 5 horizontally
    if (XX_head[0] == 2 and XX_pos[1] == len(currState.board) -1):
        return True
    else:
        return False


# state object
class State:
    def __init__(self, board, g_n, parent, heuristic):
        self.board = board # representation of the game board
        self.g_n = g_n # g(n)
        self.numBlock = 0 # number of vehicles blocking the exit
        self.carCollection = {} # contains key, value pair where key is the car unique label
                                # and value is the tuple (a,b) determine the postion of head of the car
                                # where a is starting row, b is starting index
        self.carList = []  # list of Car objects in the board
        self.f_n = 0 # f(n)
        self.parent = parent # parent node
        self.heuristic = heuristic # determine which heuristic to use: blocking or custon
        self.blockingList = [] # list of vehicles blocking the exit
        self.initialize()

    def __lt__(self, other):
        return self.f_n < other.f_n
    
    def initialize(self):
        self.findCarCollection()
        self.initiateCar()
        self.findBlockingList()
        if self.g_n != 0:
            self.numBlock = len(self.blockingList) + 1
        self.findFn()

    # find number of distinct car in the board
    def findCarCollection(self):
        for row, pos in enumerate(self.board):
            for i in range(len(pos)):
                if pos[i] != '-' and pos[i] not in self.carCollection:
                    self.carCollection[pos[i]] = (row, i)
    
    # find f(n) according to choice of heuristic
    # if heuristic == 0 use blocking heurtistic
    # else use custom heuristic
    # custom heuristic: consider the number of car blocking the exit
    # and the distance between the red car and the exit
    def findFn(self):
        if self.heuristic == 0:
            self.f_n = self.g_n + self.numBlock
        else:
            self.f_n = self.g_n + self.numBlock + self.distanceToExit() 
    # get the distance from red car to exit
    def distanceToExit(self):
        head = self.carCollection['X']
        XX_pos = self.findCarPos('X', head)
        return len(self.board) - XX_pos[1] - 1

    # find list of vehicles blocking the exit
    def findBlockingList(self):
        head = self.carCollection['X']
        # find the position of the XX car
        XX_pos = self.findCarPos('X', head)
        for i in range(XX_pos[1]+1, len(self.board)):
            if self.board[head[0]][i] != 'X' and self.board[head[0]][i] != '-' and self.board[head[0]][i] not in self.blockingList:
                self.blockingList.append(self.board[head[0]][i])

    
    # find number of moves to move blocking vehicles out of the way
    def findNumMoves(self, label):
        head = self.carCollection[label]
        pos = self.findCarPos(label, head)
        return 2 - pos[0] + 1

    # initial carList
    def initiateCar(self):
        for carLabel in self.carCollection:
            head = self.carCollection[carLabel]
            orientation = self.findCarOrientation(
                carLabel, head)
            position = self.findCarPos(carLabel, head)
            self.carList.append(Car(carLabel, head, orientation, position))
        return

    # find the postion of car in the board
    # return a tuple (a,b) where a is start position and b is end position
    # if car's orientation is "V" start and end position are in the same row
    # else start and end position are in the same columns
    def findCarPos(self, label, head):
        orientation = self.findCarOrientation(label, head)
        if orientation == 'V':
            if head[0]+2 < 6 and self.board[head[0]+2][head[1]] == label:
                return (head[0], head[0]+2)
            else:
                return (head[0], head[0]+1)
        else:
            if head[1]+2 < 6 and self.board[head[0]][head[1]+2] == label:
                return (head[1], head[1]+2)
            else:
                return (head[1], head[1]+1)

    # find car orientation
    def findCarOrientation(self, label, head):
        # check is car is vertical
        if(head[0]+1 < 6 and self.board[head[0]+1][head[1]] == label):
            return 'V'
        else:
            return 'H'

    # generate possible moves for the current state
    def generateNewStates(self):
        moves = []
        for car in self.carList:
            if car.orientation == 'H':
                if self.moveLeft(car):
                    newState = State(self.moveLeft(
                        car), self.g_n+1, self, self.heuristic)
                    moves.append(newState)
                if self.moveRight(car):
                    newState = State(self.moveRight(
                        car), self.g_n+1, self, self.heuristic)
                    moves.append(newState)
            else:
                if self.moveUp(car):
                    newState = State(self.moveUp(
                        car), self.g_n+1, self, self.heuristic)
                    moves.append(newState)
                if self.moveDown(car):
                    newState = State(self.moveDown(
                        car), self.g_n+1, self, self.heuristic)
                    moves.append(newState)

        return moves

    # checkLeft: check if left side is blocked
    def isLeftBlocked(self, car):
        if car.position[0] == 0 or (self.board[car.head[0]][car.position[0]-1] != '-' and self.board[car.head[0]][car.position[0]-1] != car.label):
            return True
        else:
            return False

    # checkRight: check if the right side is blocked
    def isRightBlocked(self, car):
        if car.position[1] == (len(self.board) -1) or self.board[car.head[0]][car.position[1]+1] != '-' and self.board[car.head[0]][car.position[1]+1] != car.label:
            return True
        else:
            return False

    # checkTop: check if the top is block
    def isTopBlocked(self, car):
        if car.position[0] == 0 or self.board[car.head[0]-1][car.head[1]] != '-' and self.board[car.head[0]-1][car.head[1]] != car.label:
            return True
        else:
            return False

    # checkBottom: check if the bottom is blocked
    def isBottomBlocked(self, car):
        if car.position[1] == (len(self.board) -1) or self.board[car.position[1]+1][car.head[1]] != '-' and self.board[car.position[1]+1][car.head[1]] != car.label:
            return True
        else:
            return False

    # move the vehicle to the left
    def moveLeft(self, car):
        nextBoard = self.board[:]
        length = car.position[1] - car.position[0] + 1
        if not self.isLeftBlocked(car):
            nextBoard[car.head[0]] = nextBoard[car.head[0]][0: car.position[0]-1] + \
                car.label*length + '-' + \
                nextBoard[car.head[0]][car.position[1] + 1:]
            return nextBoard
        else:
            return []

    # move the vehicle to the right
    def moveRight(self, car):
        nextBoard = self.board[:]
        length = car.position[1] - car.position[0] + 1
        if not self.isRightBlocked(car):
            nextBoard[car.head[0]] = nextBoard[car.head[0]][0: car.position[0]] + \
                '-' + car.label*length + \
                nextBoard[car.head[0]][car.position[1]+2:]
            return nextBoard
        else:
            return []

    # move the vehicle up
    def moveUp(self, car):
        nextBoard = self.board[:]
        if not self.isTopBlocked(car):
            for i in range(car.position[0], car.position[1]+1):
                nextBoard[i-1] = nextBoard[i-1][0:car.head[1]] + \
                    car.label + nextBoard[i-1][car.head[1]+1:]
            nextBoard[car.position[1]] = nextBoard[car.position[1]][0:car.head[1]] + \
                '-' + nextBoard[car.position[1]][car.head[1]+1:]
            return nextBoard
        else:
            return []

    # move the vehicle down
    def moveDown(self, car):
        nextBoard = self.board[:]
        if not self.isBottomBlocked(car):
            for i in range(car.position[0], car.position[1]+1):
                nextBoard[i+1] = nextBoard[i+1][0:car.head[1]] + \
                    car.label + nextBoard[i+1][car.head[1]+1:]
            nextBoard[car.position[0]] = nextBoard[car.position[0]][0:car.head[1]] + \
                '-' + nextBoard[car.position[0]][car.head[1]+1:]
            return nextBoard
        else:
            return []
    
    # print the current board
    def printBoard(self):
        for row in self.board:
            print(row)


# car object
class Car:
    def __init__(self, label, head, orientation, position):
        self.label = label
        self.head = head
        self.orientation = orientation
        self.position = position

startBoard = ["OOO--P",
 "-----P",
 "--AXXP",
 "--ABCC",
 "D-EBFF",
 "D-EQQQ"]

# print("----- Blocking heuristic -----")
rushHour(0, startBoard)
# print("----- Custom heuristic -----")
rushHour(1, startBoard)
