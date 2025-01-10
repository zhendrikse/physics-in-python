# written by Lenore Horner, 2009

from vpython import *
from random import uniform

Ndrops = 100
toggle = 0  # 0 makes all drops the same mass; 1 makes all drops the same density

power = 2
constant = .5
dropheight = 4
dt = 0.01

worldsize = sqrt(Ndrops) * 1.5
max_dropsize = 1
allowed = worldsize / 2.0 - max_dropsize

floor = box(length=worldsize, height=0.5, width=worldsize, pos=vec(0, -dropheight, 0), color=color.blue)

Drops = []


for i in range(Ndrops):  # create drops of various sizes at rest at common height
    size = uniform(0.1, max_dropsize)
    Drops = Drops + [ellipsoid(length=size, width=size, height=size, color=color.red)]
    Drops[i].velocity = vector(0, 0, 0)
    Drops[i].acceleration = vector(0, 9.8, 0)
    Drops[i].pos = vector(uniform(-allowed, allowed), dropheight, uniform(-allowed, allowed))
    # make sure drops don't overlap; including making sure changed location doesn't overlap one that was clear before
    check = -1
    while check < 0:
        check = 0
        for j in range(i):
            if mag(Drops[i].pos - Drops[j].pos) < (Drops[i].length + Drops[j].length) / 2.0:
                check = check - 1
        if check < 0:
            Drops[i].pos = vector(uniform(-allowed, allowed), dropheight, uniform(-allowed, allowed))

pop_up = label(pos=vec(0, 0, 0), text="Click mouse to start", box=False, color=color.yellow)
scene.waitfor("click")
pop_up.visible = False

while 1:
    rate(100)
    for i in range(Ndrops):  # let all the drops fall
        Drops[i].pos = Drops[i].pos + Drops[i].velocity * dt
        if Drops[i].pos.y < -dropheight + Drops[i].height + 0.5:  # check for drops hitting surface
            if Drops[i].height > 0.09:  # only worry about drops that haven't already gone splat
                Drops[i].velocity.y = 0  # drops stop
                # drops flatten on surface
                Drops[i].height = 0.09
                Drops[i].length = Drops[i].width = Drops[i].width ** (3.0 / 2)
                Drops[i].pos.y = -dropheight + 0.5
        else:
            Drops[i].velocity.y = Drops[i].velocity.y + Drops[i].acceleration.y * dt
            volume = Drops[i].width ** 2 * Drops[i].height
            accel = sign(Drops[i].velocity.y) * constant * Drops[i].width ** 2 * Drops[i].velocity.y ** power / (
                volume) ** toggle
            Drops[i].acceleration.y = -9.8 - accel
