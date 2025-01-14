import vpython as vp
import numpy as np


def SetArrowFromCN(psi, a):
    """
    Modify the arrow object, ‘a‘ to represent the complex number ‘psi‘ as a
    phasor.
    """
    a.axis.x = 0
    a.axis.y = psi.real
    a.axis.z = psi.imag


NA = 80  # how many arrows?
a = 15.0  # range of x is -a/2 to a/2 in units
# of $\sqrt{\hbar/m\omega}$
x = np.linspace(-a / 2, a / 2, NA)  # NA locations from -a/2 to a/2
NHs = 20
hs = np.zeros((NHs, NA), np.double)  # the hermite polynomials, an NHs x NA array
coefs = np.zeros(NHs, np.double)  # the coherent state coefficients, an NHs x 1 array
psis = np.zeros((NHs, NA), np.double)  # the stationary states, an NHs x NA array
hs[0] = 0 * x + 1.0  # zeroth Hermite Polynomial, H0
hs[1] = 2 * x  # first Hermite Polynomial, H1
#
# Compute the first NHs Hermite Polynomials,
# use recurrence relation to get the rest of the Hn(x)
#
# (see e.g., http://en.wikipedia.org/wiki/Hermite_polynomials#Recursion_relation)
#
for n in range(1, NHs - 1):
    hs[n + 1] = 2 * x * hs[n] - 2 * n * hs[n - 1]

#
# Get the stationary states using the hs array and compute the
# normalization factor in a loop to avoid overflow
#
normFactor = 1.0 / vp.pi ** 0.25
psis[0] = np.exp(-x ** 2 / 2)
for i in range(1, NHs):
    normFactor = normFactor / vp.sqrt(2.0 * i)
    psis[i] = normFactor * hs[i] * np.exp(-x ** 2 / 2)

#
# Now do the sum to compute the initial wavefunction
#
coefs = [1, 1, 1]  # equal parts n=(0,1,2) as an example
#
# Now do the sum to compute the initial wavefunction
#
psi = np.zeros(len(x), complex)
for m in range(len(coefs)):
    psi += coefs[m] * psis[m]
#
# Normalize!
#
psi = psi / vp.sqrt((abs(psi) ** 2).sum())

#
# build the arrows. Scale them on the screen by a factor
# of 3 so they look nice.
#
alist = []
for i in range(NA):
    alist.append(vp.arrow(pos=vp.vec(x[i], 0, 0), color=vp.color.red))
    SetArrowFromCN(3 * psi[i], alist[i])

gd = vp.graph(xtitle="t", ytitle="<x>", width=640, height=300)
gr = vp.gcurve(color=vp.color.black)

t = 0
dt = 0.01
while t < 4 * vp.pi:
    vp.rate(1.0 / dt)
    psi = np.zeros(len(x), complex)  # start with an empty wf array
    for m in range(len(coefs)):  # for each basis function
        psi += coefs[m] * psis[m] * np.exp(-1j * (0.5 + m) * t)  # add each with time dependence
    psi = psi / np.sqrt((abs(psi) ** 2).sum())  # normalize
    for i in range(NA):
        SetArrowFromCN(3 * psi[i], alist[i])  # update arrows, scale up so they’re easier to see

    pxTot = (x * abs(psi) ** 2).sum()  # compute the expectation value of x
    gr.plot(pos=(t, pxTot))  # plot it!
    t += dt
