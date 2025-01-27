#Web VPython 3.2

from vpython import *

title = """
&#x2022; Original idea (and <a href="https://jexpearce.github.io/jex/Wavepropagation.html">code</a>) by <a href="https://jexpearce.github.io/jex/">Jex Pearce</a>
&#x2022; Refactored and extended by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; Based on a <a href=""https://en.wikipedia.org/wiki/Finite_difference_method">finite difference mehtod</a>

"""

Lx, Ly = 4, 4
dx, dy = 0.05, 0.05
animation = canvas(forward=vector(-3.25, 0, -2.3), center=vector(Lx / 2, Ly / 2, 0),
                   up=vector(0, 0, 1), title=title,
                   background=color.gray(0.075), range=2.5)


class Wave:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._time = 0
        self._initialize_wave_data()
        self._old, self._new, self._now = [], [], []

    def _initialize_wave_data(self):
        self._old = [[0 for j in range(len(self._y))] for i in range(len(self._x))]
        self._now = [[0 for j in range(len(self._y))] for i in range(len(self._x))]
        self._new = [[0 for j in range(len(self._y))] for i in range(len(self._x))]

    def reset(self):
        self._initialize_wave_data()
        self._time = 0

    def update_by(self, dt):
        c = 1.5
        r = (c * dt / dx) * (c * dt / dx)
        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._new[i][j] = (2 * self._now[i][j] - self._old[i][j] +
                                   r * (self._now[i + 1][j] + self._now[i - 1][j] + self._now[i][j + 1] + self._now[i][
                            j - 1] - 4 * self._now[i][j]))
                self._old[i][j] = self._now[i][j]

        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._now[i][j] = self._new[i][j]

        if abs(self._time - 0.25) < dt:  # introducing a disturbance
            disturbance_magnitude = 0.5
            self._now[len(self._x) // 2][len(self._y) // 2] += disturbance_magnitude

        self._time += dt

    def current_values(self):
        return self._now

    def get_time(self):
        return self._time

class Pool:
    def __init__(self, x, y):
        self._x, self._y = x, y
        # self._x_contours, self._y_contours, self._surface = [], []
        self._surface = []
        self._hue = .55
        self._init_pool()
        self._init_droplets()

    def _init_droplets(self):
        positions = []
        self._surface = []
        # position_col = [[] for j in range(len(self._y))]
        for i in range(len(self._x)):
            droplets_row = []
            #position_row = []
            for j in range(len(self._y)):
                position = vector(self._x[i], self._y[j], 0)
                #position_row.append(position)
                #position_col[j].append(position)
                droplets_row.append(sphere(pos=position, radius=0.025, visible=True,
                                  color=color.hsv_to_rgb(vec(self._hue, 1, 1))))
            self._surface.append(droplets_row)
            #positions.append(position_row)

            #self._x_contours.append(curve(pos=position_row, color=vec(0, .6, 1)))

        #for i in range(len(position_col)):
            #self._y_contours.append(curve(pos=position_col[i], color=vec(0, .6, 1)))


    def _init_pool(self):
        water = box(pos=vec(Lx / 2, Ly / 2, -.1), width=.15, length=Lx, height=Ly, color=vec(0, .6, 1), opacity=0.6)
        back = box(pos=vec(dx, Ly / 2 + dy, 0), width=.4, length=.04, height=Ly, color=color.yellow)
        left = box(pos=vec(Lx / 2, 0, 0), width=.4, length=.04, height=Ly + dy, color=color.yellow)
        left.rotate(angle=radians(90), axis=vec(0, 0, 1))
        right = box(pos=vec(Lx / 2, Ly, 0), width=.4, length=.04, height=Ly + dy, color=color.yellow)
        right.rotate(angle=radians(90), axis=vec(0, 0, 1))
        bottom = box(pos=vec(Lx / 2, Ly / 2, -.2), width=0.04, length=Lx + dx, height=Ly + dy, color=color.yellow)

    def reset(self):
        for i in range(len(self._x)):
            for j in range(len(self._y)):
                self._surface[i][j].visible = False
        self._init_droplets()

    def update_by(self, dt):
        new_values = wave.current_values()
        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._x) - 1):
                self._surface[i][j].pos.z = new_values[i][j]  # Updating the z position of the surface points
                self._surface[i][j].color = color.hsv_to_rgb(vec(new_values[i][j] * 2 + self._hue, 1, 1))
                #self._x_contours[i].modify(j, pos=vector(self._x[i], self._y[j], new_values[i][j]))
                #self._y_contours[j].modify(i, pos=vector(self._x[i], self._y[j], new_values[i][j]))


    def set_hue_value_to(self, new_hue_value):
        self._hue = new_hue_value
        # for curve_ in self._x_contours:
        #     curve_.color = color.hsv_to_rgb(vec(new_hue_value, 1, 1))
        # for curve_ in self._y_contours:
        #     curve_.color = color.hsv_to_rgb(vec(new_hue_value, 1, 1))


def adjust_offset():
    pool.set_hue_value_to(offset_slider.value)
    hue_offset_text.text = "{:1.2f}".format(offset_slider.value, 2)


animation.append_to_caption("\n")
offset_slider = slider(min=0, max=1, value=.6, bind=adjust_offset)
animation.append_to_caption("hue offset = ")
hue_offset_text = wtext(text="0.55")
popup = text(text="Click mouse to start", pos=vec(-Lx / 2, 0, Ly / 3), billboard=True, color=color.yellow, height=.3)
animation_duration = 5  # seconds

animation.append_to_caption("\n\n  Remaining animation time = ")
clock = wtext(text="{:1.2f}".format(animation_duration, 2))

x_range = arange(0, Lx + dx, dx)
y_range = arange(0, Ly + dy, dy)
wave = Wave(x_range, y_range)
pool = Pool(x_range, y_range)

# The Time-loop
dt = 0.01
while True:
    popup.visible = True
    animation.waitfor("click")
    popup.visible = False
    wave.reset()
    pool.reset()
    for _ in range(int(animation_duration / dt)):
        rate(1 / (2 * dt))
        wave.update_by(dt)
        pool.update_by(dt)
        clock.text = "{:1.2f}".format(animation_duration - wave.get_time(), 2)

