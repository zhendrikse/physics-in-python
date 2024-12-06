from vpython import sphere, mag, norm, textures

G = 6.67e-11

class CelestialObject:

  def __init__(self, mass, position, velocity, radius, texture=textures.stucco):
    self._body = sphere(pos=position, radius=radius * 3, texture=texture, make_trail = True)
    self._mass = mass
    self._velocity = velocity

  def momentum(self):
    return self._mass * self._velocity

  def move_around(self, celestial_object, dt):
    distance = self._body.pos - celestial_object._body.pos
    force = -G * self._mass * celestial_object._mass * norm(distance) / mag(distance)**2
    acceleration = force / self._mass

    self._velocity += acceleration * dt
    self._body.pos += self._velocity * dt