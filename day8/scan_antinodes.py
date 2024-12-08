import argparse
import numpy as np


# Mark the location in the given boolean matrix with True value (if location is valid)
# return if mark was successfully placed
def markLoc(row: int, col: int, mat: np.ndarray): 
    couldMark =  row >= 0 and row < mat.shape[0] and  \
                 col >= 0 and col < mat.shape[1]
    
    if couldMark:
        mat[row, col] = True
        
    return couldMark


# Function to separate namespaces
# Parse arguments, read input, iterate over input
def main():
    # Handle input arguments
    cmdParser = argparse.ArgumentParser(description="Calculate number of antinodes (AoC2024/8)")
    cmdParser.add_argument("input", nargs='?', default="input")
    args = cmdParser.parse_args()
    
    # Read whole file, since it is necessary to determine map size
    mapMat = []
    with open(args.input) as inputFile:
        for line in inputFile:
            # Last char is known to be a new line
            mapMat.append(list(line[:-1]))    
    
    mapMat = np.array(mapMat)
    # Instead of building a set, create LuT, because input is small
    antinodeLoc1 = np.zeros_like(mapMat, dtype='bool')
    antinodeLoc2 = np.zeros_like(mapMat, dtype='bool')
    
    # Prepare helper objects
    freqToLoc = dict()  # dictionary to assign locations to frequencies
    
    # Process character by character
    for rowIdx in range(mapMat.shape[0]):
        for colIdx in range(mapMat.shape[1]):
            char = mapMat[rowIdx, colIdx]
            
            # If empty place, move to next
            if char == '.':
                continue
                
            # Instead of checking first, and then accessing (thus iterating twice)
            # try to insert directly and handle error if occurs
            try:
                # Try to iterate through previous same frequencies
                for loc in freqToLoc[char]:
                    # Calculate the difference between the antennas
                    deltaRow = loc[0] - rowIdx
                    deltaCol = loc[1] - colIdx
                    
                    # Part 1
                    row1 = loc[0] + deltaRow
                    col1 = loc[1] + deltaCol
                    
                    row2 = rowIdx - deltaRow
                    col2 = colIdx - deltaCol
                    
                    markLoc(row1, col1, antinodeLoc1)
                    markLoc(row2, col2, antinodeLoc1)
                    
                    # Part 2
                    r = rowIdx
                    c = colIdx
                    while markLoc(r, c, antinodeLoc2):
                        r -= deltaRow
                        c -= deltaCol
                    
                    r = loc[0]
                    c = loc[1]
                    while markLoc(r, c, antinodeLoc2):
                        r += deltaRow
                        c += deltaCol
                    
                freqToLoc[char].append((rowIdx, colIdx))
                    
            except KeyError:
                # If this freq is not present yet, insert
                freqToLoc[char] = [(rowIdx, colIdx),]
                
    # Calculate numbers
    uniqueAntinodeNum1 = np.sum(antinodeLoc1)
    uniqueAntinodeNum2 = np.sum(antinodeLoc2)
    
    # Print results
    print(f"Number of unique antinode location according to part1: {uniqueAntinodeNum1}")
    print(f"Number of unique antinode location according to part2: {uniqueAntinodeNum2}")
            

if __name__ == "__main__":
    main()
