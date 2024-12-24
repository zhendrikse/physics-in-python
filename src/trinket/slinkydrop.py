GlowScript
3.2
VPython

#
# Original is here: https://trinket.io/glowscript/e5f14ebee1
# Belongs to article: https://rhettallain.com/2019/02/06/modeling-a-falling-slinky/
# See also: https://github.com/zhendrikse/physics-in-python/
#

g = vector(0, -9.8, 0)
L0 = 2
k = 100
m = 5
ball1 = sphere(pos=vector(0, L0 / 2, 0), radius=0.25, color=color.red)
ball2 = sphere(pos=ball1.pos + vector(0, -L0 - m * mag(g) / k, 0), radius=0.25, color=color.red)

stick = cylinder(pos=ball2.pos - vector(L0, 2.75 * L0, 0), axis=vector(0, 3 * L0, 0), radius=L0 / 15, color=color.cyan)
stick2 = cylinder(pos=ball2.pos - vector(L0, 0, 0), axis=vector(L0 / 2, 0, 0), radius=L0 / 15, color=color.cyan)
floor = box(pos=vector(0, -3.5 * L0, 0), length=5 * L0, width=L0, height=0.1, color=color.magenta)
ball1.m = m
ball2.m = m

ball3 = sphere(pos=ball2.pos + vector(L0, 0, 0), radius=ball2.radius)
ball3.m = m
ball1.atom_momenta = vector(0, 0, 0)
ball2.atom_momenta = vector(0, 0, 0)
ball3.atom_momenta = vector(0, 0, 0)

spring = helix(pos=ball1.pos, axis=ball2.pos - ball1.pos, radius=0.2, thickness=0.05, coils=15)

c = .5
t = 0
dt = 0.01

scene.title = "Click to drop slinky and ball"
scene.waitfor('click')
while t < 1.02:
    rate(25)
    spring_length = ball2.pos - ball1.pos
    spring_force = -k * (mag(spring_length) - L0) * norm(spring_length)
    force_on_ball_2 = ball2.m * g + spring_force
    force_on_ball_1 = ball1.m * g - spring_force
    ball1.atom_momenta = ball1.atom_momenta + force_on_ball_1 * dt
    ball2.atom_momenta = ball2.atom_momenta + force_on_ball_2 * dt
    ball3.atom_momenta = ball3.atom_momenta + ball3.m * g * dt

    ball1.pos = ball1.pos + ball1.atom_momenta * dt / ball1.m
    ball2.pos = ball2.pos + ball2.atom_momenta * dt / ball2.m
    ball3.pos = ball3.pos + ball3.atom_momenta * dt / ball3.m
    spring.pos = ball1.pos
    spring.axis = spring_length
    t += dt

