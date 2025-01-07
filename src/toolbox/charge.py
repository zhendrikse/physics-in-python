from vpython import vec, sphere, color, mag, hat
from .field import PointChargeField

Q = 1.6E-19  # charge magnitude of electron
k = 9E9  # Coulomb's law constant
classic_electron_radius = 2.8179E-15
electron_mass = 9.1093837E-31  # kilograms


class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1E-14, charge=Q,
                 colour=None, make_trail=False, retain=-1, draw=True):
        colour = colour if colour is not None else color.blue if charge > 0 else color.red
        self._ball = sphere(mass=mass, pos=position, radius=radius, color=colour,
                            make_trail=make_trail, retain=retain) if draw else None
        self._field = PointChargeField(self)
        self._velocity = velocity
        self._position = position
        self._radius = radius
        self._charge = charge
        self._mass = mass
        self._initial_position = position
        self._initial_velocity = velocity

    def _draw(self):
        if self._ball:
            self._ball.pos = self._position

    def show_field(self):
        self._field.show()

    def field_at(self, position):
        return hat(position - self._position) * k * self._charge / mag(position - self._position) ** 2

    def reset(self):
        self._position = self._initial_position
        self._velocity = self._initial_velocity
        self._ball.clear_trail()
        self._ball.pos = self._position

    def set_initial_x_velocity(self, velocity_x):
        self._initial_velocity = vec(velocity_x, 0, 0)

    def set_charge_to(self, value):
        self._charge = value

    @property
    def coulomb(self):
        return self._charge

    @property
    def position(self):
        return self._position

    @property
    def radius(self):
        return self._radius

    @property
    def charge(self):
        return self._charge

    def delete(self):
        self._ball.clear_trail()
        self._ball.visible = False
        del self._ball
        self._field.delete()

    def coulomb_force_in(self, electric_field):
        return electric_field * self._charge

    def update(self, coulomb_force, dt):
        self._velocity += coulomb_force / self._mass * dt
        self._position += self._velocity * dt
        self._draw()


class Electron(Charge):
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=classic_electron_radius, make_trail=False, retain=-1):
        super().__init__(mass=electron_mass, position=position, velocity=velocity, radius=radius,
                         charge=-Q, make_trail=make_trail, retain=retain)


class Positron(Charge):
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=classic_electron_radius, make_trail=False, retain=-1):
        super().__init__(mass=electron_mass, position=position, velocity=velocity, radius=radius,
                         charge=-Q, make_trail=make_trail, retain=retain)
