# Kepler's Laws.py

# plots the orbit of a planet in an eccentric orbit to illustrate
# the sweeping out of equal areas in equal times, with sun at focus
# The eccentricity of the orbit is random and determined by the initial velocity
# program uses normalised units (G =1)

# program by Peter Borcherds, University of Birmingham, England
# Updated by Zeger Hendrikse: https://github.com/zhendrikse/physics-in-python

from vpython import *
from random import random

max_steps = 20

def radial_vector_color(time, offset=max_steps, whole=True):  # mark the end of each "month"
    global colour  # have to make it global, since label uses it before it is updated
    if whole:
        label_text = str(int(time * 2 + dt))  # end of 'month', printing twice time gives about 12 'months' in 'year'
    else:
        label_text = duration + str(round(time * 2, 2)) + ' "months"\n Initial speed: ' + str(round(speed, 3))
        ccolor = color.white
    label(pos=planet.pos, text=label_text, color=ccolor,
          xoffset=offset * planet.pos.x, yoffset=offset * planet.pos.y)
    ccolor = vector(0.5 * (1 + random()), random(), random())  # randomise colour of radial vector
    return ccolor


scene = canvas(title="Kepler's law of equal areas", width=1000, height=1000, range=3.2)
duration = 'Period: '
sun = sphere(color=color.yellow, radius=0.1)  # motion of sun is ignored (or centre of mass coordinates)
scale = 1.0
poss = vector(0, scale, 0)
planet = sphere(pos=poss, color=color.cyan, radius=0.05)

while 1:
    velocity = -vector(0.7 + 0.5 * random(), 0, 0)  # gives a satisfactory range of eccentricities
    ##velocity = -vector(0.984,0,0)   # gives period of 12.0 "months"
    speed = mag(velocity)
    dt = 0.5 / float(max_steps)
    step = 0
    time = 0
    colour = color.white
    old_position = vector(planet.pos)
    colour = radial_vector_color(time)
    curve(pos=[sun.pos, planet.pos], color=colour)

    while not (old_position.x > 0 > planet.pos.x):

        rate(max_steps * 2)  # keep rate down so that development of orbit can be followed
        time += dt
        old_position = vector(planet.pos)  # construction vector(planet.pos) makes oldpos a variable in its own right
        # old_position = planet.pos makes "oldposs" point to "planet.pos"
        # oldposs = planet.pos[:] does not work, because vector does not permit slicing
        denominator = mag(planet.pos) ** 3
        velocity -= planet.pos * dt / denominator  # inverse square law; force points toward sun
        planet.pos += velocity * dt

        # plot orbit
        curve(pos=[old_position, planet.pos], color=color.red)

        step += 1
        if step == max_steps:
            step = 0
            colour = radial_vector_color(time)
            curve(pos=[sun.pos, planet.pos], color=color.white)
        else:
            # plot radius vector
            curve(pos=[sun.pos, planet.pos], color=colour)

        # if scene.kb.keys:
        #     print
        #     "key pressed"
        #     duration = 'Duration: '
        #     break

    radial_vector_color(time, 50, whole=False)
    label(pos=vector(2.5, -2.5, 0), text='Click for another orbit')
    _ = scene.waitfor('click')

    for obj in scene.objects:
        if obj is sun or obj is planet: continue
        obj.visible = 0  # clear the screen to do it again
