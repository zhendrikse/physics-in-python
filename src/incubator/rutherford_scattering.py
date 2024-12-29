from vpython import *
from random import uniform

title="""
Ruth Chabay Spring 2000
Disk source of alpha particles which scatter off gold nucleus.
Gold nucleus is repositioned after each event.
"""


##scene.stereo = 'redcyan'
##scene.stereodepth = 1

def beam():
    while 1:
        yy = uniform(-R, R)
        zz = uniform(-R, R)
        if yy * yy + zz * zz <= R * R:
            return vector(-xMax * 1.5, yy, zz)


scene.x = scene.y = 0
scene.height = 800
scene.width = 800
scene.background = color.white
scene.lights = [(1, 0, 1)]

R = 6e-14

xMax = 1e-13
dt = 5e-23
k = 9e9
K0 = 10e6 * 1.6e-19
scene.autoscale = 0
scene.range = (xMax * 2.5, xMax * 2.5, xMax * 2.5)

gold = sphere(radius=6e-15, color=color.yellow)
gold.mass = 197e-3 / 6.02e23
gold.charge = 79 * 1.6e-19
gold.momentum = vector(0, 0, 0)

src = cylinder(pos=vector(-xMax * 2.0, 0, 0), axis=vector(-R * 0.1, 0, 0), radius=R, color=(.7, .7, .7))

trails = []

for nalpha in range(1000):
    alpha = sphere(pos=beam(), radius=4e-15, color=(.2, 1., 1.))
    alpha.spot = cylinder(pos=vector(src.pos.x, alpha.pos.y, alpha.pos.z), radius=2e-15, axis=vector(1e-15, 0, 0),
                          color=alpha.color)
    alpha.mass = 4e-3 / 6.12e23
    alpha.charge = 2 * 1.6e-19
    alpha.momentum = vector(sqrt(2 * alpha.mass * K0), 0, 0)

    trail = curve(color=alpha.color, pos=[(alpha.spot.pos)])

    gold.pos = vector(0, 0, 0)  ## reposition Au nucleus
    gold.momentum = vector(0, 0, 0)

    while mag(alpha.pos) < 1.8e-13:
        r = alpha.pos - gold.pos
        F = k * alpha.charge * gold.charge * r / (mag(r) ** 3)
        alpha.momentum = alpha.momentum + F * dt
        gold.momentum = gold.momentum - F * dt
        alpha.pos = alpha.pos + (alpha.momentum / alpha.mass) * dt
        gold.pos = gold.pos + (gold.momentum / gold.mass) * dt
        trail.append(pos=alpha.pos)

    if alpha.momentum.x / mag(alpha.momentum) <= cos(pi / 2):
        alpha.color = color.red
        trail.color = array(alpha.color) / 1.5
        ##        alpha.spot.color = array(alpha.color)/1.5
        alpha.spot.color = alpha.color
    elif alpha.momentum.x / mag(alpha.momentum) <= cos(pi / 4):
        alpha.color = color.blue
        trail.color = alpha.color
        alpha.spot.color = alpha.color

    for t in trails:
        t.color = t.color / 2
    trails.append(trail)
    if len(trails) > 3:
        trails.pop(0).visible = 0
