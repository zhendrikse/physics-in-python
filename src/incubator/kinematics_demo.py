from vpython import *

"""
2D-kinematics-with-vectors-circular-polar.py ( ver 10/27/2003 )
Kinematics demonstration (tested on Windows2000 with Python-2.3 and VPython23-2003-10-04)
Rob Salgado
salgado@physics.syr.edu     http://physics.syr.edu/~salgado/

(bugs: round-off errors?)
"""

PI = pi
DEG = PI / 180.

# setup (do not edit these components)
pos_init = vector(0, 0, 0)
vel_init = vector(0, 0, 0)
pos2_init = vector(0, 0, 0)
vel2_init = vector(0, 0, 0)

#####################################
##
## EDIT KINEMATICS PARAMETERS HERE
##
##
g = 0.1
pos_init = vector(4, 0, 0)
vel_init = vector(0, 2.0, 0)


def acc(t, x, v):
    radiusvect = x
    r = mag(radiusvect)
    rhat = radiusvect / r
    mag_a = mag2(v) / r
    return vector(-mag_a * rhat.x, -mag_a * rhat.y, 0)


pos2_init = vector(2, 0, 0)
vel2_init = vector(0, 1.0, 0)


def acc2(t, x, v):
    radiusvect = x
    r = mag(radiusvect)
    rhat = radiusvect / r
    return vector(-mag2(v) / r * rhat.x, -mag2(v) / r * rhat.y, 0)


# color scheme
#
BW = 1
if BW == 0:
    fgcolor = color.black;
    bgcolor = color.white
else:
    fgcolor = color.white;
    bgcolor = color.black
b1color = color.red
b1colora = vector(0.5, 0, 0.95)
b1colorx = vector(1, 1, 0)
b1colory = vector(1, 0, 1)
b2color = vector(0, .75, 0)
b2colora = vector(0, 0.5, 0.95)
b2colorx = vector(1, .75, 0)
b2colory = vector(0, .75, 1)
#
# setup main scene
#
animation = canvas(
    title="2-dimensional kinematics (circular motion - polar)",
    width=500, height=600,
    x=250, y=0,
    autoscale=0,
    range=(3, 3, 3),
    foreground=fgcolor,
    background=bgcolor
)
# TODO
#scene.lights = [vector(0, 0, 0.3)];
#scene.ambient = 0.7
#
#scene.forward = vector(0.0, 0, -10)
#scene.fov = 1e-14  # pseudo-orthogonal

#
# track
#
tracklength = 20
track = box(pos=vector(tracklength / 2, -0.05, 0), axis=vector(1, 0, 0),
            length=tracklength, height=.1, width=2, color=color.orange)

##tick marks on the track
c = []
for x in arange(tracklength):
    cu = curve(z=[arange(-1, 2, 1)], color=vector(0.25, 0.25, 1.0))
    c.append(cu)
    c[x].y = 0.01
    c[x].x = x

#
# blocks
#
block_height = 0.25

# setup initial POSITIONS (sit on track)
# pos_init.y = 0.;
# pos_init.z = 0
# pos2_init.y = 0;
# pos2_init.z = 0

block = box(pos=vector(0.01, 0, 0), axis=track.axis,
            length=block_height, height=block_height, width=block_height, color=b1color)
block2 = box(pos=vector(0.01, 0, 0), axis=track.axis,
             length=block_height, height=block_height, width=block_height, color=b2color)

block.vel = vel_init
block2.vel = vel2_init

animation.center = block.pos  # keep block in view

#
# kinematic graphs
#
pos_graph = graph(x=0, y=000, width=250, height=200,
                     title='Position vs. Time', xtitle='t(s)', ytitle='x (m)',
                     xmax=15., xmin=0., ymax=4, ymin=0,
                     foreground=fgcolor, background=bgcolor)
pos_Plot = gcurve(color=b1color)
pos2_Plot = gcurve(color=b2color)

