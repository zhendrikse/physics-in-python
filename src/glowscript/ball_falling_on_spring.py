# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=ExxDuRTIe0E
# - https://trinket.io/glowscript/58d3d4ba0b

from vpython import sphere, vector, color, rate, graph, gcurve, box, mag, norm, helix

plot = graph(title="Ball on spring",xtitle="Time",ytitle="Height",width=400, height=250)
curve = gcurve(color=color.blue)

grav_force = vector(0, -9.8, 0)
zero_force = vector(0, 0, 0)

class Spring:
  def __init__(self):
    self._spring_size = 0.4
    self._spring_constant = 1000
    self._spring = helix(pos=vector(0, 0, 0), axis=vector(0, self._spring_size, 0), radius=0.07, thickness=0.04)

  def _spring_is_compressed(self, ball_position):
    return mag(ball_position) < self._spring_size
    
  def update(self, ball_position):
      if self._spring_is_compressed(ball_position):
        self._spring.axis = ball_position

  def force(self, ball_position):
      if self._spring_is_compressed(ball_position):
        compression = self._spring_size - mag(ball_position)
        return self._spring_constant * compression * norm(ball_position)
      
      return zero_force

class Ball:
  def __init__(self, mass = 1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow):
    self._ball = sphere(mass=mass, pos=position, radius=radius, color=color, velocity=velocity)

  def update(self, spring_force, dt):
      force_vector = self._ball.mass * grav_force + spring_force
      acceleration_vector = force_vector / self._ball.mass
      self._ball.velocity += acceleration_vector * dt
      self._ball.pos += self._ball.velocity * dt

  def position(self):
    return self._ball.pos

floor = box(pos=vector(0, 0, 0), size=vector(2, 0.05, 1))
ball = Ball(position=vector(0, 2.4, 0))
spring = Spring()

def main():
  dt = 0.01
  for i in range(0, 500):
    rate(100)
    ball.update(spring.force(ball.position()), dt)
    spring.update(ball.position())
    curve.plot(i * dt, ball.position().y)

if __name__=="__main__":
    main()

