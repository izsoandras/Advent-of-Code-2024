import numpy as np
# import manim
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib as mpl
import scipy.interpolate
import itertools
import os


def getinput(use_example=False):
    if use_example:
        input="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".splitlines()
    else:
        with open('input') as f:
            input = f.read().splitlines()
        
    return np.array([[int(c) for c in line] for line in input])
        

class GeneralDerivRectiInterpolator():
    # Matrices to ccording to Wikipedia (https://en.wikipedia.org/wiki/Bicubic_interpolation)
    M_left = np.array([[1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [-3, 3, -2, -1],
                       [2, -2, 1, 1]])
    
    M_right = np.array([[1, 0, -3, 2],
                        [0, 0, 3, -2],
                        [0, 1, -2, 1],
                        [0, 0, -1, 1]])

    def __init__(self, x, y, data, dx, dy, dxy):
        # if data.shape != [len(x), len(y)]:
        #     raise ValueError('Data and location size misalignment')

        # if data.shape != dx.shape:
        #     raise ValueError('Data and derivative size misalignment')
        
        self.x = x
        self.y = y
        self.data = data
        self.dx = dx
        self.dy = dy
        self.dxy = dxy


    def eval(self, eval_x, eval_y):
        if eval_x[0] < self.x[0]:
            raise ValueError('Extrapolation not implemented (x_eval_min < x_min)')
        if eval_y[0] < self.y[0]:
            raise ValueError('Extrapolation not implemented (y_eval_min < y_min)')
        if eval_x[-1] > self.x[-1]:
            raise ValueError('Extrapolation not implemented (x_eval_max > x_max)')
        if eval_y[-1] > self.y[-1]:
            raise ValueError('Extrapolation not implemented (y_eval_max > y_max)')

        result = np.zeros((eval_x.shape[0], eval_y.shape[0]))

        for x_eval_idx, x_eval in enumerate(eval_x):
            for y_eval_idx, y_eval in enumerate(eval_y):
                x_orig_idx1 = np.searchsorted(self.x, x_eval)
                x_orig1 = self.x[x_orig_idx1]

                x_orig_idx0 = x_orig_idx1 - 1
                x_orig0 = self.x[x_orig_idx0]

                y_orig_idx1 = np.searchsorted(self.y, y_eval)
                y_orig1 = self.y[y_orig_idx1]

                y_orig_idx0 = y_orig_idx1 - 1
                y_orig0 = self.y[y_orig_idx0]

                corner_idxs = list(zip(*itertools.product([x_orig_idx0, x_orig_idx1], [y_orig_idx0, y_orig_idx1])))
                exact_corner_idx = [idx for idx, xy_orig in enumerate(itertools.product([x_orig0, x_orig1], [y_orig0, y_orig1])) if x_eval == xy_orig[0] and y_eval == xy_orig[1]]

                if exact_corner_idx:
                    result[x_eval_idx, y_eval_idx] = self.data[*corner_idxs][exact_corner_idx[0]]
                else:
                    f = self.data[*corner_idxs].reshape(2,2)

                    Dx = x_orig1 - x_orig0
                    Dy = y_orig1 - y_orig0

                    f_dx = Dx * self.dx[*corner_idxs].reshape(2,2)
                    f_dy = Dy * self.dy[*corner_idxs].reshape(2,2)
                    f_dxy = Dx * Dy * self.dxy[*corner_idxs].reshape(2,2)

                    F_top = np.hstack((f, f_dy))
                    F_bottom = np.hstack((f_dx, f_dxy))

                    F = np.vstack((F_top, F_bottom))

                    A = (self.M_left@F@self.M_right)

                    x_norm = (x_eval - self.x[x_orig_idx0])/Dx
                    y_norm = (y_eval - self.y[y_orig_idx0])/Dy

                    result[x_eval_idx, y_eval_idx] = np.sum([A[i,j] * x_norm**i * y_norm**j for i in range(4) for j in range(4)])

        return result


class ExtremeKeeperRectiInterpolator(GeneralDerivRectiInterpolator):
    def __init__(self, x, y, data):
        dx, dy = np.gradient(data)
        dxy1 = np.gradient(dx)[1]
        dxy2 = np.gradient(dy)[0]

        if not (dxy1 == dxy2).all():
            raise ValueError('Two dxy calculations are not equal')

        extremal_mask = (data == np.max(data)) | (data == np.min(data))
        dx[extremal_mask] = 0
        dy[extremal_mask] = 0
        dxy1[extremal_mask] = 0

        super().__init__(x, y, data, dx, dy, dxy1)


# class HikeScene(manim.ThreeDScene):
#     def construct(self):
#         height_map = getinput()
#         self.set_camera_orientation(phi=75 * manim.DEGREES, theta=-30 * manim.DEGREES)
#
#         axes = manim.ThreeDAxes(x_range=[-height_map.shape[0]/2, height_map.shape[0]/2])#x_range=[0, height_map.shape[0]], x_length=height_map.shape[0]-1
#         labels = axes.get_axis_labels(
#             manim.Text("x-axis").scale(0.7), manim.Text("y-axis").scale(0.45), manim.Text("z-axis").scale(0.45)
#         )
#         surface = manim.Surface(lambda u, v: np.array([u-height_map.shape[0]/2, v-height_map.shape[1]/2, v%3]), #height_map[int(u),int(v)]
#                                 u_range=[0, height_map.shape[0]-1],
#                                 v_range=[0, height_map.shape[1]-1],
#                                 resolution=height_map.shape-np.array([1,1]))
#         surface.scale(0.2, about_point=manim.ORIGIN)
#         self.add(axes, labels, surface)
#
#         print(height_map)


def dfs_hike(height_map, start, dsf_graph=None):
    visited = np.zeros_like(height_map, dtype=bool)
    to_visit = [(None, start)]

    peak_count = 0

    while to_visit:
        (parent, current) = to_visit.pop()

        if height_map[*current] == 9:
            peak_count += 1
        else:
            for offset in [[+1, 0], [-1, 0], [0, +1], [0, -1]]:
                neigh = current + offset
                if np.all(neigh >= 0) and np.all(neigh < height_map.shape):
                    if not visited[*neigh] and height_map[*current] + 1 == height_map[*neigh]:
                        to_visit.append((current, neigh))

        if dsf_graph is not None:
            dsf_graph.append((parent, current))

        visited[*current] = True

    return peak_count


def distinct_dfs_hike(height_map, start):
    visited = np.zeros_like(height_map, dtype=bool)
    to_visit = [start]
    inside = []

    trail_count = 0

    while to_visit:
        current = to_visit[-1]

        if visited[*current]:
            to_visit.pop()
            visited[*current] = False
        else:
            if height_map[*current] == 9:
                trail_count += 1
            else:
                for offset in [[+1, 0], [-1, 0], [0, +1], [0, -1]]:
                    neigh = current + offset
                    if np.all(neigh >= 0) and np.all(neigh < height_map.shape):
                        if not visited[*neigh] and height_map[*current] + 1 == height_map[*neigh]:
                            to_visit.append(neigh)

            visited[*current] = True

    return trail_count


def main():
    height_map = getinput()

    trail_heads = np.argwhere(height_map == 0)
    dsf_seqs = [[] for _ in range(len(trail_heads))]
    print(np.sum([dfs_hike(height_map, min_loc, seq) for min_loc, seq in zip(trail_heads, dsf_seqs)]))
    print(dsf_seqs[0])

    x = np.arange(0, height_map.shape[0])
    y = np.arange(0, height_map.shape[1])
    X, Y = np.meshgrid(x, y, indexing='ij')

    interp_my = ExtremeKeeperRectiInterpolator(x, y, height_map)
    interp_scipy = scipy.interpolate.RegularGridInterpolator((x, y), height_map, method='cubic')

    # x_highres, y_highres = np.meshgrid(np.linspace(0, height_map.shape[0]-1, 1000), np.linspace(0, height_map.shape[1]-1, 1000), indexing='ij')
    # height_map_highres = interpolator((x_highres, y_highres))



    x_high = np.linspace(0, height_map.shape[0]-1, 1000)
    y_high = np.linspace(0, height_map.shape[1]-1, 1000)
    X_high, Y_high = np.meshgrid(x_high, y_high)

    if os.path.exists('highres.npy'):
        high_my = np.load('highres.npy')
    else:
        high_my = interp_my.eval(x_high, y_high)
        np.save('highres.npy', high_my)
    # high_scipy = interp_scipy((X_high, Y_high))

    min_mask = height_map == np.min(height_map)
    max_mask = height_map == np.max(height_map)

    # fig, axes = plt.subplots(1, 3)
    # axes[0].imshow(height_map, cmap='terrain')
    # axes[0].plot(Y[min_mask], X[min_mask], 'o', color='orange')
    # axes[0].plot(Y[max_mask], X[max_mask], 'o', color='red')
    # axes[1].imshow(high_my, cmap='terrain', extent=[x[0], x[-1], y[-1], y[0]])
    # axes[1].plot(Y[min_mask], X[min_mask], 'o', color='orange')
    # axes[1].plot(Y[max_mask], X[max_mask], 'o', color='red')
    # axes[2].imshow(high_scipy, cmap='terrain', extent=[x[0], x[-1], y[-1], y[0]])
    # axes[2].plot(Y[min_mask], X[min_mask], 'o', color='orange')
    # axes[2].plot(Y[max_mask], X[max_mask], 'o', color='red')

    # ax.plot_surface(X_high, Y_high, high_my.T, alpha=1, cmap='viridis')
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')


    fig = plt.figure(figsize=(12,12), frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])

    def plot_init():
        # fig.set_facecolor('black')
        # plt.tight_layout()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        base = ax.imshow(high_my, cmap='terrain', extent=[0, X.max()+1, 0, Y.max()+1], vmin=-3, vmax=9.5)
        levels = np.linspace(0, 9, 7)
        contours = ax.contour(x_high, y_high, np.flipud(high_my), levels=levels, linewidths=0.5, cmap='ocean', vmax=40, extent=[0, X.max(), 0, Y.max()])

    trail_colors = mpl.colormaps['Dark2'](np.linspace(0, 1, 8))
    trails_synced = itertools.zip_longest(*dsf_seqs)
    # next(trails_synced) # throw away 1st entry, because it is [None, start]
    def update(frame):
        if frame < 1:
            return

        next_edges = next(trails_synced)
        for edge, color in zip(next_edges, itertools.cycle(trail_colors)):
            if edge is not None:
                n1 = edge[0]
                n2 = edge[1]

                if n1 is not None:
                    x_idx = [n1[0], n2[0]]
                    y_idx = [n1[1], n2[1]]
                else:
                    x_idx = n2[0]
                    y_idx = n2[1]

                ax.plot(x[x_idx] + 0.5, y[y_idx] + 0.5,color=color, marker='.', linewidth=3, markersize=12)

    animation = ani.FuncAnimation(fig=fig, func=update, init_func=plot_init, interval=100, frames=np.max([len(seq) for seq in dsf_seqs])-1)

    # ax.imshow(height_map, cmap='terrain', alpha=0.5)
    # cs = ax.contourf(x_high, y_high, np.flipud(high_my), cmap='terrain', levels=levels, vmin=-1.5, alpha=0)
    # print(height_map.shape)
    # ax.plot(Y[min_mask], X[min_mask], 'bo')
    animation.save('ani.gif', dpi=80, savefig_kwargs={'pad_inches':0})
    # update(0)
    # plt.show()

if __name__=="__main__":
    main()