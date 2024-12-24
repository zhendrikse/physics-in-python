### EFieldBuilder.py
### Interactive E-Field Builder (requires VPython)
### Rob Salgado
### salgado@physics.syr.edu     http://physics.syr.edu/~salgado/
### v0.99   2001-10-23 tested on Windows 2000
###         with Python-2.1.1.exe and VPython-2001-10-08.exe

from vpython import *
import fpformat

print
print
"Interactive E-Field Builder (v0.99)"
print
"Rob Salgado (salgado@physics.syr.edu)"
print
print
"This VPython program allows you to position point charges in space."
print
"The Electric Field due to those charges is computed dynamically."
print
"Use the control panel to change the sign and magnitude of the"
print
"    next charge to be placed."
print
"In 'Create' mode:"
print
"    Clicking once on an empty location will place a new charge there."
print
"    Clicking once on an existing charge will select it."
print
"        Then, as you move your mouse, that charge can be repositioned."
print
"        Click again to release it."
print
"In 'Edit' mode:"
print
"    Clicking once on an existing charge will change its properties."
print
"In 'Copy' mode:"
print
"    Clicking once on an existing charge will copy its settings."
print
"To delete an existing charge:"
print
"    First, select the 'Edit' mode and set the charge to 0.0."
print
"    Then, select the charge to be deleted."
print
"Left-click and drag to zoom in and out."
print
"Right-click and drag to rotate about the origin."

scene2 = display(title='set Q',
                 x=0, y=0, width=100, height=100,
                 center=(0, 0, 0), background=(0.25, 0.25, 0.25))

setQ = sphere(pos=(1, 0, 0), radius=1, color=color.blue, Q=1.0)
incQ = cylinder(pos=(-1.5, 0.5, 0), axis=(0, 1, 0), radius=0.2, color=color.blue)
decQ = cylinder(pos=(-1.5, -0.5, 0), axis=(0, -1, 0), radius=0.2, color=color.red)
labQ = label(pos=(1, 0, 0), text=fpformat.fix(setQ.Q, 1), opacity=0., box=0)
modestate = ['create', 'edit', 'copy']
modeboxQ = box(pos=(-1.5, 0, 0), color=color.black)
modeQ = label(pos=(-1.5, 0, 0), text='create', box=0, mode=0)

scene2.visible = 1
scene2.userspin = 0
scene2.userzoom = 0
scene2.autoscale = 0

scene = display(title="E-Field Builder (Rob Salgado)", x=100, y=100)
scene.select()

scale = 0.2
step = 1.
S = 3.
drag = 0

charges = []
Efield = []
for x in arange(-S, S, step):
    for y in arange(-S, S, step):
        for z in arange(-S, S, step):
            vec = arrow(pos=(x, y, z), axis=(0, 0, 0))
            Efield.append(vec)

scene.autoscale = 0
scene.range = (5, 5, 5)


def getEFieldAt(p):
    E = vector(0, 0, 0)
    for c in charges:
        delta = p - c.pos
        if mag(delta) < 2e-13:
            print
            "small"
            print
            mag(delta)
        E = E + (delta) * c.Q / mag(delta) ** 3
    return scale * E


def getField():
    for v in Efield:
        v.axis = getEFieldAt(v.pos)


def update2():
    modeQ.text = modestate[modeQ.mode]
    if modeQ.mode == 0:
        scene2.background = (0.25, 0.25, 0.25)
    else:
        scene2.background = (1, 1, 1)

    if setQ.Q > 0.0:
        setQ.color = color.blue
    elif setQ.Q < 0.0:
        setQ.color = color.red
    else:
        setQ.color = color.green
    labQ.text = "%.1f" % setQ.Q


while 1:
    if scene2.mouse.clicked:
        m = scene2.mouse.getclick()
        newPick2 = scene2.mouse.pick
        if newPick2 == incQ:
            setQ.Q = setQ.Q + 0.5
        elif newPick2 == decQ:
            setQ.Q = setQ.Q - 0.5
        elif newPick2 == modeboxQ:
            modeQ.mode = (modeQ.mode + 1) % 3
        update2()

    if scene.mouse.clicked:
        m = scene.mouse.getclick()
        newPick = scene.mouse.pick
        if newPick == None:
            newChg = sphere(pos=m.pos, radius=abs(setQ.Q) / 5, color=setQ.color, Q=setQ.Q)
            if setQ.Q == 0:
                newChg.radius = 1.0 / 5.0
            charges.append(newChg)
            getField()
        else:
            n = newPick
            if modeQ.mode == 0:
                if n.Q != 0.0:
                    n.green = (1 - n.green)
                drag = (drag + 1) % 2
            elif modeQ.mode == 1:
                if setQ.Q != 0.0:
                    n.radius = abs(setQ.Q) / 5
                    n.color = setQ.color
                    n.Q = setQ.Q
                else:
                    n.visible = 0
                    charges.remove(n)
                modeQ.mode = 0
                update2()
                getField()
            elif modeQ.mode == 2:
                setQ.Q = n.Q
                setQ.color = n.color
                labQ.text = "%f" % setQ.Q
                modeQ.mode = 0
                update2()
    elif (drag % 2) == 1:
        if n != None:
            n.pos = scene.mouse.pos
            getField()