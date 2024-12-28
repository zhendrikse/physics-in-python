# Web VPython 3.2

from vpython import pi, box, vec, color, sin, cos, rate, sphere, hat, mag, scene

#
# Original: https://bphilhour.trinket.io/physics-through-glowscript-an-introductory-course#/1-introduction-objects-parameters-and-the-3d-environment/optional-scale-models
# See also: https://github.com/zhendrikse/physics-in-python/
#

Q = 1.6E-19  # charge magnitude of electron
k = 9E9  # Coulomb's law constant


class ChargedRing:
    def __init__(self, number_of_ring_segments=60, radius=0.5e-10, draw=True, charge=-Q):
        self._segments = []  # array holding all the segments
        self._radius = radius
        self._charge = charge

        dx = 2 * pi * radius / number_of_ring_segments  # width of ring segment
        for i in range(0, number_of_ring_segments):
            theta = i * (2 * pi / number_of_ring_segments)  # angular position on ring
            x = radius * cos(theta)
            y = radius * sin(theta)
            if draw:
                self._segments.append(box(pos=vec(x, y, 0), size=vec(dx, dx, dx), color=color.green))
                self._segments[i].rotate(axis=vec(0, 0, 1), angle=theta)

    def field_at(self, position):
        dq = self._charge / len(self._segments)  # charge of ring segment
        electric_field = vec(0, 0, 0)
        for segment in self._segments:
            r = segment.pos - position
            dE = k * dq * r.norm() / r.mag2
            electric_field += dE
        return electric_field


class Electron:
    def __init__(self, mass=9.1093837E-31, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=2.8179E-15, charge=Q,
                 colour=None, make_trail=False, retain=-1, draw=True):
        colour = colour if colour is not None else color.blue if charge > 0 else color.red
        self._ball = sphere(mass=mass, pos=position, radius=radius, color=colour,
                            make_trail=make_trail, retain=retain) if draw else None
        self._velocity = velocity
        self._position = position
        self._radius = radius
        self._charge = charge
        self._mass = mass

    def _draw(self):
        if self._ball:
            self._ball.pos = self._position

    def field_at(self, position):
        return hat(position - self._ball.pos) * k * self._charge / mag(position - self._ball.pos) ** 2

    def coulomb_force_in(self, electric_field):
        return electric_field * self._charge

    def update(self, coulomb_force, dt):
        '''given a charge and position and update position'''
        self._velocity += coulomb_force / self._mass * dt
        self._position += self._velocity * dt
        self._draw()

    def position(self):
        return self._position

scene.title = "Ising sping model"
scene.caption = "If it isn't doing anything interesting, either wait or run again to randomize start position."
scene.forward=vec(-0.55, -0.65, -0.55)
scene.range=1.0e-10

radius = 0.5e-10
ring = ChargedRing(radius=radius)
electron = Electron(position=vec(0, 0, radius) + 1.5 * radius * vec.random(), radius=radius / 20, charge=-Q,
                    make_trail=True, retain=150)

dt = 1e-18  # time step
while True:
    rate(100)
    E = ring.field_at(electron.position())
    F = electron.coulomb_force_in(E)
    electron.update(F, dt)
