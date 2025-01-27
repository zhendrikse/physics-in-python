#Web VPython 3.2

from vpython import *

title = """
&#x2022; Original idea (and <a href="https://jexpearce.github.io/jex/Wavepropagation.html">code</a>) by <a href="https://jexpearce.github.io/jex/">Jex Pearce</a>
&#x2022; Refactored and extended by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; Based on a <a href=""https://en.wikipedia.org/wiki/Finite_difference_method">finite difference mehtod</a>

"""

Lx, Ly = 3, 3
dx, dy = 0.05, 0.05
animation = canvas(forward=vector(-3.6, 0, -1.75), center=vector(Lx / 2, Ly / 2, 0),
                   up=vector(0, 0, 1), title=title,
                   background=color.gray(0.075), range=2)


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
        r = (c * dt / dx) ** 2
        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._new[i][j] = (2 * self._now[i][j] - self._old[i][j] +
                                   r * (self._now[i + 1][j] + self._now[i - 1][j] + self._now[i][j + 1] + self._now[i][
                            j - 1] - 4 * self._now[i][j]))

        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._old[i][j] = self._now[i][j]

        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._now[i][j] = self._new[i][j]

        if abs(self._time - 0.25) < dt:  # introducing a disturbance
            self._now[len(self._x) // 2][len(self._y) // 2] += 0.6  # adding disturbance at the center of the grid, the 0.5 is like the 'intensity'

        self._time += dt

    # def len_x(self):
    #     return len(self._now)
    #
    # def len_y(self):
    #     return len(self._now[0])

    def current_values(self):
        return self._now

    def get_time(self):
        return self._time

class Pool:
    def __init__(self, x, y):
        # creating a list of sphere objects for the surface
        self._x = x
        self._y = y
        self._surface = []
        self._hue = .6
        self._init_pool()
        self._init_droplets()

    def _init_droplets(self):
        droplets = []
        for i in range(len(self._x)):
            row = []
            for j in range(len(self._y)):
                row.append(sphere(pos=vector(x[i], y[j], 0), radius=0.01,
                                  color=color.hsv_to_rgb(vec(self._hue, 1, 1))))
            droplets.append(row)
        self._surface = droplets

    def _init_pool(self):
        water = box(pos=vec(Lx / 2, Ly / 2, -.1), width=.2, length=Lx, height=Ly, color=vec(0, .6, 1), opacity=0.75)
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
        for i in range(1, len(self._x)):
            for j in range(1, len(self._x)):
                self._surface[i][j].pos.z = new_values[i][j]  # Updating the z position of the surface points
                self._surface[i][j].color = color.hsv_to_rgb(vec(new_values[i][j] + self._hue, 1, 1))

    def set_hue_value_to(self, new_hue_value):
        self._hue = new_hue_value


def adjust_offset():
    pool.set_hue_value_to(offset_slider.value)
    hue_offset_text.text = "{:1.2f}".format(offset_slider.value, 2)


animation.append_to_caption("\n")
offset_slider = slider(min=0, max=1, value=.6, bind=adjust_offset)
animation.append_to_caption("hue offset = ")
hue_offset_text = wtext(text="0.6")
popup = text(text="Click mouse to start", pos=vec(-Lx / 2, 0, Ly / 3), billboard=True, color=color.yellow, height=.3)
animation_duration = 4  # seconds

animation.append_to_caption("\n\n  Remaining animation time = ")
clock = wtext(text="{:1.2f}".format(animation_duration, 2))

x = arange(0, Lx + dx, dx)
y = arange(0, Ly + dy, dy)
wave = Wave(x, y)
pool = Pool(x, y)

# The Time-loop
dt = 0.01
while True:
    popup.visible = True
    animation.waitfor("click")
    popup.visible = False
    wave.reset()
    pool.reset()
    for _ in range(int(animation_duration / dt)):
        rate(30)
        wave.update_by(dt)
        pool.update_by(dt)
        clock.text = "{:1.2f}".format(animation_duration - wave.get_time(), 2)

