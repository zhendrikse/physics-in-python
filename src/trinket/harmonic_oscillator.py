from vpython import vector, sphere, color, rate, mag, norm, box, gcurve, graph, helix

class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow, make_trail=False):
    self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass, make_trail=make_trail)

  def move(self, force__vector, dt):
      acceleration_vector = force__vector / self._ball.mass
      self._ball.velocity += acceleration_vector * dt
      self._ball.pos += self._ball.velocity * dt

  def distance_to(self, other):
     return other.position() - self.position()
     
  def position(self):
    return self._ball.pos

class Spring:  
  def __init__(self, position=vector(0, 0, 0), axis=vector(1.0, 0, 0), spring_constant=1, equilibrium_size=1.0, radius=0.5, thickness=0.03):
    self._equilibrium_size = equilibrium_size
    self._spring = helix(pos=position, axis=axis, radius=radius, thickness=thickness, spring_constant=spring_constant)
    self._position = position

  def update(self, axis, position=None):
    self._spring.axis = axis
    self._spring.pos = self._position if position is None else position
  
  def force(self):
    displacement = mag(self._spring.axis) - self._equilibrium_size
    return -self._spring.spring_constant * displacement * norm(self._spring.axis)


position_plot = graph(title="Ball on spring", xtitle="Time", ytitle="Amplitude", width=400, height=250)
curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)

left_ball  = Ball(mass=1.0, position=vector(-0.75, 0, 0), radius=0.1, color=color.red)
right_ball = Ball(mass=1.0, position=vector( 0.75, 0, 0), radius=0.1, color=color.blue)
distance = left_ball.distance_to(right_ball)
spring = Spring(position=-distance / 2, axis=distance, spring_constant=1.0, equilibrium_size=1.0, radius=0.05)

def main():
  dt = 0.1
  for t in range(0, 200):
    rate(2/dt)
    right_ball.move(spring.force(), dt)
    left_ball.move(-spring.force(), dt)
    distance = left_ball.distance_to(right_ball)
    spring.update(distance, -distance / 2)
    curve_left.plot(t * dt, left_ball.position().x)
    curve_right.plot(t * dt, right_ball.position().x)

  
if __name__=="__main__":
    main()

  
  