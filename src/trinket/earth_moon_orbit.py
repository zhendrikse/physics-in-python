# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=2BisyQhNBFM

from vpython import sphere, vector, color, rate, graph, gcurve, textures, sqrt, mag, norm

plot = graph(title="Earth moon",xtitle="t [s]",ytitle="Px [kg*m/s]",width=400, height=200)
moon_curve = gcurve(color=color.blue)
earth_curve = gcurve(color=color.red)
sum_curve = gcurve(color=color.green)

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

mass_earth = 5.97e24
mass_moon = 7.37e22
earth_moon_distance = 384.4e6
velocity_moon = sqrt(G * mass_earth / earth_moon_distance) * vector(0, 1, 0)
velocity_earth = -mass_moon * velocity_moon / mass_earth

moon  = CelestialObject(mass_moon, vector(0, 0, 0), velocity_moon, 1.74e6)
earth = CelestialObject(mass_earth, vector(earth_moon_distance, 0, 0), velocity_earth, 6.3e6, textures.earth)

fifty_days = 50 * 24 * 60 * 60
dt = 500
for day in range(0, fifty_days, dt):
  rate(1000)
  moon.move_around(earth, dt)
  earth.move_around(moon, dt)
  
  moon_curve.plot(day, moon.momentum().y)
  earth_curve.plot(day, earth.momentum().y)
  sum_curve.plot(day, moon.momentum().y + earth.momentum().y)
