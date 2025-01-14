import vpython as vp
import numpy as np

rate = vp.rate

vp.scene.background = vp.color.white

gd = vp.graph(xtitle="t (sec)", ytitle="<x> (m)", width=800, height=300)
g1 = vp.gcurve(color=vp.color.black)

hbar = 1.05e-34  # Js
m = 0.067 * 9.1e-31  # and m_eff=kg
NA = 80  # how many arrows?
NA2 = int(NA / 2)  # half of the arrows
a = 5.34e-9  # width for 5 bound states and 1eV well depth.

x = np.linspace(-2.0 * a, 2.0 * a, NA)  # NA locations from -2a to 2a

z0 = 6.0  # Not a great choice. Why not? Pick a better one
k0 = z0 / a  # get k0

#
# numerical solutions for z when z0 = 2.1*pi, you should find a better z0 and
# find solutions for that choice.
#

z1 = 1.35
z2 = 2.67

k1 = k0 * z1 / z0
k2 = k0 * z2 / z0
kap1 = np.sqrt(k0 ** 2 - k1 ** 2)
kap2 = np.sqrt(k0 ** 2 - k2 ** 2)

E1 = -(hbar * kap1) ** 2 / (2.0 * m)
E2 = -(hbar * kap2) ** 2 / (2.0 * m)

w1 = E1 / hbar
w2 = E2 / hbar
wn = [w1, w2]
T = 2 * np.pi / (w2 - w1)  # the approximate period of oscillation

t = 0.0
dt = T / 200.0  # a small fraction of a period

psis = np.zeros((2, NA), np.double)


def f1(x):
    return np.cos(k1 * x)


def f2(x):
    return np.sin(k2 * x)


def f3(x):
    return f1(a) * np.exp(-abs(kap1 * x)) / np.exp(-abs(kap1 * a))


def f4(x):
    return np.sign(x) * f2(a) * np.exp(-abs(kap2 * x)) / np.exp(-abs(kap2 * a))


psis[0] = np.piecewise(x, [x < -a, (x >= -a) & (x <= a), x > a], [f3, f1, f3])
psis[0] = psis[0] / np.sqrt((abs(psis[0]) ** 2).sum())
psis[1] = np.piecewise(x, [x < -a, (x >= -a) & (x <= a), x > a], [f4, f2, f4])
psis[1] = psis[1] / np.sqrt((abs(psis[1]) ** 2).sum())

# Equal parts 1 and 2
c1 = 1.0 / np.sqrt(2)
c2 = 1.0 / np.sqrt(2)

cn = [c1, c2]  # array of amplitudes
t = 0.0  # start at t=0

psi = np.zeros(NA, complex)  # construct psi at time '0'
for i in range(len(cn)):
    psi = psi + cn[i] * psis[i]

arrowScale = a / psis[0][NA2]  # scale to make the middle of psis[0] about 3a high


def SetArrowFromCN(cn, a):
    """
    SetArrowWithCN takes a complex number  cn  and an arrow object  a .
    It sets the  y  and  z  components of the arrow s axis to the real
    and imaginary parts of the given complex number.

    Just like Computing Project 1, except y and z for real/imag.
    """
    a.axis.y = cn.real
    a.axis.z = cn.imag
    a.axis.x = 0.0


alist = []
for i in range(NA):
    ar = vp.arrow(pos=vp.vec(x[i], 0, 0), axis=vp.vec(0, a, 0),
                  shaftwidth=0.02 * a, color=vp.color.red)
    alist.append(ar)
    SetArrowFromCN(arrowScale * psi[i], alist[i])

#
# Now, all the arrows are made, and the basis functions and coefficients are
# set. Create a loop that produces the correct time evolutions.
#

while t < 2 * T:
    rate(30)

    t = t + dt
    psi = np.zeros(NA, complex)
    for i in range(2):
        psi = psi + cn[i] * psis[i] * np.exp(-1j * wn[i] * t)

    for i in range(NA):
        SetArrowFromCN(arrowScale * psi[i], alist[i])

    xexp = (x * abs(psi * psi)).sum()
    g1.plot(pos=(t, xexp))
