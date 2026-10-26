from vpython import vector, sin, cos, color, mag, arrow, sphere, rate, gcurve, canvas, box, graph, vec, pi

print('''2D-kinematics-with-vectors.py ( ver 09/25/2023;
based on ver 10/27/2003 )
''')

##print """
##2D-kinematics-with-vectors.py ( ver 10/27/2003 )
##Kinematics demonstration (tested on Windows2000 with Python-2.3 and VPython23-2003-10-04)
##Rob Salgado
##salgado@physics.syr.edu     http://physics.syr.edu/~salgado/
##"""

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
pos_init.x = 0.0
vel_init = vector(1.0 * cos(70 * DEG), 1.0 * sin(70 * DEG), 0)


def acc(t, x, v):
    return vector(0., -g, 0.)


pos2_init.x = 0.0
vel2_init = vector(1.0 * cos(20 * DEG), 1.0 * sin(20 * DEG), 0)


def acc2(t, x, v):
    return vector(0., -g, 0.)


# color scheme
#
BW = 0
if BW == 0:
    fgcolor = color.black;
    bgcolor = color.white
else:
    fgcolor = color.white;
    bgcolor = color.black
b1color = color.red
b1colorx = vec(1, 1, 0)
b1colory = vec(1, 0, 1)
b2color = vec(0, .75, 0)
b2colorx = vec(1, .75, 0)
b2colory = vec(0, .75, 1)
#
# setup main scene
#
animation = canvas(
    title="2-dimensional kinematics", align="right",
    width="900", height=600,
    x=250, y=0,
    autoscale=0,
    range=2,
    foreground=fgcolor,
    background=bgcolor
)
##scene.lights = [vector(0,0.,0.3) ]; scene.ambient = 0.7
# scene.lights = [vector(0, 0., 0.3)]
animation.ambient = 0.7 * vec(1, 1, 1)

animation.forward = vector(0.0, 0, -10.)
animation.fov = 1e-14  # pseudo-orthogonal

sphere(radius=0.1)

#
# track
#
track_length = 20

track = box(pos=vec(track_length / 2, -0.05, 0), axis=vec(1, 0, 0),
            length=track_length, height=.1, width=2, color=color.orange)

# tick marks on the track
c = []
# for x in arange(tracklength):
#    cu = curve( z = arange(-1,2,1) ,color=vec(0.25,0.25,1.0))
#    c.append(cu)
#    c[x].pos.y = 0.01
#    c[x].pos.x = x

#
# blocks
#
block_height = 0.25

# setup initial POSITIONS (sit on track)
pos_init.y = 0.
pos_init.z = -0.5
pos2_init.y = 0
pos2_init.z = 0.5

block = box(pos=pos_init, axis=track.axis,
            length=block_height, height=block_height, width=block_height, color=b1color)
block2 = box(pos=pos2_init, axis=track.axis,
             length=block_height, height=block_height, width=block_height, color=b2color)

block.vel = vel_init
block2.vel = vel2_init

animation.center = block.pos - vector(0, 1, 0)  # keep block in view

#
# kinematic graphs
#

posx_graph = graph(width=250, height=150,
                   title='x-Position vs. Time', xtitle='t(s)', ytitle='x (m)',
                   xmax=20., xmin=0., ymax=20, ymin=-4,
                   foreground=fgcolor, background=bgcolor)
posx_Plot = gcurve(color=b1color)
pos2x_Plot = gcurve(color=b2color)

velx_graph = graph(width=250, height=150,
                   title='x-Velocity vs. Time', xtitle='t(s)', ytitle='vx (m/s)',
                   xmax=20., xmin=0., ymax=2, ymin=-2,
                   foreground=fgcolor, background=bgcolor)
velx_Plot = gcurve(color=b1colorx)
vel2x_Plot = gcurve(color=b2colorx)

posy_graph = graph(width=250, height=150,
                   title='y-Position vs. Time', xtitle='t(s)', ytitle='y (m)',
                   xmax=20., xmin=0., ymax=8, ymin=-2.5,
                   foreground=fgcolor, background=bgcolor)
