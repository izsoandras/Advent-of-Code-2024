import numpy as np

def checkArray(arr):
    diff = np.diff(arr)
    absDiff = np.abs(diff)

    return np.all(absDiff <= 3)     \
           and np.all(absDiff >= 1)  \
           and (np.all(diff < 0) or np.all(diff > 0))


def checkWithDamping(arr):
    if checkArray(arr):
        return True

    indicies =  np.arange(arr.shape[0])
    for i in indicies:
        if checkArray(arr[indicies != i]):
            return True

    return False


with open('input', 'r') as file:
    counter = 0
    for line in file:
        stringArr = line.strip().split(' ')
        intArr = np.array([int(a) for a in stringArr])
        if checkWithDamping(intArr):
            counter += 1

    print(f"Safe report number: {counter}")
