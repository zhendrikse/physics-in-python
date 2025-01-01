from vpython import vector, color, hat

from ..toolbox.spring import Spring
from ..toolbox.ball import Ball

class HarmonicOscillator:
    def __init__(self, position=vector(0, 0, 0), length=0.75, spring_constant=10.0, colour=color.red, coils=15, ball_radius=0.1, ball_mass=1.0):
        left = position - length * vector(1, 0, 0)
        right = position + length * vector(1, 0, 0)
        self._position = position
        self._left_ball = Ball(mass=ball_mass, position=left, radius=ball_radius, color=colour)
        self._right_ball = Ball(mass=ball_mass, position=right, radius=ball_radius, color=colour)
        self._distance = self._left_ball.distance_to(self._right_ball)
        self._spring = Spring(position=-self._distance / 2, axis=self._distance, spring_constant=spring_constant,
                              coils=coils, radius=0.6 * ball_radius)

    def update_by(self, dt):
        self._right_ball.move(self._spring.force(), dt)
        self._left_ball.move(-self._spring.force(), dt)
        self._distance = self._left_ball.distance_to(self._right_ball)
        self._spring.update(self._distance, self._position - self._distance / 2)

    def reset(self):
        self._left_ball.reset()
        self._right_ball.reset()
        self._distance = self._left_ball.distance_to(self._right_ball)
        self._spring.update(self._distance, self._position - self._distance / 2)

    def compress_by(self, amount):
        self._left_ball.shift_by(amount / 2 * vector(1, 0, 0))
        self._right_ball.shift_by(-amount / 2 * vector(1, 0, 0))
        self._distance = self._left_ball.distance_to(self._right_ball)
        self._spring.update(-self._distance, self._position + self._distance / 2)

    def left_ball_position(self):
        return self._left_ball.position()

    def right_ball_position(self):
        return self._right_ball.position()
