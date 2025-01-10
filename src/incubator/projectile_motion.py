# written by Lenore Horner 2009
# view-source:https://www.siue.edu/~lhorner/VPython/Projectile-air/projectile-air.py
# view-source:https://www.siue.edu/~lhorner/VPython/VPython.shtml

from vpython import *  # import graphing features (which grabs the general visual stuff)

# set up the main display window
setrange = 250
scene = canvas(width=1050, height=550, x=0, y=100, background=color.white, fov=0.001, range=setrange)
scene.exit = False

# initialize the three possible balls
grav = vector(0, -9.8, 0)  # Earth gravity
initialpos = vector(-.98 * setrange, -0.355 * setrange, 0)
airpos = vector(initialpos) + (0, 0, .02 * setrange)
drag2pos = vector(initialpos) + (0, 0, .04 * setrange)
nodragpos = vector(initialpos) + (0, 0, .0)
aircolor = color.red
drag2color = color.green
nodragcolor = color.blue

bottom = -.3551 * setrange

# define various things the user can control without rewriting code and rerunning the file
GO = 0


def go():  # called on go-button click
    global GO, gobtn
    if GO:
        gobtn.button.color = color.green
    else:
        gobtn.button.color = color.red
    GO = not GO


def reset():  # called on reset click, # redraw go to change its color; redraw scene to erase old trails
    global gobtn, scene
    global Xvel, Xveldrag2, Xvelair, Xvelnodrag
    global Yvel, Yveldrag2, Yvelair, Yvelnodrag
    global Xaccel, Xacceldrag2, Xaccelair, Xaccelnodrag
    global Yaccel, Yacceldrag2, Yaccelair, Yaccelnodrag
    # switch the on/off button
    gobtn.button.color = color.green
    # clean up the main scene
    scene.visible = False
    if (NoDragBall == 1):
        nodrag.trail.pos = []
    if (AirBall == 1):
        air.trail.pos = []
    if (Drag2Ball == 1):
        drag2.trail.pos = []
    for obj in scene.objects:
        obj.visible = False
        del obj
    scene.visible = True
    #   clean up the horizontal velocity graph
    Xvel.display.visible = False
    Xvelnodrag.pos = []
    Xveldrag2.pos = []
    Xvelair.pos = []
    for obj in Xvel.display.objects:
        obj.visible = False
        del obj
    del Xvel
    Xvel = graph(x=0, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                    title='V_x(t)')
    Xvel.display.exit = False
    Xvelnodrag = gdots(size=3, color=nodragcolor)
    Xveldrag2 = gdots(size=3, color=drag2color)
    Xvelair = gdots(size=3, color=aircolor)
    #   clean up the vertical velocity graph
    Yvel.display.visible = False
    Yvelnodrag.pos = []
    Yveldrag2.pos = []
    Yvelair.pos = []
    for obj in Yvel.display.objects:
        obj.visible = False
        del obj
    del Yvel
    Yvel = graph(x=263, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                    title='V_y(t)')
    Yvel.display.exit = False
    Yvelnodrag = gdots(size=3, color=nodragcolor)
    Yveldrag2 = gdots(size=3, color=drag2color)
    Yvelair = gdots(size=3, color=aircolor)
    #   clean up the horizontal acceleration graph
    Xaccel.display.visible = False
    Xaccelnodrag.pos = []
    Xacceldrag2.pos = []
    Xaccelair.pos = []
    for obj in Xaccel.display.objects:
        obj.visible = False
        del obj
    del Xaccel
    Xaccel = graph(x=523, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                      title='A_x(t)')
    Xaccel.display.exit = False
    Xaccelnodrag = gdots(size=3, color=nodragcolor)
    Xacceldrag2 = gdots(size=3, color=drag2color)
    Xaccelair = gdots(size=3, color=aircolor)
    #   clean up the vertical acceleration graph
    Yaccel.display.visible = False
    Yaccelnodrag.pos = []
    Yacceldrag2.pos = []
    Yaccelair.pos = []
    for obj in Yaccel.display.objects:
        obj.visible = False
        del obj
    del Yaccel
    Yaccel = graph(x=787, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                      title='A_y(t)')
    Yaccel.display.exit = False
    Yaccelnodrag = gdots(size=3, color=nodragcolor)
    Yacceldrag2 = gdots(size=3, color=drag2color)
    Yaccelair = gdots(size=3, color=aircolor)


