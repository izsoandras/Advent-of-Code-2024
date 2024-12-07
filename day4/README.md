# Summary
## Task description
### 1. part
Find the number of word `XMAS` in all possible 8 orientation in given matrix of characters

### 2. aprt
Find the number of times the word `MAS` appears in any direction in any 3x3 submatrix, along both diagonals

## Solution outline
### 1. part
1. First idea: implement a block array, that takes advantage of memory caching
2. Realize that I don't have that much time
3. Notice that this is almost the same as pattern matching in computer vision -> use cross-correlation and plan for generating output image just for fun
4. Realise that scipy doesn't normalize, resulting in higher response values in case of higher input values -> normalize afterwards by hand
5. Realize that there is no way to set *don't care* parts in kernel -> try to transform by shifting columns, so the diagonals become horizontal
6. Realize that this introduces a lot of ghost matches, because the patterns don't have to be matched around the edges -> change implementation, so that shifting is done in blocks of *length of pattern*
7. Realize that this way the diagonals break, so matches will be left out
8. Realize how much time I spent on this task, without any success -> have mental crisis
9. Implement the simplest, most inefficient brute force search

### 2. part
Implement just a slightly more sophisticated brute force search, which requires only one pass
