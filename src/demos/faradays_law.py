from vpython import *

# needs a code clean-up (seems to now work on Python 2.4/VPython 3.2.9)

"""
Electromagnetism: Faraday Law (v2.76) 2008-02-29
Rob Salgado (salgado@physics.syr.edu)

Electric Field vectors are blue. Magnetic Field vectors are red.

  The thick green vector representing
d|B|/dt ("time-rate-of-change-of-the-magnitude-of-the-magnetic-field")
is associated with the spatial arrangement of the electric field according to
the FARADAY Law (as evaluated on the green loop).
[The sense of circulation on the green loop (by the RightHandRule) determines
the direction of change of the magnetic field... OPPOSITE to your thumb.]

      CLICK the mouse to start and stop the animation
      TOGGLE: (f)araday
              (d)im-fields (n) color-scheme  (v)erbose"""

scene = canvas(
    width=800, height=600,
    x=0, y=0)

colorScheme = 0  # key n (negative)
colorBackground = [color.black, color.white]
colorEdimmed = [vector(0.0, 0, 0.4), vector(0.5, 0.5, 1)]
# scene.ambient = 0.4
Ecolor = [color.blue, (0.5, 0.5, 1), color.green]
Ecolor[1] = colorEdimmed[colorScheme]

scene.background = colorBackground[colorScheme]
scene.background = color.black;
Ecolor = [color.blue, vector(0, 0, .4), color.green]
# scene.background=color.white; Ecolor=[color.blue,(0.9,0.9,0.9),color.yellow]
scene.title = "FARADAY: Changing-Bs are associated with Curly-Es\nUse the space, n, d, z, and f keys for visualisation interaction"
# scene.range = vector(2.5, 2.5, 2.5)
# scene.forward = vector(-2.85804, -1.26038, -2.96742)
# scene.forward=(0.089623,4.193811,0.983082)
# scene.range=(1.5,1.5,1.5)
# scene.forward=(2.102859,-3.185552,1.998194)

#scene.camera.pos = vector(-2.85804, -1.26038, -2.96742)
#scene.camera.axis = vector(2.5, 2.5, 2.5)

showFaraday = 0
dimFields = 0

B = []
B.append(arrow(pos=vector(0.25, 0, 0), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(-0.25, 0, 0), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(0, 0.25, 0), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(0, -0.25, 0), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(0.25, 0, -2), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(-0.25, 0, -2), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(0, 0.25, -2), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))
B.append(arrow(pos=vector(0, -0.25, -2), axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red))

N = 8
dBdt = 0.2
E = []
Ebox = []

for z in [0]:
    for r in [0.5]:
        for i in arange(0, N):
            theta = 2. * pi * i / N
            theta_hat = vector(-sin(theta), cos(theta), 0)
            Efield = -dBdt * theta_hat / r
            A = arrow(pos=vector(r * cos(theta), r * sin(theta), z), axis=Efield, shaftwidth=0.04, fixedwidth=1,
                      color=color.blue)
            E.append(A)
            Ebox.append(box(pos=A.pos + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04,
                            color=color.blue))
    for r in [1, 1.5]:
        for i in arange(0, N):
            theta = 2. * pi * i / N
            theta_hat = vector(-sin(theta), cos(theta), 0)
            Efield = -dBdt * theta_hat / r
            A = arrow(pos=vector(r * cos(theta), r * sin(theta), z), axis=Efield, shaftwidth=0.04, fixedwidth=1,
                      color=color.blue)
            E.append(A)
            Ebox.append(box(pos=A.pos + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04,
                            color=color.blue))

for z in [-0.5, 0.5, -1, 1]:
    for r in arange(.5, 1.5, .5):
        for i in arange(0, N):
            theta = 2. * pi * i / N
            theta_hat = vector(-sin(theta), cos(theta), 0)
            Efield = -dBdt * theta_hat / r
            A = arrow(pos=vector(r * cos(theta), r * sin(theta), z), axis=Efield, shaftwidth=0.04, fixedwidth=1,
                      color=color.blue)
            E.append(A)
            Ebox.append(box(pos=A.pos + A.axis / 4., axis=A.axis, length=mag(A.axis) / 2., height=0.04, width=0.04,
                            color=color.blue))

hcolor = Ecolor[2]

Bp = []
for b in B:
    Bp.append(arrow(pos=b.pos + b.axis, axis=dBdt * norm(b.axis),
                    # length=dBdt,
                    fixedwidth=1, color=hcolor, shaftwidth=0.07, headwidth=0.14, visible=showFaraday))

