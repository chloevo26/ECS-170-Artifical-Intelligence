from State import State

# minimax function implementing the minimax algorith
# input: state, depth and whether the side is a maximum player
# output: tuple (a,b) where a is int represents maximum value, b is a state
def minimax(state, depth, isMaximixing):
    if depth == 0:
        return (boardEvaluator(state, depth), state)
    # if any side wins or tie: don't generate new moves
    elif isBlackWin(state) or isWhiteWin(state) or isTie(state):
        return (boardEvaluator(state, depth), state)
    if isMaximixing:
        maxEval = float('-inf')
        generateMoves = state.movegen(state.playerSide)
        if generateMoves == [] and state.movegen(findMinPlayer(state)) == []:
            return (maxEval, state)
        elif generateMoves == [] and depth != 1:
            return minimax(state, depth-1, False)
        elif generateMoves == [] and depth == 1:
            return (boardEvaluator(state, depth), state)
        else:
            for move in generateMoves:
                currEval = minimax(move, depth-1, False)
                if currEval[0] > maxEval:
                    maxEval = currEval[0]
                    bestMove = move
            return (maxEval, bestMove)
    else:
        minEval = float('inf')
        generateMoves = state.movegen(findMinPlayer(state))
        if generateMoves == [] and state.movegen(state.playerSide) == []:
            return (minEval, state)
        elif generateMoves == [] and depth != 1:
            return minimax(state, depth-1, True)
        elif generateMoves == [] and depth == 1:
            return (boardEvaluator(state, depth), state)
        else:
            for move in generateMoves:
                currEval = minimax(move, depth-1, True)
                if currEval[0] < minEval:
                    minEval = currEval[0]
                    bestMove = move
            return (minEval, bestMove)


# oskaplayer function
# input: board: the starting board
#        side: which side is the maximum player
#        depth: maximum depth of the search
# output: board that represent best move the maximum player should make
def oskaplayer(board, side, depth):
    startState = State(board, side, depth)
    bestValue = minimax(startState, depth, True)
    return bestValue[1].board


# check if the game is tie
# input: state
# output: bool. Return True when all remaining pawns of both sides are at the opposite side
#               and number of black and white pawns are equal
def isTie(state):
    numMaxPawns = len(findAllLocations(state.board, state.playerSide))
    # number of remaining minimum pawns
    numMinPawns = len(findAllLocations(state.board, findMinPlayer(state)))
    return allWhiteInLast(state) and allBlackInFirst(state) and numMaxPawns == numMinPawns


# find the minimum player
# input: state
# output: char determines which side is minimum player
def findMinPlayer(state):
    if state.playerSide == 'b':
        return 'w'
    else:
        return 'b'


# evaluation function: static board evaluation that apply heuristic to the current board and assign a score for the board
# input: state: current state
#        depth: curre1nt depth of the search
# output: int that represents a score for the current board input
def boardEvaluator(state, depth):
    score = 0
    # number of remaining maximum pawns
    numMaxPawns = len(findAllLocations(state.board, state.playerSide))
    # number of remaining minimum pawns
    numMinPawns = len(findAllLocations(state.board, findMinPlayer(state)))
    # if all remaining black and white pawns are on the other side
    if allWhiteInLast(state) and allBlackInFirst(state):
        if numMaxPawns > numMinPawns:  # number of max pawn > number of min pawns remaining on the board => we current player wins
            score = 10
        elif numMaxPawns < numMinPawns:  # current player lose
            score = -10
        else:
            score = numMaxPawns  # tie
    else:
        # if maximum player wins: score == 10
        if isMaxPlayerWin(state):
            score = 10
        # if minimum player wins: score == -10
        elif isMinPlayerWin(state):
            score = -10
        # if netheir black or white wins: calculate positions of all black pawns
        else:
            # if remaining max pawns < remaining min pawns
            if (numMaxPawns < numMinPawns):
                score += (numMinPawns - numMaxPawns) * \
                    (getMinDistance(state) - getMaxDistance(state))
            else:  # if remaining max pawns >= remaining min pawns
                score += getMinDistance(state) - getMaxDistance(state)
    return score


