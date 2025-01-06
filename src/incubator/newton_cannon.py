from vpython import *

title = """Newton's cannonball

&#x2022; Based on <a href="https://www.siue.edu/~lhorner/VPython/Newton-Cannon2.py">Newton-Cannon2.py</a> by Lenore Horner SIUE October 22, 2009
&#x2022; Version 2 - March 26, 2010: real radius, can start from arbitrary position, show time to crash in
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

Click on your mouse to start

"""

speed = -7800  # this is the useful variable to adjust; 8000 does a good orbit
angle = 90  # degrees up from positive x-axis

earth_radius = 6371000
initial_position = earth_radius * 1.05 * vector(cos(angle / 180 * pi), sin(angle / 180 * pi), 0)
ball_radius = 0.02 * earth_radius

animation = canvas(width=800, height=600, x=0, y=0, background=color.black, fov=0.001, range=2 * earth_radius, title=title)


earth = sphere(pos=vector(0, 0, 0), radius=earth_radius, texture=textures.earth)

# initialize the cannonball coming out of Newton's cannon
cannon = sphere(pos=vector(initial_position), radius=ball_radius, color=color.cyan)
cannon.velocity = speed * vector(initial_position.y, -initial_position.x, initial_position.z) / mag(initial_position)
cannon.acceleration = - 9.8 * cannon.pos / mag(cannon.pos)  # make point to center of Earth always
cannon.trail = curve(color=cannon.color)  # trace path

# initialize the cannonball dropped through the center of the Earth
dropped_uniform = sphere(pos=vector(initial_position), velocity=vector(0, 0, 0), radius=ball_radius, color=color.red)
dropped_uniform.acceleration = -9.8 * dropped_uniform.pos / mag(dropped_uniform.pos)
dropped_uniform.trail = curve(color=dropped_uniform.color)

# initialize the cannonball dropped toward an Earth-equivalent point mass at Earth's center
dropped_central = sphere(pos=vector(initial_position), velocity=vector(0, 0, 0), radius=ball_radius, color=vec(0.7, 0.7, 0.7))
dropped_central.acceleration = -9.8 * dropped_central.pos / mag(dropped_central.pos)
dropped_central.trail = curve(color=dropped_central.color)

t = .1  # set the time step
t_elapsed = 0  # we want to keep track of elapsed time, so zero the variable now

animation.waitfor("click")          # don't start until we click
while mag(cannon.pos) >= earth_radius:
    rate(1000)

    cannon.pos = cannon.pos + cannon.velocity * t + 0.5 * cannon.acceleration * t ** 2
    cannon.trail.append(pos=cannon.pos)
    cannon.velocity = cannon.velocity + cannon.acceleration * t
    cannon.acceleration = - 9.8 * cannon.pos / mag(cannon.pos)

    dropped_uniform.pos = dropped_uniform.pos + dropped_uniform.velocity * t + 0.5 * dropped_uniform.acceleration * t ** 2
    dropped_uniform.trail.append(pos=dropped_uniform.pos)
    dropped_uniform.velocity = dropped_uniform.velocity + dropped_uniform.acceleration * t
    dropped_uniform.acceleration = - 9.8 * (
            min(mag(dropped_uniform.pos), earth_radius) / earth_radius) ** 3 * dropped_uniform.pos / mag(
        dropped_uniform.pos)
    # Cubed term scales gravity by mass enclosed (Gauss' law) assuming constant density Earth (which is false).

    dropped_central.pos = dropped_central.pos + dropped_central.velocity * t + 0.5 * dropped_central.acceleration * t ** 2
    dropped_central.trail.append(pos=dropped_central.pos)
    dropped_central.velocity = dropped_central.velocity + dropped_central.acceleration * t
    dropped_central.acceleration = - 9.8 * dropped_central.pos / mag(dropped_central.pos)
    # This version treats all Earth's mass as being at Earth's center.

    t_elapsed = t_elapsed + t

totaltime = t_elapsed / 60
label(pos=vec(earth_radius * 1.1, earth_radius * 1.1, 0), text='elapsed time = %1.3f minutes' % totaltime)

while True:
    rate(50)