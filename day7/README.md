# Summary
## Task description
### 1. part

The result of some operations are given in the lines of the input file, with the following format:
`<result>: <operand1> <operand2>[...]`

The task is to find what operation could be between the operands, and sum up the result of the ones that can be reproduced with given operations.
The set of possible operations:
- `+`: addition
- `*`: multiplication

Furthermore, the execution is always left-to-right, not according to precedence

### 2. part

Concatenation is also added to the possible operands:
- e.g. `1234: 12||34` is a possibility

## Solution outline

### 1. part

Assumption (after checking input): all numbers are positive integers

Idea: implement a recursive search, checking if the result is correct. Preform this from back-to-front, updating the result with the invers operation and reducing the number of operands.

Enhancements:
- check if operation is possible (e.g.: division results in integer)
- check if 0 or negative number is reached: failed attempt, because such a number cannot be reproduced with positive integers

**__ACED__**

### 2. part

Add implementation of concatenation to previous framework. All assumptions still hold.

**__ACED__**