def setangle(s1):  # called on angle slider nodrag events
    global angle
    angle = s1.value * pi / 180


def setspeed(s2):  # called on speed slider nodrag events
    global speed
    speed = s2.value


def setconstant(s3):  # called on constant slider nodrag events
    global constant
    constant = s3.value / 1000


# Make window for controls at the bottom of the screen and populate it with button, sliders, and labels for sliders
cw = controls(title='Controls', x=0, y=650, width=1050, height=100, background=color.white)

# starting and resetting
gobtn = button(pos=(7, 0, 0), width=10, height=10, color=color.green, text="GO", action=lambda: go())
rstbtn = button(pos=(-92, 0, 0), width=13, height=7, color=color.yellow, text="RESET", action=lambda: reset())

# Parameter settings
s1 = slider(pos=(-83, -2.5, 0), width=4, axis=(25, 0, 0), min=0, max=90, color=color.magenta,
            action=lambda: setangle(s1))
s1.value = 45  # don't set this in line above or you get a claim that axis is undefined for sliders (known bug)
setangle(s1)

vmax = sqrt(-3.8 * setrange * grav.y)
s2 = slider(pos=(-55, -2.5, 0), width=4, axis=(25, 0, 0), min=0, max=vmax, color=color.blue,
            action=lambda: setspeed(s2))
s2.value = s2.max / 2.0
setspeed(s2)

s3 = slider(pos=(-26, -2.5, 0), width=4, axis=(25, 0, 0), min=0, max=10, color=(1, 0.5, 0.2),
            action=lambda: setconstant(s3))
s3.value = s3.max / 2.
setconstant(s3)

## Set what to view
# No air resistance
NoDragBall = 1


def changeNoDragBall():  # Called by controls when button clicked
    global NoDragBall
    if bNoDragBall.text == 'On':
        bNoDragBall.text = 'Off'
        NoDragBall = 0
    else:
        bNoDragBall.text = 'On'
        NoDragBall = 1


bNoDragBall = button(pos=(70, 5), width=7, height=5, text='On', color=nodragcolor, action=lambda: changeNoDragBall())

NoDragV = 0


def changeNoDragV():  # Called by controls when button clicked
    global NoDragV
    if bNoDragV.text == 'On':
        bNoDragV.text = 'Off'
        NoDragV = 0
    else:
        bNoDragV.text = 'On'
        NoDragV = 1


bNoDragV = button(pos=(70, 0), width=7, height=5, text='Off', color=nodragcolor, action=lambda: changeNoDragV())

NoDragA = 0


def changeNoDragA():  # Called by controls when button clicked
    global NoDragA
    if bNoDragA.text == 'On':
        bNoDragA.text = 'Off'
        NoDragA = 0
    else:
        bNoDragA.text = 'On'
        NoDragA = 1


bNoDragA = button(pos=(70, -5), width=7, height=5, text='Off', color=nodragcolor, action=lambda: changeNoDragA())

# Air resistance proportional to v
AirBall = 0


def changeAirBall():  # Called by controls when button clicked
    global AirBall
    if bAirBall.text == 'On':
        bAirBall.text = 'Off'
        AirBall = 0
    else:
        bAirBall.text = 'On'
        AirBall = 1


bAirBall = button(pos=(80, 5), width=7, height=5, text='Off', color=aircolor, action=lambda: changeAirBall())

AirV = 0


def changeAirV():  # Called by controls when button clicked
    global AirV
    if bAirV.text == 'On':
        bAirV.text = 'Off'
        AirV = 0
    else:
        bAirV.text = 'On'
        AirV = 1


bAirV = button(pos=(80, 0), width=7, height=5, text='Off', color=aircolor, action=lambda: changeAirV())

AirA = 0


def changeAirA():  # Called by controls when button clicked
    global AirA
    if bAirA.text == 'On':
        bAirA.text = 'Off'
        AirA = 0
    else:
        bAirA.text = 'On'
        AirA = 1


