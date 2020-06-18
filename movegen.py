import copy


def oskaplayer(startBoard, side, moveAhead):
    pass


# move generator: this function generate all possible move
# input: current board and an indicator ('w' or 'b') determine whose turn is next
# output: list of next possible moves or current board if no move can be made
def movegen(board, nextTurn):
    n = len(board[0])
    # print(n)
    locations = findAllLocations(board, nextTurn)
    # print(locations)
    allMoves = []
    # check if nextTurn == 'w' -> move down
    # check if nextTurn == 'b' -> move up
    if nextTurn == 'w':
        for loc in locations:
            allMoves.extend(moveW(board, n, loc, nextTurn))
    else:
        for loc in locations:
            allMoves.extend(moveB(board, n, loc, nextTurn))
    return allMoves

# ---------------------- move the black piece up the board ----------------------

# ********************************** moveB **********************************
# move the black piece throughout the board
# input: board, loc(location of the current piece on the board), label('b')
# output: list of all possible moves black piece can make
# ***************************************************************************


def moveB(board, n, loc, label):
    midIndex = n - 2
    moves = []
    tempBoard = copy.deepcopy(board)
    rowIndex = loc[0]
    currentIndex = loc[1]
    # if current row == 0: can't move anymore
    if rowIndex == 0:
        return []
    elif rowIndex > midIndex:  # bottom half
        moves.extend(moveUpBottomHalf(
            tempBoard, currentIndex, rowIndex, label))

    else:  # if current row index >= midIndex
        moves.extend(moveUpTopHalf(tempBoard, currentIndex, rowIndex, label))
    # print(moves)
    return moves


# ********************************** moveUpTopHalf **********************************
# move the black piece up on the top half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible moves black piece can make on the top half of the board
# ***********************************************************************************
def moveUpTopHalf(board, currentIndex, rowIndex, label):
    moves = []
    tempBoard = copy.deepcopy(board)
    tempBoard = moveUpLeftTop(tempBoard, currentIndex, rowIndex, label)
    if tempBoard:
        resetChar(tempBoard, rowIndex, currentIndex)
        moves.append(tempBoard)

    tempBoard = copy.deepcopy(board)

    tempBoard = moveUpRightTop(tempBoard, currentIndex, rowIndex, label)
    if tempBoard:
        resetChar(tempBoard, rowIndex, currentIndex)
        moves.append(tempBoard)
    return moves

# ********************************** moveBottomTopHalf **********************************
# move the black piece up on the bottom half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible moves black piece can make on the bottom half of the board
# ***************************************************************************************


