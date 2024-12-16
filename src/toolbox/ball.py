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
    
  def has_collided_with(self, other):
    return mag(self.distance_to(other)) < (self.radius + other.radius)
    
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
        self.velocity.y = 0

  def hits_building(self, building):
      building_frontside = building.position().x + building.length()
      building_backside = building.position().x - building.length()
      return self._ball.pos.x <= (building_frontside - self._ball.radius) and self._ball.pos.x <= 0 and self._ball.pos.y <= building.height() and self._ball.pos.x >= (building_backside + self._ball.radius) and building._building.up == vector(0, 1, 0) 

  def _collision_with(self, building):
      momentum_ball = self._ball.mass * self.velocity.x
      momentum_building = building.mass() * building.velocity().x
      velocity_difference = building.velocity().x - self.velocity.x
      total_momentum = momentum_ball + momentum_building
      total_mass = self._ball.mass + building.mass()
      speed_ball = (total_momentum + self._ball.elasticity * building.mass() * velocity_difference) / total_mass
      speed_building = (total_momentum - self._ball.elasticity * self._ball.mass * velocity_difference) / total_mass
      return speed_ball, speed_building

  def collides_with_building(self, building, dt):
      velocity_ball, velocity_building = self._collision_with(building)

      # motion of ball
      self._ball.velocity.x = velocity_ball
      self.move(dt=dt)

      # motion of block
      angular_velocity = velocity_building / (self._ball.pos.y - 0.5)
      building._building.w = angular_velocity
      dtheta = -building._building.w * dt
      building.rotate(origin=vector(-110, 0, 0), axis=vector(0, 0, 1), angle=dtheta)        
  
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