#Web VPython 3.2

from vpython import arrow, hat, vec, exp, sphere, mag, color, wtext, canvas, rate, label, slider

title = """Moving charge through electric field between two plates 

&#x2022; Based on <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/8_Charge_Motion.py">8_Charge_Motion.py</a>
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/moving_charge.py">moving_charge.py</a>

"""

ec = 1.6E-19  # electron charge
k = 9E9  # Coulomb constant


class FieldArrow:
    def __init__(self, position, field):
        colour = self.mapping(field)
        arrow_length = 3E-14
        arrow(pos=position, axis=hat(field) * arrow_length, color=vec(1, colour, 0))

    def mapping(self, field):
        a = 1E-17
        return 1 - exp(-a * mag(field))


class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec, charge_color=None, make_trail=False):
        colour = charge_color
        if colour is None:
            colour = color.blue if coulomb > 0 else color.red

        self._sphere = sphere(mass=mass, pos=position, radius=radius, color=colour, make_trail=make_trail)
        self._charge = coulomb
        self._velocity = velocity
        self._position = position
        self._radius = radius
        self._mass = mass
        self._initial_position = position
        self._initial_velocity = velocity

    def reset(self):
        self._position = self._initial_position
        self._velocity = self._initial_velocity
        self._sphere.clear_trail()
        self._sphere.pos = self._position

    def field_at(self, position):
        return hat(position - self._position) * k * self._charge / mag(position - self._position) ** 2

    def radius(self):
        return self._radius

    def position(self):
        return self._position

    def charge(self):
        return self._charge

    def set_initial_x_velocity(self, velocity_x):
        self._initial_velocity = vec(velocity_x, 0, 0)

    def set_charge_to(self, value):
        self._charge = value

    def coulomb_force_in(self, electric_field):
        return electric_field * self._charge

    def update(self, coulomb_force, dt):
        # use formula: s = v0*t + 1/2*a*t^2
        self._velocity += coulomb_force / self._mass * dt
        self._position += self._velocity * dt
        self._sphere.pos = self._position


class Field:
    def __init__(self, charges=[]):
        self._charges = charges
        self._field_arrows = []

    def show(self, x_range, y_range, z_range):
        self._field_arrows = []
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    self._field_arrows.append(self._field_arrow(x, y, z))

    def _field_arrow(self, x, y, z):
        point = vec(x, y, z) * self._charge_radius()
        return FieldArrow(position=point, field=self.field_at(point))

    def _charge_radius(self):
        return self._charges[0].radius()  # Simply assuminging all charges in the field have same radius

    def field_at(self, position):
        field = vec(0, 0, 0)
        for charge in self._charges:
            field += charge.field_at(position)
        return field


class Capacitor:
    def __init__(self, pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13)):
        # fill the plates with charge
        top_plate_y_pos = vec(0, 1E-13, 0).y
        bottom_plate_y_pos = -vec(0, 1E-13, 0).y
        charges = []
        for x in range(-20, 22, 2):
            for y in [top_plate_y_pos, bottom_plate_y_pos]:
                for z in range(-20, 22, 2):
                    # positive charge and negative charge locate at top plate and down plate
                    mu = 1 if y > 0 else -1
                    charges.append(Charge(position=vec(x * 1E-14, y, z * 1E-14), radius=1E-14, coulomb=mu * ec))

        self._field = Field(charges)
        self._field.show(x_range=range(-18, 18, 8), y_range=range(-9, 9, 4), z_range=range(-18, 18, 8))

    def show_field(self, x_range, y_range, z_range):
        self._field.show(x_range, y_range, z_range)

    def field_at(self, position):
        return self._field.field_at(position)


animation = canvas(background=color.gray(.075), align='top', range=3E-13, forward=vec(0.35, -0.20, -0.9), title=title)
capacitor = Capacitor(pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13))
capacitor.show_field(x_range=range(-18, 18, 8), y_range=range(-9, 9, 4), z_range=range(-18, 18, 8))
moving_charge = Charge(position=vec(-4E-13, 5E-14, 0), velocity=vec(1.5E-13, 0, 0), radius=1.2E-14, coulomb=5E-42 * ec, charge_color=color.green, make_trail=True)
sphere(pos=vec(0, 0, 0),texture="https://i.imgur.com/1nVWbbd.jpg",radius=2e-12,shininess=0,opacity=0.5)

animation.append_to_caption("\n")


def adjust_velocity():
    moving_charge.set_initial_x_velocity(velocity_slider.value * 1E-13)
    velocity_slider_text.text = velocity_slider.value + " 1E-13 m/s"


def adjust_q():
    moving_charge.set_charge_to(charge_slider.value * ec * 5E-42)
    charge_slider_text.text = charge_slider.value + " electron charge(s)"


velocity_slider = slider(min=0.1, max=5, step=0.1, value=1.5, bind=adjust_velocity)
animation.append_to_caption(" Velocity in x-direction = ")
velocity_slider_text = wtext(text="1.5 E-13 m/s")
animation.append_to_caption("\n\n")

charge_slider = slider(min=0, max=5, step=0.1, value=1, bind=adjust_q)
animation.append_to_caption(" Q = ")
charge_slider_text = wtext(text="1 electron charge")
animation.append_to_caption("\n\n")

dt = 0.01
pop_up = label(pos=vec(0, 2E-13, 0), text="Click mouse button to repeat", visible=False)
while True:
    while moving_charge.position().x < 6E-13:
        rate(1 / dt)
        field = capacitor.field_at(moving_charge.position())
        coulomb_force = moving_charge.coulomb_force_in(field)
        moving_charge.update(coulomb_force, dt)

    pop_up.visible = True
    animation.waitfor("click")
    pop_up.visible = False
    moving_charge.reset()
