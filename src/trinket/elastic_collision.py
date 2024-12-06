# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=g_p-5YfUSnw&t=11s 
# - https://trinket.io/glowscript/c71888ae4a

from vpython import vector, color, rate, sphere, mag, norm

zero_force = vector(0, 0, 0)

class Sphere:
  def __init__(self, mass, position, velocity, radius, color, make_trail=True):
     self._sphere = sphere(mass=mass, pos=position, v=velocity, radius=radius, color=color, make_trail=True)
     self._sphere.p = self._sphere.mass * velocity

  def _distance_to(self, other):
     return other._sphere.pos - self._sphere.pos
    
  def has_collided_with(self, other):
    return mag(self._distance_to(other)) < (self._sphere.radius + other._sphere.radius)
  
  def update_position_and_momentum(self, force, dt):
    self._sphere.p += force * dt
    self._sphere.pos += self._sphere.p * dt / self._sphere.mass

  def momentum(self):
     return self._sphere.p
  
  def kinetic_energy(self):
     return mag(self.momentum())**2 / (2* self._sphere.mass)
  
  def force_between(self, other):
      k = 101
      r = self._distance_to(other)
      return k * (mag(r) - (self._sphere.radius + other._sphere.radius)) * norm(r)
      
sphere_A = Sphere(0.1, vector(-.2, .02 ,0), vector(.2, 0 ,0), 0.05, color.yellow)
sphere_B = Sphere(0.1, vector( .2, .0,  0), vector(0,  0 ,0), 0.05, color.cyan)

print("initial momentum = " + str(sphere_A.momentum() + sphere_B.momentum()) + " kg*m/s")
print("initial K = " + str(sphere_A.kinetic_energy() + sphere_B.kinetic_energy()) + " Joules")

dt = 0.01
for timestep in range(0, 350):
  rate(100)
  force_BA = zero_force
  
  if sphere_A.has_collided_with(sphere_B):
    force_BA = sphere_A.force_between(sphere_B)

  sphere_A.update_position_and_momentum(force_BA, dt)
  sphere_B.update_position_and_momentum(-force_BA, dt)

print("final momentum = " + str(sphere_A.momentum() + sphere_B.momentum()) + " kg*m/s")
print("final K = " + str(sphere_A.kinetic_energy() + sphere_B.kinetic_energy()) + " Joules")
