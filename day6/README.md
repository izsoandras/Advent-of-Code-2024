# Summary
## Task description
### 1. part

A map (*nxn* char matrix) is given, with the following notion:
- `.`: free space
- `#`: obstruction
- `^`: guard start position, facing "up"

Guard movement:
- If there is no obstruction in front of him, the guard steps forward
- If there is an obstruction in front of him, the guard turns 90deg right

#### Goal

Determine how many distinc location the guard visits, before leaving the map

### 2. part

Determine how many locations exists, where an insertion of *one* obstruction (before the guard starts moving) leads to a guard stucking in a loop.

## Solution outline
### 1. part

Implement the step simulation of the guard, and store each location in a set. A tree set could be used (e.g.: lexiographic ordering of the locations by coordinates), which would be efficient.

However I concluded, that I don't have enough time, to implement these structures in C, so I switched to Python.

*__ACED__*

### 2. part

The location and direction (the state) of the guard is stored in a set in each step. In each step, when the guard could move forward, a theoretical exploration is performed, assuming an obsturction in front of the guard.
The state of the guard in a given map uniquely defines the next state of the guard. Following from this, if it were to reach a state, that is already visited before leaving the map, the guard would stuck in a loop.
Furthermore, this theoretical obstruction can only be placed in unvisited locations, since the obstruction is assumed to be placed at the very beginning.

## Improvement suggestions

- store visited state with the location instead of in a separate set, so it can be decided in constant time if a state has been visited
- check if a graph representation of the problem with states as nodes, could speed up the process
- look up efficient graph circle detection algorithms
