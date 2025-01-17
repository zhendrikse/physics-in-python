import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
a = 1
c = 2
precision = 6
U = np.linspace(0, 2*np.pi, precision)
V = np.linspace(0, 2*np.pi, precision)
U, V = np.meshgrid(U, V)
X = (c+a*np.cos(V))*np.cos(U)
Y = (c+a*np.cos(V))*np.sin(U)
Z = a*np.sin(V)
print(X, Y)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()