import numpy as np
import manim
import matplotlib.pyplot as plt
import scipy.interpolate
import itertools


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
    def __init__(self, X, Y, data):
        pass


class HikeScene(manim.ThreeDScene):
    def construct(self):
        height_map = getinput()
        self.set_camera_orientation(phi=75 * manim.DEGREES, theta=-30 * manim.DEGREES)

        axes = manim.ThreeDAxes(x_range=[-height_map.shape[0]/2, height_map.shape[0]/2])#x_range=[0, height_map.shape[0]], x_length=height_map.shape[0]-1
        labels = axes.get_axis_labels(
            manim.Text("x-axis").scale(0.7), manim.Text("y-axis").scale(0.45), manim.Text("z-axis").scale(0.45)
        )
        surface = manim.Surface(lambda u, v: np.array([u-height_map.shape[0]/2, v-height_map.shape[1]/2, v%3]), #height_map[int(u),int(v)]
                                u_range=[0, height_map.shape[0]-1],
                                v_range=[0, height_map.shape[1]-1],
                                resolution=height_map.shape-np.array([1,1]))
        surface.scale(0.2, about_point=manim.ORIGIN)
        self.add(axes, labels, surface)

        print(height_map)


def main():
    # height_map = getinput()
    # X, Y = np.meshgrid(np.arange(0, height_map.shape[0]), np.arange(0, height_map.shape[1]), indexing='ij')

    # interpolator = scipy.interpolate.RegularGridInterpolator((np.arange(0, height_map.shape[0]), np.arange(0, height_map.shape[1])), height_map, method='cubic')

    # x_highres, y_highres = np.meshgrid(np.linspace(0, height_map.shape[0]-1, 1000), np.linspace(0, height_map.shape[1]-1, 1000), indexing='ij')
    # height_map_highres = interpolator((x_highres, y_highres))

    x = np.linspace(-3.14, 3.14, 10)
    y = np.linspace(-3.14, 3.14, 10)
    X, Y = np.meshgrid(x, y)
    orig = np.sin(X) + np.sin(Y)
    orig_dx = np.cos(X)
    orig_dy = np.cos(Y)
    orig_dxy = np.zeros_like(X)

    interp_my = GeneralDerivRectiInterpolator(x, y, orig, orig_dx, orig_dy, orig_dxy)
    interp_scipy = scipy.interpolate.RegularGridInterpolator((x, y), orig, method='cubic')

    x_high = np.linspace(-3.14, 3.14, 100)
    y_high = np.linspace(-3.14, 3.14, 100)
    X_high, Y_high = np.meshgrid(x_high, y_high)

    high_my = interp_my.eval(x_high, y_high)
    high_scipy = interp_scipy((X_high, Y_high))


    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X_high, Y_high, high_my.T)
    plt.show()

    # fig = plt.figure()
    # ax = fig.add_subplot()
    # ax.imshow(height_map_highres, cmap='terrain', extent=[0, X.max(), 0, Y.max()])
    # ax.imshow(height_map, cmap='terrain', alpha=0.5)
    # cs = ax.contourf(x_highres, y_highres, height_map_highres, cmap='terrain', levels=10, alpha=0)
    # # print(height_map.shape)
    # # c = ax.contour(cs, colors='k', linewidths=0.5)
    # min_mask = height_map == np.min(height_map)
    # # ax.plot(Y[min_mask], X[min_mask], 'bo')
    # plt.show()

if __name__=="__main__":
    main()