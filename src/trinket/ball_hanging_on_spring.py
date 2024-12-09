from vpython import vector, sphere, color, rate, mag, norm, box, gcurve, graph, helix

class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow, make_trail=False):
    self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass, make_trail=make_trail)

  def move(self, force__vector, dt):
      acceleration_vector = force__vector / self._ball.mass
      self._ball.velocity += acceleration_vector * dt
      self._ball.pos += self._ball.velocity * dt

  def position(self):
    return self._ball.pos
  
  def mass(self):
    return self._ball.mass
    
class Spring:  
  def __init__(self, position=vector(0, 0, 0), axis=vector(1.0, 0, 0), spring_constant=1, equilibrium_size=1.0, radius=0.5, thickness=0.03):
    self._equilibrium_size = equilibrium_size
    self._spring = helix(pos=position, axis=axis, radius=radius, thickness=thickness, spring_constant=spring_constant)

  def update(self, axis):
    self._spring.axis = axis

  def force(self):
      displacement = mag(self._spring.axis) - self._equilibrium_size
      return -self._spring.spring_constant * displacement * norm(self._spring.axis)
      

position_plot = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.blue)

spring_size = 1.0
spring_rest_position = vector(0, 0, 0)

ceiling = box(pos=vector(0, 0, 0), size=vector(2, 0.05, 1), color=color.green)
ball = Ball(mass=5.0, position=vector(0, -spring_size - 0.5, 0), color=color.red)
spring = Spring(axis=ball.position(), spring_constant=1000, equilibrium_size=spring_size, radius=0.07)#, thickness=0.04)

gravitational_force = vector(0, -9.8 * ball.mass(), 0)

def main():
  dt = 0.01
  for i in range(0, 500):
    rate(1 / (2 * dt))
    ball.move(spring.force() + gravitational_force, dt)
    spring.update(ball.position())

    curve.plot(i * dt, ball.position().y)


if __name__=="__main__":
    main()
