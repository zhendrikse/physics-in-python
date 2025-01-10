#Web VPython 3.2

from  vpython import get_library, arange, pi, cylinder, vec, vector, color, pi
#
# https://groups.google.com/g/glowscript-users/c/nAe7zx6lBE8?pli=1
#
# You need to import the "browser" version of the Javascript library
#

get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")
d = math.distance([0, 0], [3, 4])
print(d)

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')

def numpy_linspace(start, stop, num):
    return numpy_array([x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop])


def numpy_arange(n):
    return numpy_array([i for i in range(n)])


def numpy_array(an_array):
    return nj.array(an_array)


def numpy_meshgrid(linspace_1, linspace_2):
    xx = nj.stack([linspace_1 for _ in range(linspace_1.shape)])
    temp = []
    for i in range(linspace_2.shape[0]):
        for j in range(linspace_2.shape[0]):
            temp.append(linspace_2.get(i))
    yy = nj.array(temp).reshape(linspace_2.shape[0], linspace_2.shape[0])
    return xx, yy


# x, y = numpy_meshgrid(numpy_linspace(0, 3, 3), numpy_linspace(0, 3, 3))

scene.background = color.gray(0.7)
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
coefs = {}  # dictionary for precomputed fourier coef.
omegas = {}  # dictionary for energies
kn_max = pi * NX[-1] / a
km_max = pi * NY[-1] / a
Emax = ((hbar * kn_max) ** 2 + (hbar * km_max) ** 2) / (2 * m)
omegaMax = Emax / hbar
dt = pi / (10 * omegaMax)  # come up with a sensible dt

RSdict = {'runStop': False}

x, y = numpy_meshgrid(numpy_linspace(0, a, NA), numpy_linspace(0, a, NA))

# draw the boundaries of the ISW in 2D

boundary_radius = a / 100

cylinder(pos=vec(-a / 2, -a / 2, 0), axis=vec(a, 0, 0), color=color.blue, radius=boundary_radius)
cylinder(pos=vec(-a / 2, -a / 2, 0), axis=vec(0, a, 0), color=color.blue, radius=boundary_radius)
cylinder(pos=vec(a / 2, -a / 2, 0), axis=vec(0, a, 0), color=color.blue, radius=boundary_radius)
cylinder(pos=vec(-a / 2, a / 2, 0), axis=vec(a, 0, 0), color=color.blue, radius=boundary_radius)

arrow_base_pos = vector(-a / 2, -a / 2, 0)  # place origin of arrows

#
# build cylinders.... in 2-D space, store them in a set of nested lists
#

alist = []
for i in range(NA):
    sublist = []
    alist.append(sublist)
    for j in range(NA):
        position = arrow_base_pos + vector(x.get(i, j), y.get(i, j), 0)
        sublist.append(cylinder(pos=position, axis=vec(0, 0, 1), color=color.red))

#
# compute the eigenstates and store them in a dictionary 'eigenstates'
#
eigenstates = {}  # dictionary for precomputed eigenstates
for nx in NX:
    for ny in NY:
        psi_nx_ny = x.divide(a).multiply(nx * pi))
        # psi_nx_my = np.sin(nx * np.pi * x / a) * np.sin(ny * np.pi * y / a)  # compute the n,m energy eigenstate
        # psi_nx_my /= np.sqrt((abs(psi_nx_my) ** 2).sum())  # normalize it.
        # eigenstates[(nx, ny)] = psi_nx_my
