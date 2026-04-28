#Web VPython 3.2

from vpython import label, box, canvas, vec, color, cylinder, sphere, cos, sin, pi, rate, checkbox, textures, slider

title="""&#x2022; Based on <a href="https://glowscript.org/#/user/yizhe/folder/Public/program/PendulumWave">PendulumWave</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/waves/code/pendulum_wave.py">pendulum_wave.py</a>
&#x2022; Related to <a href="https://www.hendrikse.name/science/kinematics/newtons_cradle.html">Newton&apos;s cradle</a> simulation

&#x2022; $\\theta(t)=\\theta_0 \\cos \\bigg( \\sqrt{  \\dfrac {g} {L}} t \\bigg)$

"""


g = 9.8
Tpw = 30
N = 15
Tmax = Tpw / N
Lmax = Tmax ** 2 * g / (4 * pi ** 2)
width = Lmax
total_balls = 20
size = .75 * (width / total_balls)


display = canvas(title=title, width=600, height=600, background=color.gray(0.075))
display.camera.pos = 1.4 * vec(-1.5 * width, 0 * width, width)
display.camera.axis = -display.camera.pos

floor = box(pos=vec(0, -.75 * (width + size) , 0), size=2 * vec(width, size, width), texture=textures.granite)
roof = box(pos=vec(0, (width + size) / 2, 0), size=vec(width * 1.25, size, 0.5 * width), texture=textures.wood)
cylinder(pos=vec(width * 1.2, width + size, -.4* width) / 2, axis=vec(0, -1.25, -.5), radius=-.02, texture=textures.wood)
cylinder(pos=vec(width * 1.2, width + size, +.4* width) / 2, axis=vec(0, -1.25,  .5), radius=-.02, texture=textures.wood)
cylinder(pos=vec(-width * 1.2, width + size, +.4* width) / 2, axis=vec(0, -1.25,  .5), radius=-.02, texture=textures.wood)
cylinder(pos=vec(-width * 1.2, width + size, -.4* width) / 2, axis=vec(0, -1.25, -.5), radius=-.02, texture=textures.wood)
timer = label(pos=vec(width, width, 0) * 1.5, text="t =  s", space=50, height=24, font="monospace", box=False, color=color.yellow)


class Pendulum:
    def __init__(self, T, position, colour, theta0=pi/6, mass=1):
        self._pos = position
        self._length = T ** 2 * g / (4 * pi * pi)
        self._inertia = mass * self._length ** 2
        self._omega = 0
        self._theta = theta0
        self._mass = mass
        ball_position = vec(self._pos, 0.5 * width - self._length * cos(theta0), self._length * sin(theta0))
        self._ball = sphere(pos=ball_position, radius=size, color=colour)
        self._rope = cylinder(pos=vec(self._pos, width / 2, 0), axis=ball_position - vec(self._pos, width / 2, 0), radius=0.1 * size, color=color.yellow)

    def update(self, dt):
        alpha = -self._mass * g * self._ball.pos.z / self._inertia
        self._omega += alpha * dt
        self._theta += self._omega * dt
        self._ball.pos = vec(self._pos, 0.5 * width - self._length * cos(self._theta), self._length * sin(self._theta))
        self._rope.axis = self._ball.pos - vec(self._pos, 0.5 * width, 0)


pendulums = []
for i in range(total_balls):
    T = Tpw / (N + i)
    loc = width * (-0.5 + (i / (total_balls - 1)))
    pendulum = Pendulum(T, loc, vec(1 - i / total_balls, 0, i / total_balls))
    pendulums.append(pendulum)

def toggle_clock(event):
    timer.visible = event.checked

fps = 500
def animation_speed(event):
    global fps
    fps = event.value

_ = checkbox(text="Clock", bind=toggle_clock, checked=True)
display.append_to_caption("\n\nFrames per second")
_ = slider(min=1, max=500, value=500, bind=animation_speed)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])
t = 0
delta_t = 0.001
while True:
    rate(fps)
    for pendulum in pendulums:
        pendulum.update(delta_t)
    timer.text = "t = {:.1f} s".format(t)
    t += delta_t
