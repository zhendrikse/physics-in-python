#Web VPython 3.2

from vpython import sphere, vector, cross, arange, arrow, sqrt, color, rate, canvas, slider, button

title="""&#x2022; <a href="https://www.glowscript.org/#/user/wlane/folder/PHYS152/program/magnetic-field">Original code</a> by <a href="https://www.youtube.com/@LetsCodePhysics">Let&apos;s code physics</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/proton_in_magnetic_field.py">proton_in_magnetic_field.py</a>

"""
display = canvas(title=title, width=600, forward=vector(0, .9, -.45), background=color.gray(0.075))

class Proton:
    def __init__(self, position=vector(0, 2, 0), velocity=vector(1, 0, 0), colour=color.red, radius=.1):
        self._proton = sphere(pos=position, radius=radius, color=colour, make_trail=True)
        self._velocity = velocity
        self._velocity_magnitude = 1
        self._mass = 1
        self._charge = 1

    def update_with(self, magnetic_field, dt=1e-4):
        force = self._charge * cross(self._velocity, magnetic_field)
        self._velocity += force * dt / self._mass
        self._proton.pos += self._velocity_magnitude * self._velocity * dt

    def position(self):
        return self._proton.pos

    def set_velocity_to(self, event):
        self._velocity_magnitude = event.value

    def reset(self):
        self._proton.clear_trail()
        self._proton.pos = vector(0, 2, 0)
        self._velocity = vector(1, 0, 0)

    def clear_trail(self):
        self._proton.clear_trail()

class MagneticField:
    def __init__(self, colour=color.cyan):
        self._strength = 1
        self._field_arrows = []

        dx, x_min, x_max, y_min, y_max = 0.5, -6, 6, -6, 6
        for x in arange(x_min, x_max + dx, dx):
            for y in arange(y_min, y_max + dx, dx):
                axis = self.field_vector_at(vector(x, y, 0)) * self._strength * .1
                self._field_arrows += [arrow(pos=vector(x, y, -0.5), axis=axis, color=colour)]

    def field_vector_at(self, position):
        b_x, b_y, b_z = 0, 0, sqrt(position.x * position.x + position.y * position.y)
        # b_z = 5 if (abs(abs(position.x)-1) < 0.2 and abs(abs(position.y)-1) < 0.2) else 0

        return self._strength * vector(b_x, b_y, b_z)

    def set_magnitude_to(self, event):
        self._strength = event.value
        for field_arrow in self._field_arrows:
            field_arrow.axis = self.field_vector_at(field_arrow.pos) * self._strength * .1

proton = Proton()
field = MagneticField()

display.append_to_caption("\nMagnetic field:")
_ = slider(min=0, max=2, value=1, length=300, bind=field.set_magnitude_to, right=display.width)
display.append_to_caption("\n\nProton velocity:")
_ = slider(min=0, max=3, value=1, length=300, bind=proton.set_velocity_to, right=display.width)
display.append_to_caption("\n\n")
_ = button(text="Reset", bind=proton.reset)
display.append_to_caption("  ")
_ = button(text="Clear trail", bind=proton.clear_trail)

dt = 1e-4  # Decrease in case of misbehavior!
while True:
    rate(1 / dt)
    proton.update_with(field.field_vector_at(proton.position()))
