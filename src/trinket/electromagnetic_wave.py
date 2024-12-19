### EMWave.py
### Electromagnetic Plane Wave visualization (requires VPython)
### Rob Salgado
### salgado@physics.syr.edu     http://physics.syr.edu/~salgado/
### v0.5  2001-11-07 tested on Windows 2000
### v0.51 2003-02-16 tested on Windows 2000
###         with Python-2.1.1.exe and VPython-2001-10-31.exe
### v1.00 2004-03-21 tested on Windows 2000
###         with Python-2.3.3.exe and VPython-2003-10-15.exe
###
### Updated by Zeger Hendrikse: https://github.com/zhendrikse/physics-in-python/
###

from vpython import *

show_neighboring_waves = 1

"""
Electromagnetic Plane Wave visualization (v1.00) 2004-03-21
Rob Salgado (salgado@physics.syr.edu)

The blue arrows are Electric Field vectors.
The red arrows are Magnetic Field vectors.

The thick green vector representing
dE/dt ("time-rate-of-change-of-the-magnitude-of-the-electric-field")
is associated with the spatial arrangement of the magnetic field according to
the AMPERE-MAXWELL Law (as evaluated on the green loop).
[Use the RightHandRule to determine the sense of circulation on the green loop.
The direction of change of the electric field is determined by your thumb.]

The thick yellow vector representing
dB/dt ("time-rate-of-change-of-the-magnitude-of-the-magnetic-field")
is associated with the spatial arrangement of the electric field according to
the FARADAY Law (as evaluated on the yellow loop).
[Use the RightHandRule to determine the sense of circulation on the yellow loop.
The direction of change of the magnetic field is determined by the
opposite direction of where your thumb points (due to Faraday's minus sign).]

Intuitively, dE/dt tells the current value of E at that point to look like
the value of E at the point to its left (in this example).
In other words, the pattern of the electric field moves to the RIGHT.

Similarly, dB/dt tells the current value of B at that point to look like
the value of B at the point to its left (in this example).
In other words, the pattern of the magnetic field moves to the RIGHT.

Thus, this electromagnetic plane wave moves to the RIGHT.

WHAT YOU CAN DO:
    move the mouse to reposition the loops
    click the mouse to start and stop the animation
    change the showNeighboringWaves parameter to hide or show the other waves
"""

scene = canvas(title="EM Wave (Rob Salgado), updated by Zeger Hendrikse")
scene.caption += "\\( \\bigg ( v^2\\nabla^2 - \\frac {\partial^2}{{\partial t}^2} \\bigg) \\vec{E} = 0, \\bigg ( v^2\\nabla^2 - \\frac {\partial^2}{{\partial t}^2} \\bigg) \\vec{B} = 0, v=\\dfrac {1} {\\sqrt {\mu \epsilon}} \\)\n where \\( v \\) is the speed of light (i.e. phase velocity) in a medium with permeability μ, and permittivity ε"
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

# scene.autoscale = 0
# scene.range = vector(6, 6, 6)
# scene.forward = vector(-1.0, -1.250, -4)
# scene.newzoom = 1
# scene.background = color.black
#
electric_field = []
magnetic_field = []

electric_field_colors = [color.blue, color.yellow, color.cyan]
magnetic_field_colors = [color.red, color.green, color.magenta]

time_derivative_colors = [color.green, color.yellow]

electric_field_max = 4.0
wave_separation = 10.0
#
magnify = 2.5
S = 20
#
fi = 0

for i in range(-S, S):
    Ev = arrow(pos=vector(i, 0, 0), axis=vector(0, 0, 0), color=electric_field_colors[0], shaftwidth=0.2, fixedwidth=1)
    electric_field.append(Ev)

for i in range(-S, S):
    Bv = arrow(pos=vector(i, 0, 0), axis=vector(0, 0, 0), color=magnetic_field_colors[0], shaftwidth=0.2, fixedwidth=1)
    magnetic_field.append(Bv)

if show_neighboring_waves > 0:
    for j in range(1, 3):
        for i in range(-S, S):
            Ev = arrow(pos=vector(i, 0, j * wave_separation), axis=vector(0, 0, 0), color=electric_field_colors[0], shaftwidth=0.2,
                       fixedwidth=1)
            electric_field.append(Ev)
        for i in range(-S, S):
            Bv = arrow(pos=vector(i, 0, j * wave_separation), axis=vector(0, 0, 0), color=magnetic_field_colors[0], shaftwidth=0.2,
                       fixedwidth=1)
            magnetic_field.append(Bv)

        for i in range(-S, S):
            Ev = arrow(pos=vector(i, 0, -j * wave_separation), axis=vector(0, 0, 0), color=electric_field_colors[0], shaftwidth=0.2,
                       fixedwidth=1)
            electric_field.append(Ev)
        for i in range(-S, S):
            Bv = arrow(pos=vector(i, 0, -j * wave_separation), axis=vector(0, 0, 0), color=magnetic_field_colors[0], shaftwidth=0.2,
                       fixedwidth=1)
            magnetic_field.append(Bv)

height = wave_separation / 2.
FaradayLoop = curve(pos=[vector(-1, -height, 0), vector(-1, height, 0), vector(1, height, 0), vector(1, -height, 0),
                         vector(-1, -height, 0)],
                    color=time_derivative_colors[1])
