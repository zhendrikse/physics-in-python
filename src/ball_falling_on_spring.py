# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=ExxDuRTIe0E
# - https://trinket.io/glowscript/58d3d4ba0b

from vpython import vector, sphere, color, rate, mag, norm, helix, box, graph, gcurve

g1 = graph(title="Ball on spring",xtitle="Time",ytitle="Height",width=400, height=250)
curve = gcurve(color=color.blue)

grav_force = vector(0, -9.8, 0)
zero_force = vector(0, 0, 0)

class Spring:
  def __init__(self, floor_position):
    self._spring_size = 0.4
    self._spring_constant = 1000
    self._spring = helix(pos=floor_position, axis=vector(0, self._spring_size, 0), radius=0.07, thickness=0.04)

  def _spring_is_compressed(self, distance_to_floor):
    return mag(distance_to_floor) < self._spring_size

  def update(self, distance_to_floor):
      if self._spring_is_compressed(distance_to_floor):
        self._spring.axis = distance_to_floor

  def force(self, distance_to_floor):
      if self._spring_is_compressed(distance_to_floor):
        compression = self._spring_size - mag(distance_to_floor)
        return self._spring_constant * compression * norm(distance_to_floor)

      return zero_force

class Ball:
  def __init__(self):
    self._mass = 1.5
    self._ball = sphere(pos=vector(0, 2, 0), radius=0.1, color=color.yellow)
    self._ball.v = vector(0, 0, 0)

  def update(self, spring_force, dt):
      force = self._mass * grav_force + spring_force
      acceleration = force / self._mass
      self._ball.v += acceleration * dt
      self._ball.pos += self._ball.v * dt

  def position(self):
    return self._ball.pos


floor_position = vector(0, -0.4, 0)
floor = box(pos=floor_position, size=vector(2, 0.05, 1))
ball = Ball()
spring = Spring(floor_position)

def main():
  dt = 0.01
  for i in range(0, 300):
    rate(100)
    ball.update(spring.force(ball.position() - floor_position), dt)
    spring.update(ball.position() - floor_position)
    curve.plot(i * dt, ball.position().y)


if __name__=="__main__":
    main()

