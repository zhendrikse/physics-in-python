#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=4UIabjGb1qI&t=553s
# - https://trinket.io/glowscript/f56c5e1ba2d6
#

from vpython import vector, rate, color, pi, mag, norm, cross
from toolbox.celestial_object import G, Eros, EROS_RADIUS, EROS_MASS
from toolbox.ball import Ball

T = 5 # hours
omega = 2 * pi / (T * 60 * 60)
dt = 1


position_vector = vector(-EROS_RADIUS, 0,0 )
velocity_vector = vector(-3, 3, 3)
ball_mass = 1
rotation_axis = vector(0, 1, 0)

eros = Eros()
ball = Ball(ball_mass, position=position_vector, velocity=velocity_vector, radius=EROS_RADIUS / 20,color=color.yellow, make_trail=True)

t = 0
while mag(ball.position) >= EROS_RADIUS:
  rate(1000)
  r = eros.distance_to(ball)
  W = omega * rotation_axis
  force = -G * EROS_MASS * ball_mass * norm(r) / mag(r)**2 + ball_mass * cross(cross(W, r), W) - 2 * cross(W, ball.momentum)  
  ball.move(force, dt)
  t += dt

velocity_vector += cross(W, position_vector)
ball_2 = Ball(ball_mass, position=position_vector, velocity=velocity_vector, radius=EROS_RADIUS / 20,color=color.magenta, make_trail=True)

t = 0
while mag(ball_2.position) >= EROS_RADIUS:
  rate(1000)
  r2 = eros.distance_to(ball_2)
  force = -G * EROS_MASS * ball_mass * norm(r2) / mag(r2)**2
  ball_2.move(force, dt)
  eros.rotate(angle = omega * dt)
  ball.rotate(angle = omega * dt)
  t += dt