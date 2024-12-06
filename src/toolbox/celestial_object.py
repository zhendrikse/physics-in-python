from vpython import sphere, mag, norm, textures

G = 6.67e-11

class CelestialObject:
  
  def __init__(self, mass, position, velocity, radius, texture=textures.stucco):
    self._body = sphere(mass=mass, pos=position, v=velocity, radius=radius * 3, texture=texture, make_trail = True)
    
  def momentum(self):
    return self._body.mass * self._body.v

  def move_around(self, celestial_object, dt):
    distance = self._body.pos - celestial_object._body.pos
    force_magnitude =  -G * self._body.mass * celestial_object._body.mass / mag(distance)**2
    force_vector = force_magnitude * norm(distance)
    acceleration_vector = force_vector / self._body.mass
    
    self._body.v += acceleration_vector * dt
    self._body.pos += self._body.v * dt