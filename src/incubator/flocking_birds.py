# Flock of Birds
# B. Philhour 10/9/17
# inspired by Gary Flake's "Computational Beauty of Nature"
# 1998 MIT Press ISBN-13 978-0-262-56127-3
# https://www.amazon.com/Computational-Beauty-Nature-Explorations-Adaptation/dp/0262561271

from vpython import scene, color, arrow, vector, vec, slider, button, rate, random

N = 250
bird = []
scene.height = 350
scene.background = color.white

spread = 3   # initial physical radius of entire flock
speed = 6   # initial horizontal speed
size = 1   # length of bird vector
fov = 10   # field of view in degrees

# class Bird:
#   def __init__(self):
#     self._bird = arrow(pos=spread * vector.random(), axis=size * bi)
#     self._acceleration = vec(0, 0, 0)
#     self._axis

for i in range(N):
  bird[i] = arrow()
  bird[i].pos = spread * vector.random()
  bird[i].vel = vec (speed, 0, 0) + speed * vector.random()
  bird[i].acc = vec(0,0,0)
  bird[i].axis = size * bird[i].vel.norm()
  bird[i].color = color.black

# initial weights of different behaviors
randomWeight = 0.1
centerWeight = 0.1
directionWeight = 0.05
avoidWeight = 0.5

# set up some slider interaction
def randomBird():
  nonlocal randomWeight
  randomWeight = randomSlider.value

scene.append_to_caption("\nRandom behavior\n")
randomSlider = slider(bind = randomBird, value = randomWeight, min = 0.0, max = 50.0)

def centerBird():
  nonlocal centerWeight
  centerWeight = centerSlider.value

scene.append_to_caption("\n\nCentering behavior\n")
centerSlider = slider(bind = centerBird, value = centerWeight, min = 0.0, max = 2.0)

def directionBird():
  nonlocal directionWeight
  directionWeight = directionSlider.value

scene.append_to_caption("\n\nDirection behavior\n")
directionSlider = slider(bind = directionBird, value = directionWeight, min = 0.0, max = 2.0)

def avoidBird():
  nonlocal avoidWeight
  avoidWeight = avoidSlider.value

scene.append_to_caption("\n\nAvoidance behavior\n")
avoidSlider = slider(bind = avoidBird, value = avoidWeight, min = 0.0, max = 2.0)

# make a button for startling the birds
def startle():
    nonlocal bird, N
    for i in range(N):
      bird[i].vel = 2 * speed * vector.random()

scene.append_to_caption('\n\n')
button( bind=startle, text='Startle' )

# set up the time step interval
dt = 0.01

while (True):

  rate(1/dt)   # approximate real time if possible

  # compute average position and direction
  center = vec(0,0,0)
  direction = vec(0,0,0)
  for i in range(N):
    center = center + bird[i].pos
    direction = direction + bird[i].vel
  center = center/N
  direction = direction/N

  avoid = []
  # avoid nearest birds (A BETTER VERSION WOULD ANTICIPATE COLLISIONS)
  for i in range(N):
    avoid[i] = vec(0,0,0)
    for j in range(N):
      avoid[j] = vec(0,0,0)
      if i == j: continue
      separationDist = bird[i].pos - bird[j].pos
      if separationDist.mag < 5 * size:
        avoid[i] = avoid[i] - (bird[j].pos - bird[i].pos) / separationDist.mag2
        avoid[j] = avoid[j] - (bird[i].pos - bird[j].pos) / separationDist.mag2

  for i in range(N):

    # figure out changes to the bird's motion
    bird[i].acc = randomWeight * vector.random()
    bird[i].acc = bird[i].acc + centerWeight * (center - bird[i].pos)
    bird[i].acc = bird[i].acc + directionWeight * (direction - bird[i].vel)
    bird[i].acc = bird[i].acc + avoidWeight * (avoid[i].norm() - bird[i].pos)

    # do kinematics
    bird[i].vel = bird[i].vel + bird[i].acc * dt
    bird[i].pos = bird[i].pos + bird[i].vel * dt

    # repoint the bird's arrow
    bird[i].axis = size * bird[i].vel.norm()

  # scene.center = center