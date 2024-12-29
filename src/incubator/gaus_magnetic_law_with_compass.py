from vpython import *

title = """GAUSS: No Radial-B's [n]

Electromagnetism: Gauss Magnetic Law 
v3.50 2022-04-04 Rob Salgado (robertoBsalgado@gmail.com)
v2.80 2010-03-22 Rob Salgado 
Magnetic Field vectors are cyan.
"""

scene = canvas(
    width=800, height=600,
    x=0, y=0,
    title=title)

colorBackground = [color.black, color.white]
colorScheme = 0

scene.background = colorBackground[colorScheme]

colorBdimmed = [vec(0.4, 0, 0), vec(1, 0.5, 0.5)]

Bcolor = [color.cyan, vec(1, 0.5, 0.5), vec(1, 0.75, 0.0)]
Bcolor = [color.cyan, vec(0, 0.0, 0.4), vec(0, 1, 0.0)]

colorBdimmed = [vec(0.0, 0, 0.4), vec(0.8, 0.96, 0.96)]
colorNO = color.red

#scene.ambient = vec(.4, .4, .4)

Ecolor = [color.orange, vec(.4, 0, 0), color.yellow, vec(0, 1, 0)]
Bcolor = [color.cyan, vec(0, 0, .4), color.yellow, vec(0, 0., 1)]
ddtcolor = [Bcolor[2 + colorScheme], Ecolor[2 + colorScheme]]  # for Ampere and Faraday

Bcolor[1] = colorBdimmed[colorScheme]

#scene.autoscale = 1
scene.range = vec(2.5, 2.5, 2.5)
scene.forward = vec(-0.162765, 0.013403, -0.986574)

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
# print (n)

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
    A = arrow(pos=p[i], axis=E * p[i], shaftwidth=0.04, fixedwidth=1, color=Bcolor[0])
    box(pos=p[i] + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04, color=Bcolor[0])

E /= 4.
for i in arange(0, N):
    A = arrow(pos=2 * p[i], axis=E * p[i], shaftwidth=0.04, fixedwidth=1, color=Bcolor[0])
    box(pos=2 * p[i] + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04, color=Bcolor[0])

A = ring(pos=(scene.mouse.pos + scene.center) / 2., axis=scene.mouse.pos - scene.center, color=colorNO)
A2 = cylinder(pos=A.pos, axis=cross(scene.up, A.axis), radius=0.5, color=colorNO)

scene.autoscale = 1


##########################################################################################################
##########################################################################################################

def keyInput(evt):
    global colorScheme, gaussSurface, Gcolor_boundary
    global scene, colorBackground, Ecolor, Bcolor

    if 1:  # evt.event== 'click': #CLICK TOGGLE PAUSE

        #        scene.waitfor('click')
        #        trun = (trun+1)%2
        #
        #    else:  #process key instead
        s = evt.key

        # if scene.kb.keys: # is there an event waiting to be processed?
        #    s = scene.kb.getkey() # obtain keyboard information
        if s == 'z':
            print("scene.center=", scene.center)
            print("scene.forward=", scene.forward)
            print("scene.range=", scene.range)

        if s == 'n':
            colorScheme = (colorScheme + 1) % 2  # TOGGLE colorScheme
            scene.background = colorBackground[colorScheme]


# scene.bind('keydown click', keyInput)
scene.bind('keydown', keyInput)

##########################################################################################################
##########################################################################################################


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

    if 0:  # scene.mouse.button == 'right' or scene.mouse.button == 'middle':
        A.visible = 0
        A2.visible = 0
    else:
        A.visible = 0
        A2.visible = 0
        cam = scene.mouse.pos  # camera
        ctr = scene.center
        up = scene.up
        A.pos = scene.forward / 2.  # (cam+ctr)/2.
        A.radius = mag(cam - ctr) / 3.;
        A.thickness = A.radius / 10.
        A.axis = A.pos  # cam-ctr
        A2.axis = 2 * norm(cross(up, A.axis)) * A.radius
        A2.rotate(angle=-pi / 4., axis=A.axis, origin=A.pos)
        A2.pos = A.pos - A2.axis / 2.
        A2.radius = A.thickness

        A.visible = 1
        A2.visible = 1
###        time.sleep(1)



