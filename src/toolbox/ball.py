from vpython import vector, sphere, color, mag, norm

from src.toolbox.moveable import Moveable

zero_force = vector(0, 0, 0)


class Ball(Moveable):
    def __init__(self,
                 mass=1.5,
                 position=vector(0, 0, 0),
                 velocity=vector(0, 0, 0),
                 radius=0.1,
                 color=color.yellow,
                 elasticity=1.0,
                 make_trail=False,
                 draw=True):

        self._ball = self._vpython_ball(mass, position, velocity, radius, color, elasticity,
                                        make_trail) if draw else None
        self._mass = mass
        self._radius = radius
        self._velocity = velocity
        self._elasticity = elasticity
        self._position = position
        self._start_position = position
        self._start_velocity = velocity

    @staticmethod
    def _vpython_ball(mass, position, velocity, radius, color, elasticity, make_trail):
        return sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass, elasticity=elasticity,
                      make_trail=make_trail)

    def reset(self):
        self._position = self._start_position
        self._velocity = self._start_velocity
        self._draw()

    def _draw(self):
        if self._ball:
            self._ball.pos = self._position
            self._ball.velocity = self._velocity

    def move(self, force_vector=vector(0, 0, 0), dt=0.01):
        # Newton's second law: F = m * a
        acceleration_vector = force_vector / self.mass
        self._velocity += acceleration_vector * dt
        self._position += self._velocity * dt
        self._draw()

    def shift(self, delta):
        self._position += delta
        self._draw()

    def force_between(self, other_ball):
        if not self.has_collided_with(other_ball):
            return zero_force

        k = 101
        r = self.distance_to(other_ball)
        return k * (mag(r) - (self.radius + other_ball.radius)) * norm(r)

    def distance_to(self, other):
        return other.position - self.position

    def has_collided_with(self, other_ball):
        return mag(self.distance_to(other_ball)) < (self.radius + other_ball.radius)

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

        self._draw()

    def _is_approaching_from_the_right(self, right_side):
        return self.velocity.x < 0 and self.position.x > right_side

    def _is_approaching_from_the_left(self, left_side):
        return self.velocity.x > 0 and self.position.x < left_side

    def hits(self, building):
        right_side = building.position.x + building.L / 2
        left_side = building.position.x - building.L / 2

        if self._is_approaching_from_the_right(right_side):
            return self.position.x <= right_side + self.radius and self.position.y <= building.H

        if self._is_approaching_from_the_left(left_side):
            return self.position.x >= left_side - self.radius and self.position.y <= building.H

        return False

    def collide_with(self, building):
        building.collide_with(self)
        # set new velocity in x-direction after collision with building
        momentum_ball = self.mass * self.velocity.x
        momentum_building = building.mass * building.velocity.x
        self._velocity.x = (momentum_ball + momentum_building + self.elasticity * building.mass * (
                    building.velocity.x - self.velocity.x)) / (self.mass + building.mass)
        self._draw()

    @property
    def momentum(self):
        return self.velocity * self.mass

    @property
    def kinetic_energy(self):
        return mag(self.momentum) * mag(self.momentum) / (2 * self.mass)

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def mass(self):
        return self._mass

    @property
    def radius(self):
        return self._radius

    @property
    def elasticity(self):
        return self._elasticity
