# Web VPython 3.2 WASM

import numpy as np
from vpython import *


def SetCylinderFromCN(cn, a):
    """
    SetCylinderFromCN takes a complex number  cn  and an arrow object  a .
    This version assumes 'a' is a vp.cylinder and sets the height of
    the vp.cylinder based on the real part, and the radius based
    on the imaginary part. The radius is never set to less than 5% of the
    magnitude of the complex number. The vp.color is set based on the phase.
    """
    a.axis.z = cn.real
    a.radius = max(0.05 * abs(cn), abs(cn.imag) / 6.0)
    phase = np.arctan2(cn.imag, cn.real) / (2 * np.pi)
    a.color = vp.color.hsv_to_rgb(vp.vec(phase, 1, 1))


scene.background = vp.color.white
hbar = 1.0  # use units where hbar = 1
m = 1.0  # and m=1.0
NA = 20  # how many arrows per dimension NAxNA grid
NA2 = int(NA / 2)  # integer version of NA/2
NX = [1, 2, 3, 5, 6, 7, 9, 10]  # which fourier terms in x direction
NY = [1, 2, 3, 5, 6, 7, 9, 10]  # which fourier terms in y direction
a = 10.0  # size of box
dt = 0.1  # time step
t = 0.0  # start time at zero...
cylinderScale = 20.0  # just make the arrows long enough to see..
eigenstates = {}  # dictionary for precomputed eigenstates
coefs = {}  # dictionary for precomputed fourier coef.
omegas = {}  # dictionary for energies
kn_max = np.pi * NX[-1] / a
km_max = np.pi * NY[-1] / a
Emax = ((hbar * kn_max) ** 2 + (hbar * km_max) ** 2) / (2 * m)
omegaMax = Emax / hbar
dt = np.pi / (10 * omegaMax)  # come up with a sensible dt

RSdict = {'runStop': False}

x, y = np.meshgrid(np.linspace(0, a, NA), np.linspace(0, a, NA))

#
#
# draw the boundaries of the ISW in 2D

boundary_radius = a / 100

vp.cylinder(pos=vp.vec(-a / 2, -a / 2, 0), axis=vp.vec(a, 0, 0), color=vp.color.blue, radius=boundary_radius)
vp.cylinder(pos=vp.vec(-a / 2, -a / 2, 0), axis=vp.vec(0, a, 0), color=vp.color.blue, radius=boundary_radius)
vp.cylinder(pos=vp.vec(a / 2, -a / 2, 0), axis=vp.vec(0, a, 0), color=vp.color.blue, radius=boundary_radius)
vp.cylinder(pos=vp.vec(-a / 2, a / 2, 0), axis=vp.vec(a, 0, 0), color=vp.color.blue, radius=boundary_radius)

r0 = vector(-a / 2, -a / 2, 0)  # place origin of arrows

#
# build vp.cylinders.... in 2-D space, store them in a set of nested lists
#

alist = []
for i in range(NA):
    sublist = []
    alist.append(sublist)
    for j in range(NA):
        r = r0 + vector(x[i, j], y[i, j], 0)
        sublist.append(vp.cylinder(pos=r, axis=(0, 0, 1), color=vp.color.red))

#
# compute the eigenstates and store them in a dictionary 'eigenstates'
#

for nx in NX:
    for ny in NY:
        psinxmy = np.sin(nx * np.pi * x / a) * np.sin(ny * np.pi * y / a)  # compute the n,m energy eigenstate
        psinxmy = psinxmy / np.sqrt((abs(psinxmy) ** 2).sum())  # normalize it.
        eigenstates[(nx, ny)] = psinxmy

psi0 = np.zeros((NA, NA), complex)
psi0[:NA2, :NA2] = 1.0
psi0 = psi0 / np.sqrt((abs(psi0) ** 2).sum())  # get psi at t=0, normalized

omega0 = hbar * np.pi ** 2 / (2 * m * a ** 2)  # compute factor omega0

for nmPair in eigenstates.keys():
    nx, ny = nmPair
    psinxmy = eigenstates[nmPair]  # get nth basis
    cnm = ((psi0[:NA2, :NA2] * psinxmy[:NA2, :NA2]).sum())  # compute fourier coef.
    coefs[nmPair] = cnm  # save it.
    omega = omega0 * (nx ** 2 + ny ** 2)  # get omega for nmPair, multiple of omega0
    omegas[nmPair] = omega  # save it.

#
# build up psi via fourier series
#

psi = np.zeros((NA, NA), complex)  # initialize psi

for nmPair in eigenstates.keys():
    psi += coefs[nmPair] * eigenstates[nmPair]

for i in range(NA):
    for j in range(NA):
        SetCylinderFromCN(cylinderScale * psi[i, j], alist[i][j])


def toggleRun(e):
    RSdict['runStop'] = not RSdict['runStop']
    setRunLabel()


def setRunLabel():
    if RSdict['runStop']:
        runStopButton.text = "Pause"
    else:
        runStopButton.text = "Resume"


runStopButton = button(bind=toggleRun, align="left", text="Start")

while True:
    rate(20.0 / dt)

    if RSdict['runStop']:
        t += dt
        psi = np.zeros((NA, NA), complex)  # initialize psi

        #
        # Here's where you put in your code to compute the
        # wavefunction psi, at later times
        #
        for nmPair in eigenstates.keys():
            psi += coefs[nmPair] * eigenstates[nmPair] * np.exp(1j * omegas[nmPair] * t)

        for i in range(NA):
            for j in range(NA):
                SetCylinderFromCN(cylinderScale * psi[i, j], alist[i][j])