bAirA = button(pos=(80, -5), width=7, height=5, text='Off', color=aircolor, action=lambda: changeAirA())

# air resistance proportional to v^2
Drag2Ball = 1


def changeDrag2Ball():  # Called by controls when button clicked
    global Drag2Ball
    if bDrag2Ball.text == 'On':
        bDrag2Ball.text = 'Off'
        Drag2Ball = 0
    else:
        bDrag2Ball.text = 'On'
        Drag2Ball = 1


bDrag2Ball = button(pos=(90, 5), width=7, height=5, text='On', color=drag2color, action=lambda: changeDrag2Ball())

Drag2V = 0


def changeDrag2V():  # Called by controls when button clicked
    global Drag2V
    if bDrag2V.text == 'On':
        bDrag2V.text = 'Off'
        Drag2V = 0
    else:
        bDrag2V.text = 'On'
        Drag2V = 1


bDrag2V = button(pos=(90, 0), width=7, height=5, text='Off', color=drag2color, action=lambda: changeDrag2V())

Drag2A = 0


def changeDrag2A():  # Called by controls when button clicked
    global Drag2A
    if bDrag2A.text == 'On':
        bDrag2A.text = 'Off'
        Drag2A = 0
    else:
        bDrag2A.text = 'On'
        Drag2A = 1


bDrag2A = button(pos=(90, -5), width=7, height=5, text='Off', color=drag2color, action=lambda: changeDrag2A())

# slider labels
label1 = label(display=cw.display, pos=(-70, 5, 0), text='angle(deg)')
label2 = label(display=cw.display, pos=(-42, 5, 0), text='speed(m/s)')
label3 = label(display=cw.display, pos=(-13, 5, 0), text='constant*1000')

# label on/off buttons for display elements (rows)
label4 = label(display=cw.display, pos=(55, 5, 0), text='ball & trail:', opacity=0, color=color.black)
label5 = label(display=cw.display, pos=(55, 0, 0), text='v arrows:', opacity=0, color=color.black)
label6 = label(display=cw.display, pos=(55, -5, 0), text='a arrows:', opacity=0, color=color.black)

# label colors
label7 = label(display=cw.display, pos=(35, 5, 0), text='no drag', opacity=0, color=nodragcolor)
label8 = label(display=cw.display, pos=(35, 0, 0), text='v drag', opacity=0, color=aircolor)
label9 = label(display=cw.display, pos=(35, -5, 0), text='v^2 drag', opacity=0, color=drag2color)

# Create some graph windows and functions to plot
Xvel = gdisplay(x=0, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                title='V_x(t)')
Xvel.display.exit = False
Xvelnodrag = gdots(size=3, color=nodragcolor)
Xveldrag2 = gdots(size=3, color=drag2color)
Xvelair = gdots(size=3, color=aircolor)

Yvel = gdisplay(x=263, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                title='V_y(t)')
Yvel.display.exit = False
Yvelnodrag = gdots(size=3, color=nodragcolor)
Yveldrag2 = gdots(size=3, color=drag2color)
Yvelair = gdots(size=3, color=aircolor)

Xaccel = gdisplay(x=523, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                  title='A_x(t)')
Xaccel.display.exit = False
Xaccelnodrag = gdots(size=3, color=nodragcolor)
Xacceldrag2 = gdots(size=3, color=drag2color)
Xaccelair = gdots(size=3, color=aircolor)

Yaccel = gdisplay(x=787, y=0, width=262, height=100, background=color.white, xmin=0, xmax=12, ymin=-vmax, ymax=vmax,
                  title='A_y(t)')
Yaccel.display.exit = False
Yaccelnodrag = gdots(size=3, color=nodragcolor)
Yacceldrag2 = gdots(size=3, color=drag2color)
Yaccelair = gdots(size=3, color=aircolor)

# Dummy = gdisplay(x=523, y=200, width=262, height=100, background=color.orange, title = "!")
# Dummy display that never gets redone so program doesn't die on reset - is this a bug?

