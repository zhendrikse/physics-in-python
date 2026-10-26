# We VPython 3.2
from vpython import vector, canvas, color, cylinder, arrow, rate, sin, cos, checkbox, pi, norm, mag, cross, slider, arange, wtext, sphere

title = """ 
&#x2022; <a href="https://lectdemo.github.io/virtual/23_antenna.html">23_antenna.py</a> by Ruth Chabay Spring 2001
&#x2022; Refactored by <a href="https://www.hendrikse.name">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/antenna.py">antenna.py</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;v&gt; &rarr; verbose output

"""

animation = canvas(title=title, background=color.gray(0.075), forward=vector(-0.1, -0.4, -0.9), range=10)

show_decrease = True
lambda_ = 2.  ##1e-10
c = 3e8
omega = 2 * pi * c / lambda_
d = 2 * lambda_
L = 2 * lambda_
antenna = cylinder(pos=vector(0, -L / 2, 0), axis=vector(0, L, 0), color=vector(.7, .7, .7), radius=0.5)

ds = lambda_ / 20.
dt = lambda_ / c / 100.
dist_to_screen = 4.0 * lambda_

slit1 = vector(0, 0, -d / 2)


class ElectromagneticWave:
    def __init__(self, E0=lambda_ * 5):
        self._E0 = E0
        self._electric_field = []
        self._magnetic_field = []
        dtheta = pi / 3
        for r1 in [dist_to_screen * vector(cos(theta), 0, sin(theta)) for theta in arange(0, 2 * pi, dtheta)]:
            dr1 = ds * norm(r1)
            rr1 = slit1 + 10 * dr1  ##vector(0,0,0) ## current loc along wave 1
            for ct in range(0, 120):
                axis = vector(0, (self._E0 * cos(2 * pi * mag(rr1 - slit1)) / lambda_), 0)
                electric_arrow = arrow(pos=rr1, axis=axis, color=color.orange, shaftwidth=lambda_ / 40.)
                magnetic_arrow = arrow(pos=rr1, axis=vector(0, 0, 0), color=color.cyan, shaftwidth=lambda_ / 40.)
                self._magnetic_field.append(magnetic_arrow)
                self._electric_field.append(electric_arrow)
                rr1 += dr1

    def update(self):
        for index in range(len(self._electric_field)):
            field_arrow = self._electric_field[index]
            decrease = 1 / (mag(field_arrow.pos) + lambda_ / 20) if show_decrease else 1.0
            field_arrow.axis = vector(0, decrease * self._E0 * cos(
                omega * t - 2 * pi * mag(field_arrow.pos - slit1) / lambda_), 0)
            self._magnetic_field[index].axis = -cross(field_arrow.axis, i_hat) * .7

    def toggle_magnetic_field(self):
        for field_vector in self._magnetic_field:
            field_vector.visible = not field_vector.visible

    def set_field_strength_to(self, new_value):
        self._E0 = new_value


def toggle_magnetic_field():
    electromagnetic_wave.toggle_magnetic_field()


def toggle_background():
    animation.background = color.gray(0.075) if animation.background == color.white else color.white


def toggle_decrease():
    global show_decrease
    show_decrease = not show_decrease


def adjust_field():
    electromagnetic_wave.set_field_strength_to(field_slider.value * lambda_)
    field_text.text = "{:1.2f}".format(field_slider.value, 2)


_ = checkbox(bind=toggle_background, text="Dark color scheme", checked=True)
_ = checkbox(bind=toggle_decrease, text="Show decrease", checked=True)
_ = checkbox(bind=toggle_magnetic_field, text="Show magnetic field", checked=True)

animation.append_to_caption("\n\n")
field_slider = slider(min=1, max=10, value=5, bind=adjust_field)
animation.append_to_caption(" Field strength = ")
field_text = wtext(text="5")


def on_key_press(event):
    global show_decrease
    if event.key == 's':
        animation.capture("antenna_waves")
    if event.key == 'v':
        print("animation.center=" + str(animation.center))
        print("animation.forward=" + str(animation.forward))
        print("animation.range=" + str(animation.range))

sphere(pos=vector(0, 0, 0),texture="https://i.imgur.com/1nVWbbd.jpg",radius=30,shininess=0,opacity=0.5)
electromagnetic_wave = ElectromagneticWave()
animation.bind("keydown", on_key_press)

t = 0.0
i_hat = vector(1, 0, 0)
while 1:
    rate(50)
    t = t + dt
    electromagnetic_wave.update()
