from vpython import *

# import povexport

"""Instructions: 
Change viewpoint by using ctrl-click or cmd-click and dragging.

To generate POV-Ray code of a particular view, click in the scene.
You may export multiple views.  Each file will be given a name
prefixed with a number which increments with each picture FOR
AN INSTANCE OF THE PROGRAM.
"""

######################################################
# B field
Bshaft = 0.5
Bsize = -2
Bdirect = vector(0, 0, Bsize)
inc1 = vector(2.5, 0, 0)
inc2 = vector(0, 2.5, 0)
######################################################

scene = canvas(background=color.white)
plane = box(pos=vector(0, 0, 0), length=2.5 * mag(inc1), width=0.1, height=2.5 * mag(inc1))
plane.color = color.green
plane.opacity = 0.2

B00 = arrow(pos=vector(0, 0, -Bsize / 2.0) + 0.0 * inc1 + 0.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)
B20 = arrow(pos=vector(0, 0, -Bsize / 2.0) - 1.0 * inc1 + 0.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)
B30 = arrow(pos=vector(0, 0, -Bsize / 2.0) + 1.0 * inc1 + 0.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)

B01 = arrow(pos=vector(0, 0, -Bsize / 2.0) + 0.0 * inc1 - 1.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)
B21 = arrow(pos=vector(0, 0, -Bsize / 2.0) - 1.0 * inc1 - 1.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)
B31 = arrow(pos=vector(0, 0, -Bsize / 2.0) + 1.0 * inc1 - 1.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)

B03 = arrow(pos=vector(0, 0, -Bsize / 2.0) + 0.0 * inc1 + 1.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)
B23 = arrow(pos=vector(0, 0, -Bsize / 2.0) - 1.0 * inc1 + 1.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)
B33 = arrow(pos=vector(0, 0, -Bsize / 2.0) + 1.0 * inc1 + 1.0 * inc2, axis=Bdirect, shaft=Bshaft, color=color.blue)

# simple current loop
Ishaft = 1.0
corner = vector(-1, -0.75, +.3)
axis1 = vector(2, 0, -0.6)
axis2 = vector(0, 1.5, 0)
axis3 = vector(-2, 0, 0.6)
axis4 = vector(0, -1.5, 0)

current = 0.25
Iarrow1 = arrow(pos=corner, axis=axis1, shaft=Ishaft)
Iarrow2 = arrow(pos=Iarrow1.pos + Iarrow1.axis, axis=axis2, shaft=Ishaft)
Iarrow3 = arrow(pos=Iarrow2.pos + Iarrow2.axis, axis=axis3, shaft=Ishaft)
Iarrow4 = arrow(pos=Iarrow3.pos + Iarrow3.axis, axis=axis4, shaft=Ishaft)

force1 = current * cross(axis1, Bdirect)
force2 = current * cross(axis2, Bdirect)
force3 = current * cross(axis3, Bdirect)
force4 = current * cross(axis4, Bdirect)

fshaft = 0.75
farrow1 = arrow(pos=Iarrow1.pos + axis1 / 2, axis=force1, color=color.red)
farrow2 = arrow(pos=Iarrow2.pos + axis2 / 2, axis=force2, color=color.red)
farrow3 = arrow(pos=Iarrow3.pos + axis3 / 2, axis=force3, color=color.red)
farrow4 = arrow(pos=Iarrow4.pos + axis4 / 2, axis=force4, color=color.red)

tarrow = arrow(pos=vector(0, 0, 0), axis=cross(axis1, force2) * 3, color=color.yellow)

import time

counter = 0

while 1:
    rate(100)
    # scene.mouse.getclick()  ## position camera somewhere, then click
    # povexport.export(filename="%1.0_loopTorque.pov" %counter, display=scene)
    # print("Export finished")
    counter = counter + 1
