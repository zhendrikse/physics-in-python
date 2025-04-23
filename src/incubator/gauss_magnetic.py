from random import *
from vpython import *

print
"""
Electromagnetism: Gauss Magnetic Law (v2.75) 2008-01-20
Rob Salgado (salgado@physics.syr.edu)

Magnetic Field vectors are red.
"""

animation = canvas(
    width=800, height=600,
    x=0, y=0,
    title="GAUSS: No Radial-B's")

#scene.ambient = 0.24
colorBackground = [color.black, color.white]
colorScheme = 0

animation.background = colorBackground[colorScheme]

#scene.range = (2.5, 2.5, 2.5)
animation.range=2.5
animation.forward = vec(-0.162765, 0.013403, -0.986574)

# based on
#
#   http://www.math.niu.edu/~rusin/known-math/97/spherefaq
# then
#   http://astronomy.swin.edu.au/~pbourke/geometry/spherepoints/source1.c
#


p = []
sp = []

theta = []
phi = []

N = 24

for k in arange(0, N):
    # print "k=",k,
    h = -1 + 2 * k / (N - 1.)
    # print "h=",h,
    theta.append(acos(h))
    if k == 0 or k == N - 1:
        phi.append(0)
        # print "q=0.00"
    else:
        phi_last = phi[-1]
        q = N * (1 - h * h)
        # print "q=",q
        phi.append(phi_last + 3.6 / sqrt(q))

for i in arange(0, N):
    p.append(vector(cos(phi[i]) * sin(theta[i]), sin(phi[i]) * sin(theta[i]), cos(theta[i])))
#    sp.append( sphere(pos=p[-1],radius=0.05) )

counter = 0
countmax = 100

n = len(p)
print
n

while (counter < countmax):
    minp1 = 0
    minp2 = 1
    mind = mag2(p[minp1] - p[minp2])
    maxd = mind

    for i in arange(0, n - 1):
        for j in arange(i + 1, n):
            d = mag2(p[i] - p[j])
            if (d < mind):
                mind = d;
                minp1 = i
                minp2 = j
            if (d > maxd):
                maxd = d
    p1 = p[minp1]
    p2 = p[minp2]

    p[minp2] = norm(p1 + 1.1 * (p2 - p1))
    p[minp1] = norm(p1 - 0.1 * (p2 - p1))

    counter += 1

####################################################

box(pos=vec(-0.05, 0.0, 0.0), axis=vec(0, .15, 0), width=0.02, height=0.02)
box(pos=vec(0.0, 0.0, 0.0), axis=vec(.1, -.1382, 0), width=0.02, height=0.02)
box(pos=vec(0.05, 0.0, 0.0), axis=vec(0, .15, 0), width=0.02, height=0.02)

E = 0.5 * 1 / mag2(p[0])
for i in arange(0, N):
    A = arrow(pos=p[i], axis=E * p[i], shaftwidth=0.04, fixedwidth=1, color=color.red)
    box(pos=p[i] + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04, color=color.red)

E /= 4.
for i in arange(0, N):
    A = arrow(pos=2 * p[i], axis=E * p[i], shaftwidth=0.04, fixedwidth=1, color=color.red)
    box(pos=2 * p[i] + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04, color=color.red)

A = ring(pos=(animation.camera.pos + animation.center) / 2., axis=animation.camera.pos - animation.center, color=color.magenta)
A2 = cylinder(pos=A.pos, axis=cross(animation.up, A.axis), radius=0.1, color=color.magenta)

# Now... WHEN AN OBJECT IS PICKED,
# TRANSLATE THE scene.center TO THE OBJECT'S POSITION
while 1:
    rate(5)
    ##    if scene.mouse.clicked:
    ##        scene.mouse.getclick()
    ##        newPick=scene.mouse.pick
    ##        if newPick !=None:
    ##            ### ANIMATE TO SELECTED POSITION
    ##            tempcolor=newPick.color
    ##            newPick.color=color.yellow
    ##            target=newPick.pos
    ##            step=(target-scene.center)/20.
    ##            for i in arange(1,20,1):
    ##                rate(10)
    ##                scene.center +=step
    ##                scene.scale *= 1.037  #(1.037**19=1.99)
    ##            newPick.color=tempcolor

    # if scene.mouse.button == 'right' or scene.mouse.button == 'wheel':
    #     A.visible = 0
    #     A2.visible = 0
    # else:
    A.visible = 0
    A2.visible = 0
    cam = animation.camera.pos
    ctr = animation.center
    up = animation.up
    A.pos = animation.forward / 2.  # (cam+ctr)/2.
    A.radius = mag(cam - ctr) / 3.;
    A.thickness = A.radius / 10.
    A.axis = A.pos  # cam-ctr
    A2.axis = 2 * norm(cross(up, A.axis)) * A.radius
    A2.rotate(angle=-pi / 4., axis=A.axis, origin=A.pos)
    A2.pos = A.pos - A2.axis / 2.
    A2.radius = A.thickness

    A.visible = 1
    A2.visible = 1
    #time.sleep(1)

    # if scene.kb.keys:  # is there an event waiting to be processed?
    #     s = scene.kb.getkey()  # obtain keyboard information
    #     if s == 'z':
    #         print
    #         "scene.center=(%f,%f,%f)" % tuple(scene.center)
    #         print
    #         "scene.forward=(%f,%f,%f)" % tuple(scene.forward)
    #         print
    #         "scene.range=(%f,%f,%f)" % tuple(scene.range)
    #
    #     if s == 'n':
    #         colorScheme = (colorScheme + 1) % 2  # TOGGLE colorScheme
    #         scene.background = colorBackground[colorScheme]