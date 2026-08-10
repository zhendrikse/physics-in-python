# Web VPython 3.2

from vpython import canvas, rate, color, vector, sphere, cross, mag, hat, sin, cos, pi, arrow, label

title = """&#x2022; Based on <a href="https://www.glowscript.org/#/user/wlane/folder/PHYS152/program/MovingLineOfCharge">MovingLineOfCharge</a> by Ksenja Llazar and Alyssa McCaskey
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/charged_rod.py">charged_rod.py</a>

"""

display = canvas(forward=vector(.15, -.4, -.9), range=1.4, title=title, width=600, height=600,
                 background=color.gray(0.075), center=vector(0, .5, 0))

scale_electric = .002
scale_magnetic = 2e15
oofpez = 9e9  # Electric constant.
muzofp = 1e-7  # Magnetic constant.
c = 3e8  # Speed of light


class PointCharge:
    def __init__(self, position, charge, radius, mass=1.67e-27, colour=color.yellow):
        self._charge = sphere(pos=position, mass=mass, radius=radius, color=colour)
        self._velocity = vector(0, 0.2, 0)
        self._q = charge

    def update(self, dt):
        self._charge.pos += self._velocity * dt

    def electric_force_at(self, position):
        r = position - self._charge.pos
        return (oofpez * self._q / mag(r) ** 2) * hat(r) * (1 - (mag(self._velocity) ** 2) / c ** 2)

    def magnetic_force_at(self, position):
        r = position - self._charge.pos
        return muzofp * (self._q * cross(self._velocity, hat(r))) / mag(r) ** 2


class ChargedRod:
    def __init__(self, length=1, num_charges=10, charge=1e-9):
        self._slices = []
        dy = length / num_charges
        y0 = .5 * (-length / 2 + dy)  # Center of bottom slice.
        for i in range(num_charges):
            self._slices.append(PointCharge(vector(0, y0 + i * dy, 0), charge / num_charges, dy / 2))

    def update(self, dt):
        for point_charge in self._slices:
            point_charge.update(dt)

    def electric_field_at(self, position):
        net_field = vector(0, 0, 0)
        for charge in self._slices:
            net_field += charge.electric_force_at(position)
        return net_field

    def magnetic_field_at(self, position):
        net_field = vector(0, 0, 0)
        for charge in self._slices:
            net_field += charge.magnetic_force_at(position)
        return net_field


class FieldArrows:
    def __init__(self, radius=0.15):
        self._electric_field, self._magnetic_field, self._positions = [], [], []

        for y in [-.5, -.3, 0, .3, .5]:
            self._create_arrows(y, radius)

    def _create_arrows(self, y, radius):
        theta = 0
        while theta < 2 * pi:
            position = vector(radius * cos(theta), y, radius * sin(theta))
            self._positions.append(position)
            self._electric_field.append(arrow(pos=position, color=color.red))
            self._magnetic_field.append(arrow(pos=position, color=color.blue))
            theta += pi / 6

    def update(self, rod):
        for j in range(len(self._positions)):
            self._electric_field[j].axis = scale_electric * rod.electric_field_at(self._positions[j])
            self._magnetic_field[j].axis = scale_magnetic * rod.magnetic_field_at(self._positions[j])


dt = .01
while True:
    for obj in display.objects:
        obj.visible = False

    field_arrows = FieldArrows()
    charged_rod = ChargedRod()
    field_arrows.update(charged_rod)
    popup = label(text="Click mouse to start", pos=vector(0, 1, 0))

    display.waitfor("click")
    popup.visible = False

    for _ in range(500):
        rate(.5 / dt)
        charged_rod.update(dt)
        field_arrows.update(charged_rod)