Eloop_rad = mag(E[0].pos)
pos = [Eloop_rad * vector(cos(2. * pi * n / 40.), sin(2. * pi * n / 40.), 0) for n in range(40)]
FaradayLoop = curve(color=hcolor, pos=pos, visible=True)

I=cylinder(radius=0.04,pos=vector(0,0,-2),axis=vector(0,0,4), color=color.yellow)
chgpos=[]
chg=[]
for i in arange(0,N):
   chgpos.append(vector(I.pos+I.axis*i/N))
   chg.append(sphere(pos=chgpos[-1],radius=0.05,color=I.color))

t = 9.50
# t=10.0
# t=10.5

dt = 1


def toggle_show_faraday(show=True):
    # FaradayLoop.visible = show
    for k in Bp:
        k.visible = show

    if show == 1:
        for l in range(0, N):
            E[l].color = hcolor
            Ebox[l].color = hcolor
    else:
        for l in range(0, N):
            E[l].color = color.blue
            Ebox[l].color = color.blue


def toggle_show_fields(show=0):
    for i in range(N, len(E)):
        E[i].color = Ecolor[show]
        Ebox[i].color = Ecolor[show]
    for i in range(1, 4 * N + 1):
        E[-i].visible = (1 - show)
        Ebox[-i].visible = (1 - show)


def toggle_color_scheme(color_scheme=0):
    scene.background = colorBackground[color_scheme]
    Ecolor[1] = colorEdimmed[color_scheme]
    scene.background = colorBackground[color_scheme]

    for i in range(N, len(E)):
        E[i].color = Ecolor[dimFields]
        Ebox[i].color = Ecolor[dimFields]
    for i in range(1, 4 * N + 1):
        E[-i].visible = (1 - dimFields)
        Ebox[-i].visible = (1 - dimFields)


def pause_animation():
    global dt
    dt += 1
    dt %= 2


class KeyboardEventProcessor:
    def __init__(self):
        self._show_faraday = False
        self._show_fields = 0
        self._color_scheme = 0

    def toggle_show_faraday(self):
        self._show_faraday = not self._show_faraday
        return self._show_faraday

    def toggle_show_fields(self):
        self._show_fields += 1
        return self._show_fields % 2

    def toggle_color_schemes(self):
        self._color_scheme += 1
        return self._color_scheme % 2

    def on_key_press(self, key):
        if key == 'f':
            toggle_show_faraday(keyboard_event_processor.toggle_show_faraday())
        if key == 'd':
            toggle_show_fields(keyboard_event_processor.toggle_show_fields())
        if key == 'n':
            toggle_color_scheme(keyboard_event_processor.toggle_color_schemes())
        if key == 'z':
            print("scene.center=" + str(scene.center))
            print("scene.forward=" + str(scene.forward))
            print("scene.range=" + str(scene.range))
            print("t=" + str(t) + "\n")
        if key == ' ':
            pause_animation()

keyboard_event_processor = KeyboardEventProcessor()

def key_pressed(event):
  key = event.key
  keyboard_event_processor.on_key_press(key)
scene.bind('keydown', key_pressed)

def on_mouse_click():
    # mouse_coordinates = scene.mouse(pick=sphere)
    mouse_coordinates = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 2, 0))
    if not mouse_coordinates is None:
        # temp_color = mouse_coordinates.color
        # mouse_coordinates.color = color.yellow
        pick_r = mouse_coordinates.x * 4.
        pick_label_text = "r=" + str(round(pick_r, 5))
        label(pos=mouse_coordinates, text=pick_label_text, xoffset=-5, yoffset=5)

        target = mouse_coordinates
        step = (target - scene.center) / 20.
        for i in arange(1, 20, 1):
            rate(10)
            scene.center += step
            scene.range /= 1.037  # (1.037**19=1.99)
        # mouse_coordinates.color = temp_color


scene.bind('click', on_mouse_click)

# Now... WHEN AN OBJECT IS PICKED,
# TRANSLATE THE scene.center TO THE OBJECT'S POSITION
while 1:
    rate(10)
    t += dt
    ##    for i in arange(0,N):
    ##        chg[i].pos = chgpos[i]+(t%4)*vector(0,0,.125)
    bcount = 0
    for b in B:
        b.length = (t % 20) / 10. + 1e-3
        Bp[bcount].pos = b.pos + b.axis
        bcount += 1
