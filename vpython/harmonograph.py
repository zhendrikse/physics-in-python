# Web VPython 3.2

from vpython import *

title = """3D Spectral Harmonographs   Copyright 2014 Alan Richmond (Tuxar.uk)
&#x2022; Original <a href="https://www.glowscript.org/#/user/Mandrian/folder/My_Programs/program/Harmonograph3D">Harmonograph3D</a> found via <a href="https://prettymathpics.com/online-3d-spectral-harmonograph/">prettymathpics.com</a>
&#x2022; Refurbished in <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/harmonograph.py">harmonograph.py</a> by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Click with mouse to create another harmonograph!
&#x2022; MIT License.

"""

from vpython import *

width, height = 600, 600
mx = 4  # amplitude & frequency ranges (-/+)

display = canvas(title=title, width=width, height=height, background=color.gray(0.075))
display.autoscale = False


def randint(m, n):
    return int(random() * (n - m) + m)


# Box-Muller Transform To Create a Normal Distribution
def gauss(average, standard_deviation):
    u1 = random()
    u2 = random()
    vt = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
    vt *= standard_deviation + average
    return vt


def uniform(a, b):
    return random() * b


#   Amplitudes & scales
def scale(length):
    scale_factor = 90.0  # What this does is not exactly clear
    while True:
        a1, a2 = randint(-mx, mx), randint(-mx, mx)
        max = abs(a1) + abs(a2)
        if max > 0: break
    return a1, a2, length / (scale_factor * max)


# Main loop
class Harmonograph:
    def __init__(self, depth=width, trail_thickness=0.02, hue_increment=.159, decay_factor=0.9999, iters=150):
        self._drawing = True
        self._depth = depth
        self._iters = iters
        self._trail_thickness = trail_thickness
        self._hue_increment = hue_increment
        self._decay_factor = decay_factor
        self._trail = curve()

    def is_drawing(self):
        return self._drawing

    def start_drawing(self):
        self._drawing = True
        self.draw()

    def stop_drawing(self):
        self._drawing = False

    def draw(self):
        self._trail.visible = True
        #   Amplitudes & scales
        ax1, ax2, xscale = scale(width)
        ay1, ay2, yscale = scale(height)
        az1, az2, zscale = scale(self._depth)
        #   Frequencies
        sd = 0.002
        fx1, fx2 = randint(1, mx) + gauss(0, sd), randint(1, mx) + gauss(0, sd)
        fy1, fy2 = randint(1, mx) + gauss(0, sd), randint(1, mx) + gauss(0, sd)
        fz1, fz2 = randint(1, mx) + gauss(0, sd), randint(1, mx) + gauss(0, sd)
        #   Phases
        px1, px2 = uniform(0, 2 * pi), uniform(0, 2 * pi)
        py1, py2 = uniform(0, 2 * pi), uniform(0, 2 * pi)
        pz1, pz2 = uniform(0, 2 * pi), uniform(0, 2 * pi)

        first = True
        x = y = z = 0.0
        k = 1
        hue = 0

        t = 0
        dt = 0.02

        #   Note that there are 2 nested loops here, where 1 should suffice BUT curve() only takes
        #   1000 points before dropping some. See bottom of http://vpython.org/contents/docs/curve.html
        #   My solution is to start a new trail every 1000 points.
        for j in range(self._iters):
            if not first:
                self._trail = curve(pos=vector(x, y, z), color=color.hsv_to_rgb(vector(hue, 1, 1)),
                                    radius=self._trail_thickness)
            for i in range(self._iters):
                # rate(600)
                #   Each pendulum axis is sum of 2 independent frequencies
                x = xscale * k * (ax1 * sin(t * fx1 + px1) + ax2 * sin(t * fx2 + px2))
                y = yscale * k * (ay1 * sin(t * fy1 + py1) + ay2 * sin(t * fy2 + py2))
                z = zscale * k * (az1 * sin(t * fz1 + pz1) + az2 * sin(t * fz2 + pz2))
                self._trail.append(pos=vector(x, y, z), color=color.hsv_to_rgb(vector(hue, 1, 1)),
                                   radius=self._trail_thickness)
                #            f.rotate(angle=0.00005)
                # cycle hue
                hue = (hue + dt * self._hue_increment) % 360
                t += dt
                k *= self._decay_factor
            first = False
        self._drawing = False


harmonograph = Harmonograph()
harmonograph.draw()


def on_mouse_click():
    global draw
    if harmonograph.is_drawing():
        harmonograph.stop_drawing()
    else:
        for obj in display.objects:
            obj.visible = False
        harmonograph.start_drawing()


display.bind('click', on_mouse_click)

draw = True
while True:
    rate(60)
