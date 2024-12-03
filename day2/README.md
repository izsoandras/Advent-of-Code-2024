# Summary
## Task Description
### 1. part
The number of lines had to be calculated, that satisfy the following two constraints:
- The series are strictly monotone (either increasing or decreasing)
- The absolute difference between consecutive elements are maximum 3

### 2. part
Thoose lines had to be included in the calculation, where removing one element from the series results in the fulfillment of the criteria.

## Solution outline
### 1. part
A state machine based approach had been used, where two state machines process the input:
1. The first state machine is responsible for finding the numbers in the line
2. The second state machine performs the checks

This way, with minimal processing power and memory, the defects can be found, with reading the input only character by character.

### 2. part
Unfortunately the architecture of the first task does not support well this modified scenario.
