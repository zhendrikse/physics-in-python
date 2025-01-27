#Web VPython 3.2

from vpython import canvas, vec, color, slider, wtext, radians, sin, cos, sphere, curve, rate

animation = canvas(title="Water", background=vec(0.3, 0.2, 0.25),
                forward=vec(10, -8, 5), center=vec(0, 0, 0), ambient=color.gray(0.25))

oxygen_radius = 0.3
hydrogen_radius = 0.2
bond_radius = 0.05

class WaterMolecule:
    def __init__(self, oxygen_atom_count = 1, hydrogen_atom_count = 2):
        phi = radians(104.5)
        phi_hydrogen = phi / 2
        sinphih = sin(phi_hydrogen)
        cosphih = cos(phi_hydrogen)

        self._oxygen_atoms = []
        self._hydrogen_atoms = []

        for i in range(0, oxygen_atom_count):
            self._oxygen_atoms.append(sphere(radius=oxygen_radius, color=color.blue))
        for i in range(0, hydrogen_atom_count):
            self._hydrogen_atoms.append(sphere(radius=hydrogen_radius, color=color.red))

        self._oxygen_atoms[0].pos = vec(0, 0, 0)
        self._hydrogen_atoms[0].pos = vec(0, cosphih, sinphih)
        self._hydrogen_atoms[1].pos = vec(0, cosphih, -sinphih)

        curve(pos=[self._oxygen_atoms[0].pos, self._hydrogen_atoms[0].pos], radius=bond_radius, color=vec(0.5, 0.5, 0.5))
        curve(pos=[self._oxygen_atoms[0].pos, self._hydrogen_atoms[1].pos], radius=bond_radius, color=vec(0.5, 0.5, 0.5))

    def scale_atomic_radius_by(self, scale):
        for oxygen in self._oxygen_atoms:
            oxygen.radius *= scale
        for hydrogen in self._hydrogen_atoms:
            hydrogen.radius *= scale


water = WaterMolecule()

def on_radius_change(s):
    wt.text = 'Atomic radius scale factor: {:1.2f}'.format(s.value)
    water.scale_atomic_radius_by(atomic_radius.value)

atomic_radius = slider(min=0.1, max=2, value=1, bind=on_radius_change)
wt = wtext(text='Atomic radius scale factor: {:1.2f}'.format(atomic_radius.value))

while True:
    rate(10)

