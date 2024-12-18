from vpython import vec, arrow, hat, exp, mag, sin, cos, pi
from functools import reduce


class FieldArrow:
    def __init__(self, position, field, point_charge=False, arrow_length=3E-14):
        color = FieldArrow.color_mapping(field)
        colour = vec(color, 0, 1) if point_charge else vec(1, color, 0)
        arrow(pos=position, axis=hat(field) * arrow_length, color=colour)

    @staticmethod
    def color_mapping(field):
        a = 1E-17
        return 1 - exp(-a * mag(field))


class PointChargeField:
    def __init__(self, charge):
        self._charge = charge
        self._field_arrows = []

    def show(self, r_range=range(1, 30, 5), theta_range=range(0, 6), phi_range=range(0, 6)):
        self._field_arrows = [self._field_arrow(r, theta, phi) for r in r_range for theta in theta_range for phi in
                              phi_range]

    def _field_arrow(self, r, theta, phi):
        xyz = PointChargeField.to_carthesian_coordinates(self._charge.radius * r, theta * pi / 3, phi * pi / 3)
        return FieldArrow(xyz, self._charge.field_at(xyz), True)

    @staticmethod
    def to_carthesian_coordinates(r, theta, phi):
        x = r * sin(theta) * cos(phi)
        y = r * sin(theta) * sin(phi)
        z = r * cos(theta)
        return vec(x, y, z)


class Field:
    def __init__(self, charges=[]):
        self._charges = charges
        self._field_arrows = []

    def show(self, x_range, y_range, z_range):
        self._field_arrows = [self._field_arrow(x, y, z) for x in x_range for y in y_range for z in z_range]

    def _field_arrow(self, x, y, z):
        point = vec(x, y, z) * self._charge_radius
        return FieldArrow(point, self.field_at(point))

    @property
    def _charge_radius(self):
        return self._charges[0].radius  # Simply assuming all charges in the field have same radius

    def field_at(self, position):
        return reduce(lambda x, y: x + y, [charge.field_at(position) for charge in self._charges])
