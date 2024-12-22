from vpython import *

N = 4

# x = arrow(axis= vec(2, 0, 0), color=color.red)
# y = arrow(axis= vec(0, 2, 0), color=color.green)
# z = arrow(axis= vec(0, 0, 2), color=color.blue)

class Spin:
    def __init__(self, x, y, draw=True):
        self._x = x
        self._y = y
        self._is_up = True
        self._spin = arrow(pos=vec(x, y, 0), axis=vec(0, 0.8, 0), color=color.cyan)

    def _draw(self):
        if self._spin:
            if self._is_up:
                self._spin.axis = vec(0, 0.8, 0)
            else:
                self._spin.axis = vec(0, -0.8, 0)
                self._spin.pos = vec(self._x, self._y + 0.8, 0)

    def flip(self):
        self._is_up = not self._is_up
        self._draw()

spins = [Spin(x, y) for y in range(N) for x in range(N)]

# while True:
#     rate(1)
#     for spin in spins:
#         if random() < 0.5:
#             spin.flip()

# arrow(pos=vec(0, 0, 0), axis=vec(0, 0.8, 0))
# a2 = arrow(pos=vec(1, 0.8, 0), axis=vec(0, -0.8, 0))
# arrow(pos=vec(2, 0, 0), axis=vec(0, 0.8, 0))
#
# a2.pos = vec(1, 0, 0)
# a2.axis = vec(0, 0.8, 0)
# a2.pos = vec(1, 0.8, 0)
# a2.axis = vec(0, -0.8, 0)

# spins[1]._spin.pos = vec(spins[1]._spin.pos.x, spins[1]._spin.pos.y + 0.8, 0)
# spins[1]._spin.axis = vec(0, -0.8, 0)
for spin in spins:
    if random() < 0.5:
        spin.flip()

while True:
    rate(1)
    pass