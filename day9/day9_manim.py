import manim
import numpy as np
import itertools


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

    sparse_layout = np.zeros([n_rows, n_cols])

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

def calculate_rect_coord(n_rows, n_cols, idx, screen_height=8, screen_width=8*16/9):
    rect_size = np.min([screen_height/n_rows, screen_width/n_cols])

    y_max = (n_rows-1)/2 * rect_size#screen_height/2 - rect_size/2
    x_min = -(n_cols-1)/2 * rect_size
    cell_coords = np.unravel_index(idx, (n_rows, n_cols))

    return [x_min + cell_coords[1]*rect_size, y_max - cell_coords[0]*rect_size]


class FragmenterScene(manim.Scene):
    def construct(self):
        # default screen units in Manim
        screen_height = 8
        screen_width = screen_height * 16/9
        runtime = 0.5

        # read data
        disk_layout, n_files = prepare_data(True)

        # create initial grid
        rect_size = screen_height / disk_layout.shape[0]
        n_rect = np.prod(disk_layout.shape)
        colors = [manim.random_bright_color() for _ in range(n_files)]
        texts = []
        rects = []
        for idx in range(n_rect):
            disk_idx = np.unravel_index(idx, disk_layout.shape)
            file_id = int(disk_layout[disk_idx])
            if file_id != -1:
                color = colors[file_id]
            else:
                color = manim.BLACK


            loc = calculate_rect_coord(disk_layout.shape[0], disk_layout.shape[1], idx) + [0,]

            rects.append(manim.Square(rect_size, fill_color=color, fill_opacity=1).move_to(loc))
            if file_id != -1:
                texts.append(manim.Text(f'{file_id}', height=0.5*rect_size, color=manim.DARK_GREY).
                             move_to(loc).
                             add_updater(lambda x, rect=rects[idx] : x.move_to(rect.get_center()))
                        )


        create_animation = [manim.Create(r) for r in rects]
        self.play(manim.LaggedStart(*create_animation, run_time=3, lag_ratio=0.01))
        self.play(manim.FadeIn(*texts))

        front_caret = manim.Square(rect_size, stroke_width=10, stroke_color=manim.PURE_GREEN).move_to(rects[0].get_center())
        rear_caret = manim.Square(rect_size, stroke_width=10, stroke_color=manim.PURE_RED).move_to(rects[-1].get_center())
        self.play(manim.FadeIn(front_caret, rear_caret))

        checksum_vt = manim.ValueTracker(0)
        display = manim.DecimalNumber(0, num_decimal_places=0, font_size=80)
        display.add_updater(lambda disp : disp.set_value(checksum_vt.get_value()))
        display.move_to([-8*16/9/2+rect_size/2,4-rect_size/2, 0])
        self.play(manim.Write(display))


        front_idx = 0
        rear_idx = len(rects) - 1


        # def caret_updater(caret, idx_tracker):
        #     idx0 = int(np.floor(idx_tracker.get_value()))
        #     p0 = rects[idx0].get_center()

        #     if idx0 == len(rects) - 1:
        #         caret.move_to(p0)
        #     else:    
        #         p1 = rects[idx0+1].get_center()
        #         diff = idx_tracker.get_value() - idx0
        #         caret.move_to((1-diff)*p0 + diff*p1)


        disk_unravel = lambda idx : np.unravel_index(idx, disk_layout.shape)
        while front_idx < rear_idx:
            if disk_layout[disk_unravel(front_idx)] != -1:
                front_idx += 1
                # self.play(front_vt.animate.set_value(front_idx))
                self.play(front_caret.animate.move_to(rects[front_idx].get_center()), run_time=runtime)
            elif disk_layout[disk_unravel(rear_idx)] == -1:
                rear_idx -= 1
                # self.play(rear_vt.animate.set_value(rear_idx))
                self.play(rear_caret.animate.move_to(rects[rear_idx].get_center()), run_time=runtime)
            else:
                tmp = disk_layout[disk_unravel(front_idx)]
                disk_layout[disk_unravel(front_idx)] = disk_layout[disk_unravel(rear_idx)]
                disk_layout[disk_unravel(rear_idx)] = tmp
                p_front = rects[front_idx].get_center()
                p_rear = rects[rear_idx].get_center()
                tmp = rects[front_idx]
                self.play(rects[rear_idx].animate.move_to(p_front), run_time=runtime)
                rects[front_idx].move_to(p_rear)
                rects[front_idx] = rects[rear_idx]
                rects[rear_idx] = tmp

            file_id = disk_layout[disk_unravel(front_idx)]
            if file_id != -1:
                self.play(checksum_vt.animate.increment_value(front_idx * file_id), run_time=runtime)

            

        self.wait(2)

if __name__ == "__main__":
    disk, file_no = prepare_data(True)
    pass