#Web VPython 3.2

#
# https://github.com/zhendrikse
# https://stackoverflow.com/questions/36585517/ising-model-in-python
#

from vpython import arrow, scene, vec, random, color, rate, graph, gcurve, arange, exp

class Spin:
    def __init__(self, x, y, draw=True):
        self._spin_axis = vec(0, 0.8, 0)
        self._x = x
        self._y = y
        self._spin = arrow(pos=vec(x, 0 if self.is_up() else abs(self._spin_axis.y), y), axis=self._spin_axis,
                           color=color.cyan)

    def _draw(self):
        if self._spin:
            self._spin.axis = self._spin_axis
            self._spin.pos = vec(self._x, 0 if self.is_up() else abs(self._spin_axis.y), self._y)
            self._spin.color = color.cyan if self.is_up() else color.red

    def is_up(self):
        return self._spin_axis.y > 0

    def energy(self):
        return 1 if self.is_up() else -1

    def flip(self):
        self._spin_axis = -self._spin_axis
        self._draw()


class SpinLattice:
    def __init__(self, size=10):
        self._spins = []
        self._size = size

        for row in range(size):
            spin_row = []
            for column in range(size):
                spin_row.append(Spin(-size / 2 + row, -size / 2 + column))
            self._spins.append(spin_row)

    def flip_at(self, x, y):
        self._spins[x][y].flip()

    def find_neighbors(self, x, y):
        left = (x, y - 1)
        right = (x, (y + 1) % self._size)
        top = (x - 1, y)
        bottom = ((x + 1) % self._size, y)

        return [self._spins[left[0]][left[1]].energy(),
                self._spins[right[0]][right[1]].energy(),
                self._spins[top[0]][top[1]].energy(),
                self._spins[bottom[0]][bottom[1]].energy()]

    def energy(self, x, y):
        return 2 * self._spins[x][y].energy() * sum(self.find_neighbors(x, y))

    def sweep(self):
        for row in range(self._size):
            for column in range(self._size):
                e = spins.energy(row, column)
                if e <= 0:
                    spins.flip_at(row, column)
                elif exp((-1.0 * e) / temperature) > random():
                    spins.flip_at(row, column)

        energy = 0
        for row in range(self._size):
            for column in range(self._size):
                energy += self.energy(row, column) / (self._size * self._size)

        return energy

    def reset(self):
        for row in range(self._size):
            for column in range(self._size):
                if not self._spins[row][column].is_up():
                    self._spins[row][column].flip()


scene.title = "Ising sping model"
scene.center = vec(0, 0, 0)
scene.forward = vec(0.059628, -0.522687, -0.850437)
scene.range = 11
scene.caption = "\\(  H(\\sigma) = \\sum\\limits_{\\langle ij \\rangle} J_{ij} \\sigma_i \\sigma_j - \\mu \\sum\\limits_{j} h_{j} \\sigma_j \\)\n"
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

mag_plot = graph(title="Magnetization", xtitle="Temperature", ytitle="Magnetization", width=400, height=250)
mag_curve = gcurve(color=color.red)

temperature = 2.0

RELAX_SWEEPS = 50
lattice_size = 20
sweeps = 100  # the number of Monte Carlo Sweeps
spins = SpinLattice(lattice_size)
for temperature in arange(0.1, 5, 0.1):
    mag = []
    for sweep in range(sweeps + RELAX_SWEEPS):
        mag.append(spins.sweep())
        rate(250)
        spins.reset()

    mag_curve.plot(temperature, sum(mag[RELAX_SWEEPS:]) / sweeps)

