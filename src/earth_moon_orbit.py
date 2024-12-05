# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=2BisyQhNBFM

from vpython import vector, sphere, color, rate, mag, norm, graph, gcurve, textures, sqrt

g1 = graph(title="Earth moon",xtitle="t [s]",ytitle="Px [kg*m/s]",width=400, height=200)
fm = gcurve(color=color.blue)
fe = gcurve(color=color.red)
ft = gcurve(color=color.green)

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

mass_earth = 5.97e24
mass_moon = 7.37e22
earth_moon_distance = 384.4e6
velocity_moon = sqrt(G * mass_earth / earth_moon_distance) * vector(0, 1, 0)
velocity_earth = -mass_moon * velocity_moon / mass_earth

moon  = CelestialObject(mass_moon, vector(0, 0, 0), velocity_moon, 1.74e6)
earth = CelestialObject(mass_earth, vector(earth_moon_distance, 0, 0), velocity_earth, 6.3e6, textures.earth)

fifty_days = 50 * 24 * 60 * 60
dt = 500

def main():
  for day in range(0, fifty_days, dt):
    rate(1000)
    moon.move_around(earth, dt)
    earth.move_around(moon, dt)
  
    fm.plot(day, moon.momentum().y)
    fe.plot(day, earth.momentum().y)
    ft.plot(day, moon.momentum().y + earth.momentum().y)

if __name__=="__main__":
    main()
