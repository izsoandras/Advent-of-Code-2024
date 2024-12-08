import numpy as np

# Check for the given pattern along the diagonals of mat
# mat and pattern must have appropriate dimensions
def checkPatternX(mat, pattern):
    patternFlipped = np.flip(pattern)
    patternFound = 0

    middleIdx = len(pattern)/2 + 1;
    
    diagA = mat[range(pattern.shape[0]), range(pattern.shape[0])]
    diagB = mat[range(pattern.shape[0]), range(pattern.shape[0]-1, -1, -1)]
    
    if (all(diagA == pattern) or all(diagA == patternFlipped)) and  \
       (all(diagB == pattern) or all(diagB == patternFlipped)):
       return True


if __name__ == "__main__":
    # Brute force Task 1
    p1 = np.array(list("XMAS")) # pattern to look for
    p2 = np.flip(p1)            # reverse pattern
    
    # Read the file into a np array for easier indexing
    inMat = []
    with open("input",'r') as file:
        for line in file:
            line = list((line[:-1]))
            inMat.append(line)
    inMat = np.array(inMat)

    # Initialize match counter
    count = 0
    
    # Look for matches horizonatally
    for rowIdx in range(inMat.shape[0]):
        for colIdx in range(inMat.shape[1] - (p1.shape[0]-1)):
            sect = inMat[rowIdx, colIdx:colIdx+p1.shape[0]]
            if all(sect == p1) or all(sect == p2):
                count += 1
                
    # Look for matches vertically
    for rowIdx in range(inMat.shape[0] - (p1.shape[0]-1)):
        for colIdx in range(inMat.shape[1]):
            sect = inMat[rowIdx:rowIdx+p1.shape[0], colIdx]
            if all(sect == p1) or all(sect == p2):
                count += 1
    
    # Look for matches along main diagonal
    for diagIdx in range(np.sum(inMat.shape)-1):
        diagStartRow = np.max([inMat.shape[0]-1 - diagIdx, 0])
        diagStartCol = np.max([diagIdx - (inMat.shape[0]-1), 0])
        diagLength = np.min([inMat.shape[0] - diagStartRow, inMat.shape[1] - diagStartCol])
        
        if diagLength < p1.shape[0]:
            continue
        
        diag = inMat[range(diagStartRow, diagStartRow + diagLength), range(diagStartCol, diagStartCol + diagLength)]
        for idxInDiag in range(diagLength - (p1.shape[0]-1)):
            sect = diag[idxInDiag : idxInDiag + p1.shape[0]]

            if all(sect == p1) or all(sect == p2):
                count += 1
        
    # Look for matches along other diagonal
    for diagIdx in range(np.sum(inMat.shape)-1):
        diagStartRow = np.max([diagIdx - (inMat.shape[1]-1), 0])
        diagStartCol = np.min([diagIdx, inMat.shape[1]-1])
        diagLength = np.min([inMat.shape[0] - diagStartRow, diagStartCol + 1])
        
        if diagLength < p1.shape[0]:
            continue
        
        diag = inMat[range(diagStartRow, diagStartRow + diagLength), range(diagStartCol, diagStartCol - diagLength,-1)]
        for idxInDiag in range(diagLength - (p1.shape[0]-1)):
            sect = diag[idxInDiag : idxInDiag + p1.shape[0]]
            if all(sect == p1) or all(sect == p2):
                count += 1

    # Print result
    print(f"XMAS: {count}")
    
    # Look for matches in an X
    p3 = np.array(list("MAS"))
    p3len = p3.shape[0]
    count = 0
    for rowIdx in range(inMat.shape[0] - (p3len-1)):
        for colIdx in range(inMat.shape[1] - (p3len-1)):
            if checkPatternX(inMat[rowIdx:rowIdx + p3len, colIdx:colIdx+p3len], p3):
                count += 1

    print(f"X-MAS: {count}")
