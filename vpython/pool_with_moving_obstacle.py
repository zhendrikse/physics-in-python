#Web VPython 3.2


from vpython import *

title = """
&#x2022; Original idea (and <a href="https://jexpearce.github.io/jex/Wavepropagation.html">code</a>) by <a href="https://jexpearce.github.io/jex/">Jex Pearce</a>
&#x2022; Refactored and extended by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/waves/code/pool_with_moving_obstacle.py">pool_with_moving_obstacle.py</a>
&#x2022; Based on a <a href=""https://en.wikipedia.org/wiki/Finite_difference_method">finite difference method</a>

"""

Lx, Ly = 2, 2
dx, dy = 0.05, 0.05
animation = canvas(forward=vector(3.4, 0, -2.), center=vector(Lx / 2, Ly / 2, 0),
                   up=vector(0, 0, 1), title=title,
                   background=color.gray(0.075), range=1.35)


class Wave:
    def __init__(self, x, y, obstacle):
        self._x, self._y, self._obstacle = x, y, obstacle
        self._hue = 2.55
        self._opacity = 1.0
        self._radius = 0.03
        self._time = 0
        self._initialize_wave_data()
        self._old, self._new, self._surface = [], [], []
        self._init_droplets()

    def _init_droplets(self):
        self._surface = []
        for i in range(len(self._x)):
            droplets_row = []
            for j in range(len(self._y)):
                # Don't show the entry droplets, otherwise they'll
                # be visibile inside the box
                show = False if i == len(self._x) - 1 or i == 0 else True
                colour = color.hsv_to_rgb(vec(self._hue, 1, 1))
                position = vector(self._x[i], self._y[j], 0)
                droplets_row.append(
                    simple_sphere(pos=position, visible=show, radius=self._radius, opacity=self._opacity, color=colour))
            self._surface.append(droplets_row)

    def _initialize_wave_data(self):
        self._old = [[0 for j in range(len(self._y))] for i in range(len(self._x))]
        self._new = [[0 for j in range(len(self._y))] for i in range(len(self._x))]

    def update(self, dt):
        c = 1.5
        r = (c * dt / dx) * (c * dt / dx)
        now = self._surface

        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                boxstart, boxwidth, box_ystart, box_yend = self._obstacle.boundaries()
                if boxstart <= self._x[i] <= boxstart + boxwidth and box_ystart <= self._y[j] <= box_yend:
                    # Inside the box, create a wave disturbance, putting the amplitude on the same
                    self._new[i][j] = .05 * self._obstacle.speed() * sin(
                        2 * pi * self._x[i])  # just the x spacial coordinates this time
                    self._surface[i][j].visible = False
                else:
                    self._surface[i][j].visible = True
                    self._new[i][j] = (2 * now[i][j].pos.z - self._old[i][j] +
                                       r * (now[i + 1][j].pos.z + now[i - 1][j].pos.z + now[i][j + 1].pos.z + now[i][
                                j - 1].pos.z - 4 * now[i][j].pos.z))
                    self._old[i][j] = self._surface[i][j].pos.z

        # Update surface
        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._surface[i][j].pos.z = self._new[i][j]  # Updating the z position of the surface points
                self._surface[i][j].color = color.hsv_to_rgb(vec(self._new[i][j] * 1.5 + self._hue, 1, 1))

        self._time += dt

    def get_time(self):
        return self._time

    def set_opacity_to(self, new_value):
        self._opacity = new_value
        for i in range(len(self._x)):
            for j in range(len(self._y)):
                self._surface[i][j].opacity = new_value

    def set_hue_value_to(self, new_hue_value):
        self._hue = new_hue_value

    def set_droplet_radius_to(self, new_radius):
        self._radius = new_radius
        for i in range(len(self._x)):
            for j in range(len(self._y)):
                self._surface[i][j].radius = new_radius

    def reset(self):
        self._initialize_wave_data()
        self._time = 0

        for i in range(len(self._x)):
            for j in range(len(self._y)):
                self._surface[i][j].visible = False
                # self._surface[i][j].delete()
        self._init_droplets()


