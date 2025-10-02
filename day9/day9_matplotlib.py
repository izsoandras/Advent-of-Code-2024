import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.colors as mplcol


def prepare_data(use_example=False):
    if use_example:
        instring = '2333133121414131402'
        n_rows = 6
        n_cols = 7
    else:
        with open("input") as input:
            instring = input.readline()[:-1]

        # gridsize determined manually
        n_rows = 272
        n_cols = 350

    dense_layout = np.array([int(char) for char in instring])

    sparse_layout = -np.ones([n_rows, n_cols])

    file_idx = 0
    sparse_idx = 0
    is_file = True
    for block_size in dense_layout:
        # calculate indices
        flat_idxs = np.arange(sparse_idx, sparse_idx + block_size)
        coord_idxs = np.unravel_index(flat_idxs, (n_rows, n_cols))

        # write value
        if is_file:
            sparse_value = file_idx
            file_idx += 1
        else:
            sparse_value = -1

        sparse_layout[coord_idxs] = sparse_value

        # update indices
        sparse_idx += block_size
        is_file = not is_file

    return sparse_layout, int(np.ceil(len(instring)/2))


def main():
    disk, n_files = prepare_data()

    orig_color = mpl.colormaps['Set3'].resampled(13)
    newcolors = orig_color(np.linspace(0, 1, 13))
    black = np.array([0, 0, 0, 1])
    newcolors[0, :] = black
    cmap = mplcol.ListedColormap(newcolors)


    disk[disk!=-1] = disk[disk!=-1]%10
    print(disk[0,0:30])
    plt.imshow(disk, interpolation='nearest', cmap=cmap)
    plt.show()


if __name__ == "__main__":
    main()