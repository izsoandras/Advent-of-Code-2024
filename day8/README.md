# Summary
## Task description
### 1. part

The input is a map, the `.` is an empty space, other characters (non-whitespaces) represent location of antennas.
The different characters represent different frequencies.
Every pair of antennas of the same frequency have two antinodes.
They are
- lying on the grid exactly
- on the same line as the antennas
- **outside** of them (not stated clearly in the original description)
- on the location where one of the antennas are twice as far as the other

The task is to find the number of unique locations of these antinodes.

### 2. part

The antinodes can be anywhere on the line defined by the pair of antennas, as long as they fit the grid exactly.

## Solution outline
### 1. part

1. Read the whole array
    - it is not big
    - interpreting character by character would be possible, but would involve many addition to lists
2. Iterate over the grid, while maintaining a `dict`, mappng the frequencies to lists of locations and a boolean matrix, initialized to `false`, with the same size as the input map
    1. If a new character appears: add it to the `dict` with a list initialized with the current location on the grid
    2. If a previous character appears: iterate over all of it's previous locations and
        1. Calculate difference between them
        2. Add it to the previous and try to set the resulting location on the boolean matrix
        3. Subtract it from the current and try to set the resulting location on the boolean matrix
        4. Add the current location to the list
3. Count the number of `true` in the boolean matrix

**__ACED__**

### 2. part

Extend with not only subtracting/adding one location, but keep on repeating and marking, until we reach the edge of the matrix

**__ACED__**