# loop until we quit the program
while 1:
    cw.interact()  # check to see if any buttons or sliders have been touched

    if not (GO):  # wait until we say go
        continue

    floor = box(pos=(0, -0.4 * setrange, 0), length=2 * setrange, height=setrange / 30., width=setrange,
                color=color.green)  # create ground

    # set up timing
    dt = 0.05  # time step
    t = 0  # initial time

    # Three balls with same starting location, velocity, and acceleration
    if (NoDragBall == 1):
        nodrag = sphere(pos=vector(nodragpos), radius=0.02 * setrange, color=color.blue)
        nodrag.velocity = vector(speed * math.cos(angle), speed * math.sin(angle), 0)
        nodrag.acceleration = vector(grav.x, grav.y, grav.z)  # copy values and sever all future ties
        nodrag.trail = curve(color=nodragcolor)  # draw a line showing where ball has been

    if (AirBall == 1):
        air = sphere(pos=vector(airpos), radius=0.02 * setrange, color=color.red)
        air.velocity = vector(speed * math.cos(angle), speed * math.sin(angle), 0)
        air.acceleration = vector(grav.x, grav.y, grav.z)
        air.trail = curve(color=aircolor)

    if (Drag2Ball == 1):
        drag2 = sphere(pos=vector(drag2pos), radius=0.02 * setrange, color=color.green)
        drag2.velocity = vector(speed * math.cos(angle), speed * math.sin(angle), 0)
        drag2.acceleration = vector(grav)  # another way to copy values and sever ties
        drag2.trail = curve(color=drag2color)

    # Initialize each line in the graphs
    if (NoDragBall == 1):
        Xvelnodrag.plot(gdisplay=Xvel.display, pos=(t, nodrag.velocity.x))
        Yvelnodrag.plot(gdisplay=Yvel.display, pos=(t, nodrag.velocity.y))
        Xaccelnodrag.plot(gdisplay=Xaccel.display, pos=(t, nodrag.acceleration.x))
        Yaccelnodrag.plot(gdisplay=Yaccel.display, pos=(t, nodrag.acceleration.y))

    if (AirBall == 1):
        Xvelair.plot(gdisplay=Xvel.display, pos=(t, air.velocity.x))
        Yvelair.plot(gdisplay=Yvel.display, pos=(t, air.velocity.y))
        Xaccelair.plot(gdisplay=Xaccel.display, pos=(t, air.acceleration.x))
        Yaccelair.plot(gdisplay=Yaccel.display, pos=(t, air.acceleration.y))

    if (Drag2Ball == 1):
        Xveldrag2.plot(gdisplay=Xvel.display, pos=(t, drag2.velocity.x))
        Yveldrag2.plot(gdisplay=Yvel.display, pos=(t, drag2.velocity.y))
        Xacceldrag2.plot(gdisplay=Xaccel.display, pos=(t, drag2.acceleration.x))
        Yacceldrag2.plot(gdisplay=Yaccel.display, pos=(t, drag2.acceleration.y))

    arrowcounter = 1  # only draw arrows sometimes

    hitnodrag = hitdrag2 = hitair = False  # set up to check for everything having landed
    while not (hitnodrag and hitdrag2 and hitair):  # until all three have landed; w/ margin
        rate(100)  # how fast the simulation runs
        cw.interact()  # make it possible to stop mid-flight
        if not (GO):
            continue

        arrowcounter = arrowcounter + 1
        t = t + dt

        if (NoDragBall == 1):
            if nodrag.pos.y > bottom:
                # physics
                nodrag.pos = nodrag.pos + nodrag.velocity * dt + 0.5 * nodrag.acceleration * dt ** 2
                nodrag.trail.append(pos=nodrag.pos)
                nodrag.velocity = nodrag.velocity + grav * dt
                # make graphs
                Xvelnodrag.plot(gdisplay=Xvel.display, pos=(t, nodrag.velocity.x))
                Yvelnodrag.plot(gdisplay=Xvel.display, pos=(t, nodrag.velocity.y))
                Xaccelnodrag.plot(gdisplay=Xvel.display, pos=(t, nodrag.acceleration.x))
                Yaccelnodrag.plot(gdisplay=Xvel.display, pos=(t, nodrag.acceleration.y))
                # draw arrows showing current velocity and acceleration
                if arrowcounter == 30:
                    if (NoDragV == 1):
                        nodragVertV = arrow(pos=nodrag.pos, axis=(0, nodrag.velocity.y, 0), color=nodragcolor)
                        nodragHorV = arrow(pos=nodrag.pos, axis=(nodrag.velocity.x, 0, 0), color=nodragcolor)
                    if (NoDragA == 1):
                        nodragVertA = arrow(pos=nodrag.pos, axis=(0, nodrag.acceleration.y * 2, 0), color=(0, 0, 0.4))
                        nodragHorA = arrow(pos=nodrag.pos, axis=(nodrag.acceleration.x * 2, 0, 0), color=(0, 0, 0.4))
                    arrowcounter = 1
            else:
                hitnodrag = True
        else:
            hitnodrag = True

        if (AirBall == 1):
            if air.pos.y > bottom:
                # physics
                air.pos = air.pos + air.velocity * dt + 0.5 * air.acceleration * dt ** 2
                air.trail.append(pos=air.pos)  # this actually adds points to draw the line
                air.velocity = air.velocity + air.acceleration * dt
                air.acceleration = grav - constant * air.radius * air.velocity  # air resistance changes acceleration
                # make graphs
                Xvelair.plot(gdisplay=Xvel.display, pos=(t, air.velocity.x))
                Yvelair.plot(gdisplay=Xvel.display, pos=(t, air.velocity.y))
                Xaccelair.plot(gdisplay=Xvel.display, pos=(t, air.acceleration.x))
                Yaccelair.plot(gdisplay=Xvel.display, pos=(t, air.acceleration.y))
                # draw arrows showing current velocity and acceleration
                if arrowcounter == 10:  # draw arrows at diff positions for diff balls
                    if (AirV == 1):
                        airVertV = arrow(pos=air.pos, axis=(0, air.velocity.y, 0), color=aircolor)
                        airHorV = arrow(pos=air.pos, axis=(air.velocity.x, 0, 0), color=aircolor)
                    if (AirA == 1):
                        airVertA = arrow(pos=air.pos, axis=(0, air.acceleration.y * 2, 0), color=(0.4, 0, 0))
                        airHorA = arrow(fpos=air.pos, axis=(air.acceleration.x * 2, 0, 0), color=(0.4, 0, 0))
            else:
                hitair = True
        else:
            hitair = True

        if (Drag2Ball == 1):
            if drag2.pos.y > bottom:  # skip if it has already landed
                # physics
                drag2.pos = drag2.pos + drag2.velocity * dt + 0.5 * drag2.acceleration * dt ** 2
                drag2.trail.append(pos=drag2.pos)
                drag2.velocity = drag2.velocity + drag2.acceleration * dt
                drag = vector(-sign(drag2.velocity.x) * drag2.velocity.x ** 2,
                              -sign(drag2.velocity.y) * drag2.velocity.y ** 2, 0)
                drag2.acceleration = grav + constant * drag2.radius * drag
                # make graphs
                Xveldrag2.plot(gdisplay=Xvel.display, pos=(t, drag2.velocity.x))
                Yveldrag2.plot(gdisplay=Xvel.display, pos=(t, drag2.velocity.y))
                Xacceldrag2.plot(gdisplay=Xvel.display, pos=(t, drag2.acceleration.x))
                Yacceldrag2.plot(gdisplay=Xvel.display, pos=(t, drag2.acceleration.y))
                # draw arrows showing current velocity and acceleration
                if arrowcounter == 20:
                    if (Drag2V == 1):
                        drag2VertV = arrow(pos=drag2.pos, axis=(0, drag2.velocity.y, 0), color=drag2color)
                        drag2HorV = arrow(pos=drag2.pos, axis=(drag2.velocity.x, 0, 0), color=drag2color)
                    if (Drag2A == 1):
                        drag2VertA = arrow(pos=drag2.pos, axis=(0, drag2.acceleration.y * 2, 0), color=(0, 0.4, 0))
                        drag2HorA = arrow(pos=drag2.pos, axis=(drag2.acceleration.x * 2, 0, 0), color=(0, 0.4, 0))
            else:
                hitdrag2 = True
        else:
            hitdrag2 = True

    gobtn.button.color = color.green
    GO = 0  # wait to rerun until we say go again