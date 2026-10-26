# Web VPython 3.2
from vpython import local_light, sphere, cylinder, vec, vector, mag, rate, canvas, color, curve, cos, pi, sqrt
from random import uniform

title = """&#x2022; Original <a href="https://lectdemo.github.io/virtual/scripts/08_Rutherford_dist.py">08_Rutherford_dist.py</a> by Ruth Chabay Spring 2000
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/molecularphysics/code/rutherford_scattering.py">rutherford_scattering.py</a>

"""

xMax = 1e-13
animation = canvas(x=0, y=0, background=color.gray(0.075), range=xMax * 2.5, title=title)

local_light(pos=vec(1, 0, 1))


dt = 5e-23
k = 9e9
K0 = 10e6 * 1.6e-19
alpha_mass = 4e-3 / 6.12e23
alpha_color = vector(.2, 1., 1.)

class Particle:
    def __init__(self, position, mass, charge, momentum, radius, colour=color.yellow):
        self._particle = sphere(pos=position, radius=radius, color=colour)
        self._mass = mass
        self._momentum = momentum
        self._charge = charge
        self._initial_position = position
        self._initial_momentum = momentum

    def position(self):
        return self._particle.pos

    def charge(self):
        return self._charge

    def momentum(self):
        return self._momentum

    def colour(self):
        return self._particle.color

    def colour_is(self, colour):
        self._particle.color = colour

    def force_between(self, other_particle):
        r = self.distance_to(other_particle)
        return k * other_particle.charge() * self.charge() * r / (mag(r) ** 3)

    def distance_to(self, other_particle):
        return other_particle.position() - self.position()

    def update_with(self, force, dt):
        self._momentum += force * dt
        self._particle.pos += (self._momentum / self._mass) * dt

    def reset(self):
        self._particle.pos = self._initial_position
        self._momentum = self._initial_momentum

class Source:
    def __init__(self, position=vec(0, 0, 0), radius=6e-14):
        self._position = position
        self._radius = radius
        _ = cylinder(pos=position, axis=vector(-radius * 0.1, 0, 0), radius=radius, color=color.gray(0.6))

    def beam(self):
        while True:
            yy = uniform(-self._radius, self._radius)
            zz = uniform(-self._radius, self._radius)
            if yy * yy + zz * zz <= self._radius * self._radius:
                return vector(-xMax * 1.5, yy, zz)

    def position(self):
        return self._position

source = Source(vector(-xMax * 2.0, 0, 0))
gold = Particle(position=vec(0, 0, 0), radius=6e-15, colour=color.yellow, mass=197e-3 / 6.02e23, charge=79 * 1.6e-19, momentum=vector(0, 0, 0))

trails = []
for nalpha in range(1000):
    rate(5)
    alpha_particle = Particle(position=source.beam(), radius=4e-15, colour=vector(.2, 1., 1.), mass=alpha_mass, charge=2 * 1.6e-19, momentum=vector(sqrt(2 * alpha_mass * K0), 0, 0))
    departure_spot = cylinder(pos=vector(source.position().x, alpha_particle.position().y, alpha_particle.position().z), radius=2e-15, axis=vector(1e-15, 0, 0), color=alpha_color)

    trail = curve(color=alpha_color, pos=[departure_spot.pos])
    gold.reset()

    while mag(alpha_particle.position()) < 1.8e-13:
        F = gold.force_between(alpha_particle)
        alpha_particle.update_with(F, dt)
        gold.update_with(F, dt)
        trail.append(pos=alpha_particle.position())

    if alpha_particle.momentum().x / mag(alpha_particle.momentum()) <= cos(pi / 2):
        alpha_particle.colour_is(color.red)
        trail.color = alpha_particle.colour() / 1.5
        departure_spot.color = alpha_particle.colour() / 1.5
    elif alpha_particle.momentum().x / mag(alpha_particle.momentum()) <= cos(pi / 4):
        alpha_particle.colour_is(color.blue)
        trail.color = alpha_particle.colour()
        departure_spot.color = alpha_particle.colour()

    for a_trail in trails:
       a_trail.color /=  2
    trails.append(trail)
    if len(trails) > 3:
        trails.pop(0).visible = 0