class Obstacle:
    def __init__(self, x, y, start=Lx, width=Lx / 3, ystart=Ly / 3, yend=2 * Ly / 3):
        self._height = .9
        self._has_reached_end = False
        self._width = width
        self._start, self._initial_start = start, start
        self._speed = 1
        self._y_start = ystart
        self._y_end = yend
        self._box = self._create_block(start, width, ystart, yend, self._height)

    def _create_block(self, start, width, ystart, yend, height):
        return box(pos=vector(start + width / 2, (ystart + yend) / 2, 0),
                   size=vector(width, yend - ystart, height),
                   color=color.green, opacity=0.8)

    def reset(self):
        self._has_reached_end = False
        self._box.pos.x, self._start = self._initial_start, self._initial_start

    def boundaries(self):
        return self._start, self._width, self._y_start, self._y_end

    def move(self, dt):
        if not self._has_reached_end:
            self._start -= self._speed * dt
            self._box.pos.x = self._start + self._width / 2

            # Check if box has reached the end
            if self._start <= 0:
                self._has_reached_end = True

    def set_speed_to(self, new_speed):
        self._speed = new_speed

    def speed(self):
        return self._speed


class Pool:
    def __init__(self, Lx, Ly, dx, dy):
        water = box(pos=vec(Lx / 2, Ly / 2, -.3), width=.425, length=Lx, height=Ly, color=vec(0, .6, 1), opacity=0.5)
        # back = box(pos=vec(-dx, Ly / 2, -0.17), width=.7, length=.04, height=Ly+2*dy, color=color.yellow)
        left = box(pos=vec(Lx / 2, -dy, -.17), width=.7, length=.04, height=Lx + dx, color=color.yellow)
        left.rotate(angle=radians(90), axis=vec(0, 0, 1))
        right = box(pos=vec(Lx / 2, Ly + dy, -.17), width=.7, length=.04, height=Lx + dx, color=color.yellow)
        right.rotate(angle=radians(90), axis=vec(0, 0, 1))
        bottom = box(pos=vec(Lx / 2, Ly / 2, -.5), width=0.04, length=Lx + dx, height=Ly + dy, color=color.yellow)


def adjust_offset():
    wave.set_hue_value_to(offset_slider.value + 2.55)
    hue_offset_text.text = "{:1.2f}".format(offset_slider.value, 2)


def adjust_speed():
    obstacle.set_speed_to(speed_slider.value)
    speed_text.text = "{:1.2f}".format(speed_slider.value, 2)


def adjust_droplet_radius():
    wave.set_droplet_radius_to(radius_slider.value * .01)
    droplet_radius_text.text = "{:1.2f}".format(radius_slider.value, 2)

def adjust_opacity():
    wave.set_opacity_to(opacity_slider.value)
    opacity_text.text = "{:1.2f}".format(opacity_slider.value, 2)

animation.append_to_caption("\n")
radius_slider = slider(min=1, max=4, value=3.0, step=.1, bind=adjust_droplet_radius)
animation.append_to_caption("droplet radius = ")
droplet_radius_text = wtext(text="3.0")

animation.append_to_caption("\n\n")
offset_slider = slider(min=0, max=1, value=0, bind=adjust_offset)
animation.append_to_caption("hue offset = ")
hue_offset_text = wtext(text="0.0")

animation.append_to_caption("\n\n")
opacity_slider = slider(min=0, max=1, step=0.01, value=1.0, bind=adjust_opacity)
animation.append_to_caption("opacity = ")
opacity_text = wtext(text="1.0")

animation.append_to_caption("\n\n")
speed_slider = slider(min=0.7, max=1.2, value=.8, bind=adjust_speed)
animation.append_to_caption("speed = ")
speed_text = wtext(text="0.8")

popup = text(text="Click mouse to start", pos=vec(1, 2.2, .9), billboard=True, color=color.yellow, height=.2)
animation_duration = 3

animation.append_to_caption("\n\n  Remaining animation time = ")
clock = wtext(text="{:1.2f}".format(animation_duration, 2))

x_range = arange(0, Lx + dx, dx)
y_range = arange(0, Ly + dy, dy)

obstacle = Obstacle(x_range, y_range)
wave = Wave(x_range, y_range, obstacle)
pool = Pool(Lx, Ly, dx, dy)

# The Time-loop
dt = 0.01
while True:
    animation.waitfor("click")
    popup.visible = False
    obstacle.reset()
    wave.reset()
    for _ in range(int(animation_duration / dt)):
        # Update box position if it hasn't reached the end
        obstacle.move(dt)

        rate(1 / (10 * dt))
        wave.update(dt)
        clock.text = "{:1.2f}".format(animation_duration - wave.get_time(), 2)

    popup.visible = True