posy_Plot = gcurve(color=b1color)
pos2y_Plot = gcurve(color=b2color)

# skip_graph = graph(width=250, height=150,  align="right")
# skip_Plot = gcurve(color=b1color)


vely_graph = graph(width=250, height=150,
                   title='y-Velocity vs. Time', xtitle='t(s)', ytitle='vy (m/s)',
                   xmax=20., xmin=0., ymax=1, ymin=-1,
                   foreground=fgcolor, background=bgcolor)
vely_Plot = gcurve(color=b1colory)
vel2y_Plot = gcurve(color=b2colory)

#
# SETUP ANIMATION
#
time = 0.
counter = 0

count_tick = 100  # for ticks at 1-second intervals
count_subtick = count_tick / 5  # for ticks at 0.2-second intervals
dt = 1. / count_tick

animation.waitfor("click")


# let's allow the user to change the camera view point
def changeView():  # define a new function by name
    chosenObject = animation.mouse.pick  # find out which object the user clicked on
    if not chosenObject is None:  # if it is a real object that they clicked on ...
        animation.camera.follow(chosenObject)  # .. then have the camera follow that object


animation.bind("mousedown", changeView)  # allow mouse clicks to call the changeView function

while time <= 2 * vel_init.y / g + .2:  # run for 10 seconds
    rate(50)

    # CLICK TO PAUSE, THEN CLICK AGAIN TO CONTINUE
    #    if scene.mouse.clicked:
    #        scene.mouse.getclick()
    #        scene.mouse.getclick()

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
            arrow(pos=block.pos, axis=vec(block.vel.x / 2., 0, 0), color=b1colorx, fixedwidth=1)
            arrow(pos=block.pos, axis=vec(0, block.vel.y / 2., 0), color=b1colory, fixedwidth=1)
        if mag(block2.vel) > 0:
            arrow(pos=block2.pos, axis=block2.vel / 2., color=b2color, fixedwidth=1)
            arrow(pos=block2.pos, axis=vec(block2.vel.x / 2., 0, 0), color=b2colorx, fixedwidth=1)
            arrow(pos=block2.pos, axis=vec(0, block2.vel.y / 2., 0), color=b2colory, fixedwidth=1)
    elif counter % count_subtick == 0:
        box(pos=block.pos, axis=block.vel, size=vec(0.05, 0.05, 0.05), color=0.3 * b1color)
        box(pos=block2.pos, axis=block2.vel, size=vec(0.05, 0.05, 0.05), color=0.3 * b2color)

    if counter % count_subtick == 0:
        posx_Plot.plot(pos=(time, block.pos.x))
        pos2x_Plot.plot(pos=(time, block2.pos.x))

        velx_Plot.plot(pos=(time, block.vel.x))
        vel2x_Plot.plot(pos=(time, block2.vel.x))

        posy_Plot.plot(pos=(time, block.pos.y))
        pos2y_Plot.plot(pos=(time, block2.pos.y))
        #        skip_Plot.plot(pos=(time,block.vel.x))

        vely_Plot.plot(pos=(time, block.vel.y))
        vel2y_Plot.plot(pos=(time, block2.vel.y))

    animation.center = block.pos - vector(0, 1, 0)  # keep block in view

    time = time + dt
    counter += 1

print("scene.center=", animation.center)
print("scene.forward=", animation.forward)
print("scene.range=", animation.range)
# Now... WHEN AN OBJECT IS PICKED,
# TRANSLATE THE scene.center TO THE OBJECT'S POSITION
# while 1:
#    rate(5)
#    if scene.mouse.clicked:
#        scene.mouse.getclick()
#        newPick=scene.mouse.pick
#        if newPick !=None:
#            ### ANIMATE TO SELECTED POSITION
#            tempcolor=newPick.color
#            newPick.color=color.yellow
#            target=newPick.pos
#            step=(target-scene.center)/20.
#            for i in arange(1,20,1):
#                rate(10)
#                scene.center +=step
#            newPick.color=tempcolor
