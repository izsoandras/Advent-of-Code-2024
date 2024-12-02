# Task description
## 1. part
The input file contains two, unsigned integers in each row, representing two columns.
The task was to order each of the two columns increasingly,
and calculate the sum of the absolute difference between the arising pairs.

## 2. part
Having the same input file, for each element in the left column:
1. count the number of appearance in the right column
2. multiply the count by the number itself
3. sum these up, this way creating a similarity score

# Solution outline
## 1. part
1. Read values into a linked list
  1. assuming that the input length is not given
  2. avoiding many memory reallocations)
2. Convert the linked list to regular C array
  1. Sorting with quicksort requires indexing into the middle of the array, which is not well-supported by linked lists
3. Sort with quicksort (3 partition version)
  1. Choice was made to keep memory footprint low, thus perform sorting inplace
  2. No requirement for keeping the order of the equal elements
4. Iterate over lists and summarize the absolute difference

## 2. part
1. Take advantage of the fact that the input is sorted:
  1. Use interval shrinking search functions to find first and last appearances
  2. Calculate number of appearance by subtracting the first appearance index from last (+1)
2. Integrate evaluation into the same loop, so arrays are only traversed once (after reading)
  1. Also keep track of previous left array value, to eliminate non-unique elements (duplicates will be in continous parts because of sorting)
