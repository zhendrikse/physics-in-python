# Web VPython 3.2

from vpython import canvas, vec, color, sphere, vector, box, mag, arrow, rate, arange

title = """
&#x2022; Original <a href="https://trinket.io/glowscript/38fbc7b2d01d">code</a> by Byron Philhour
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/charged_sheet.py">charged_sheet.py</a>

If it isn't doing anything interesting, either wait or run again to randomize start position. 
Two-finger drag to change perspective.

"""

animation = canvas(title=title, forward=vector(0.34, 0.7, -0.6), background=color.gray(0.075))

Q = 1.6e-19  # charge magnitude of electron / nucleus
k = 9e9  # Coulomb's law constant
fieldScale = 5e23  # arbitrary field size reduction for aesthetics

class ChargedSheet:
    def __init__(self, segments_total=50, size=0.5e-10):
        self._sheet_segments = []
        dx = size / segments_total  # width of ring segment
        for i in range(segments_total):
            for j in range(segments_total):
                x, y = -.5 * size + i * dx, -.5 * size + j * dx
                self._sheet_segments += [box(pos=vec(x, y, 0), size=vec(dx, dx, dx), color=color.red)]
        self._dx = dx
        self._segments_total = segments_total
        self._size = size

    def field_at(self, position):
        resulting_field = vec(0, 0, 0)
        dq = Q / (self._segments_total * self._segments_total)  # charge of ring segment
        for sheet_segment in self._sheet_segments:
            r = sheet_segment.pos - position
            resulting_field += k * dq * r.norm() / r.mag2  # Coulomb's Law

        return resulting_field

    def display_field(self):
        dx_squared = self._dx * self._dx
        for x in arange(-self._size, self._size, self._size / 8):
            for y in arange(-self._size, self._size, self._size / 8):
                for z in arange(-self._size, self._size, self._size / 12):
                    position = vec(x, y, z)
                    # don't move forward if we are embedded in the shell itself
                    if z * z <= dx_squared: continue  # avoid infinities

                    electric_field = self.field_at(position)
                    arrow(axis=-electric_field / fieldScale, pos=position)


class Electron:
    def __init__(self, mass=9.11e-31, radius=0.5e-10):
        self._ball = sphere(pos=vec(0, 0, radius) + (radius / 2) * vector.random(), radius=radius / 40, color=color.yellow, make_trail=True, retain=150)
        self._velocity = vec(0, 0, 0)
        self._mass = mass

    def increment_by(self, force, dt):
        self._velocity += (force * dt) / self._mass
        self._ball.pos += self._velocity * dt

    def position(self):
        return self._ball.pos


charged_sheet = ChargedSheet()
charged_sheet.display_field()
electron = Electron()

dt = 1e-18  # time step
while True:
    rate(100)
    force_on_electron = Q * charged_sheet.field_at(electron.position())
    electron.increment_by(force_on_electron, dt)
