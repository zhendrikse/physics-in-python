Web VPython 3.2
class Spring:
  def __init__(self, pos, axis, radius=0.20, thickness=0.05):
    self._spring = helix(pos=pos, axis=axis, radius=radius, thickness=thickness, color=color.yellow)
    self._size = mag(axis)
    
  def force(self):
    displacement = mag(self._spring.axis) - self._size
    return -1 * 2000 * displacement * norm(self._spring.axis)
  
  def update(self, delta, position=vector(0, 0, 0)):
    self._spring.axis += delta
    self._spring.pos += position
    
class Ball:
  def __init__(self, pos, color, mass=200):
    self._ball = sphere(mass=mass, pos=pos, velocity=vector(0, 0, 0), radius=0.30, color=color)
    
  def update(self, net_force, dt):
    self._ball.velocity += dt * net_force / self._ball.mass 
    self._ball.pos += self._ball.velocity * dt  
    
  def shift(self, delta):
    self._ball.pos += delta

class Oscillator:
  def __init__(self, number_of_balls=3):
    self._total_balls = number_of_balls
    ball_radius = 0.30
    spring_size = vector(2, 0, 0)
    total_size = mag(spring_size) * (self._total_balls + 1) + self._total_balls * ball_radius
    self._spring_size = mag(spring_size)
    
    left = vector(-total_size / 2, 0, 0)
    
    self._left_wall = box(pos=left, size=vector(2, 0.05, 2), color=color.green, up=vector(1, 0, 0))
    self._right_wall = box(pos=-left, size=vector(2, 0.05, 2), color=color.green, up=vector(1, 0, 0))
    
    self._springs = []
    for i in range(0, self._total_balls + 1):
      self._springs += [Spring(pos=left + i * spring_size + i * vector(ball_radius, 0, 0), axis=spring_size)]
    
    self._balls = []
    for i in range(1, self._total_balls + 1):
      self._balls += [Ball(pos=left + i * spring_size + (i - 0.5) * vector(ball_radius, 0, 0), color=vector(random(), random(), random()))]

  def ball_position(self, ball_index):
    return self._balls[ball_index]._ball.pos
    
  def shift_ball(self, ball_index, delta):
    self.update_ball_springs(ball_index, delta)
    self._balls[ball_index].shift(delta)
    
  def update(self, dt):
    for ball_i in range(0, self._total_balls):
      net_force = self._springs[ball_i].force() - self._springs[ball_i + 1].force()
      self._balls[ball_i].update(net_force, dt)
      self.update_ball_springs(ball_i, self._balls[ball_i]._ball.velocity * dt)  
    
  def update_ball(self, ball_index, dt):
    net_force = self._springs[ball_index].force() - self._springs[ball_index + 1].force()
    self._balls[ball_index].update(net_force, dt)
    self.update_ball_springs(ball_index, self._balls[ball_index]._ball.velocity * dt)  

  def update_ball_springs(self, ball_index, delta):
    self._springs[ball_index].update(delta)
    self._springs[ball_index + 1].update(-delta, delta) 
    

balls = 4
plot = graph(title=str(balls)+ "-body coupled oscillator",xtitle="Time",ytitle="Amplitude",width=500, height=250)
oscillator = Oscillator(balls)
curve = []
for ball_i in range(0, balls):
  curve += [gcurve(color=oscillator._balls[ball_i]._ball.color)]

# Initial displacement of balls
oscillator.shift_ball(0, vector(1, 0, 0))
#oscillator.shift_ball(1, vector(-.7, 0, 0))
#oscillator.shift_ball(2, vector(0.7, 0, 0))
#oscillator.shift_ball(3, vector(-.7, 0, 0))

dt = 0.001
for i in range(0, 10000):
  rate(1/dt)
  oscillator.update(dt)
  for ball_i in range(0, balls):
    curve[ball_i].plot(i * dt, oscillator.ball_position(ball_i).x - ball_i + balls / 2)