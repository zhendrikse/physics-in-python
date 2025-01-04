#Web VPython 3.2

from vpython import box, vec, rate, vector, sphere, color, mag, norm, label, canvas, cos, sin, radians, graph, gdots


title = """Balls from shooting tower hitting a block
&#x2022; Based on original <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/3_Block_Rotation.py">3_Block_rotation.py</a>
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

zero_force = vector(0, 0, 0)

# initial perimeter setting
theta, v0, e = 45, 100, 0.9
g = 98


class Timer:
    def __init__(self, position=vector(0, 0, 0), use_scientific=False, relative_to=None, timer_color=color.white):
        self._use_scientific = use_scientific
        self._relative_to = relative_to
        self._distance_to_attached_object = relative_to.position - position if relative_to else 0
        if use_scientific:
            self._timer_label = label(pos=position, text='00E01', box=False, color=timer_color)
        else:
            self._timer_label = label(pos=position, text='00:00:00.00', box=False, color=timer_color)

    def update(self, t):
        # Basically just use sprintf formatting according to either stopwatch or scientific notation
        if self._relative_to:
            self._timer_label.pos = self._distance_to_attached_object + self._relative_to.position

        if self._use_scientific:
            self._timer_label.text = "%.4E".format(t)
            return

        hours = int(t / 3600)
        minutes = int((t / 60) % 60)
        secs = int(t % 60)
        frac = int(round(100 * (t % 1)))
        if frac == 100:
            frac = 0
            secs = secs + 1

        self._timer_label.text = "{:02d}:".format(hours) + "{:02d}:".format(minutes) + "{:02d}.".format(
            secs) + "{:02d}".format(frac)


class Building:
    def __init__(self, mass=10, position=vec(0, 0, 0), length=20, height=100, width=50, color=color.orange,
                 up=vec(0, 1, 0), velocity=vec(0, 0, 0), omega=0):
        self._building = box(mass=mass, pos=position, length=length, height=height, width=width, color=color, up=up,
                             velocity=velocity)
        self._position_in_rest = position
        self._position = position
        self._length = length
        self._height = height
        self._width = width
        self._velocity = velocity
        self._up = up
        self._w = omega
        self._mass = mass

    def _angular_acceleration(self):
        if self.position() == self._position_in_rest:
            return 0

        center = self.position().x
        r = abs(self.position().x + self.H() + self.L() / 2)
        omega = g * r / self.moment_of_inertia()
        if -self.H() - center > 10:
            return -omega  # backward_rotation
        elif -self.H() - center <= 10:
            return omega  # forward rotation
        else:
            return 0

    def collide_with(self, ball):
        # sets angular velocity omega after collision with ball
        velocity = (
                               ball.mass() * ball.velocity().x + self.mass() * self.velocity().x + ball.elasticity() * ball.mass() * (
                               ball.velocity().x - self.velocity().x)) / (ball.mass() + self.mass())
        radius = ball.position().y - 0.5
        omega = velocity / radius
        self._w = omega

    def _lies_flat_on_ground(self):
        return self.position().y <= self.L() / 2 + .5

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
            self._building.rotate(origin=vec(-self.L() / 2 - self.H(), 0, 0), axis=vec(0, 0, 1), angle=dtheta)
            self._up = self._building.up
            self._position = self._building.pos

    def mass(self):
        return self._mass

    def velocity(self):
        return self._velocity

    def H(self):
        return self._height

    def position(self):
        return self._position

    def L(self):
        return self._length

    def omega(self):
        return self._w

    def W(self):
        return self._width

    def up(self):
        return self._up

    def moment_of_inertia(self):
        # I = m / 12 * (H * H + L * L), see https://kids.kiddle.co/Moment_of_inertia
        h = self.H()
        l = self.L()
        m = self.mass()
        return m / 12 * (h * h + l * l)


class Ball:
    def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow,
                 elasticity=1.0, make_trail=False):
        self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass,
                            elasticity=elasticity, make_trail=make_trail)
        self._mass = mass
        self._radius = radius
        self._velocity = velocity
        self._elasticity = elasticity
        self._position = position

    def _draw(self):
        if self._ball:
            self._ball.pos = self.position()
            self._ball.velocity = self.velocity()

    def move(self, force__vector=vector(0, 0, 0), dt=0.01):
        # Newton's second law: F = m * a
        acceleration_vector = force__vector / self.mass()
        self._velocity += acceleration_vector * dt
        self._position += self._velocity * dt
        self._draw()

    def shift(self, delta):
        self._position += delta
        self._draw()

    def distance_to(self, other):
        return other.position() - self.position()

    def has_collided_with(self, other_ball):
        return mag(self.distance_to(other_ball)) < (self.radius() + other_ball.radius())

    def rotate(self, angle, origin=vector(0, 0, 0), axis=vector(0, 1, 0)):
        self._ball.rotate(origin=origin, axis=axis, angle=angle)

    def lies_on_floor(self):
        return self.position().y - self.radius() <= 0.5

    def bounce_from_floor(self, dt):
        self._velocity.y *= -self.elasticity()
        self._position += self._velocity * dt

        # if the velocity is too slow, stay on the ground
        if self._velocity.y <= 0.1:
            self._position.y = self.radius() + self.radius() / 10

        self._draw()

    def _is_approaching_from_the_right(self, right_side):
        return self.velocity().x < 0 and self.position().x > right_side

    def _is_approaching_from_the_left(self, left_side):
        return self.velocity().x > 0 and self.position().x < left_side

    def hits(self, building):
        right_side = building.position().x + building.L() / 2
        left_side = building.position().x - building.L() / 2

        if self._is_approaching_from_the_right(right_side):
            return self.position().x <= right_side + self.radius() and self.position().y <= building.H()

        if self._is_approaching_from_the_left(left_side):
            return self.position().x >= left_side - self.radius() and self.position().y <= building.H()

        return False

    def collide_with(self, building):
        building.collide_with(self)
        # set new velocity in x-direction after collision with building
        momentum_ball = self.mass() * self.velocity().x
        momentum_building = building.mass() * building.velocity().x
        self._velocity.x = (momentum_ball + momentum_building + self.elasticity() * building.mass() * (
                building.velocity().x - self.velocity().x)) / (self.mass() + building.mass())
        self._draw()

    def momentum(self):
        return self.velocity() * self.mass()

    def kinetic_energy(self):
        return mag(self.momentum()) * mag(self.momentum()) / (2 * self.mass())

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity

    def mass(self):
        return self._mass

    def radius(self):
        return self._radius

    def elasticity(self):
        return self._elasticity


def set_scene():
    global scene
    scene = canvas(title=title, width=1000, height=600, background=vec(0, 0.6, 0.6), align='left', range=200)
    floor = box(pos=vec(0, 0, 0), size=vec(1000, 1, 1000), color=color.blue)
    scene.camera.pos = vec(0, 60, 200)
    scene.caption = " Moment of intertia \\( I = \\dfrac{M} {12} (L^2 + H^2) \\),\n Angular momentum \\( \\omega=\\dfrac{L}{I}=\\dfrac{\\vec{F} \\times \\vec{r}}{I}=\\dfrac{M\\vec{a} \\times \\vec{r}}{I} \\)\n\n\n\n"
    MathJax.Hub.Queue(["Typeset", MathJax.Hub])


def create_ball(velocity):
    global ball_counter
    a = Ball(mass=1, position=vec(100, 105, 0), radius=5, color=vec(random(), random(), random()), velocity=velocity,
             elasticity=e)
    balls.append(a)
    ball_counter += 1


set_scene()
balls = []  # enable multiple shots
ball_counter = 0
create_ball(v0 * vec(-cos(radians(theta)), sin(radians(theta)), 0))

target_building = Building(mass=10, position=vec(-100, 50.5, 0))
shooting_tower = Building(mass=30, position=vec(100, 50, 0), length=10, height=100, width=10, color=color.cyan)

g1 = graph(title='<b>Angular Velocity (for block)</b>',
           xtitle='<b>time</b>', ytitle='<b>Angular Velocity</b>', align='right',
           width=500, height=300)

w = gdots(graph=g1)


def increment_time_for(ball, dt):
    if ball.lies_on_floor():
        ball.bounce_from_floor(dt)
        return

    if ball.hits(shooting_tower):
        ball.collide_with(shooting_tower)
    elif ball.hits(target_building):
        ball.collide_with(target_building)
        target_building.rotate(-target_building.omega() * dt)

    # ball travelling through the air
    target_building.update(dt)
    ball.move(vec(0, -g, 0) * ball.mass(), dt)


t, dt = 0, 0.01
timer = Timer(position=vec(0, -25, 0))
while True:
    rate(2 / dt)
    timer.update(t)
    for ball in balls:
        increment_time_for(ball, dt)
    t += dt
    w.plot(pos=(t, target_building.omega()))