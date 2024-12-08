import numpy as np
import sys

# Recursive search for possible operators. The order is arbitrary,
# could possibly squeeze out some performance if order of checking
# would be rethought
def checkPossible(result: int, operands: list, concatEnabled: bool):
    # End conditions of recursion
    if result <= 0:
        # If we reached a non-positive number, the attempt is a fail, 
        # because such a number cannot be reproduced by + and * (nor concat) over positive integers 
        return False

    if len(operands) == 1:
        if result == operands[0]:
            # If the result matches, when we run out of operands, a solution is found
            return True
        else:
            # If we run out of operands and the result is wrong, it is a failed combination
            return False
        
    # Evaluation of possible next operations
    lastOperand = operands[-1]
    # Concatenation
    if concatEnabled:
        lastOperandStr = str(lastOperand)
        lenLastOperand = len(lastOperandStr)
        resultStr = str(result)
        
        if len(resultStr) > lenLastOperand and resultStr[-lenLastOperand:] == lastOperandStr:
            # Check if concatenation can be applied
            if checkPossible(int(resultStr[0:-lenLastOperand]), operands[:-1], concatEnabled):
                # There are more chances, only return if successful
                return True
    
    # Multiplication
    if result % lastOperand == 0:
        # operands are all positive integers => subtraction only has to be evaluated
        # if the new result is 
        if checkPossible(result // lastOperand, operands[:-1], concatEnabled):
            # There are more chances, only return if successful
            return True
      
    # Addition is the last chance -> result can be directly returned 
    return checkPossible(result - lastOperand, operands[:-1], concatEnabled)
 
 
# Main function to avoid global namespace collision
def main(argv: list):
    # Handle input arguments
    inputName = argv[1] if len(argv) > 1 else "input"
    taskNo = int(argv[2]) if len(argv) > 2 else 1
    sum = 0

    # Iterate over input
    with open(inputName) as inputFile:
        for line in inputFile:
            # The result and operands are divided by a :
            resOpPart = line.split(':')
            result = int(resOpPart[0])
            # After the : there is always a space and there is a \n at the end
            operands = [int(opStr) for opStr in resOpPart[1].strip().split(' ')]
            
            if checkPossible(result, operands, taskNo == 2):
                sum += result
    
    # Present result
    print(f"The sum is: {sum}")
    
# Guard for import (as if this would be imported anywhere...)
if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv)
