################
# Interference  #
# Michael Malahe#
# 2006          #
################

# Instructions:
# The leftmost and rightmost buttons cycle through the wave types coming from either direction.
# The start/pause button is pretty self-explanatory.
# The stop button stops the animation entirely, so you can start at the beginning again with changes.
# When the auto/manual button is set to manual, the start/pause button becomes a frame-by-frame clicker.
# The last parameter, globstep, should be increased on slow machines and reduced on faster ones.

# Modules
from vpython import *

# Parameters
observer_location = 0
tlen = 20
speed = 1.5
frame_rate = 35
theta_max = 10
globstep = 0.1

# Constants
t = 0
dt = 1 / frame_rate


# Wave class
class wave:
    def __init__(self, function, xmin, xmax, step, pos, render):
        self.pos = pos
        self.function = function
        if render == 1:
            self.curve = []
            self.xmin = xmin
            self.xmax = xmax
            self.step = step
            for x in arange(xmin, xmax, step):
                exec("y=" + function + "(x)")
                self.curve.append((x, y))
            lol = [(a[0] + pos[0], a[1] + pos[1]) for a in self.curve]
            lol.insert(0, (-tlen, 0))
            lol.append((tlen, 0))
            self.render = curve(pos=lol, radius=0.03)
        else:
            pass

    def interfere(self, wave):
        self.curve = []
        for x in arange(-tlen, tlen, self.step):
            pos1 = x - self.pos[0]
            pos2 = x - wave.pos[0]
            exec("y=" + self.function + "(pos1)" + "+" + wave.function + "(pos2)")
            self.curve.append((x, y))
        self.render.pos = self.curve


# Additional wave types
def triangle(x):
    if x <= -1 or x >= 1:
        y = 0
    else:
        y = 1 - abs(x)
    return y


def lopsided(x):
    if x <= -1 or x >= 0.5:
        y = 0
    elif x >= 0:
        y = 2 * (0.5 - x)
    elif x < 0:
        y = 1 + x
    return y


def square(x):
    if x <= -1 or x >= 1:
        y = 0
    else:
        y = 1
    return y


def sqsin(x):
    if x < -pi or x > pi:
        y = 0
    else:
        y = (sin(x)) ** 2
    return y


def sqtri(x):
    if x < -2:
        y = 0
    if x < 0 and x >= -2:
        y = -1
    if x >= 0 and x < 2:
        y = -abs(-x + 1) + 1
    if x >= 2:
        y = 0
    return y


def sine(x):
    if x < -pi or x > pi:
        y = 0
    else:
        y = sin(x)
    return y


# 3d Scene
animation = canvas(title='Pulse',
                   width=1024, height=600, x=0, y=0,
                   center=vector(observer_location, 0, 0), background=vector(0, 0, 0))
# scene.autoscale = 0
animation.userspin = 0
# scene.range = (10,7,1)
obs = curve(pos=[vec(observer_location, 1.5, 0), vec(observer_location, -1.5, 0)], color=color.yellow, radius=0.03)


# Control functions
def togglego():
    if ss.go == 1:
        ss.go = 0
        ss.text = "Start"
    elif ss.go == 0:
        ss.go = 1
        ss.text = "Pause"

def wfcycle(wf):
    if wf.text == "1/2 sin":
        wf.text = "triangle"
    elif wf.text == "triangle":
        wf.text = "square"
    elif wf.text == "square":
        wf.text = "lopsided"
    elif wf.text == "lopsided":
        wf.text = "sine"
    elif wf.text == "sine":
        wf.text = "sqsin"
    elif wf.text == "sqsin":
        wf.text = "sqtri"
    elif wf.text == "sqtri":
        wf.text = "1/2 sin"


def stop():
    #print("TODO: HOW TO STOP?")
    what_is_this_variable.stp = 1


def autotoggle():
    print("TODO: HOW TO AUTO TEXT?")
    # if auto.text == "Auto":
    #     auto.text = "Manual"
    # elif auto.text == "Manual":
    #     auto.text = "Auto"


def wfcycle_1():
    wfcycle(wf1)

def wfcycle_2():
    wfcycle(wf2)


# Control scene
my_scene = controls(title='Controls',
                    x=0, y=600, width=1024, height=150, range=50)
ss = button(pos=vec(-5, 0, 0), width=10, height=10,
            text='Start', bind=togglego)
wf1 = button(pos=vec(-15, 0, 0), width=10, height=10,
             text='sine', bind=wfcycle_1)
wf2 = button(pos=vec(25, 0, 0), width=10, height=10,
             text='sine', bind=wfcycle_2)
what_is_this_variable = button(pos=vec(5, 0, 0), width=10, height=10,
                               text='Stop', bind=stop())
auto = button(pos=vec(15, 0, 0), width=10, height=10,
              text='Auto', bind=autotoggle)

# Main Loop:
while 1:
    ss.go = 0
    what_is_this_variable.stp = 0
    ss.text = "Start"
    #my_scene.interact()
    if ss.go == 1:
        t = 0
        try:
            wave1.render.visible = 0
            wave2.render.visible = 0
        except:
            pass
        # New wave
        if wf1.text == "1/2 sin":
            wave1 = wave("sine", 0, pi, globstep, (-15, 0), 1)
        else:
            wave1 = wave(wf1.text, -pi, pi, globstep, (-7, 0), 1)
        if wf2.text == "1/2 sin":
            wave2 = wave("sine", 0, pi, globstep, (15, 0), 0)
        else:
            wave2 = wave(wf2.text, -pi, pi, globstep, (7, 0), 0)
        # Motion Loop
        while t < theta_max:
            my_scene.interact()
            if ss.go == 1:
                rate(frame_rate)
                t += dt
                wave1.pos = (wave1.pos[0] + speed * dt, wave1.pos[1])
                wave2.pos = (wave2.pos[0] - speed * dt, wave2.pos[1])
                wave1.interfere(wave2)
            if auto.text == "Manual":
                ss.go = 0
                ss.text = "Start"
            if what_is_this_variable.stp == 1:
                t = theta_max
