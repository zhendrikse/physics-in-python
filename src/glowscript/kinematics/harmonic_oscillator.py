#Web VPython 3.2

from vpython import vector, sphere, color, rate, mag, norm, scene, gcurve, graph, helix, arange


title = """Basic harmonic oscillator

&#x2022; Written by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> 
&#x2022; The code resides in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

&lt;mouse click&gt; &rarr; start the animation for a limited time interval

"""


class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow,
               make_trail=False):
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
  def __init__(self, position=vector(0, 0, 0), axis=vector(1.0, 0, 0), spring_constant=10.0, radius=0.5,
               thickness=0.03):
    self._equilibrium_size = mag(axis)
    self._spring = helix(pos=position, axis=axis, radius=radius, thickness=thickness, spring_constant=spring_constant,
                         coils=15)
    self._position = position
    self._spring_constant = spring_constant

  def update(self, axis, position=None):
    self._spring.axis = axis
    self._spring.pos = self._position if position is None else position

  def force(self):
    displacement = mag(self._spring.axis) - self._equilibrium_size
    return -self._spring_constant * displacement * norm(self._spring.axis)


class Oscillator:
  def __init__(self, position=vector(0, 0, 0), length=0.75, spring_constant=10.0, ball_radius=0.1, ball_mass=1.0,
               colour=color.red):
    left = position - length * vector(1, 0, 0)
    right = position + length * vector(1, 0, 0)
    self._position = position
    self._left_ball = Ball(mass=ball_mass, position=left, radius=ball_radius, color=colour)
    self._right_ball = Ball(mass=ball_mass, position=right, radius=ball_radius, color=colour)
    self._distance = self._left_ball.distance_to(self._right_ball)
    self._spring = Spring(position=position - self._distance / 2, axis=self._distance, spring_constant=spring_constant,
                          radius=0.6 * ball_radius)

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


position_plot = graph(title="Ball on spring", xtitle="Time", ytitle="Amplitude", width=400, height=250)
curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)

oscillator = Oscillator()
oscillator.compress_by(0.75)

scene.title = title

t = 0
dt = 0.01
while True:
  scene.waitfor("click")
  for i in arange(0, 10 / dt):
    t += dt
    rate(1 / dt)
    oscillator.update_by(dt)
    curve_left.plot(t, oscillator.left_ball_position().x)
    curve_right.plot(t, oscillator.right_ball_position().x)

