# Web VPython 3.2
from vpython import *

title="""&#x2022; <a href="https://www.glowscript.org/#/user/wlane/folder/Modern-Physics/program/Double-Slit">Original code</a> by <a href="https://www.youtube.com/@LetsCodePhysics">Let&apos;s code physics</a>
&#x2022; See also <a href="https://www.youtube.com/watch?v=Zjmg6n7Wc8I">his accompanying video</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/quantumphysics/code/double_slit.py">double_slit.py</a>
&#x2022; Check out my other <a href="https://www.hendrikse.name/science/quantumphysics/dynamic_double_slit.html">double slit experiment page</a> on this site as well!

"""

animation = canvas(title=title, forward=vec(0, 0.85, -0.55), background=color.gray(0.075), center=vector(0, 0, 0))

wavelength = 1.0
distant_light(direction=vector(0, -1, 0), color=color.white)

source_1 = sphere(pos=vector(-1, -3, 0), color=color.white, radius=0.25)
source_2 = sphere(pos=vector(1, -3, 0), color=color.white, radius=0.25)

class InterferencePattern:
    def __init__(self, slit_1_pos, slit_2_pos, dx, x_max):
        # Make points on grid.
        vertices = []
        for x in arange(-2 * x_max, 2 * x_max, dx):
            for y in arange(-x_max, x_max, dx):
                vertex_ = box(pos=vector(x, y, 0), size=vector(dx, dx, 0.01))
                if y >= x_max - dx:
                    vertex_.size.z *= 500
                path_difference = abs(mag(vertex_.pos - slit_1_pos) - mag(vertex_.pos - slit_2_pos))
                n = path_difference % wavelength
                brightness = abs(n - 0.5) / 0.5
                vertex_.color = vector(brightness, brightness, 0)
                vertices.append(vertex_)

dx = 0.1
x_max = 4
interference_pattern = InterferencePattern(source_1.pos, source_2.pos, dx, x_max)

MathJax.Hub.Queue(["Typeset", MathJax.Hub])
# Now let's shoot particles.
dt = 0.1
particles = []
while len(particles) < 500:
    rate(10)
    r = random()
    if r > 0.90:  # 10% chance
        particles.append(simple_sphere(pos=source_1.pos, color=color.green, radius=0.06,
                                       velocity=vector(0.1 * random(), 1, 0.1 * random())))
    r = random()
    if r > 0.90:  # 10% chance
        particles.append(simple_sphere(pos=source_2.pos, color=color.green, radius=0.06,
                                       velocity=vector(0.1 * random(), 1, 0.1 * random())))

    for p in particles:
        p.pos += p.velocity * dt
        if p.pos.y >= x_max - 2 * dx:
            p.velocity = vector(0, 0, 0)
