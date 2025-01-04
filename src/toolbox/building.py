from vpython import box, vec, color

g = 98


class Building:
    def __init__(self,
                 mass=10,
                 position=vec(0, 0, 0),
                 length=20,
                 height=100,
                 width=50,
                 color=color.orange,
                 up=vec(0, 1, 0),
                 velocity=vec(0, 0, 0),
                 omega=0,
                 draw=True):

        self._building = self._vpython_box(mass, position, length, height, width, color, up, velocity,
                                           omega) if draw else None
        self._position_in_rest = position
        self._position = position
        self._length = length
        self._height = height
        self._width = width
        self._velocity = velocity
        self._up = up
        self._w = omega
        self._mass = mass

    @staticmethod
    def _vpython_box(mass, position, length, height, width, color, up, velocity, w):
        return box(mass=mass, pos=position, length=length, height=height, width=width, color=color, up=up,
                   velocity=velocity, w=w)

    def _angular_acceleration(self):
        if self.position == self._position_in_rest:
            return 0

        center = self._position.x
        r = abs(self._position.x + self.H + self.L / 2)
        omega = g * r / self.moment_of_inertia
        if -self.H - center > 10:
            return -omega  # backward_rotation
        elif -self.H - center <= 10:
            return omega  # forward rotation
        else:
            return 0

    def collide_with(self, ball):
        # sets angular velocity omega after collision with ball
        velocity = (ball.mass() * ball.velocity().x + self.mass * self.velocity.x + ball.elasticity() * ball.mass() * (
                    ball.velocity().x - self.velocity.x)) / (ball.mass() + self.mass)
        radius = ball.position().y - 0.5
        omega = velocity / radius
        self._w = omega

    def _lies_flat_on_ground(self):
        return self.position.y <= self.L / 2 + .5

    def update(self, dt):
        self._w += self._angular_acceleration() * dt
        dtheta = -self._w * dt

        if self._lies_flat_on_ground():
            self._w = 0
            self._up = vec(-1, 0, 0)
            dtheta = 0

        self.rotate(dtheta)

    def rotate(self, dtheta):
        if self._building:
            self._building.up = self._up
            self._building.rotate(origin=vec(-self.L / 2 - self.H, 0, 0), axis=vec(0, 0, 1), angle=dtheta)
            self._up = self._building.up
            self._position = self._building.pos

    @property
    def mass(self):
        return self._mass

    @property
    def velocity(self):
        return self._velocity

    @property
    def H(self):
        return self._height

    @property
    def position(self):
        return self._position

    @property
    def L(self):
        return self._length

    @property
    def omega(self):
        return self._w

    @property
    def W(self):
        return self._width

    @property
    def up(self):
        return self._up

    @property
    def moment_of_inertia(self):
        # I = m / 12 * (H * H + L * L), see https://kids.kiddle.co/Moment_of_inertia
        h = self.H
        l = self.L
        m = self.mass
        return m / 12 * (h * h + l * l)
