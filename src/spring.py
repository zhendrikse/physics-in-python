from vpython import vector,  mag, norm, helix

zero_force = vector(0, 0, 0)

class Spring:
  def __init__(self):
    self._spring_size = 0.4
    self._spring_constant = 1000
    self._spring = helix(pos=vector(0, 0, 0), axis=vector(0, self._spring_size, 0), radius=0.07, thickness=0.04)

  def _spring_is_compressed(self, ball_position):
    return mag(ball_position) < self._spring_size
    
  def update(self, ball_position):
      if self._spring_is_compressed(ball_position):
        self._spring.axis = ball_position

  def force(self, ball_position):
      if self._spring_is_compressed(ball_position):
        compression = self._spring_size - mag(ball_position)
        return self._spring_constant * compression * norm(ball_position)
      
      return zero_force