vel_graph = graph(x=0, y=200, width=250, height=200,
                     title='Velocity vs. Time', xtitle='t(s)', ytitle='v (m/s)',
                     xmax=15., xmin=0., ymax=2, ymin=0,
                     foreground=fgcolor, background=bgcolor)
vel_Plot = gcurve(color=b1color)
vel2_Plot = gcurve(color=b2color)

acc_graph = graph(x=0, y=400, width=250, height=200,
                     title='Acceleration vs. Time', xtitle='t(s)', ytitle='a (m/s^2)',
                     xmax=15., xmin=0., ymax=2, ymin=0,
                     foreground=fgcolor, background=bgcolor)
acc_Plot = gcurve(color=b1colora)
acc2_Plot = gcurve(color=b2colora)

#
# SETUP ANIMATION
#
time = 0.
counter = 0

count_tick = 100  # for ticks at 1-second intervals
count_subtick = count_tick / 5  # for ticks at 0.2-second intervals
dt = 1. / count_tick

def on_mouse_click():
    pass

animation.bind('click', on_mouse_click)

while time <= 2 * PI * mag(pos2_init) / mag(vel2_init):  # run for 10 seconds
    rate(50)

    # # CLICK TO PAUSE, THEN CLICK AGAIN TO CONTINUE
    # if scene.mouse.clicked:
    #     scene.mouse.getclick()
    #     scene.mouse.getclick()

    a = acc(time, block.pos, block.vel)
    a2 = acc2(time, block2.pos, block2.vel)

    block.acc = a
    block2.acc = a2

    block.pos += block.vel * dt
    block.vel += block.acc * dt

    block2.pos += block2.vel * dt
    block2.vel += block2.acc * dt

    ### MARK MOTION WITH TICKS
    if counter % count_tick == 0:
        # box(pos=block.pos, axis=track.axis, size=(0.075,0.075,0.075), color=b1color)
        # box(pos=block2.pos, axis=track.axis, size=(0.075,0.075,0.075), color=b2color)
        if mag(block.vel) > 0:
            arrow(pos=block.pos, axis=block.vel / 2., color=b1color, fixedwidth=1)
            arrow(pos=block.pos, axis=block.acc / 2, color=b1colora, fixedwidth=1)
        if mag(block2.vel) > 0:
            arrow(pos=block2.pos, axis=block2.vel / 2., color=b2color, fixedwidth=1)
            arrow(pos=block2.pos, axis=block2.acc / 2., color=b2colora, fixedwidth=1)
    elif counter % count_subtick == 0:
        box(pos=block.pos, axis=block.vel, size=vec(0.05, 0.05, 0.05), color=b1color)
        box(pos=block2.pos, axis=block2.vel, size=vec(0.05, 0.05, 0.05), color=b2color)

    if counter % count_subtick == 0:
        vel_Plot.plot(pos=(time, mag(block.vel)))
        pos_Plot.plot(pos=(time, mag(block.pos)))
        vel2_Plot.plot(pos=(time, mag(block2.vel)))
        pos2_Plot.plot(pos=(time, mag(block2.pos)))
        acc_Plot.plot(pos=(time, mag(block.acc)))
        acc2_Plot.plot(pos=(time, mag(block2.acc)))

    animation.center = block.pos  # keep block in view

    time = time + dt
    counter += 1

# Now... WHEN AN OBJECT IS PICKED,
# TRANSLATE THE scene.center TO THE OBJECT'S POSITION
while 1:
    rate(5)
    # if scene.mouse.clicked:
    #     scene.mouse.getclick()
    #     newPick = scene.mouse.pick
    #     if newPick != None:
    #         ### ANIMATE TO SELECTED POSITION
    #         tempcolor = newPick.color
    #         newPick.color = color.yellow
    #         target = newPick.pos
    #         step = (target - scene.center) / 20.
    #         for i in arange(1, 20, 1):
    #             rate(10)
    #             scene.center += step
    #         newPick.color = tempcolor