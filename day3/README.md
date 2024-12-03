# Summary
## Task description
### 1. part
The task was to select the valid `mul(<uint>,<uint>)` commands from the input file, perform the multiplication of the two operands and sum up the results.

## Solution outline
### 1. part
The state-machine based approach would have suited this task better, however I didn't want to use the same principle twice.

Since I am getting more into linux, I have decided to use the command line utilities of bash as much as I can, and only write a simple C code for the and of the processing.

This resulted in the following command, that solves the task (my C code compled as `mul_add`:
```bash
at input | sed -e 's/mul/\nmul/g' -e 's/)/)\n/g' | grep 'mul([0-9][0-9]*,[0-9][0-9]*)' | ./mul_add
```
