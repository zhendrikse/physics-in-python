#Web VPython 3.2
from vpython import canvas, color, textures, vector, simple_sphere, rate, box, sin, cos, dot, pi

title="""&#x2022; <a href="https://www.glowscript.org/#/user/wlane/folder/Let'sCodePhysics/program/particles-bouncing">Original code</a> by <a href="https://www.youtube.com/@LetsCodePhysics">Let&apos;s code physics</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/kinematics/code/bouncing_particles.py">bouncing_particles.py</a>

"""

display = canvas(title=title, background=color.gray(0.075), width=650, height=650, forward=vector(-0.25, -.65, -.75), center=vector(0, .82, -1.1))

class Particle:
    def __init__(self, position_x):
        self._sphere = simple_sphere(pos=vector(position_x, 2, 0), radius=0.05, color=color.yellow)
        self._mass=1.0
        self._force=vector(0, 0, 0)
        self._velocity=vector(0, 0, 0)

    def update(self, delta_t):
        self._force = vector(0, -self._mass * grav, 0)
        self._velocity += self._force / self._mass * delta_t
        self._sphere.pos += self._velocity * delta_t

    def flip(self, barrier):
        v1par = dot(self._velocity, barrier.up()) * barrier.up()
        v1perp = self._velocity - v1par
        self._velocity = v1perp - v1par

    def collides_with(self, barrier):
        r = self._sphere.pos - barrier.pos()
        return barrier.distance_is_close_to(r)

class Barrier:
    def __init__(self, position, length, width, theta, phi):
        self._box = box(pos=position, size=vector(length, 0.05, width), texture=textures.wood, up=vector(sin(theta) * cos(phi), cos(theta), sin(theta) * sin(phi)))

    def distance_is_close_to(self, r):
        eps = 0.1
        return (abs(r.x) < self._box.length) and abs(r.z) < self._box.width and abs(dot(r, self._box.up)) < eps

    def pos(self):
        return self._box.pos

    def up(self):
        return self._box.up

barriers = [Barrier(vector(-1.5, 0, 0), 10, 0.5, pi / 3, 0), Barrier(vector(0, -2, 0), 10, 0.5, 0, 0), Barrier(vector(1.5, 0, 0), 10, 0.5, -pi / 3, 0)]

particles = []
n = 20
dx = 0.25
x = -n * dx / 2
for _ in range(0, n):
    particles.append(Particle(x))
    x += dx

grav = 1.0
dt = 0.01
while True:
    rate(100)
    for particle in particles:
        for barrier_ in barriers:
            if particle.collides_with(barrier_):
                particle.flip(barrier_)
        particle.update(dt)


