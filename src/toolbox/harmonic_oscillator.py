from vpython import vector, color, hat

from ..toolbox.spring import Spring


class HarmonicOscillator:
    def __init__(self, left_ball, right_ball, spring_constant=1.0, radius=20, coils=15,
                 thickness=3, colour=color.yellow, draw=True):
        self._left_ball = left_ball
        self._right_ball = right_ball
        self._axis = self._left_ball.distance_to(self._right_ball)
        self._spring = Spring(position=left_ball.position, axis=self._axis,
                              spring_constant=spring_constant, radius=radius, thickness=thickness, colour=colour,
                              coils=coils, draw=draw)

    def increment_by(self, dt):
        self._right_ball.move(self._spring.force, dt)
        self._left_ball.move(-self._spring.force, dt)
        self._axis = self._left_ball.distance_to(self._right_ball)
        self._spring.update(self._axis, position=self._left_ball.position)

    def pull(self, delta):
        self._left_ball.shift(delta * hat(self._axis))
        self.increment_by(0)

    @property
    def ball_position_vectors(self):
        return self._left_ball.position, self._right_ball.position
