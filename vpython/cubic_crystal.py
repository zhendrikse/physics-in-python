from vpython import *

#http://new.math.uiuc.edu/math198/MA198-2014/csbaile2/final_program.py

scene.title = "Cubic Crystal Unit Cell"

# This program was written by Connor Bailey on 12/06/14 for MATH 198
# project, UIUC. It is a compilation of my previous programs in one,
# and adds a second window with sliders and buttons to allow the user
# to change the direction, plane, and crystal system viewed. Future
# revisions could allow for the color and size of atoms to be changed,
# or for pre-made atomic arrangements to be displayed with a button.


# Change size of atoms can simulate different elements/compounds
outerRad = .2
outerColor = color.red
innerRad = .2
innerColor = color.red


# Creation of unit cell for each cubic type
def scunit(x, y, z):
    q = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                q.append(sphere(pos=vec(x + i, y + j, z + k), radius=outerRad, color=outerColor))


def bccunit(x, y, z):
    outer = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                outer.append(sphere(pos=vec(x + i, y + j, z + k), radius=outerRad, color=outerColor))

    inner = []
    inner.append(sphere(pos=vec(x + .5, y + .5, z + .5), radius=innerRad, color=innerColor))


def fccunit(x, y, z):
    outer = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                outer.append(sphere(pos=vec(x + i, y + j, z + k), radius=outerRad, color=outerColor))

    inner = []
    inner.append(sphere(pos=vec(x + .5, y + .5, z), radius=innerRad, color=innerColor))
    inner.append(sphere(pos=vec(x + .5, y, z + .5), radius=innerRad, color=innerColor))
    inner.append(sphere(pos=vec(x, y + .5, z + .5), radius=innerRad, color=innerColor))
    inner.append(sphere(pos=vec(x + 1, y + .5, z + .5), radius=innerRad, color=innerColor))
    inner.append(sphere(pos=vec(x + .5, y + 1, z + .5), radius=innerRad, color=innerColor))
    inner.append(sphere(pos=vec(x + .5, y + .5, z + 1), radius=innerRad, color=innerColor))


def setup():
    # Create Axes and labels

    curve(pos=[(0, 0, 0), (1.55, 0, 0)])
    curve(pos=[(0, 0, 0), (0, 1.55, 0)])
    curve(pos=[(0, 0, 0), (0, 0, 1.55)])

    xlab = label(pos=vec(1.55, 0, 0), text="x")
    ylab = label(pos=vec(0, 1.55, 0), text="y")
    zlab = label(pos=vec(0, 0, 1.55), text="z")

    # Create semi-transparent walls. Inspired by James Beardsworth's work.
    wall1 = box(pos=vec(.5, .5, 0), size=(1, 1, .01), color=color.green, opacity=.15)
    wall2 = box(pos=vec(.5, 0, .5), size=(1, .01, 1), color=color.green, opacity=.15)
    wall3 = box(pos=vec(1, .5, .5), size=(.01, 1, 1), color=color.green, opacity=.15)
    wall4 = box(pos=vec(0, .5, .5), size=(.01, 1, 1), color=color.green, opacity=.15)
    wall5 = box(pos=vec(.5, 1, .5), size=(1, .01, 1), color=color.green, opacity=.15)
    wall6 = box(pos=vec(.5, .5, 1), size=(1, 1, .01), color=color.green, opacity=.15)


# Displays direction arrow given h,k, and l (x,y,z)
def direc(x, y, z):
    x1 = 0
    y1 = 0
    z1 = 0
    if x < 0:
        x1 = 1
    if y < 0:
        y1 = 1
    if z < 0:
        z1 = 1
    comDenom = max(abs(x), abs(y), abs(z))

    if x != 0 or y != 0 or z != 0:
        x2 = x1 + x / float(comDenom)
        y2 = y1 + y / float(comDenom)
        z2 = z1 + z / float(comDenom)

        length1 = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** (0.5)

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        point = arrow(pos=vec(x1, y1, z1), axis=(dx, dy, dz), length=length1)


