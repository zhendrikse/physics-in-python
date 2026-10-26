# Web VPython 3.2
from vpython import graph, gcurve, color, pi, vector, sphere, cylinder, mag, rate, norm, sin, canvas, text

title = """ 
&#x2022; Based on <a href="https://trinket.io/glowscript/7aa45bb79b">original code</a> by Rhett Allain
&#x2022; An elaborate explanation is given in <a href="https://www.youtube.com/watch?v=DpfnIh3oEGk">his video</a> 
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/waves/code/traveling_wave.py">traveling_wave.py</a>

"""

animation = canvas(background=color.gray(0.075), title=title, height=300)

b = 0.5 * 0

class Ball:
    def __init__(self, position, radius, mass, colour=color.yellow):
        self._sphere = sphere(pos=position, radius=radius, color=colour)
        self._force = vector(0, 0, 0)
        self._momentum = vector(0, 0, 0)
        self._mass = mass

    def set_position_given(self, t, rest_position):
        omega = 45
        halve_wave_time = 2 * pi / omega
        amplitude = 5
        self._sphere.pos = rest_position
        if t < halve_wave_time:
            self._sphere.pos += amplitude * sin(omega * t) * vector(0, 1, 0)

    def pos(self):
        return self._sphere.pos

    def update_by(self, dt):
        self._momentum += self._force * dt
        self._sphere.pos += self._momentum * dt / self._mass

    def update_force(self, spring_left, spring_right, l_0, k):
        self._force = -k * (mag(spring_left) - l_0) * norm(spring_left) + k * (mag(spring_right) - l_0) * norm(spring_right) - b * self._momentum

class String:
    def __init__(self, masses_count=100, total_mass=0.025, length=100):
        self._left_end = left_end=vector(-length / 2, 0, 0)
        self._length = length
        #right_end = left_end + vector(L, 0, 0)
        ds = vector(1, 0, 0) * length / (masses_count - 1)
        radius = length / (3 * masses_count)
        self._springs, self._balls = [], []

        for i in range(masses_count):
            self._balls += [Ball(left_end + i * ds, radius, total_mass / masses_count)]

        for i in range(masses_count - 1):
            self._springs += [cylinder(pos=left_end + i * ds, axis=ds, radius=radius / 2, color=color.red)]

    def max_of_x_and_y(self):
        x_max = y_max = 0
        for bb in self._balls:
            if bb.pos().y > y_max:
                y_max = bb.pos().y
                x_max = bb.pos().x
        return x_max

    def _update_springs(self):
        for i in range(1, len(self._balls)):
            self._springs[i - 1].axis = self._balls[i].pos() - self._balls[i - 1].pos()
            self._springs[i - 1].pos = self._balls[i - 1].pos()

    def _update_balls_by(self, dt):
        for ball in self._balls:
            ball.update_by(dt)

    def _update_ball_forces(self):
        K = 1.64  # total spring constant (in theory)
        l_0 = 0.9 * self._length / len(self._springs)
        k = K * len(self._springs)
        for i in range(1, len(self._springs)):
            self._balls[i].update_force(self._springs[i - 1].axis, self._springs[i].axis, l_0, k)

    def update_by(self, t, dt):

        self._move_first_ball(t)
        self._update_ball_forces()
        self._update_balls_by(dt)
        self._update_springs()

    def _move_first_ball(self, t):
        self._balls[0].set_position_given(t, self._left_end)


g1 = graph(title="Wave String", xtitle="t [s]", ytitle="wave pulse x [m]", width=600, height=300, fast=False, background=color.black, align="top")
f1 = gcurve(color=color.blue)


# Tk = k * (mag(balls[7].pos - balls[8].pos) - L0)
# print("T calc = ", Tk, " N")

_ = String()
delta_t = 0.0001
while True:
    popup = text(text="Click mouse to start", pos=vector(-25, 4, 0), billboard=True, color=color.yellow, height=3)
    animation.waitfor("click")
    animation.delete()
    f1.delete()
    animation = canvas(x=0, y=0, height=300, background=color.gray(0.075))
    chord = String()
    time = 0
    while time < 1:
        rate(500)
        chord.update_by(time, delta_t)
        f1.plot(time, chord.max_of_x_and_y())
        time += delta_t



