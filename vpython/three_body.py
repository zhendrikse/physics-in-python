# Web VPython 3.2

from vpython import sphere, rate, canvas, vector, color, sqrt

title = """&#x2022; Based on original by <a href="https://trinket.io/glowscript/9ece3648f0">Rhett Allain</a>
&#x2022; Belongs to <a href="https://www.youtube.com/watch?v=Ye2wIV8-SB8">this video</a> 
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> into <a href="https://github.com/zhendrikse/science/blob/main/astrophysics/code/three_body.py">three_body.py</a>

&#x2022; Click mouse to start animation

"""

animation = canvas(title=title, background=color.gray(0.075))

G = 6.67e-11
astronomical_unit = 1.49e11
mass = 1e30
rA = 0.1 * astronomical_unit
rB = rA * 1 / 0.8
vA = sqrt(G * 0.8 * mass * rA) / (rA + rB)

class CelestialObject:
    def __init__(self, position, velocity, mass, radius, colour=color.yellow, make_trail=True):
        self._sphere = sphere(pos=position, radius=radius, color=colour, make_trail=make_trail)
        self._mass = mass
        self._velocity = velocity

    def momentum(self):
        return self._mass * self._velocity

    def distance_to(self, other):
        return other._sphere.pos - self._sphere.pos

    def force_between(self, other):
        radius = self.distance_to(other)
        force_magnitude = G * self._mass * other._mass / (mag(radius) * mag(radius))
        force_vector = force_magnitude * norm(radius)
        return force_vector

    def move(self, force, dt):
        self._velocity += force / self._mass * dt
        self._sphere.pos += self._velocity * dt

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