def moveUpBottomHalf(board, currentIndex, rowIndex, label):
    moves = []
    tempBoard = copy.deepcopy(board)
    # if currentIndex is the first index: only move diagonally right
    if(currentIndex == 0):
        tempBoard = moveUpRightBottom(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
    # if currentIndex is the last index: only move diagonally left
    elif(currentIndex == len(tempBoard[rowIndex]) - 1):
        tempBoard = moveUpLeftBottom(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
    else:
        # if currentIndex is in the middle: move to 2 different spots: diagonal left and right
        # move left
        tempBoard = moveUpLeftBottom(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
        tempBoard = copy.deepcopy(board)

        # move right
        tempBoard = moveUpRightBottom(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
    return moves


# ********************************** moveUpLeftBottom **********************************
# move up diagonally left on the bottom half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible left moves black piece can make on the bottom half of the board
# ***************************************************************************************
def moveUpLeftBottom(board, currentIndex, rowIndex, label):
    # check if replacing position is block
    if board[rowIndex-1][currentIndex-1] == '-':
        # => move left
        board[rowIndex -
              1] = updateRow(board[rowIndex-1], currentIndex-1, label)
    elif isBlockByOponent(board, currentIndex-1, rowIndex-1, label):
        # print("Next move is block by oponent")
        if rowIndex - 2 >= 0:
            return jumpB(board, (rowIndex, currentIndex), (rowIndex-1, currentIndex-1), label)
        else:
            return []
    else:
        return []
    return board

# ********************************** moveUpRightBottom **********************************
# move up diagonally right on the bottom half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible right moves black piece can make on the bottom half of the board
# ***************************************************************************************


def moveUpRightBottom(board, currentIndex, rowIndex, label):
    if board[rowIndex-1][currentIndex] == '-':
        # => move right
        board[rowIndex - 1] = updateRow(board[rowIndex-1], currentIndex, label)
    elif isBlockByOponent(board, currentIndex, rowIndex-1, label):
        # print("Next move is block by oponent")
        if rowIndex - 2 >= 0:
            return jumpB(board, (rowIndex, currentIndex), (rowIndex-1, currentIndex), label)
        else:
            return []
    else:
        return []
    return board


# ************************************ moveUpLeftTop ************************************
# move up diagonally left on the top half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible left moves black piece can make on the top half of the board
# ***************************************************************************************
def moveUpLeftTop(board, currentIndex, rowIndex, label):
    if board[rowIndex-1][currentIndex] == '-':
        # move left
        board[rowIndex - 1] = updateRow(board[rowIndex-1], currentIndex, label)
    elif isBlockByOponent(board, currentIndex, rowIndex-1, label):
        # print("Next move is block by oponent")
        if rowIndex - 2 >= 0:
            return jumpB(board, (rowIndex, currentIndex), (rowIndex-1, currentIndex), label)
        else:
            return []
    else:
        return []
    return board


# *********************************** moveUpRightTop ***********************************
# move up diagonally right on the top half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible right moves black piece can make on the top half of the board
# ***************************************************************************************
def moveUpRightTop(board, currentIndex, rowIndex, label):
    if board[rowIndex-1][currentIndex+1] == '-':
        # move right
        board[rowIndex-1] = updateRow(board[rowIndex-1], currentIndex+1, label)
    elif isBlockByOponent(board, currentIndex+1, rowIndex-1, label):
        # print("Next move is block by oponent")
        if rowIndex - 2 >= 0:
            return jumpB(board, (rowIndex, currentIndex), (rowIndex-1, currentIndex+1), label)
        else:
            return []
    else:
        return []
    return board


# **************************************** jumpB ***************************************
# jump the black piece up
# input: board, currentLocation = (rowIndex, currentIndex),
#               blockingLocation = (blockingRowIndex, blockingIndex), label
# output: all possible jump black piece can make
# **************************************************************************************
def jumpB(board, currentLocation, blockingLocation, label):
    n = len(board[0])
    midIndex = n - 2
    currentIndex = currentLocation[1]
    rowIndex = currentLocation[0]
    blockingIndex = blockingLocation[1]

    # if rowIndex > mid
    if rowIndex > midIndex:  # bottom half
        if blockingIndex >= currentIndex:
            return jumpUpRight(board, currentLocation, blockingLocation, label)
        else:
            return jumpUpLeft(board, currentLocation, blockingLocation, label)
    else:  # if rowIndex <= mid => top half
        if blockingIndex > currentIndex:
            return jumpUpRight(board, currentLocation, blockingLocation, label)
        else:
            return jumpUpLeft(board, currentLocation, blockingLocation, label)


# ************************************* jumpUpRight ************************************
# jump the black piece up diagonally right
# input: board, currentLocation = (rowIndex, currentIndex),
#               blockingLocation = (blockingRowIndex, blockingIndex), label
# output: all possible right jump black piece can make
# **************************************************************************************
def jumpUpRight(board, currentLocation, blockingLocation, label):
    n = len(board[0])
    midIndex = n-2
    currentIndex = currentLocation[1]
    rowIndex = currentLocation[0]
    blockingIndex = blockingLocation[1]
    blockingRowIndex = blockingLocation[0]
    if blockingRowIndex > midIndex:  # if blockingRowIndex is in bottom half
        if blockingIndex < len(board[blockingRowIndex-1]) and board[blockingRowIndex-1][blockingIndex] == '-':
            board[blockingRowIndex -
                  1] = updateRow(board[blockingRowIndex-1], blockingIndex, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []
    else:  # if blockingRowIndex is in the top half
        if blockingIndex+1 < len(board[blockingRowIndex-1]) and board[blockingRowIndex-1][blockingIndex+1] == '-':
            board[blockingRowIndex -
                  1] = updateRow(board[blockingRowIndex-1], blockingIndex+1, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []


# ************************************* jumpUpLeft ************************************
# jump the black piece up diagonally left
# input: board, currentLocation = (rowIndex, currentIndex),
#               blockingLocation = (blockingRowIndex, blockingIndex), label
# output: all possible left jump black piece can make
# *************************************************************************************
def jumpUpLeft(board, currentLocation, blockingLocation, label):
    n = len(board[0])
    midIndex = n-2
    currentIndex = currentLocation[1]
    rowIndex = currentLocation[0]
    blockingIndex = blockingLocation[1]
    blockingRowIndex = blockingLocation[0]

    if blockingRowIndex > midIndex:  # if blockingRowIndex is in bottom half
        if blockingIndex-1 >= 0 and board[blockingRowIndex-1][blockingIndex-1] == '-':
            # move left
            board[blockingRowIndex -
                  1] = updateRow(board[blockingRowIndex-1], blockingIndex-1, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []
    else:  # if blockingRowIndex is in top half
        if blockingIndex >= 0 and board[blockingRowIndex-1][blockingIndex] == '-':
            board[blockingRowIndex -
                  1] = updateRow(board[blockingRowIndex-1], blockingIndex, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []


# ---------------------- move the white piece down the board ----------------------

# ********************************** moveW **********************************
# move the white piece throughout the board
# input: board, loc(location of the current piece on the board), label('w')
# output: list of all possible moves white piece can make
# ***************************************************************************
def moveW(board, n, loc, label):
    midIndex = n - 2
    moves = []
    tempBoard = copy.deepcopy(board)
    rowIndex = loc[0]
    currentIndex = loc[1]
    # if current row == 0: can't move anymore
    if rowIndex == len(board) - 1:
        return []
    elif rowIndex >= midIndex:  # bottom half
        moves.extend(moveDownBottomHalf(
            tempBoard, currentIndex, rowIndex, label))

    else:  # if current row index >= midIndex
        moves.extend(moveDownTopHalf(tempBoard, currentIndex, rowIndex, label))
    # print(moves)

    return moves

# ********************************** moveDownTopHalf ********************************
# move the white piece up on the top half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible moves white piece can make on the top half of the board
# ***********************************************************************************


def moveDownTopHalf(board, currentIndex, rowIndex, label):
    moves = []
    tempBoard = copy.deepcopy(board)
    # if currentIndex is the first index: only move diagonally right
    if(currentIndex == 0):
        tempBoard = moveDownRightTop(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
    # if currentIndex is the last index: only move diagonally left
    elif(currentIndex == len(tempBoard[rowIndex]) - 1):
        tempBoard = moveDownLeftTop(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
    else:
        # if currentIndex is in the middle: move to 2 different spots: diagonal left and right
        # move left
        tempBoard = moveDownLeftTop(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
        tempBoard = copy.deepcopy(board)

        # move right
        tempBoard = moveDownRightTop(tempBoard, currentIndex, rowIndex, label)
        if tempBoard:
            resetChar(tempBoard, rowIndex, currentIndex)
            moves.append(tempBoard)
    return moves

# ********************************** moveDownBottomHalf ********************************
# move the white piece up on the bottom half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible moves white piece can make on the bottom half of the board
# ***********************************************************************************


def moveDownBottomHalf(board, currentIndex, rowIndex, label):
    moves = []
    tempBoard = copy.deepcopy(board)
    # move left
    tempBoard = moveDownLeftBottom(tempBoard, currentIndex, rowIndex, label)
    if tempBoard:
        resetChar(tempBoard, rowIndex, currentIndex)
        moves.append(tempBoard)

    # move right
    tempBoard = copy.deepcopy(board)
    tempBoard = moveDownRightBottom(tempBoard, currentIndex, rowIndex, label)
    if tempBoard:
        resetChar(tempBoard, rowIndex, currentIndex)
        moves.append(tempBoard)
    return moves


# ********************************** moveDownLeftBottom **********************************
# move down diagonally left on the bottom half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible left moves white piece can make on the bottom half of the board
# ***************************************************************************************
def moveDownLeftBottom(board, currentIndex, rowIndex, label):
    # check if replacing position is block
    if board[rowIndex+1][currentIndex] == '-':
        # => move left
        board[rowIndex + 1] = updateRow(board[rowIndex+1], currentIndex, label)
    elif isBlockByOponent(board, currentIndex, rowIndex+1, label):
        # print("Next move is block by oponent")
        if rowIndex + 2 < len(board):
            return jumpW(board, (rowIndex, currentIndex), (rowIndex+1, currentIndex), label)
        else:
            return []
    else:
        return []
    return board


# ********************************** moveDownRightBottom **********************************
# move down diagonally right on the bottom half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible right moves white piece can make on the bottom half of the board
# ***************************************************************************************
def moveDownRightBottom(board, currentIndex, rowIndex, label):
    # check if replacing position is block
    if board[rowIndex+1][currentIndex+1] == '-':
        # => move left
        board[rowIndex +
              1] = updateRow(board[rowIndex+1], currentIndex+1, label)
    elif isBlockByOponent(board, currentIndex+1, rowIndex+1, label):
        # print("Next move is block by oponent")
        if rowIndex + 2 < len(board):
            return jumpW(board, (rowIndex, currentIndex), (rowIndex+1, currentIndex+1), label)
        else:
            return []
    else:
        return []
    return board


# *********************************** moveDownLeftTop ***********************************
# move down diagonally left on the top half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible left moves white piece can make on the top half of the board
# ***************************************************************************************
def moveDownLeftTop(board, currentIndex, rowIndex, label):
    # check if replacing position is block
    if board[rowIndex+1][currentIndex-1] == '-':
        # => move left
        board[rowIndex +
              1] = updateRow(board[rowIndex+1], currentIndex-1, label)
    elif isBlockByOponent(board, currentIndex-1, rowIndex+1, label):
        # print("Next move is block by oponent")
        if rowIndex + 2 < len(board):
            return jumpW(board, (rowIndex, currentIndex), (rowIndex+1, currentIndex-1), label)
        else:
            return []
    else:
        return []
    return board


# *********************************** moveDownRightTop ***********************************
# move down diagonally right on the top half of the board
# input: board, currentIndex (current index of the piece on the row),
#        rowIndex(index of the row on the entire board), label
# output: all possible right moves white piece can make on the top half of the board
# ***************************************************************************************
def moveDownRightTop(board, currentIndex, rowIndex, label):
    # check if replacing position is block
    if board[rowIndex+1][currentIndex] == '-':
        # => move left
        board[rowIndex + 1] = updateRow(board[rowIndex+1], currentIndex, label)
    elif isBlockByOponent(board, currentIndex, rowIndex+1, label):
        # print("Next move is block by oponent")
        if rowIndex + 2 < len(board):
            return jumpW(board, (rowIndex, currentIndex), (rowIndex+1, currentIndex), label)
        else:
            return []
    else:
        return []
    return board

# **************************************** jumpW ***************************************
# jump the white piece down
# input: board, currentLocation = (rowIndex, currentIndex),
#               blockingLocation = (blockingRowIndex, blockingIndex), label
# output: all possible jump white piece can make
# **************************************************************************************


def jumpW(board, currentLocation, blockingLocation, label):
    n = len(board[0])
    midIndex = n - 2
    currentIndex = currentLocation[1]
    rowIndex = currentLocation[0]
    blockingIndex = blockingLocation[1]

    # if rowIndex >= mid
    if rowIndex >= midIndex:  # bottom half
        if blockingIndex > currentIndex:
            return jumpDownRight(board, currentLocation, blockingLocation, label)
        else:
            return jumpDownLeft(board, currentLocation, blockingLocation, label)
    else:  # if rowIndex < mid => top half
        if blockingIndex >= currentIndex:
            return jumpDownRight(board, currentLocation, blockingLocation, label)
        else:
            return jumpDownLeft(board, currentLocation, blockingLocation, label)

# ************************************* jumpDownRight ************************************
# jump the white piece down diagonally right
# input: board, currentLocation = (rowIndex, currentIndex),
#               blockingLocation = (blockingRowIndex, blockingIndex), label
# output: all possible right jump white piece can make
# *************************************************************************************


def jumpDownRight(board, currentLocation, blockingLocation, label):
    n = len(board[0])
    midIndex = n-2
    currentIndex = currentLocation[1]
    rowIndex = currentLocation[0]
    blockingIndex = blockingLocation[1]
    blockingRowIndex = blockingLocation[0]
    if blockingRowIndex >= midIndex:  # if blockingRowIndex is in bottom half
        if blockingIndex+1 < len(board[blockingRowIndex+1]) and board[blockingRowIndex+1][blockingIndex+1] == '-':
            board[blockingRowIndex +
                  1] = updateRow(board[blockingRowIndex+1], blockingIndex+1, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []
    else:  # if blockingRowIndex is in the top half
        if blockingIndex < len(board[blockingRowIndex+1]) and board[blockingRowIndex+1][blockingIndex] == '-':
            board[blockingRowIndex +
                  1] = updateRow(board[blockingRowIndex+1], blockingIndex, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []


# ************************************* jumpDownLeft **********************************
# jump the white piece down diagonally left
# input: board, currentLocation = (rowIndex, currentIndex),
#               blockingLocation = (blockingRowIndex, blockingIndex), label
# output: all possible left jump white piece can make
# *************************************************************************************
def jumpDownLeft(board, currentLocation, blockingLocation, label):
    n = len(board[0])
    midIndex = n-2
    currentIndex = currentLocation[1]
    rowIndex = currentLocation[0]
    blockingIndex = blockingLocation[1]
    blockingRowIndex = blockingLocation[0]
    if blockingRowIndex >= midIndex:  # if blockingRowIndex is in bottom half
        if blockingIndex >= 0 and board[blockingRowIndex+1][blockingIndex] == '-':
            # move left
            board[blockingRowIndex +
                  1] = updateRow(board[blockingRowIndex+1], blockingIndex, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []
    else:  # if blockingRowIndex is in top half
        if blockingIndex-1 >= 0 and board[blockingRowIndex+1][blockingIndex-1] == '-':
            board[blockingRowIndex +
                  1] = updateRow(board[blockingRowIndex+1], blockingIndex-1, label)
            if board:
                resetChar(board, blockingRowIndex, blockingIndex)
                return board
        else:
            return []


# ********************** helper functions **********************

# reset the current character to '-'
def resetChar(board, rowIndex, currentIndex):
    board[rowIndex] = updateRow(board[rowIndex], currentIndex, '-')
    return


# update the current row by inserting the lable in the spliting position
# input: current board, spliting position, label (can be 'w', 'b' or '-')
# output: new board with updating state
def updateRow(board, splitingPos, label):
    board = board[0:splitingPos] + label + board[splitingPos+1:]
    return board


# find locations of all 'w' or 'b' in the board
# input: board, label represents whose turn
# output: list of tuples (a,b) where a is a row index and b is index of 'w' or 'b' in row a
def findAllLocations(board, label):
    locations = []  # list of all locations of 'w' or 'b' in the board
    # each element is a tuple represent row index and current location in the row
    # find location of all 'w' or 'b' on the board
    for rowIndex, row in enumerate(board):
        # print(rowIndex, row)
        if isLabelIn(board, label, row):
            # find all location on a current row
            for loc in findLocation(board, label, row, rowIndex):
                # update list of all locations
                locations.append((rowIndex, loc))
    return locations


# find current location of 'w' or 'b' in the current row
# return a list of location of 'w' or 'b' on the current row
def findLocation(boad, label, row, rowIndex):
    return [i for i, char in enumerate(row) if char == label]


# check if there is a label in a current row
def isLabelIn(board, label, row):
    return label in row

# check if the position is blocked by itself


def isBlockByItself(board, currentIndex, rowIndex, label):
    return board[rowIndex][currentIndex] == label
# check if the position is block by the oponent


def isBlockByOponent(board, currentIndex, rowIndex, label):
    return board[rowIndex][currentIndex] != label and board[rowIndex][currentIndex] != '-'


startBoard = ['----w','---w','--b','w-','-b-','---b','----b']
print(movegen(startBoard, 'w'))
