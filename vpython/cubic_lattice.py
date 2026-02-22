# Web VPython 3.2
from vpython import simple_sphere, vector, color, helix, rate, mag, hat, canvas

title="""&#x2022; <a href="https://www.glowscript.org/#/user/wlane/folder/Let'sCodePhysics/program/atoms-array">Original code</a> by <a href="https://www.youtube.com/@LetsCodePhysics">Let&apos;s code physics</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/molecularphysics/code/cubic_lattice.py">cubic_lattice.py</a>

"""

display = canvas(title=title, width=600, center=vector(.12, -.33, 0), forward=vector(-.65, -.55, -.5), background=color.gray(0.075), range=2.25)

class Atom:
    def __init__(self, pos, radius=0.1, colour=color.green, velocity=vector(0, 0, 0), visible=False):
        self._atom = simple_sphere(pos=pos, radius=radius, color=colour, visible=visible)
        self._velocity = velocity
        self._force = vector(0, 0, 0)
        self._neighbors = []

    def pos(self):
        return self._atom.pos

    def is_visible(self):
        return self._atom.visible

    def radius(self):
        return self._atom.radius

    def append_neighbor(self, other_atom):
        self._neighbors.append(other_atom)

    def update_force(self):
        self._force = vector(0, 0, 0)
        k = 1e3
        leq = 1
        for atom in self._neighbors:
            s = mag(atom.pos() - self.pos()) - leq
            self._force += k * s * hat(atom.pos() - self.pos())

    def update_by(self, dt):
        if not self._atom.visible:
            return

        self._velocity += self._force * dt
        self._atom.pos += self._velocity * dt

    def shift_by(self, displacement):
        self._atom.color = color.yellow
        self._atom.pos += displacement

    def is_neighbor_of(self, other_atom):
        neighbor = self.pos() == other_atom.pos() + vector(1, 0, 0)
        neighbor |= self.pos() == other_atom.pos() - vector(1, 0, 0)
        neighbor |= self.pos() == other_atom.pos() + vector(0, 1, 0)
        neighbor |= self.pos() == other_atom.pos() - vector(0, 1, 0)
        neighbor |= self.pos() == other_atom.pos() + vector(0, 0, 1)
        neighbor |= self.pos() == other_atom.pos() - vector(0, 0, 1)
        return neighbor

class Bond:
    def __init__(self, atom, other_atom):
        self._bond =helix(pos=atom.pos(), axis=other_atom.pos() - atom.pos(), thickness=.1 * atom.radius(), radius=atom.radius() / 2, coils=15)
        self._atoms = [atom, other_atom]

    def update(self):
        self._bond.pos = self._atoms[0].pos()
        self._bond.axis = self._atoms[1].pos() - self._atoms[0].pos()

    def is_between(self, atom, other_atom):
        return atom in self._atoms and other_atom in self._atoms

class Lattice:
    def __init__(self, nrows=2):
        self._atoms = []
        self._bonds = []
        nrows += 2
        for z in range(-nrows // 2, nrows // 2, 1):
            for y in range(-nrows // 2, nrows // 2, 1):
                for x in range(-nrows // 2, nrows // 2, 1):
                    vis = (abs(x) != nrows // 2 and abs(y) != nrows // 2 and abs(z) != nrows // 2)
                    self._atoms.append(Atom(pos=vector(x, y, z), visible=vis))

        for atom in self._atoms:
            for other_atom in self._atoms:
                if atom.is_neighbor_of(other_atom):
                    atom.append_neighbor(other_atom)
                    need_spring = atom.is_visible() and other_atom.is_visible()
                    if need_spring:
                        for bond in self._bonds:
                            if bond.is_between(other_atom, atom):
                                need_spring = False
                    if need_spring:
                        self._bonds.append(Bond(atom, other_atom))

    def update_by(self, dt):
        for atom in self._atoms:
            atom.update_force()
        for atom in self._atoms:
            atom.update_by(dt)
        for bond in self._bonds:
            bond.update()

    def move_atom(self, atom_index, displacement):
        self._atoms[atom_index].shift_by(displacement)


lattice = Lattice()
dt = 0.01
lattice.move_atom(26, vector(0, 0, 0.2))
while True:
    rate(1/dt)
    lattice.update_by(dt)

