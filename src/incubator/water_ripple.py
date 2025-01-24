import numpy
from matplotlib import pyplot
#from matplotlib import cm

# https://medium.com/@matiasortizdiez/beginners-introduction-to-natural-simulation-in-python-ii-simulating-a-water-ripple-809356ffcb43

Lx = 10 # total width of the pool
Nx = 80 # amount of points in the x direction, the more the better
Ly = 10 # total height of the pool
Ny = 80 # amount of points in the y direction, the more the better

# meshes the x dimension of the domain as being from 0 to Lx and
# containing Nx points. The linspace function returns an array of
# all the points
x_vec = numpy.linspace(0, Lx, Nx)
dx = x_vec[2] - x_vec[1] # defines dx as the space between 2 points in x

# meshes the y dimension of the domain as being from 0 to Ly and
# containing Ny points. The linspace function returns an array of
# all the points
y_vec = numpy.linspace(0, Ly, Ny)
dy = y_vec[2] - y_vec[1] # defines dy as the space between 2 points in y

dt = .025 # the amount of time that will pass after every iteration
Nt = 4000 # amount of iterations

# this means that the simulation will simulate .025*4000 real
# seconds of water rippling

c = 1 # keeping it simple

# defines a 2-dimensional array that corresponds to the value of u at
# every point in the mesh
u = numpy.zeros([Nt, len(x_vec), len(y_vec)])

u[0, Nx // 2, Ny // 2] = numpy.sin(0) # disturbance at t = 0
u[1, Nx // 2, Ny // 2] = numpy.sin(1/10) # disturbance at t = 1

for t in range(1, Nt-1):
    #print(t/Nt)
    c_squared = c * c
    dt_squared = dt * dt
    dx_squared = dx * dx
    dy_squared = dy * dy
    for x in range(1, Nx-1):
        for y in range(1, Ny-1):
            if t < 100:
                u[t, Nx // 2, Ny // 2] = numpy.sin(t / 10)

            u[t+1, x, y] = c_squared * dt_squared * ( ((u[t, x+1, y] - 2*u[t, x, y] + u[t, x-1, y])/dx_squared) + ((u[t, x, y+1] - 2*u[t, x, y] + u[t, x, y-1])/dy_squared) ) + 2*u[t, x, y] - u[t-1, x, y]

fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = numpy.meshgrid(x_vec, y_vec)
for t in range(0, Nt):
    surf = ax.plot_surface(X, Y, u[t], color='g', shade=True, linewidth=0, antialiased=False)

    ax.view_init(elev=45)
    ax.set_zlim(-.0001, 2.4)
    pyplot.axis('off')

    pyplot.pause(.0001)
    pyplot.cla()