# get the distance from all current maximum pawns to the opposite side of the board
# input: state
# output: int
def getMaxDistance(state):
    if state.playerSide == 'w':
        return getWhiteDistance(state)
    else:
        return getBlackDistance(state)


# get the distance from all current minimum pawns to the opposite side of the board
# input: state
# output: int
def getMinDistance(state):
    if findMinPlayer(state) == 'w':
        return getWhiteDistance(state)
    else:
        return getBlackDistance(state)


# check if the maximum player wins
# input: state
# output: bool
def isMaxPlayerWin(state):
    if state.playerSide == 'w':  # if max player is white: check if white wins
        return isWhiteWin(state)
    else:  # if max player is black: check if black wins
        return isBlackWin(state)


# check if the minimum player wins
# input: state
# output: bool
def isMinPlayerWin(state):
    if findMinPlayer(state) == 'w':  # if min player is white: check if white wins
        return isWhiteWin(state)
    else:  # if min player is black: check if black wins
        return isBlackWin(state)


# get the total white pawns distance to the bottom of the board
# input: state
# output: int
def getWhiteDistance(state):
    distance = 0
    for position in findAllLocations(state.board, 'w'):
        distance += len(state.board) - position[0] - 1
    return distance

# get the total black pawns distance to the top of the board
# input: state
# output: int


def getBlackDistance(state):
    distance = 0
    for position in findAllLocations(state.board, 'b'):
        distance += position[0]
    return distance


# check if black wins
# input: state
# output: bool
def isBlackWin(state):
    numWhite = len(findAllLocations(state.board, 'w'))
    numBlack = len(findAllLocations(state.board, 'b'))
    # if all black pawns are in first row, black wins
    if allBlackInFirst(state):
        return True
    elif numWhite == 0 and numBlack != 0:  # if no white pawns left
        return True
    return False

# check if white wins
# input: state
# output: bool


def isWhiteWin(state):
    numWhite = len(findAllLocations(state.board, 'w'))
    numBlack = len(findAllLocations(state.board, 'b'))
    # if all white pawns are in last row, white wins
    if allWhiteInLast(state):
        return True
    elif numBlack == 0 and numWhite != 0:  # if no black pawns left
        return True
    return False


# check if all remaining white pawns are in the last row
# input: state
# output: bool
def allWhiteInLast(state):
    if findAllLocations(state.board, 'w'):
        for location in findAllLocations(state.board, 'w'):
            if location[0] != len(state.board)-1:
                return False
        return True
    else:
        return False

# check if all remaining black pawns are in the first row
# input: state
# output: bool


def allBlackInFirst(state):
    if findAllLocations(state.board, 'b'):
        for location in findAllLocations(state.board, 'b'):
            if location[0] != 0:
                return False
        return True
    else:
        return False


# find all the locations of the label in the board
# input: board, label('b' or 'w')
# output: list of locations,
#         where each location is a tuple (a,b) where a is the row index and b is index of the label in that row
def findAllLocations(board, label):
    locations = []  # list of all locations of 'w' or 'b' in the board
    # each element is a tuple represent row index and current location in the row
    # find location of all 'w' or 'b' on the board
    for rowIndex, row in enumerate(board):
        if isLabelIn(board, label, row):
            # find all location on a current row
            for loc in findLocation(board, label, row, rowIndex):
                # update list of all locations
                locations.append((rowIndex, loc))
    return locations

# check if the label is in the current row
# input: board, label, row
# output: bool


def isLabelIn(board, label, row):
    return label in row

# find locations of label in a row
# input: board, label, current row, and row index
# output: list of index of label in a row


def findLocation(boad, label, row, rowIndex):
    return [i for i, char in enumerate(row) if char == label]


print(oskaplayer(['-b--', 'w-b', 'wb', 'b--', '----'], 'b', 6))
