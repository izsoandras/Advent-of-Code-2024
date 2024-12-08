from enum import IntEnum
from enum import auto
import numpy as np

class Directions(IntEnum):
    Up = auto()
    Right = auto()
    Down = auto()
    Left = auto()
    Closure = auto()
    
    def getNext(self):
        newDir = self + 1
        if newDir >= Directions.Closure:
            newDir = 1
            
        return Directions(newDir)
        
    def getPrev(self):
        newDir = self - 1
        if newDir < Directions.Up:
            newDir = Direction.Left
        else:
            newDir = Directions(newDir)
            
        return newDir


def getNextLoc(loc: tuple, d: Directions):
    if d == Directions.Up:
        return tuple([loc[0] - 1 , loc[1]])
    elif d == Directions.Right:
        return tuple([loc[0]    , loc[1] + 1])
    elif d == Directions.Down:
        return tuple([loc[0] + 1, loc[1]])
    elif d == Directions.Left:
        return tuple([loc[0]    , loc[1] - 1])


def locToTuple(tupleOfArrIdx: tuple):
    return (int(tupleOfArrIdx[0][0]), int(tupleOfArrIdx[1][0]))


def getNextState(layout: np.ndarray, loc: tuple, d: Directions):
    nextLoc = getNextLoc(loc, d)
    nextDir = d
    if nextLoc[0] < 0 or nextLoc[0] >= layout.shape[0] or \
       nextLoc[1] < 0 or nextLoc[1] >= layout.shape[1]:
        return None, None
    elif layout[nextLoc] == '#':
        nextLoc = loc
        nextDir = d.getNext()
        
    return nextLoc, nextDir


def checkIfClosurePosbbile(layout: np.ndarray, loc: tuple, d: Directions, prevStates: set):
    theoryLoc = loc
    theoryDir = d.getNext()
    theoryState = theoryLoc + (theoryDir,)
    theoryStates = set()
    while not((theoryState in prevStates) or (theoryState in theoryStates)):
        theoryStates.add(theoryState)
        theoryLoc, theoryDir = getNextState(layout, theoryLoc, theoryDir)
        if theoryLoc is None:
            return False
        else:
            theoryState = theoryLoc + (theoryDir,)
    
    return True


def main():
    # Read the file into a np array for easier indexing
    inMat = []
    with open("input",'r') as file:
        for line in file:
            line = list((line[:-1]))
            inMat.append(line)
    inMat = np.array(inMat)
    
    # Define start state
    loc = np.nonzero(inMat == '^')
    loc = (int(loc[0][0]), int(loc[1][0]))
    direction = Directions.Up
    nextLoc = loc
    
    # Replace start indicator with '.'
    inMat[loc] = '.'
    
    # Define sets to keep track of traverse
    visitedLoc = {loc}
    visitedStates = set()
    loopCloseCount = 0
    closeLoc = set()
    
    # Run
    while(True):
        visitedStates.add(loc+(direction,))
        nextLoc, nextDir = getNextState(inMat, loc, direction)
        
        if nextLoc is None:
            break
            
        if loc != nextLoc:
            if nextLoc not in visitedLoc:
                inMat[nextLoc] = '#'
                if checkIfClosurePosbbile(inMat, loc, direction, visitedStates):
                    loopCloseCount += 1
                    closeLoc.add(loc)
                    
                inMat[nextLoc] = '.'
            
            visitedLoc.add(nextLoc)
            loc = nextLoc
            
        direction = nextDir
            
    print(f"Distinct positions visited: {len(visitedLoc)}")
    print(f"Possible number of obstructions: {loopCloseCount}")

if __name__ == "__main__":
    main()
        
