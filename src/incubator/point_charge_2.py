# Web VPython 3.2

##from random import *
##from visual import *
from vpython import *

"""
Electromagnetism:  Electric Gauss Law
(v3.50) 2022-04-04 Rob Salgado (robertoBsalgado@gmail.com)
(v2.80) 2010-03-22 Rob Salgado (salgado@physics.syr.edu)
Electric Field vectors are orange.
"""

scene = canvas(width=800, height=600, x=0, y=0)

scene.ambient = 0.24 * vec(1, 1, 1)
colorBackground = [color.black, color.white]
colorScheme = 0

scene.background = colorBackground[colorScheme]
scene.title = "GAUSS: Radial E's are associated with ElectricPoint-Charges (n)"
scene.range = 2.5
scene.forward = vec(-0.162765, 0.013403, -0.986574)
scene.autoscale = 1

# based on
#
#   http://www.math.niu.edu/~rusin/known-math/97/spherefaq
# then
#   http://astronomy.swin.edu.au/~pbourke/geometry/spherepoints/source1.c
#

colorEdimmed = [vec(0.0, 0, 0.4), vec(0.96, 0.96, 0.8)]

Ecolor = [color.orange, vec(0.5, 0.5, 1), color.magenta]
Ecolor[1] = colorEdimmed[colorScheme]
Bcolor = [color.cyan, vec(1, 0.5, 0.5), vec(1, 0.75, 0.0)]

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

for i in range(0, N):
    p.append(vector(cos(phi[i]) * sin(theta[i]), sin(phi[i]) * sin(theta[i]), cos(theta[i])))
#    sp.append( sphere(pos=p[-1],radius=0.05) )

counter = 0
countmax = 100

n = len(p)

while counter < countmax:
    minp1 = 0
    minp2 = 1
    mind = mag2(p[minp1] - p[minp2])
    maxd = mind

    for i in arange(0, n - 1):
        for j in arange(i + 1, n):
            d = mag2(p[i] - p[j])
            if d < mind:
                mind = d;
                minp1 = i
                minp2 = j
            if d > maxd:
                maxd = d
    p1 = p[minp1]
    p2 = p[minp2]

    p[minp2] = norm(p1 + 1.1 * (p2 - p1))
    p[minp1] = norm(p1 - 0.1 * (p2 - p1))

    counter += 1

sphere(radius=0.04, color=color.cyan)

E = 0.5 * 1 / mag2(p[0])
for i in arange(0, N):
    A = arrow(pos=p[i], axis=E * p[i], shaftwidth=0.04, fixedwidth=1, color=Ecolor[0])
    box(pos=p[i] + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04, color=Ecolor[0])

E /= 4.
for i in arange(0, N):
    A = arrow(pos=2 * p[i], axis=E * p[i], shaftwidth=0.04, fixedwidth=1, color=Ecolor[0])
    box(pos=2 * p[i] + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04, color=Ecolor[0])


def on_key_press(event):
    global colorScheme
    if event.key == 'n':
        colorScheme = (colorScheme + 1) % 2  # TOGGLE colorScheme
        scene.background = colorBackground[colorScheme]
    if event.key == 'z':
        print("scene.center=", scene.center)
        print("scene.forward=", scene.forward)
        print("scene.range=", scene.range)


scene.bind('keydown', on_key_press)


def zoom_in_on(selected_object):
    if selected_object is None:
        return

    ### ANIMATE TO SELECTED POSITION
    temp_color = vec(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    step = (target - scene.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(10)
        scene.center += step
        scene.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color


while 1:
    rate(60)
    scene.waitfor('click')
    zoom_in_on(scene.mouse.pick)
