import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.animation as ani
import matplotlib.colors as mplcol
from copy import deepcopy


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

    # front_idx = 0
    # rear_idx = np.prod(disk.shape)-1
    # checksum = 0
    # cntr = 0
    # while front_idx < rear_idx:
    #     cntr += 1
    #     front_coord = np.unravel_index(front_idx, disk.shape)
    #     rear_coord = np.unravel_index(rear_idx, disk.shape)
    #     # print(checksum)
    #     if disk[front_coord] != -1:
    #         checksum += front_idx * disk[front_coord]
    #         front_idx += 1
    #     elif disk[rear_coord] == -1:
    #         rear_idx -= 1
    #     else:
    #         tmp = disk[front_coord]
    #         disk[front_coord] = disk[rear_coord]
    #         disk[rear_coord] = tmp

    # print(checksum)
    # print(cntr)

    # return

    orig_color = mpl.colormaps['Set3'].resampled(12)
    newcolors = orig_color(np.linspace(0, 1, 12))
    black = np.array([0, 0, 0, 1])
    green = np.array([0, 1, 0, 1])
    red = np.array([1, 0, 0, 1])
    newcolors = np.vstack((black, newcolors, green, red))
    # newcolors = np.vstack((black, newcolors))
    cmap = mplcol.ListedColormap(newcolors)

    fig, ax = plt.subplots(dpi=300)
    im_artist = ax.pcolormesh(np.zeros_like(disk), cmap=cmap, rasterized=True, vmin=-1, vmax=13.9)
    # im_artist = ax.imshow((disk+1)%13, cmap=cmap, interpolation='nearest')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_facecolor('black')
    fig.set_facecolor('black')
    fig.suptitle('Disk fragmentation', color='white')
    ax.set_title('Chksum: 0', color='white')
    
    # fig.colorbar(im_artist, ax=ax)
    plt.tight_layout()

    frame_no = 120000
    fps=60
    length_s = 40
    step_per_frame = int(frame_no/(fps*length_s))
    anim_frame_no = fps*length_s
    class Animator():
        def __init__(self):
            self.front_idx = 0
            self.rear_idx = np.prod(disk.shape)-1
            self.checksum = 0
        def update(self, frame):
            print(frame/frame_no)
            for _ in range(step_per_frame):
                if self.front_idx < self.rear_idx:
                    front_coord = np.unravel_index(self.front_idx, disk.shape)
                    rear_coord = np.unravel_index(self.rear_idx, disk.shape)
                    if disk[front_coord] != -1:
                        self.checksum += self.front_idx * disk[front_coord]
                        self.front_idx += 1
                    elif disk[rear_coord] == -1:
                        self.rear_idx -= 1
                    else:
                        tmp = disk[front_coord]
                        disk[front_coord] = disk[rear_coord]
                        disk[rear_coord] = tmp

            
            image = deepcopy(disk)
            image[image != -1] = image[image != -1] % 12
            if self.front_idx < self.rear_idx:
                image[front_coord] = 12
                image[rear_coord] = 13

            im_artist.set_array(np.flipud(image))
            # im_artist.set_data(data)
            ax.set_title(f'Chksum: {self.checksum:.0f}')
    updater = Animator()

    anim = ani.FuncAnimation(fig, updater.update, interval=1, frames=int(anim_frame_no))#, frames=np.prod(disk.shape)*2)
    anim.save('pyplot.mp4', fps=fps)
    # plt.show()

    print("Done")


if __name__ == "__main__":
    main()