# The following functions display a plane from h,k,l Miller Indices
# depending on how many are 0. The planes functions determines which
# to use (only one is used per Miller Index). Note that code can be
# greatly simplified in the future.
def planes_nozero(h, k, l):
    x1 = 0.0
    y1 = 0.0
    z1 = 0.0

    if h < 0:
        x1 = 1.0
    if k < 0:
        y1 = 1.0
    if l < 0:
        z1 = 1.0

    xint = 1.0 / h
    yint = 1.0 / k
    zint = 1.0 / l

    # Make plane a face.
    f = frame()
    myfaces = faces(
        pos=[
            [x1 + xint, y1, z1], [x1, y1 + yint, z1], [x1, y1, z1 + zint],  # Triangle vertices
        ],
        color=[
            [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
        ],
#        frame=f,
        emissive=True
    )
    myfaces.make_twosided()
    myfaces.make_normals()


def planes_onezero(h, k, l):
    if h == 0:
        y = 1.0 / k
        z = 1.0 / l
        if y > 0 and z > 0:
            f = frame()
            myfaces = faces(
                pos=[
                    [1, 0, z], [1, y, 0], [0, y, 0],  # Triangle vertices
                    [1, 0, z], [0, 0, z], [0, y, 0],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if y < 0 and z > 0:
            f = frame()
            myfaces = faces(
                pos=[
                    [1, 1, z], [1, y + 1, 0], [0, y + 1, 0],  # Triangle vertices
                    [1, 1, z], [0, 1, z], [0, y + 1, 0],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if y > 0 > z:
            f = frame()
            myfaces = faces(
                pos=[
                    [1, 0, z + 1], [1, y, 1], [0, y, 1],  # Triangle vertices
                    [1, 0, z + 1], [0, 0, z + 1], [0, y, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (y < 0 and z < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [1, 1, z + 1], [1, y + 1, 1], [0, y + 1, 1],  # Triangle vertices
                    [1, 1, z + 1], [0, 1, z + 1], [0, y + 1, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
    if (k == 0):
        x = 1.0 / h
        z = 1.0 / l
        if (x > 0 and z > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [0, 0, z], [0, 1, z], [x, 1, 0],  # Triangle vertices
                    [0, 0, z], [x, 0, 0], [x, 1, 0],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x < 0 and z > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [1, 0, z], [1, 1, z], [x + 1, 1, 0],  # Triangle vertices
                    [1, 0, z], [x + 1, 0, 0], [x + 1, 1, 0],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x > 0 and z < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [0, 0, z + 1], [0, 1, z + 1], [x, 1, 1],  # Triangle vertices
                    [0, 0, z + 1], [x, 0, 1], [x, 1, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x < 0 and z < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [1, 0, z + 1], [1, 1, z + 1], [x + 1, 1, 1],  # Triangle vertices
                    [1, 0, z + 1], [x + 1, 0, 1], [x + 1, 1, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
    if (l == 0):
        x = 1.0 / h
        y = 1.0 / k
        if (x > 0 and y > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [x, 0, 0], [x, 0, 1], [0, y, 1],  # Triangle vertices
                    [x, 0, 0], [0, y, 0], [0, y, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x < 0 and y > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [x + 1, 0, 0], [x + 1, 0, 1], [1, y, 1],  # Triangle vertices
                    [x + 1, 0, 0], [1, y, 0], [1, y, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x > 0 and y < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [x, 1, 0], [x, 1, 1], [0, y + 1, 1],  # Triangle vertices
                    [x, 1, 0], [0, y + 1, 0], [0, y + 1, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x < 0 and y < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [x + 1, 1, 0], [x + 1, 1, 1], [1, y + 1, 1],  # Triangle vertices
                    [x + 1, 1, 0], [1, y + 1, 0], [1, y + 1, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()


def planes_twozero(h, k, l):
    if (h != 0):
        x = 1.0 / h
        if (x > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [x, 0, 1], [x, 0, 0], [x, 1, 0],  # Triangle vertices
                    [x, 0, 1], [x, 1, 1], [x, 1, 0],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (x < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [x + 1, 0, 1], [x + 1, 0, 0], [x + 1, 1, 0],  # Triangle vertices
                    [x + 1, 0, 1], [x + 1, 1, 1], [x + 1, 1, 0],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
    if (k != 0):
        y = 1.0 / k
        if (y > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [0, y, 0], [0, y, 1], [1, y, 1],  # Triangle vertices
                    [0, y, 0], [1, y, 0], [1, y, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (y < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [0, y + 1, 0], [0, y + 1, 1], [1, y + 1, 1],  # Triangle vertices
                    [0, y + 1, 0], [1, y + 1, 0], [1, y + 1, 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
    if (l != 0):
        z = 1.0 / l
        if (z > 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [0, 0, z], [1, 0, z], [1, 1, z],  # Triangle vertices
                    [0, 0, z], [0, 1, z], [1, 1, z],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()
        if (z < 0):
            f = frame()
            myfaces = faces(
                pos=[
                    [0, 0, z + 1], [1, 0, z + 1], [1, 1, z + 1],  # Triangle vertices
                    [0, 0, z + 1], [0, 1, z + 1], [1, 1, z + 1],
                ],
                color=[
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],  # Triangle colors
                    [1., 1., 1.], [1., 1., 1.], [1., 1., 1.],
                ],
#                frame=f,
                emissive=True
            )
            myfaces.make_twosided()
            myfaces.make_normals()


# The planes function takes in a Miller Index and
# sends it to teh appropriate function to create the given
# plane, depending on how many indices are zero.
def planes(h, k, l):
    totalzero = 0
    if (h == 0):
        totalzero += 1
    if (k == 0):
        totalzero += 1
    if (l == 0):
        totalzero += 1
    if (totalzero == 0):
        planes_nozero(h, k, l)
    elif (totalzero == 1):
        planes_onezero(h, k, l)
    elif (totalzero == 2):
        planes_twozero(h, k, l)


# refresh function updates the scene with whatever changes
# to parameters have been made from buttons and sliders. Updates
# the text box with current indices as well.
def refresh(evt):
    for obj in scene.objects:
        obj.visible = False
    setup()

    hp = int(p1.GetValue())
    kp = int(p2.GetValue())
    lp = int(p3.GetValue())
    planes(hp, kp, lp)

    crystal = c1.GetSelection()
    if (crystal == 0):
        scunit(0, 0, 0)
    elif (crystal == 1):
        bccunit(0, 0, 0)
    elif (crystal == 2):
        fccunit(0, 0, 0)

    hd = int(d1.GetValue())
    kd = int(d2.GetValue())
    ld = int(d3.GetValue())
    direc(hd, kd, ld)

    tc.Value = ("Plane Miller Index = (" + str(hp) + " " +
                str(kp) + " " + str(lp) + ")\n" + "Direction Miller Index = [" +
                str(hd) + " " + str(kd) + " " + str(ld) + "]")


# Resets the direction h,k, and l sliders to zero.
def direcreset(evt):
    d1.Value = 0
    d2.Value = 0
    d3.Value = 0
    refresh(True)


# Resets the plane h,k, and l sliders to zero.
def planereset(evt):
    p1.Value = 0
    p2.Value = 0
    p3.Value = 0
    refresh(True)


# Initialization- SC, no plane or direction.
setup()
scunit(0, 0, 0)

# Create window for "widgets" to allow user to dynamically change crystal setting.
# Widget style inspired by "widgets" program that comes with VPython.
w = canvas(title="Crystal Parameters", x=450, y=0, width=450, height=300)

p = w.panel

# p1-3 and d1-3 are the sliders for each plane and direction
# h(1), k(2), and l(3) value. Changing their value will automatically
# reset/refresh the scene with the changed values.

wx.StaticText(p, pos=vec(0, 0), label='Set h value for plane:')
p1 = wx.Slider(p, pos=vec(0, 15), size=(200, 25), minValue=-7, maxValue=7)
p1.Bind(wx.EVT_SCROLL, refresh)

wx.StaticText(p, pos=vec(0, 40), label='Set k value for plane:')
p2 = wx.Slider(p, pos=vec(0, 55), size=(200, 25), minValue=-7, maxValue=7)
p2.Bind(wx.EVT_SCROLL, refresh)

wx.StaticText(p, pos=vec(0, 80), label='Set l value for plane:')
p3 = wx.Slider(p, pos=vec(0, 95), size=(200, 25), minValue=-7, maxValue=7)
p3.Bind(wx.EVT_SCROLL, refresh)

wx.StaticText(p, pos=vec(0, 120), label='Set h value for direction:')
d1 = wx.Slider(p, pos=vec(0, 135), size=(200, 25), minValue=-7, maxValue=7)
d1.Bind(wx.EVT_SCROLL, refresh)

wx.StaticText(p, pos=vec(0, 160), label='Set k value for direction:')
d2 = wx.Slider(p, pos=vec(0, 175), size=(200, 25), minValue=-7, maxValue=7)
d2.Bind(wx.EVT_SCROLL, refresh)

wx.StaticText(p, pos=vec(0, 200), label='Set l value for direction:')
d3 = wx.Slider(p, pos=vec(0, 215), size=(200, 25), minValue=-7, maxValue=7)
d3.Bind(wx.EVT_SCROLL, refresh)

# Create radio box with options for which crystal unit cell (or none) to view.
wx.StaticText(p, pos=vec(200, 0), label="Choose crystal type:")
c1 = wx.RadioBox(p, pos=vec(200, 20), size=(60, 105), choices=['SC', 'BCC', 'FCC', 'None'],
                 style=wx.RA_SPECIFY_ROWS)
c1.Bind(wx.EVT_RADIOBOX, refresh)

# Create Plane and Direction reset buttons.
dreset = wx.Button(p, label="Reset Direction", pos=vec(200, 130))
dreset.Bind(wx.EVT_BUTTON, direcreset)

preset = wx.Button(p, label="Reset Plane", pos=vec(200, 160))
preset.Bind(wx.EVT_BUTTON, planereset)

# Create text box to display current Miller Indices for Plane and Direction.
tc = wx.TextCtrl(p, pos=vec(200, 200), size=(200, 50), style=wx.TE_MULTILINE)
