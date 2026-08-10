#Web VPython 3.2

from vpython import pi, box, vec, color, sin, cos, rate, sphere, hat, mag, canvas, arange, arrow

title="""
&#x2022; Based on original <a href="https://bphilhour.trinket.io/physics-through-glowscript-an-introductory-course#/1-introduction-objects-parameters-and-the-3d-environment/optional-scale-models#">example</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/charged_ring.py">charged_ring.py</a>

If it isn't doing anything interesting, either wait or run again to randomize start position.

"""

Q = 1.6E-19  # charge magnitude of electron
k = 9E9  # Coulomb's law constant
fieldScale = 1e23  # arbitrary field size reduction for aesthetics

animation = canvas(title=title, forward=vec(-0.55, -0.65, -0.55), range=1e-10, background=color.gray(0.075))

class ChargedRing:
    def __init__(self, number_of_ring_segments=60, radius=0.5e-10, render=True, charge=-Q):
        self._segments = []  # array holding all the segments
        self._radius = radius
        self._charge = charge

        dx = 2 * pi * radius / number_of_ring_segments  # width of ring segment
        for i in range(0, number_of_ring_segments):
            theta = i * (2 * pi / number_of_ring_segments)  # angular position on ring
            x = radius * cos(theta)
            y = radius * sin(theta)
            if render:
                self._segments.append(box(pos=vec(x, y, 0), size=vec(dx, dx, dx), color=color.green))
                self._segments[i].rotate(axis=vec(0, 0, 1), angle=theta)

        self._dx = dx

    def field_at(self, position):
        dq = self._charge / len(self._segments)  # charge of ring segment
        electric_field = vec(0, 0, 0)
        for segment in self._segments:
            r = segment.pos - position
            electric_field += k * dq * r.norm() / r.mag2
        return electric_field

    def display_field(self):
        dx_squared = self._dx * self._dx
        for x in arange(-self._radius * 1.5, self._radius * 1.5, self._radius / 4):
            for y in arange(-self._radius * 1.5, self._radius * 1.5, self._radius / 4):
                for z in arange(-self._radius * 1.5, self._radius * 1.5, self._radius / 6):
                    position = vec(x, y, z)
                    # don't move forward if we are embedded in the shell itself
                    if z * z <= dx_squared: continue  # avoid infinities

                    electric_field = self.field_at(position)
                    arrow(axis=-electric_field / fieldScale, pos=position, color=color.yellow)

class Electron:
    def __init__(self, mass=9.1093837E-31, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=2.8179E-15, charge=Q, colour=None, make_trail=False, retain=-1, draw=True):
        colour = colour if colour is not None else color.blue if charge > 0 else color.red
        self._ball = sphere(mass=mass, pos=position, radius=radius, color=colour, make_trail=make_trail, retain=retain) if draw else None
        self._velocity = velocity
        self._position = position
        self._radius = radius
        self._charge = charge
        self._mass = mass

    def render(self):
        if self._ball:
            self._ball.pos = self._position

    def field_at(self, position):
        return hat(position - self._ball.pos) * k * self._charge / mag(position - self._ball.pos) ** 2

    def coulomb_force_in(self, electric_field):
        return electric_field * self._charge

    def update(self, coulomb_force, dt):
        self._velocity += coulomb_force / self._mass * dt
        self._position += self._velocity * dt
        self.render()

    def position(self):
        return self._position


radius = 0.5e-10
ring = ChargedRing(radius=radius)
ring.display_field()
electron = Electron(position=vec(0, 0, radius) + 1.5 * radius * vec.random(), radius=radius / 20, charge=-Q, make_trail=True, retain=150)

dt = 1e-18  # time step
while True:
    rate(100)
    field = ring.field_at(electron.position())
    force = electron.coulomb_force_in(field)
    electron.update(force, dt)
