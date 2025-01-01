#Web VPython 3.2

title = """Electric field of a dipole 

    &#x2022; Based on <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py">7_Dipole.py</a>
    &#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
    &#x2022; Select an object with mouse to zoom in'

    """

ec = 1.6E-19  # electron charge
k = 9E9  # Coulomb constant

from vpython import *


class FieldArrow:
    def __init__(self, position, field):
        colour = self.mapping(field)
        arrow_length = log(mag(field)) * 1E-15
        arrow(pos=position, axis=hat(field) * arrow_length, color=vec(1, colour, 0))

    def mapping(self, field):
        a = 1E-17
        return 1 - exp(-a * mag(field))


class Field:
    def __init__(self, charges=[]):
        self._charges = charges
        self._field_arrows = []

    def show(self, x_range, y_range, z_range):
        self._field_arrows = []
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    self._field_arrows += [self._field_arrow(x, y, z)]

    def _field_arrow(self, x, y, z):
        point = vec(x, y, z) * self._charge_radius()
        return FieldArrow(position=point, field=self.field_at(point))

    def _charge_radius(self):
        return self._charges[0].radius()  # Simply assuming all charges in the field have same radius

    def field_at(self, position):
        field = vector(0, 0, 0)
        for charge in self._charges:
            field += charge.field_at(position)
        return field


class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec,
                 colour=color.red, make_trail=False):
        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=coulomb, color=colour,
                              make_trail=make_trail)
        self._field_arrows = []

    def field_at(self, position):
        return hat(position - self._charge.pos) * k * self._charge.coulomb / mag(position - self._charge.pos) ** 2

    def radius(self):
        return self._charge.radius


class Dipole:
    def __init__(self, radius=1.2E-14):
        position = vec(10 * radius, 0, 0)
        self._charges = []
        self._charges += [Charge(position=position, radius=radius, coulomb=ec, colour=color.blue)]
        self._charges += [Charge(position=-position, radius=radius, coulomb=-ec)]

    def field(self):
        return Field(charges=self._charges)


def zoom_in_on(selected_object):
    if selected_object is None:
        return

    ### ANIMATE TO SELECTED POSITION
    temp_color = vec(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    step = (target - scene.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(20)
        scene.center += step
        scene.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color


def on_mouse_click():
    zoom_in_on(scene.mouse.pick)


scene = canvas(width=1000, height=600, align='top', range=3E-13)
scene.title = title
# scene.background = color.white
scene.caption = "Electric field \\( \\vec{E} ( \\vec{r} ) = -\\dfrac {1} {4\\pi\\epsilon_0} \\nabla \\bigg( \\dfrac{\\vec{r}  \\cdot \\vec{p}} {r^3} \\bigg) \\), where \\( \\vec{p}=+q(\\vec{r}_+) + -q(\\vec{r}_-) \\)"
MathJax.Hub.Queue(["Typeset", MathJax.Hub])
scene.bind('click', on_mouse_click)

dipole = Dipole()
dipole.field().show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))

