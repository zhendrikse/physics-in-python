#Web VPython 3.2

from vpython import vector, vec, sphere, helix, mag, color, cylinder, curve, scene, arange, sqrt, rate, norm

title = """Semi-classical visualization of quantum oscillator

&#x2022; Original <a href="https://lectdemo.github.io/virtual/06_oscillator.html">06_oscillator.py</a> by Ruth Chabay 2004
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

Click on an energy level to put the oscillator into that state

"""

y_axis_pos = -10
ks = 1.2  ## 200
ball_mass = 0.025
omega = sqrt(ks / ball_mass)
L0 = 10
show_vertical_lines = False

class Ball:
    def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow, make_trail=False):
        self._ball = sphere(pos=position, radius=radius, color=color, make_trail=make_trail)
        self._mass = mass
        self._velocity = velocity
        self._start_velocity = velocity
        self._start_position = position

    def move(self, force__vector, dt):
        acceleration_vector = force__vector / self._mass
        self._velocity += acceleration_vector * dt
        self._ball.pos += self._velocity * dt

    def shift_by(self, amount):
        self._ball.pos += amount

    def reset(self):
        self._ball.pos = self._start_position
        self._velocity = self._start_velocity

    def distance_to(self, other):
        return other.position() - self.position()

    def position(self):
        return self._ball.pos


class Spring:
    def __init__(self, position=vector(0, 0, 0), axis=vector(1.0, 0, 0), spring_constant=10.0, radius=0.5, thickness=0.03):
        self._equilibrium_size = mag(axis)
        self._spring = helix(pos=position, axis=axis, radius=radius, thickness=thickness, spring_constant=spring_constant, coils=15)
        self._position = position
        self._spring_constant = spring_constant

    def update(self, axis, position=None):
        self._spring.axis = axis
        self._spring.pos = self._position if position is None else position

    def force(self):
        displacement = mag(self._spring.axis) - self._equilibrium_size
        return -self._spring_constant * displacement * norm(self._spring.axis)


class HarmonicOscillator:
    def __init__(self, position=vector(0, 0, 0), length=0.75, spring_constant=10.0, ball_radius=0.1, ball_mass=1.0, colour=color.red):
        left = position - length * vector(1, 0, 0)
        right = position + length * vector(1, 0, 0)
        self._position = position
        self._left_ball = Ball(mass=ball_mass, position=left, radius=ball_radius, color=colour)
        self._right_ball = Ball(mass=ball_mass, position=right, radius=ball_radius, color=colour)
        self._distance = self._left_ball.distance_to(self._right_ball)
        self._spring = Spring(position=position - self._distance / 2, axis=self._distance,spring_constant=spring_constant, radius=ball_radius / 2, thickness=0.3)

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


current_level = None
def on_mouse_click():
    global oscillator, energy_levels, current_level

    selected_level = scene.mouse.pick
    if selected_level in energy_levels:
        old_level = current_level
        current_level = selected_level
        current_level.color = color.red
        if old_level is not None:
            old_level.color = color.white
        amplitude = abs(current_level.pos.x)
        oscillator.reset()
        oscillator.compress_by(amplitude)
        vertical_line_left.pos = current_level.pos
        vertical_line_right.pos = current_level.pos + current_level.axis

    elif scene.mouse.project(normal=vec(0, 0, 1)).y > .5 * ks * 5.2 ** 2 + y_axis_pos:
        if current_level:
            current_level.color = color.white
        while oscillator.right_ball_position().x < 2 * L0:
            rate(200)
            # ball_2.position.x += L0 / 100
            oscillator.pull(L0 / 100)


scene.x = scene.y = 0
scene.width = scene.height = 600
scene.title = title
scene.bind("click", on_mouse_click)

equilibrium_position = cylinder(pos=vector(0, y_axis_pos, 0), axis=vector(0, 18, 0), radius=0.1, color=color.green)
well = curve(radius=0.2, pos=[vector(-5.8, 5.8 * 5.8 * .5 * ks + y_axis_pos, 0)])
for xx in arange(-5.8, 5.3, 0.1):
    well.append(pos=vector(xx, .5 * ks * xx ** 2 + y_axis_pos, 0))
well.append(pos=vector(8,.5 * ks * 5.2**2 + y_axis_pos, 0))

vertical_line_left = cylinder(pos=vector(-5, y_axis_pos, 0), axis=vector(0, 15, 0), radius=0.1, color=vector(.6, .6, .6), visible=show_vertical_lines)
vertical_line_right = cylinder(pos=vector(5, y_axis_pos, 0), axis=vector(0, 15, 0), radius=0.1, color=vector(.6, .6, .6), visibile=show_vertical_lines)

energy_levels = []
dU = 2
for Ux in arange(0.5 * dU, 7.51 * dU, dU):
    s = sqrt(2 * Ux / ks)
    e_level = cylinder(radius=0.2, pos=vector(-s, Ux + y_axis_pos, 0), axis=vector(2 * s, 0, 0), color=color.white)
    energy_levels.append(e_level)

oscillator = HarmonicOscillator(position=vec(0, 0.5 * 5 ** 2, 0), length=L0 / 2, spring_constant=ks, ball_radius=0.5, ball_mass=ball_mass)

t = 0.0
dt = 0.01
while 1:
    rate(1 / dt)
    if current_level:
        oscillator.update_by(dt)
        t += dt

