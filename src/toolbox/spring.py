from vpython import vector,  mag, norm, helix

zero_force = vector(0, 0, 0)

class Spring:  
  def __init__(self, position=vector(0, 0, 0), axis=vector(1.0, 0, 0), spring_constant=1, equilibrium_size=1.0, radius=0.5, thickness=0.03):
    self._equilibrium_size = equilibrium_size
    self._spring = helix(pos=position, axis=axis, radius=radius, thickness=thickness, spring_constant=spring_constant)
    self._position = position

  def is_stretched_or_compressed(self):
    return not mag(self._spring.axis) == self._equilibrium_size
    
  def update(self, axis, position=None):
    self._spring.axis = axis
    self._spring.pos = self._position if position is None else position
  
  @property
  def force(self):
      if self.is_stretched_or_compressed():
        displacement = mag(self._spring.axis) - self._equilibrium_size
        return -self._spring.spring_constant * displacement * norm(self._spring.axis)
      
      return zero_force

