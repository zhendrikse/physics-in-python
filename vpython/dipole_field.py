#Web VPython 3.2

from vpython import arrow, canvas, log, hat, vec, exp, mag, sin, cos, pi, color, rate, sphere

title = """&#x2022; Based on <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py">7_Dipole.py</a>
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/dipole_field.py">dipole_field.py</a>

"""

caption = """
Electric field $\\vec{E} ( \\vec{r} ) = -\\dfrac {1} {4\\pi\\epsilon_0} \\nabla \\bigg( \\dfrac{\\vec{r}  \\cdot \\vec{p}} {r^3} \\bigg)$, where $\\vec{p}=+q(\\vec{r}_+) + -q(\\vec{r}_-)$
"""

ec = 1.6E-19  # electron charge
k = 9E9  # Coulomb constant

animation = canvas(background=color.gray(0.075), align='top', range=4E-13, title = title, caption=caption)

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
        field = vec(0, 0, 0)
        for charge in self._charges:
            field += charge.field_at(position)
        return field


class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec, colour=color.red, make_trail=False):
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

    def show_field(self):
        Field(charges=self._charges).show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))

#animation.autoscale = False
sphere(pos=vec(0, 0, 0),texture="https://i.imgur.com/1nVWbbd.jpg",radius=1e-12,shininess=0,opacity=0.5)
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

Dipole().show_field()

n_max = 100
n_rot = 10
R_camera = mag(animation.camera.pos)
theta_camera = pi/2
phi_camera = 0
d_theta_camera = -pi/(5 * n_max)
d_phi_camera = pi / (5 * n_max) * 2
theta_camera_max = 2*pi/3
theta_camera_min = pi/3

while True:
   rate(20)
   if theta_camera > theta_camera_max or theta_camera < theta_camera_min:
       d_theta_camera *= -1
   theta_camera += d_theta_camera
   phi_camera += d_phi_camera
   animation.camera.pos = R_camera*vec(sin(theta_camera)*sin(phi_camera),cos(theta_camera),sin(theta_camera)*cos(phi_camera))
   animation.camera.axis = -animation.camera.pos
