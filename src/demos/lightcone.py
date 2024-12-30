from vpython import points, vec, color, rate

from ..toolbox.axis import Base

axis=Base(mesh=True, labels=False)

t = 0
while True:
    points(pos=[vec(t, t, t)], radius=7, color=color.cyan)
    rate(2)
    t += .3
    pass