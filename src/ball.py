from vpython import vector, sphere, color, mag, norm

gravitational_force = vector(0, -9.8, 0)
zero_force = vector(0, 0, 0)

class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow):
    self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass)

  def update(self, dt, spring_force=zero_force, has_gravitational_force=False):
      net_force = gravitational_force * self._ball.mass if has_gravitational_force else zero_force
      net_force += spring_force
      
      acceleration = net_force / self._ball.mass
      self._ball.velocity += acceleration * dt
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
  
  def momentum(self):
     return self._ball.velocity * self._ball.mass
  
  def kinetic_energy(self):
     return mag(self.momentum())**2 / (2* self._ball.mass)
  
  def position(self):
    return self._ball.pos