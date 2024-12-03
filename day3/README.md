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
cat input | sed -e 's/mul/\nmul/g' -e 's/)/)\n/g' | grep 'mul([0-9][0-9]*,[0-9][0-9]*)' | ./mul_add
```
The processing steps are:
1. place new line before every `mul` instance and after every `)`
2. select lines, which are correct operations
3. feed result into the C program

### 2. part
With the previous command saved into `solve.bash`, the new task can be easily solved by the following command:
```bash
cat input | tr -d '\n' | sed -e 's/do()/\ndo()/g' -e "s/don't()/\ndon't()/g" | sed -e "/^don't/d" | ./solve.bash
```
Where the prerocess steps are:
1. delete newlines, because we are going to do our own separation
2. separate at each `do()` and `don't()` instruction (full name is used to ensure, that only valid ones are matched)
3. delete lines starting with `don't` (actully only `don` would do it, we don't need the full instruction, because we performed the line breakings)
4. result can bee piped into the previous command
