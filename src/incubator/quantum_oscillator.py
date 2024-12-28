from vpython import *

## Ruth Chabay 2003-03-18
## Semi-classical visualization of quantum oscillator.

scene.x = scene.y = 0
scene.width = scene.height = 600
scene.background = color.white
scene.foreground = color.black
scene.title = "Quantum oscillator\n\nClick on an energy level to put the oscillator into that state"


class helix:
    def __init__(self, pos=vector(0, 0, 0), axis=vector(1, 0, 0), radius=0.2, coils=5,
                 thickness=None, color=None):
        self.frame = canvas(pos=vector(pos), axis=norm(axis))
        self.pos = vector(pos)
        self.axis = vector(axis)
        self.length = mag(axis)
        self.radius = radius
        self.coils = coils
        if thickness is None:
            thickness = radius / 20.
        k = self.coils * (2. * pi / self.length)
        dx = (self.length / self.coils) / 12.
        self.positions = [vector(xx, radius * sin(k * xx), radius * cos(k * xx)) for xx in arange(0, self.length + dx, dx)]
        #xx = arange(0, self.length + dx, dx)
        self.helix = curve(frame=self.frame, radius=thickness / 2., color=color, pos=self.positions)

    def modify(self, pos=None, axis=None, length=None):
        oldlength = self.length
        if not pos is None:
            self.frame.pos = vector(pos)
            self.pos = vector(pos)
        if not axis is None:
            self.axis = vector(axis)
            self.frame.axis = vector(axis)
            self.length = mag(axis)
        if not length is None:
            self.length = length
        k = self.coils * (2. * pi / self.length)
        dx = (self.length / self.coils) / 12.
        x = 0.
        for index in range(len(self.positions)):
            self.helix.pos[index][0] = self.helix.pos[index][0] * self.length / oldlength
            x = x + dx


def U(s):
    global ks
    Us = 0.5 * ks * s ** 2
    return Us


showguides = 0
L0 = 10
U0 = -10
dU = 2
m1 = sphere(pos=vector(-L0, 0.5 * 5 ** 2, 0), radius=0.5, color=color.red)
m2 = sphere(pos=vector(0, 0.5 * 5 ** 2, 0), radius=0.5, color=color.cyan)
m1.mass = 0.025  ## 14*1.7e-27
m2.mass = 0.025  ## 14*1.7e-27
ks = 1.2  ## 200
omega = sqrt(ks / m2.mass)
##print omega
spring = helix(pos=m1.pos, axis=vector(m2.pos - m1.pos), radius=0.40, coils=10,
               thickness=0.2, color=vector(.7, .5, 0))
eqpos = cylinder(pos=vector(0, U0, 0), axis=vector(0, 18, 0), radius=0.05, color=vector(.6, .6, .6))


curve_positions = [vector(xx, .5 * ks * xx ** 2 + U0, 0) for xx in arange(-5.8, 5.3, 0.1)]
well = curve(radius=0.2, pos=curve_positions, color=vector(.7, .7, .7))
well.append(pos=(8, .5 * ks * 5.2 ** 2 + U0, 0))

vline1 = cylinder(pos=vector(-5, U0, 0), axis=vector(0, 15, 0), radius=0.05, color=vector(.6, .6, .6),
                  visible=showguides)
vline2 = cylinder(pos=vector(5, U0, 0), axis=vector(0, 15, 0), radius=0.05, color=vector(.6, .6, .6),
                  visible=showguides)
scene.autoscale = 0
energy_levels = []
for Ux in arange(0.5 * dU, 7.51 * dU, dU):
    s = sqrt(2 * Ux / ks)
    l1 = cylinder(radius=0.2, pos=vector(-s, Ux + U0, 0), axis=vector(2 * s, 0, 0),
                  color=color.white)
    energy_levels.append(l1)

t = 0.0
dt = 0.003
old_level = None
level = None
RUN = 0

##TODO
Ampl = 1

mouse_clicked = False
def on_mouse_click():
    print("Mouse clicked")
    global mouse_clicked
    mouse_clicked = True

spring.frame.bind("click", on_mouse_click)

while 1:
    if not mouse_clicked and RUN:
        rate(200)
        m2.pos = vector(Ampl * cos(omega * t), m2.pos.y, m2.pos.z)
        spring.modify(axis=m2.pos - m1.pos)
        t += dt
    else:
        mouse_clicked = False
        selected_level = spring.frame.mouse.pick
        if selected_level is None or not type(selected_level) is cylinder:
            continue
        print("Picked a level" + str(selected_level.pos))
        if selected_level in energy_levels:
            old_level = level
            level = selected_level
            level.color = color.red
            if old_level is not None:
                old_level.color = color.white
            Ampl = abs(level.pos.x)
            vline1.pos = level.pos
            vline2.pos = level.pos + level.axis
            RUN = 1
        elif scene.mouse.pos.y > .5 * ks * 5.2 ** 2 + U0:
            RUN = 0
            if level is not None:
                level.color = color.white
            while m2.pos.x < 2 * L0:
                rate(200)
                m2.pos.x += L0 / 100
            continue
        else:
            continue
