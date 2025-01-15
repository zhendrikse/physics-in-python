# Web VPython 3.2

from vpython import *

caption = """ 
&#x2022; Based on original by <a href="https://trinket.io/glowscript/9ece3648f0">Rhett Allain</a>
&#x2022; Belongs to <a href="https://www.youtube.com/watch?v=Ye2wIV8-SB8">this video</a> 
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

title = "<h3>Click mouse to start animation</h3>"

animation = canvas(title=title, width="800", height="600", caption=caption)

G = 6.67e-11
astronomical_unit = 1.49e11


class CelestialObject:
    def __init__(self, position, velocity, mass, radius, color=color.yellow, make_trail=True):
        self._sphere = sphere(pos=position, v=velocity, mass=mass, radius=radius, color=color, make_trail=make_trail)

    def momentum(self):
        return self._sphere.mass * self._sphere.v

    def distance_to(self, other):
        return other._sphere.pos - self._sphere.pos

    def force_between(self, other):
        radius = self.distance_to(other)
        force_magnitude = G * self._sphere.mass * other._sphere.mass / mag(radius) ** 2
        force_vector = force_magnitude * norm(radius)
        return force_vector

    def move(self, force, dt):
        self._sphere.v += force / self._sphere.mass * dt
        self._sphere.pos += self._sphere.v * dt


mass = 1e30
rA = 0.1 * astronomical_unit
rB = rA * 1 / 0.8
vA = sqrt(G * 0.8 * mass * rA) / (rA + rB)

sphere_A = CelestialObject(vector(rA, 0, 0), vector(0, vA, 0), mass, 190e7)
sphere_B = CelestialObject(vector(-rB, 0, 0), vector(0, -vA / 0.8, 0), 0.8 * mass, 190e7, color.cyan)
sphere_C = CelestialObject(vector(0, 0, rA), vector(0, 0, 0), 0.5 * mass, 190e7, color.magenta)

animation.waitfor("click")
for t in range(0, 1500 * 5000, 5000):
    rate(100)

    force_BA = sphere_A.force_between(sphere_B)
    force_CB = sphere_B.force_between(sphere_C)
    force_AC = sphere_C.force_between(sphere_A)

    sphere_A.move(+force_BA - force_AC, dt=5000)
    sphere_B.move(-force_BA + force_CB, dt=5000)
    sphere_C.move(-force_CB + force_AC, dt=5000)
