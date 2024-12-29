from vpython import *

from ..toolbox.harmonic_oscillator import HarmonicOscillator
from ..toolbox.ball import Ball

title="""Quantum oscillator

&#x2022; Original <a href="https://lectdemo.github.io/virtual/06_oscillator.html">06_oscillator.py</a> by Ruth Chabay 2004
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

Click on an energy level to put the oscillator into that state

"""

scene.x = scene.y = 0
scene.width = scene.height = 600
scene.background = color.white
#scene.foreground = color.black
scene.title = title

spring_frame = canvas(pos=vector(vector(0, 0, 0)), axis=norm(vector(1, 0, 0)))


# class helix:
#     def __init__(self, pos=vector(0, 0, 0), axis=vector(1, 0, 0), radius=0.2, coils=5,
#                  thickness=None, color=None):
#         self.frame = canvas(pos=vector(pos), axis=norm(axis))
#         self.pos = vector(pos)
#         self.axis = vector(axis)
#         self.length = mag(axis)
#         self.radius = radius
#         self.coils = coils
#         if thickness is None:
#             thickness = radius / 20.
#         k = self.coils * (2. * pi / self.length)
#         dx = (self.length / self.coils) / 12.
#         self.positions = [vector(xx, radius * sin(k * xx), radius * cos(k * xx)) for xx in arange(0, self.length + dx, dx)]
#         #xx = arange(0, self.length + dx, dx)
#         self.helix = curve(frame=self.frame, radius=thickness / 2., color=color, pos=self.positions)
#
#     def modify(self, pos=None, axis=None, length=None):
#         oldlength = self.length
#         if not pos is None:
#             self.frame.pos = vector(pos)
#             self.pos = vector(pos)
#         if not axis is None:
#             self.axis = vector(axis)
#             self.frame.axis = vector(axis)
#             self.length = mag(axis)
#         if not length is None:
#             self.length = length
#         k = self.coils * (2. * pi / self.length)
#         dx = (self.length / self.coils) / 12.
#         x = 0.
#         for index in range(len(self.positions)):
#             #self.helix.pos[index][0] = self.helix.pos[index][0] * self.length / oldlength
#             self.helix.modify(index, pos=self.positions[index] * self.length / oldlength)
#             x = x + dx


def U(s):
    global ks
    Us = 0.5 * ks * s ** 2
    return Us


showguides = 0
L0 = 10
U0 = -10
dU = 2
# ball_1 = sphere(pos=vector(-L0, 0.5 * 5 ** 2, 0), radius=0.5, color=color.red)
# ball_2 = sphere(pos=vector(0, 0.5 * 5 ** 2, 0), radius=0.5, color=color.cyan)
mass = 0.025  ## 14*1.7e-27
ball_1 = Ball(position=vector(-L0, 0.5 * 5 ** 2, 0), radius=0.5, color=color.red, mass=mass)
ball_2 = Ball(position=vector(0, 0.5 * 5 ** 2, 0), radius=0.5, color=color.cyan, mass=mass)
ks = 1.2  ## 200
omega = sqrt(ks / ball_2.mass)
##print omega
# spring = helix(pos=ball_1.pos, axis=vector(ball_2.pos - ball_1.pos), radius=0.40, coils=10,
#               thickness=0.2, color=vector(.7, .5, 0))

oscillator = HarmonicOscillator(ball_1, ball_2, spring_constant=ks, radius=0.40, coils=10,
                                thickness=0.2, colour=vector(.7, .5, 0))

equilibrium_position = cylinder(pos=vector(0, U0, 0), axis=vector(0, 18, 0), radius=0.1, color=color.green)

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

mouse_clicked = False
def on_mouse_click():
    global mouse_clicked
    mouse_clicked = True


spring_frame.bind("click", on_mouse_click)

t = 0.0
dt = 0.003
old_level = None
current_level = None
run = False
amplitude = 1

while 1:
    if (not mouse_clicked) and run:
        rate(200)
        oscillator.increment_by(dt)
        t += dt
    else:
        spring_frame.waitfor("click")
        selected_level = spring_frame.mouse.pick
        if selected_level is None or not type(selected_level) is cylinder:
            continue
        if selected_level in energy_levels:
            old_level = current_level
            current_level = selected_level
            current_level.color = color.red
            if old_level is not None:
                old_level.color = color.white
            amplitude = abs(current_level.pos.x)
            oscillator.pull(amplitude * cos(omega * t))
            vline1.pos = current_level.pos
            vline2.pos = current_level.pos + current_level.axis
            run = True
            mouse_clicked = False
        elif scene.mouse.pos.y > .5 * ks * 5.2 ** 2 + U0:
            print("Wanneer kom ik hier?")
            run = False
            if current_level is not None:
                current_level.color = color.white
            while ball_2.position.x < 2 * L0:
                rate(200)
                #ball_2.position.x += L0 / 100
                oscillator.pull(L0 / 100)
            continue
        else:
            continue

