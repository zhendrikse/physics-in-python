#Web VPython 3.2
from vpython import vector, canvas, sphere, norm, mag, color, rate, sin, cos

title="""&#x2022; Original <a href="https://www.mso.anu.edu.au/pfrancis/simulations/spaghettification.py">spaghettification.py</a> by <a href="http://www.mso.anu.edu.au/pfrancis/simulations/">Paul Francis</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/relativity/code/spaghettification.py">spaghettification.py</a>

"""

display = canvas(title=title, background=color.gray(0.075), range=10, width=650, height=400)
stars = sphere(pos=vector(0, 0, 0), texture="https://www.hendrikse.name/science/astrophysics/images/textures/universe.jpg", radius=20, shininess=0, opacity=0.5)

# Set up particle grid
size = 0.15
vel0 = vector(0, 0.65, 0)
rad = 0.2
spacing = 0.10
base_angle = 0.2

class Person:
    def __init__(self):
        self._grid = []
        self._head()
        self._body()
        self._left_arm()
        self._right_arm()
        self._left_leg()
        self._right_leg()

    def _head(self, pos=vector(10, 1.0, 0), colour=vector(0.7, 0.6, 0.5)):
        self._grid.append(sphere(pos=pos, radius=2.0 * rad, vel=vel0, color=colour))

    def _body(self, pos=vector(10, 1.0, 0), colour=vector(0.2, 0.4, 0.7)):
        theta = 0.0
        for i in range(0, 21):
            offset = vector(spacing * i * sin(theta + base_angle), -spacing * i * cos(theta + base_angle), 0)
            self._grid.append(sphere(pos=pos + offset, radius=rad, vel=vel0, color=colour))

    def _right_arm(self, pos=vector(10, 0.7, 0), colour=vector(0.2, 0.8, 0.9)):
        theta = 0.7
        for i in range(0, 11):
            offset = vector(spacing * i * sin(theta + base_angle), -spacing * i * cos(theta + base_angle), 0)
            self._grid.append(sphere(pos=pos + offset, radius=rad, vel=vel0, color=colour))

    def _left_arm(self, pos=vector(10, 0.7, 0), colour=vector(0.2, 0.8, 0.9)):
        theta = -0.7
        for i in range(0, 11):
            offset = vector(spacing * i * sin(theta + base_angle), -spacing * i * cos(theta + base_angle), 0)
            self._grid.append(sphere(pos=pos + offset, radius=rad, vel=vel0, color=colour))

    def _right_leg(self, pos=vector(10, 1.0, 0) + 2.0 * vector(sin(base_angle), -cos(base_angle), 0), colour=vector(0.2, 0.2, 0.7)):
        theta = 0.4
        for i in range(0, 11):
            offset = vector(spacing * i * sin(theta + base_angle), -spacing * i * cos(theta + base_angle), 0)
            self._grid.append(sphere(pos=pos + offset, radius=rad, vel=vel0, color=colour))

    def _left_leg(self, pos=vector(10, 1.0, 0) + 2.0 * vector(sin(base_angle), -cos(base_angle), 0), colour=vector(0.2, 0.2, 0.7)):
        theta = -0.4
        for i in range(0, 11):
            offset = vector(spacing * i * sin(theta + base_angle), -spacing * i * cos(theta + base_angle), 0)
            self._grid.append(sphere(pos=pos + offset, radius=rad, vel=vel0, color=colour))

    def update(self, dt):
        for thing in self._grid:
            thing.pos = thing.pos + thing.vel * dt
            acceleration = - 15.0 * norm(thing.pos - black_hole.pos) / (mag(thing.pos - black_hole.pos) ** 2)
            thing.vel = thing.vel + acceleration * dt


black_hole = sphere(pos=vector(-1, 0, 0), radius=1.0, color=color.gray(0.3))
person = Person()

t = 0
delta_t = 0.02
while True:
    rate(100)
    t += delta_t
    person.update(delta_t)


