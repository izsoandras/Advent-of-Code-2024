import numpy as np
import scipy.signal
import matplotlib.pyplot as plt


def charStringToIntArray(charString: str):
    lineAsNums = [ord(c) for c in charString]
    return np.array(lineAsNums, dtype='uint32')
    

def strListToIntMatrix(strList: list):
    listOfIntLists = [charStringToIntArray(string) for string in strList]
    return np.vstack(listOfIntLists)


def normalizerMtx(mtxIn: np.ndarray, kernelIn: np.ndarray):
    kernel = kernelIn.astype('double')
    mtx = mtxIn.astype('double')
    
    # calculate square of every matrix element
    mtx = mtx * mtx;
    
    # create lower diagonal band matrix, with 1s in main+kernelShape[1] diag
    # result: multiplying from right with this results in adding elements in a row,
    #         who are covered by the kernel at the same moment 
    rightToepCol = np.zeros(mtx.shape[1])
    rightToepCol[0:kernel.shape[1]] = 1
    rightToepRow = np.zeros_like(rightToepCol) # taking advantage of that out[0,0] = col[00] in all cases (row[0] is ignored)
    rightToepMtx = scipy.linalg.toeplitz(rightToepCol, rightToepRow)
    
    # create upper diagonal band matrix, with 1s in main+kernelShape[1] diag
    # result: multiplying from right with this results in adding elements in a column,
    #         who are overlayed by the kernel at the same moment     
    leftToepRow = np.zeros(mtx.shape[0])
    leftToepRow[0:kernel.shape[0]] = 1
    leftToepCol = np.zeros_like(leftToepRow)
    leftToepCol[0] = 1
    leftToepMtx = scipy.linalg.toeplitz(leftToepCol, leftToepRow)
    
    normMtx = np.sqrt(leftToepMtx @ mtx @ rightToepMtx) * np.sqrt(np.sum(kernel * kernel))
    # return only the valid part
    return normMtx[ 0:mtx.shape[0] - kernel.shape[0] + 1,
                    0:mtx.shape[1] - kernel.shape[1] + 1
        ]
    
    
def skew(mtx: np.ndarray, kernelLength: int, direct = 'pos', axis=None):
    if direct =='pos':
        shiftPerRow = 1
    elif direct == 'neg':
        shiftPerRow = -1
    else:
        raise ValueError
        
    ret = mtx.copy()
    myRoll = lambda m : np.roll(m, shiftPerRow, axis=axis) 
    permMtx = np.eye(mtx.shape[1])  
    if direct == 'pos':
        permMtx = np.fliplr(permMtx)
        permMtx = np.roll(permMtx, 3, axis=axis)
    
    if axis == 1:
        for i in range(0, kernelLength):
            ret[i:kernelLength:,:] = ret[i:kernelLength:,:] @ permMtx
            permMtx = myRoll(permMtx)
    elif axis == 0:
        for i in range(0, kernelLength):
            ret[:,i::kernelLength] = permMtx @ ret[:,i::kernelLength]
            permMtx = np.roll(permMtx, -1, axis=axis)
    else:
        raise NotImplementedError
        
    if axis == 1:
        return ret[:, 0:-kernelLength+1]
    elif axis == 0:
        return ret[0:-kernelLength+1, :]
    

if __name__ == "__main__":

    pattern = charStringToIntArray("XMAS")
    pattern = np.expand_dims(pattern, 0)
    
    patterns = [
        pattern,
        np.fliplr(pattern)
    ]     

    inMat = []
    with open("input",'r') as file:
        for line in file:
            lineAsNums = charStringToIntArray(line[:-1])
            inMat.append(lineAsNums)
            
    inMat = np.array(inMat)
    print(skew(np.eye(6), 3, 'neg', 0))
    print(skew(np.array([[0,0,1,0,0,0],
                         [0,1,0,0,0,0],
                         [1,0,0,0,0,0],
                         [0,0,0,0,0,1],
                         [0,0,0,0,1,0],
                         [0,0,0,1,0,0]
                        ]), 3, 'pos', 0))

    matVariants = [inMat, inMat.T, skew(inMat, pattern.shape[1], 'neg', 0), skew(inMat, pattern.shape[1], 'pos', 0)]
    
    matchNum = 0
    for p in patterns:
        for m in matVariants:
            c = scipy.signal.correlate2d(m, p, mode='valid')
            n = normalizerMtx(m, p)
            c_norm = c/n
            matchNum += np.sum(c_norm == c_norm.max())
    
    print(matchNum)
    #plt.subplot(1,2,1)
    #plt.imshow(inMat, cmap="Greys")
    #plt.subplot(1,2,2)
    # plt.imshow(c_norm, cmap="Greys")
    # plt.show()
