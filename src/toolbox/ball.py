from vpython import vector, sphere, color, mag, norm

#gravitational_force = vector(0, -9.8, 0)
zero_force = vector(0, 0, 0)

class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow, make_trail=False):
    self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass, make_trail=make_trail)

  def move(self, force__vector, dt):
      acceleration_vector = force__vector / self._ball.mass
      self._ball.velocity += acceleration_vector * dt
      self._ball.pos += self._ball.velocity * dt
  
  def force_between(self, other_ball):
      if not self.has_collided_with(other_ball):
         return zero_force
      
      k = 101
      r = self.distance_to(other_ball)
      return k * (mag(r) - (self._ball.radius + other_ball._ball.radius)) * norm(r)
  
  def distance_to(self, other):
     return other._ball.pos - self._ball.pos
    
  def has_collided_with(self, other):
    return mag(self.distance_to(other)) < (self._ball.radius + other._ball.radius)
    
  def rotate(self, angle, origin=vector(0, 0, 0), axis=vector(0, 1, 0)):
    self._ball.rotate(origin=origin, axis=axis, angle=angle)

  @property
  def momentum(self):
     return self._ball.velocity * self._ball.mass
  
  @property
  def kinetic_energy(self):
     return mag(self.momentum)**2 / (2 * self._ball.mass)
  
  @property
  def position(self):
    return self._ball.pos
  
  @property
  def mass(self):
     return self._ball.mass