AmpereLoop = curve(pos=[vector(-1, 0, -height), vector(-1, 0, height), vector(1, 0, height), vector(1, 0, -height),
                        vector(-1, 0, -height)],
                   color=time_derivative_colors[0])

dBdt = arrow(pos=vector(fi, 0, 0), axis=vector(0, 0, 0), color=time_derivative_colors[1], shaftwidth=0.35, headwidth=0.7,
             fixedwidth=1)
dEdt = arrow(pos=vector(fi, 0, 0), axis=vector(0, 0, 0), color=time_derivative_colors[0], shaftwidth=0.35, headwidth=0.7,
             fixedwidth=1)
dBdtlabel = label(pos=vector(fi, 0, 0), text='dB/dt', color=time_derivative_colors[1], xoffset=20, yoffset=12, height=16, border=6)
dEdtlabel = label(pos=vector(fi, 0, 0), text='dE/dt', color=time_derivative_colors[0], xoffset=20, yoffset=12, height=16, border=6)

wavelength = S
omega = 0.1
t = 0
k = 2 * pi / wavelength
run_toggle = 1


def on_mouse_click():
    global run_toggle
    run_toggle = (run_toggle + 1) % 2

scene.bind('click', on_mouse_click)

while True:

    newfi = int(scene.mouse.pos.x)
    newfi = max(min(newfi, S - 2), -(S - 2))

    phase = k * (newfi - S) - omega * t
    if fi != newfi:  # MOVE THE LOOP
        electric_field[S + fi - 1].color = electric_field_colors[0]
        electric_field[S + fi + 1].color = electric_field_colors[0]
        magnetic_field[S + fi - 1].color = magnetic_field_colors[0]
        magnetic_field[S + fi + 1].color = magnetic_field_colors[0]
        fi = newfi
        electric_field[S + fi - 1].color = electric_field_colors[1]
        electric_field[S + fi + 1].color = electric_field_colors[1]
        magnetic_field[S + fi - 1].color = magnetic_field_colors[1]
        magnetic_field[S + fi + 1].color = magnetic_field_colors[1]


        # FaradayLoop.x[0] = fi - 1

        # FaradayLoop.pos[0].x = fi - 1
        # FaradayLoop.pos[1].x = fi - 1
        # FaradayLoop.pos[2].x = fi + 1
        # FaradayLoop.pos[3].x = fi + 1
        # FaradayLoop.pos[4].x = FaradayLoop.pos[0].x
        #
        # AmpereLoop.pos[0].x = fi - 1
        # AmpereLoop.pos[1].x = fi - 1
        # AmpereLoop.pos[2].x = fi + 1
        # AmpereLoop.pos[3].x = fi + 1
        # AmpereLoop.pos[4].x = AmpereLoop.pos[0].x

    # UPDATE THE FIELDS
    for i in arange(0, len(electric_field)):
        amp = electric_field_max * sin(k * (i % (2 * S) - S) - omega * t)
        electric_field[i].axis.y = amp
        magnetic_field[i].axis.z = amp

    # UPDATE THE dB/dt
    dBdt.axis.z = magnify * omega * electric_field_max * abs(cos(phase)) * -sign(
        dot(electric_field[S + newfi + 1].axis - electric_field[S + newfi - 1].axis, vector(0, 1, 0)))
    if dot(dBdt.axis, magnetic_field[S + newfi].axis) > 0:
        dBdtlabel.text = 'dB/dt>0'
        dBdt.pos = vector(newfi, 0, magnetic_field[S + newfi].axis.z)
    elif dot(dBdt.axis, magnetic_field[S + newfi].axis) < 0:
        dBdtlabel.text = 'dB/dt<0'
        dBdt.pos = vector(newfi, 0, magnetic_field[S + newfi].axis.z - dBdt.axis.z)
    else:
        dBdtlabel.text = 'dB/dt=0'
        dBdt.pos = vector(newfi, 0, magnetic_field[S + newfi].axis.z)
    dBdtlabel.pos = magnetic_field[S + newfi].pos + magnetic_field[S + newfi].axis

    # UPDATE THE dE/dt
    dEdt.axis.y = magnify * omega * electric_field_max * abs(cos(phase)) * sign(
        dot(magnetic_field[S + newfi + 1].axis - magnetic_field[S + newfi - 1].axis, vector(0, 0, -1)))
    if dot(dEdt.axis, electric_field[S + newfi].axis) > 0:
        dEdtlabel.text = 'dE/dt>0'
        dEdt.pos = vector(newfi, electric_field[S + newfi].axis.y, 0)
    elif dot(dEdt.axis, electric_field[S + newfi].axis) < 0:
        dEdtlabel.text = 'dE/dt<0'
        dEdt.pos = vector(newfi, electric_field[S + newfi].axis.y - dEdt.axis.y, 0)
    else:
        dEdtlabel.text = 'dE/dt=0'
        dEdt.pos = vector(newfi, electric_field[S + newfi].axis.y, 0)
    dEdtlabel.pos = electric_field[S + newfi].pos + electric_field[S + newfi].axis

    if run_toggle > 0:
        t += 0.1

    rate(60)  # v0.51 suggested by Jonathan Brandmeyer to reduce mouse polling when idle
