#Web VPython 3.2

title = """Click to drop slinky and ball 

&#x2022; Based on original by <a href="https://trinket.io/glowscript/e5f14ebee1">Rhett Allain</a>
&#x2022; Belongs to <a href="https://rhettallain.com/2019/02/06/modeling-a-falling-slinky/">this article</a> 
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

from vpython import sphere, cylinder, box, vector, helix, scene, rate, mag, norm, color

g = vector(0, -9.8, 0)
L0 = 2
k = 100

class Ball:
    def __init__(self, position=vector(0, 0, 0), mass=5, radius=0.25, colour=color.red):
        self._mass = mass
        self._velocity = vector(0, 0, 0)
        self._ball = sphere(pos=position, radius=radius, color=colour)

    def distance_to(self, other):
        return other.position() - self.position()

    def position(self):
        return self._ball.pos

    def mass(self):
        return self._mass

    def move(self, force__vector=vector(0, 0, 0), dt=0.01):
        # Newton's second law: F = m * a
        acceleration_vector = force__vector / self.mass()
        self._velocity += acceleration_vector * dt
        self._ball.pos += self._velocity * dt


ball1 = Ball(position=vector(0, L0 / 2, 0))
ball2 = Ball(position=ball1.position() + vector(0, -L0 - ball1.mass() * mag(g) / k, 0))
ball3 = Ball(position=ball2.position() + vector(L0, 0, 0), colour=color.yellow)

stick = cylinder(pos=ball2.position() - vector(L0, 2.75 * L0, 0), axis=vector(0, 3 * L0, 0), radius=L0 / 15, color=color.cyan)
stick2 = cylinder(pos=ball2.position() - vector(L0, 0, 0), axis=vector(L0 / 2, 0, 0), radius=L0 / 15, color=color.cyan)
floor = box(pos=vector(0, -3.5 * L0, 0), length=5 * L0, width=L0, height=0.1, color=color.magenta)

spring = helix(pos=ball1.position(), axis=ball1.distance_to(ball2), radius=0.2, thickness=0.05, coils=15)

c = .5
t = 0
dt = 0.01

scene.title = title
scene.forward=vector(0.45, -0.30, -0.83)
scene.range=8
scene.waitfor('click')
while t < 1.02:
    rate(25)
    spring_length = ball1.distance_to(ball2)
    spring_force = -k * (mag(spring_length) - L0) * norm(spring_length)
    force_on_ball_1 = ball1.mass() * g - spring_force
    force_on_ball_2 = ball2.mass() * g + spring_force
    ball1.move(force_on_ball_1, dt)
    ball2.move(force_on_ball_2, dt)
    ball3.move(g * ball3.mass(), dt)
    spring.pos = ball1.position()
    spring.axis = spring_length
    t += dt

