from vpython import vector, sphere, color, mag, norm

zero_force = vector(0, 0, 0)

class Ball:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow, elasticity=1.0, make_trail=False):
    self._ball = sphere(pos=position, radius=radius, color=color, velocity=velocity, mass=mass, elasticity=elasticity, make_trail=make_trail)

  def move(self, force__vector=vector(0, 0, 0), dt=0.01):
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
    
  def has_collided_with(self, other_ball):
    return mag(self.distance_to(other_ball)) < (self.radius + other_ball.radius)
    
  def rotate(self, angle, origin=vector(0, 0, 0), axis=vector(0, 1, 0)):
    self._ball.rotate(origin=origin, axis=axis, angle=angle)

  def is_on_ground(self):
    return self.position.y - self.radius <= 0.5
  
  def bounce_from_ground(self, dt):
    self._ball.velocity.y *= - self.elasticity
    self._ball.pos += self._ball.velocity * dt

    # if the velocity is too slow, stay on the ground
    if self._ball.velocity.y <= 0.1:
        self._ball.pos.y = self.radius + self.radius / 10

  def hits_building(self, building):
      building_frontside = building.position.x + building.L
      building_backside = building.position.x - building.L
      return self.position.x <= (building_frontside - self.radius) and self.position.x <= 0 and self.position.y <= building.H and self.position.x >= (building_backside + self.radius) and building._building.up == vector(0, 1, 0) 

  def collide_with(self, building):
    # set new velocity in x-direction after collision with building
    self._ball.velocity.x = (self.mass * self.velocity.x + building.mass * building.velocity.x + self.elasticity * building.mass * (building.velocity.x - self.velocity.x))/(self.mass + building.mass)
  
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
  
  @property
  def elasticity(self):
     return self._ball.elasticity