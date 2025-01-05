from vpython import vec, mag

# Abstract base class
class Moveable:
    def __init__(self, pos=vec(0, 0, 0), velocity=vec(0, 0, 0), mass=1.0):
        self._position = pos
        self._velocity = velocity
        self._mass = mass
        self._start_position = pos
        self._start_velocity = velocity

    # To be implemented by each movable
    def render(self):
        pass

    def reset(self):
        self._position = self._start_position
        self._velocity = self._start_velocity
        self.render()

    def move_to(self, position):
        self._position = position
        self.render()

    def move_due_to(self, force_vector=vec(0, 0, 0), dt=0.01):
        # Newton's second law: F = m * a
        acceleration_vector = force_vector / self._mass
        self._velocity += acceleration_vector * dt
        self._position += self._velocity * dt
        self.render()

    def _is_approaching_from_the_right(self, right_side):
        return self.velocity().x < 0 and self.position().x > right_side

    def _is_approaching_from_the_left(self, left_side):
        return self.velocity().x > 0 and self.position().x < left_side

    def shift_by(self, delta):
        self._position += delta
        self.render()

    def distance_to(self, other):
        return other.position() - self.position()

    def momentum(self):
        return self.velocity * self.mass

    def kinetic_energy(self):
        return mag(self.momentum) * mag(self.momentum) / (2 * self._mass)

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity

    def mass(self):
        return self._mass
