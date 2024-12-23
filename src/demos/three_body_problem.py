#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=Ye2wIV8-SB8
# - https://trinket.io/glowscript/9ece3648f0
#

from vpython import sphere, vector, color, rate, sqrt, mag, norm
from ..toolbox.celestial_object import CelestialObject, G

astronomical_unit = 1.49e11
mass = 1e30
rA = 0.1 * astronomical_unit
rB = rA * 1 / 0.8
vA = sqrt(G * 0.8 * mass * rA) / (rA + rB)

sphere_A = CelestialObject(mass, vector(rA, 0, 0), vector(0, vA, 0), 190e7)
sphere_B = CelestialObject(mass * 0.8, vector(-rB, 0, 0), vector(0, -vA / 0.8, 0), 190e7, color.cyan)
sphere_C = CelestialObject(mass * 0.5, vector(0, 0, rA), vector(0, 0, 0),  190e7, color.magenta)

for t in range(0, 1500 * 5000, 5000):
  rate(100)
  
  force_BA = sphere_A.force_between(sphere_B)
  force_CB = sphere_B.force_between(sphere_C)
  force_AC = sphere_C.force_between(sphere_A)

  sphere_A.move(+force_BA - force_AC, dt = 5000)
  sphere_B.move(-force_BA + force_CB, dt = 5000)
  sphere_C.move(-force_CB + force_AC, dt = 5000)