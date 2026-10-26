#Web VPython 3.2

from vpython import canvas, cylinder, pi, cos, sin, color, sphere, vector, norm, mag, arrow, rate, arange

title = """
&#x2022; Original <a href="https://lectdemo.github.io/virtual/15_E_disk.html">15_E_disk.py</a> by Ruth Chabay 2004
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; toggle display of electric field

"""

animation = canvas(title = title, forward= vector( 0.34, 0.7, -0.6), background=color.gray(0.075))


w = .18
R = w * 50.
d = cylinder(pos=vector(0, 0, -w / 2), radius=R, axis=vector(0, 0, w), color=color.red)
Q = 1e-7
kel = 9e9
scale_factor_electric_Field = .2
r = 0.9 * R
N = 60.
dtheta = 2. * pi / N
arc = r * dtheta
dr = arc  ##0.15*R

class ChargedDisk:
    def __init__(self):
        self._sources = []
        for r in arange(1. * R, 0.01 * R, -dr):
            N = 2. * pi * r / arc
            dtheta = 2 * pi / N
            for theta in arange(0, 2 * pi - dtheta / 2., dtheta):
                p = sphere(pos=vector(r * cos(theta), r * sin(theta), w / 2), radius=0.2,
                           color=color.blue)
                self._sources.append(p)

        self._charges = [Q / float(len(self._sources)) for _ in self._sources]

        self._field = []
        self._show_field = False
        dx = R / 10.
        for x in arange(-1.1 * R, 1.1 * R + dr, dx):
            observer_location = vector(x, 0, 5. * w)
            electric_field = vector(0, 0, 0)
            for index in range(len(self._sources)):
                r = observer_location - self._sources[index].pos
                electric_field += kel * norm(r) * self._charges[index] / mag(r) ** 2

            self._field.append(arrow(pos=observer_location, color=vector(1, .5, 0), axis=scale_factor_electric_Field * electric_field, shaftwidth=0.4))

    def toggle_field(self):
        self._show_field = not self._show_field
        for field_arrow in self._field:
            field_arrow.visible = self._show_field

def toggle_background():
    animation.background = color.gray(0.075) if animation.background == color.white else color.white

def toggle_field():
    charged_disk.toggle_field()

def on_key_press(event):
    if event.key == " ":
        toggle_background()
    if event.key == 's':
        animation.capture("electric_field_of_charged_disk")

animation.bind("click", toggle_field)
animation.bind('keydown', on_key_press)

charged_disk = ChargedDisk()

while True:
    rate(60)
