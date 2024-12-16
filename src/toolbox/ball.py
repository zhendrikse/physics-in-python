from vpython import vector, sphere, color, mag, norm

zero_force = vector(0, 0, 0)

class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow, elasticity=1.0, make_trail=False):
    self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass, elasticity=elasticity, make_trail=make_trail)

  def move(self, force__vector, dt):
      acceleration_vector = force__vector / self._ball.mass
      self._ball.velocity += acceleration_vector * dt
      self._ball.pos += self._ball.velocity * dt
  
  def force_between(self, other_ball):
      if not self.has_collided_with(other_ball):
         return zero_force
      
      k = 101
      r = self.distance_to(other_ball)
      return k * (mag(r) - (self.radius + other_ball.radius)) * norm(r)
  
  def distance_to(self, other):
     return other.position - self.position
    
  def has_collided_with(self, other):
    return mag(self.distance_to(other)) < (self._ball.radius + other._ball.radius)
    
  def rotate(self, angle, origin=vector(0, 0, 0), axis=vector(0, 1, 0)):
    self._ball.rotate(origin=origin, axis=axis, angle=angle)

  def is_on_ground(self):
      return self.position.y - self.radius <= 0
  
  def bounce_from_ground(self, dt):
    self.velocity.y *= - self._ball.elasticity
    self._ball.pos += self._ball.velocity * dt

    # if the velocity is too slow, stay on the ground
    if self._ball.velocity.y <= 0.1:
        self.position.y = self.radius 
  
  @property
  def momentum(self):
     return self.velocity * self.mass
  
  @property
  def kinetic_energy(self):
     return mag(self.momentum) * mag(self.momentum) / (2 * self.mass)
  
  @property
  def position(self):
    return self._ball.pos
  
  @property
  def velocity(self):
    return self._ball.velocity
  
  @property
  def mass(self):
     return self._ball.mass
  
  @property
  def radius(self):
     return self._ball.radius