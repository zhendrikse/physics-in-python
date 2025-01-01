#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=_ZopJ_qAF_s
# - https://trinket.io/glowscript/dca4e41cfa10
#

from vpython import vector, random, color, pi, mag, norm, arrow, rate
from ..toolbox.celestial_object import G, Earth, Moon, EARTH_MOON_DISTANCE, MOON_MASS, EARTH_RADIUS

scale = 1e12
moon_position_vector = vector(EARTH_MOON_DISTANCE, 0, 0)
moon = Moon(position=moon_position_vector * 0.05)
earth = Earth(position=moon_position_vector * -0.05, shininess=0)

def gravitational_force(radius):
  return -G * MOON_MASS * norm(radius) / mag(radius)**2

#
# The fake gravitational force to make the earth "behave"
# like an intertial frame. You may want to remember that 
# the earth is also moving in its orbit!
#
FAKE_FORCE = gravitational_force(moon_position_vector)
n = 0
N = 500
dR = 500
while n < N:
  rt = EARTH_RADIUS * vector(2 * random() - 1, 2 * random() - 1, 2 * random() - 1)
  if mag(rt) < (EARTH_RADIUS + dR) and mag(rt) > (EARTH_RADIUS - dR):
    r = rt - moon_position_vector
    gravitational_force_moon = gravitational_force(r)
    arrow(pos=rt - moon_position_vector * 0.05, axis=scale * (gravitational_force_moon + FAKE_FORCE), color=color.yellow)
    n += 1

n = 0
while n < N:
  rate(50)
  earth.rotate(2 * pi / 500, origin=moon_position_vector * -0.05)
  n += 1