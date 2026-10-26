# Web VPython 3.2

from vpython import canvas, sphere, rate, vector, mag, norm, vec, helix, color, graph, box, gcurve, arange

title = """ &#x2022; <a href="https://github.com/zhendrikse/science/blob/main/waves/code/n_body_oscillator.py">n_body_oscillator.py</a> by <a href="http://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; The number of beads still needs to be modified in the code itself

"""

display = canvas(background=color.gray(0.075), title=title, forward=vec(-.5, -.4, -.75), center=vec(1.5, -.55, -.75),
                 range=4)


class Spring:
    def __init__(self, pos, axis, radius=0.15, thickness=0.05):
        self._spring = helix(pos=pos, axis=axis, radius=radius, thickness=thickness, color=color.white, coils=15)
        self._size = mag(axis)

    def force(self):
        displacement = mag(self._spring.axis) - self._size
        return -1 * 2000 * displacement * norm(self._spring.axis)

    def update(self, delta, position=vector(0, 0, 0)):
        self._spring.axis += delta
        self._spring.pos += position


class Ball:
    def __init__(self, pos, colour, mass=200):
        self._ball = sphere(pos=pos, radius=0.30, color=colour)
        self._velocity = vector(0, 0, 0)
        self._mass = mass

    def update(self, net_force, dt):
        self._velocity += dt * net_force / self._mass
        self._ball.pos += self._velocity * dt

    def shift(self, delta):
        self._ball.pos += delta

    def position(self):
        return self._ball.pos

    def velocity(self):
        return self._velocity


class Oscillator:
    def __init__(self, number_of_balls=3):
        self._total_balls = number_of_balls
        ball_radius = 0.30
        spring_size = vector(2, 0, 0)
        total_size = mag(spring_size) * (self._total_balls + 1) + self._total_balls * ball_radius
        self._spring_size = mag(spring_size)

        left = vector(-total_size / 2, 0, 0)

        self._left_wall = box(pos=left, size=vector(2, 0.05, 2), color=color.green, up=vector(1, 0, 0))
        self._right_wall = box(pos=-left, size=vector(2, 0.05, 2), color=color.green, up=vector(1, 0, 0))

        self._springs = []
        for i in range(0, self._total_balls + 1):
            self._springs += [Spring(pos=left + i * spring_size + i * vector(ball_radius, 0, 0), axis=spring_size)]

        self._balls = []
        for i in range(1, self._total_balls + 1):
            self._balls += [
                Ball(pos=left + i * spring_size + (i - 0.5) * vector(ball_radius, 0, 0), colour=color.orange)]

    def ball_position(self, ball_index):
        return self._balls[ball_index].position()

    def shift_ball(self, ball_index, delta):
        self.update_ball_springs(ball_index, delta)
        self._balls[ball_index].shift(delta)

    def update(self, dt):
        for ball_i in range(0, self._total_balls):
            net_force = self._springs[ball_i].force() - self._springs[ball_i + 1].force()
            self._balls[ball_i].update(net_force, dt)
            self.update_ball_springs(ball_i, self._balls[ball_i].velocity() * dt)

    def update_ball_springs(self, ball_index, delta):
        self._springs[ball_index].update(delta)
        self._springs[ball_index + 1].update(-delta, delta)


def zoom_in_on(selected_object):
    if selected_object is None:
        return

    ### ANIMATE TO SELECTED POSITION
    temp_color = vec(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    step = (target - display.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(20)
        display.center += step
        display.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color


def on_mouse_click():
    zoom_in_on(display.mouse.pick)


display.bind('click', on_mouse_click)

balls = 4
plot = graph(title=str(balls) + "-body coupled oscillator", xtitle="Time", ytitle="Amplitude", width=500, height=250,
             background=color.black)
oscillator = Oscillator(balls)
curve = []
for ball_i in range(0, balls):
    curve += [gcurve(color=color.magenta)]

# Initial displacement of balls
oscillator.shift_ball(0, vector(1, 0, 0))
# oscillator.shift_ball(1, vector(-.7, 0, 0))
# oscillator.shift_ball(2, vector(0.7, 0, 0))
# oscillator.shift_ball(3, vector(-.7, 0, 0))

delta_t = 0.001
t = 0
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])
while True:
    rate(1 / delta_t)
    oscillator.update(delta_t)
    for ball_i in range(0, balls):
        curve[ball_i].plot(t / delta_t, oscillator.ball_position(ball_i).x - ball_i + balls / 2)
    t += delta_t
