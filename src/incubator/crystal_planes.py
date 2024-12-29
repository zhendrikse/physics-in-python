from vpython import *

title = """
Original <a href="https://lectdemo.github.io/virtual/24_crystal_planes.html">24_crystal_planes.html</a> by Ruth Chabay Spring 2001
Click to see planes containing many atoms.
"""

scene.x = scene.y = 0
scene.width = scene.height = 800
scene.forward = vector(1, -0.8, -2)


def wire_box(s=5., box_color=vector(0, 1, 1)):
    pts = [vector(-s, -s, -s), vector(-s, -s, s), vector(-s, s, s),
           vector(-s, s, -s), vector(-s, -s, -s), vector(s, -s, -s),
           vector(s, s, -s), vector(-s, s, -s), vector(s, s, -s),
           vector(s, s, s), vector(-s, s, s), vector(s, s, s),
           vector(s, -s, s), vector(-s, -s, s), vector(s, -s, s), vector(s, -s, -s)]
    c = curve(color=box_color, radius=0.05, pos=pts)
    return c

_ = [sphere(pos=vector(x, y, z), radius=0.3, color=vector(1, 0, 1)) for x in arange(-2, 3, 2) for z in arange(-2, 3, 2) for y in arange(-2, 3, 2)]
_ = [sphere(pos=vector(x, y, z), radius=0.3, color=vector(0, 1, 1)) for x in arange(-1, 3, 2) for z in arange(-1, 3, 2) for y in arange(-1, 3, 2)]

#scene.autoscale = 0

unit = wire_box(s=1, box_color=vector(.8, .8, .8))
unit._pos = unit._pos + vector(-1, -1, -1)

plane1 = box(pos=vector(0, 0, 0), size=vector(6, 0.01, 6), color=vector(.8, .8, .8), visible=0)
plane2 = box(pos=vector(0, 0, 0), size=vector(6, 0.01, 6), color=vector(.8, .8, .8), visible=0)
plane2.rotate(axis=vector(0, 0, 1), angle=pi / 4.)

scene.waitfor('click')
unit.visible = 0
plane1.visible = 1
pv = 1
planes = [plane1, plane2]

while 1:
    scene.waitfor("click")
    pv = pv + 1
    if pv > 2: pv = 1
    plane1.visible = (pv == 1)
    plane2.visible = (pv == 2)
