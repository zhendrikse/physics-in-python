#
# https://stackoverflow.com/questions/36585517/ising-model-in-python
#
from vpython import *

N = 5


# x = arrow(axis= vec(2, 0, 0), color=color.red)
# y = arrow(axis= vec(0, 2, 0), color=color.green)
# z = arrow(axis= vec(0, 0, 2), color=color.blue)

class Spin:
    def __init__(self, x, y, draw=True):
        self._spin_axis = vec(0, 0.8, 0)
        self._x = x
        self._y = y
        self._spin = arrow(pos=vec(x, 0 if self._is_up() else abs(self._spin_axis.y), y), axis=self._spin_axis,
                           color=color.cyan)

    def _draw(self):
        if self._spin:
            self._spin.axis = self._spin_axis
            self._spin.pos = vec(self._x, 0 if self._is_up() else abs(self._spin_axis.y), self._y)
            self._spin.color = color.cyan if self._is_up() else color.red

    def _is_up(self):
        return self._spin_axis.y > 0

    def flip(self):
        self._spin_axis = -self._spin_axis
        self._draw()


scene.center = vec(0, 0, 0)
scene.forward = vec(0.059628, -0.522687, -0.850437)
scene.range = 5.5088958151447684

spins = [Spin(x, y) for y in range(-N, N) for x in range(-N, N)]

while True:
    rate(1)
    for spin in spins:
        if random() < 0.5:
            spin.flip()

