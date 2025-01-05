from vpython import mag, helix, vector, box, color, random, rate, gcurve, graph, norm

from src.toolbox.ball import Ball
from src.toolbox.spring import Spring


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
            self._springs += [Spring(position=left + i * spring_size + i * vector(ball_radius, 0, 0), axis=spring_size,
                                     spring_constant=2000, radius=0.2)]

        self._balls = []
        for i in range(1, self._total_balls + 1):
            self._balls += [Ball(mass=100.0, position=left + i * spring_size + (i - 0.5) * vector(ball_radius, 0, 0),
                                 radius=ball_radius, colour=vector(random(), random(), random()))]

    def ball_position(self, ball_index):
        return self._balls[ball_index].position

    def shift_ball(self, ball_index, delta):
        self.update_ball_springs(ball_index, delta)
        self._balls[ball_index].shift(delta)

    def update(self, dt):
        for ball_i in range(0, self._total_balls):
            net_force = self._springs[ball_i].force - self._springs[ball_i + 1].force
            self._balls[ball_i].move(net_force, dt)
            self.update_ball_springs(ball_i, self._balls[ball_i].velocity * dt)

    def update_ball_springs(self, ball_index, delta):
        spring_left = self._springs[ball_index]
        spring_right = self._springs[ball_index + 1]
        spring_left.update(spring_left.axis + delta)
        spring_right.update(spring_right.axis - delta, spring_right.position + delta)


balls = 4
plot = graph(title=str(balls) + "-body coupled oscillator", xtitle="Time", ytitle="Amplitude", width=500, height=250)
oscillator = Oscillator(balls)
curve = []
for ball_i in range(0, balls):
    curve += [gcurve(color=oscillator._balls[ball_i]._ball.color)]

# Initial displacement of balls
oscillator.shift_ball(0, vector(1, 0, 0))
# oscillator.shift_ball(1, vector(-.7, 0, 0))
# oscillator.shift_ball(2, vector(0.7, 0, 0))
# oscillator.shift_ball(3, vector(-.7, 0, 0))

dt = 0.001
for i in range(0, 10000):
    rate(1 / dt)
    oscillator.update(dt)
    for ball_i in range(0, balls):
        curve[ball_i].plot(i * dt, oscillator.ball_position(ball_i).x - ball_i + balls / 2)
