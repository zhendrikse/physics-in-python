from vpython import vec, arrow, hat, exp, mag, sin, cos, pi
from functools import reduce    

class FieldArrow:
    def __init__(self, position, field, point_charge=False, arrow_length= 3E-14):
        color = FieldArrow.color_mapping(field)
        colour = vec(color, 0, 1) if point_charge else vec(1, color, 0)
        arrow(pos=position, axis=hat(field) * arrow_length, color=colour)

    @staticmethod
    def color_mapping(field):
        a = 1E-17
        return 1 - exp(-a * mag(field))

class Field:
    def __init__(self, charges=[]):
        self._charges = charges
        self._single_charge = len(charges) == 1
        self._field_arrows = []

    def show_field(self, x_range=range(-9, 9, 4), y_range=range(-9, 9, 4), z_range=range(-9, 9, 4)):
        self._field_arrows = self._radial_field() if self._single_charge else self._field()
            
    def _field(self, x_range=range(-9, 9, 4), y_range=range(-9, 9, 4), z_range=range(-9, 9, 4)):
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    point = vec(x * 2E-14, y * 1E-14, z * 2E-14)
                    self._field_arrows.append(FieldArrow(point, self.field_at(point)))

    def _radial_field(self):
        for r in range(1, 30, 5):
            for theta in range(0, 6):
                for phi in range(0, 6):
                    xyz = Field.to_carthesian_coordinates(self._charges[0].radius * r, theta * pi/3, phi * pi/3)
                    self._field_arrows.append(FieldArrow(xyz, self.field_at(xyz), True))

    @staticmethod
    def to_carthesian_coordinates(r, theta, phi):
        x = r * sin(theta) * cos(phi)
        y = r * sin(theta) * sin(phi)
        z = r * cos(theta)
        return vec(x, y, z)


    def field_at(self, position):
        return reduce(lambda x, y: x + y, [charge.field_at(position) for charge in self._charges])