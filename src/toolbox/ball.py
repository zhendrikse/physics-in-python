from vpython import vector, sphere, color, mag, norm

from src.toolbox.moveable import Moveable

zero_force = vector(0, 0, 0)


class Ball(Moveable):
    def __init__(self,
                 mass=1.5,
                 position=vector(0, 0, 0),
                 velocity=vector(0, 0, 0),
                 radius=0.1,
                 colour=color.yellow,
                 elasticity=1.0,
                 make_trail=False,
                 draw=True):
        super().__init__(pos=position, velocity=velocity, mass=mass)

        self._ball = self._vpython_ball(mass, position, velocity, radius, colour, elasticity,
                                        make_trail) if draw else None
        self._radius = radius
        self._elasticity = elasticity

    @staticmethod
    def _vpython_ball(mass, position, velocity, radius, colour, elasticity, make_trail):
        return sphere(pos=position, radius=radius, color=colour, velocity=velocity, mass=mass, elasticity=elasticity,
                      make_trail=make_trail)

    def hits(self, building):
        right_side = building.position.x + building.L / 2
        left_side = building.position.x - building.L / 2

        if self._is_approaching_from_the_right(right_side):
            return self.position().x <= right_side + self.radius and self.position().y <= building.H

        if self._is_approaching_from_the_left(left_side):
            return self.position().x >= left_side - self.radius and self.position().y <= building.H

        return False

    def collide_with(self, building):
        building.collide_with(self)
        # set new velocity in x-direction after collision with building
        momentum_ball = self.mass() * self.velocity().x
        momentum_building = building.mass * building.velocity.x
        self._velocity.x = (momentum_ball + momentum_building + self.elasticity * building.mass * (
                building.velocity.x - self.velocity().x)) / (self.mass() + building.mass)
        self.render()

    def render(self):
        if self._ball:
            self._ball.pos = self._position

    def force_between(self, other_ball):
        if not self.has_collided_with(other_ball):
            return zero_force

        k = 101
        r = self.distance_to(other_ball)
        return k * (mag(r) - (self.radius + other_ball.radius())) * norm(r)

    def has_collided_with(self, other_ball):
        return mag(self.distance_to(other_ball)) < (self.radius + other_ball.radius())

    def rotate(self, angle, origin=vector(0, 0, 0), axis=vector(0, 1, 0)):
        self._ball.rotate(origin=origin, axis=axis, angle=angle)

    def lies_on_floor(self):
        return self.position.y - self.radius <= 0.5

    def bounce_from_floor(self, dt):
        self._velocity.y *= -self.elasticity
        self._position += self._velocity * dt

        # if the velocity is too slow, stay on the ground
        if self._velocity.y <= 0.1:
            self._position.y = self.radius + self.radius / 10

        self.render()

    @property
    def radius(self):
        return self._radius

    @property
    def elasticity(self):
        return self._elasticity
