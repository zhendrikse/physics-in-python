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
        self._spin = arrow(pos=vec(x, y, 0), axis=self._spin_axis, color=color.cyan)

    def _draw(self):
        if self._spin:
            self._spin.axis = self._spin_axis
            self._spin.pos = vec(self._x, self._y, 0)

    def _is_up(self):
        return self._spin_axis.y > 0

    def flip(self):
        self._y += self._spin_axis.y
        self._spin_axis = -self._spin_axis
        self._draw()

spins = [Spin(x, y) for y in range(-N, N) for x in range(-N, N)]

while True:
    rate(1)
    for spin in spins:
        if random() < 0.5:
            spin.flip()
    pass