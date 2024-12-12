from vpython import box, vector, color, mag, arrow, hat, exp
from .charge import Charge, ec
from .field import Field

class Capacitor:
    def __init__(self, pos=vector(0, 1E-13, 0), plate_size=vector(4E-13, 4E-16, 4E-13), scale=1E-14):
        #self._up_plate = box(pos=pos, size=plate_size, color=color.blue)
        #self._down_plate = box(pos=-pos, size=plate_size, color=color.red)
        self._scale = scale
        self._up_plate = pos 
        self._down_plate = -pos
        self._field = None

    def charge(self):
        x_range = range(-20, 22, 2) 
        z_range = range(-20, 22, 2)
        charges = [Charge(
            position=vector(x * self._scale, self._up_plate.y, z * self._scale), 
            radius=self._scale, 
            coulomb=ec) for x in x_range for z in z_range]
        charges += [Charge(
            position=vector(x * self._scale, self._down_plate.y, z * self._scale), 
            radius=1E-14, 
            coulomb=-ec) for x in x_range for z in z_range]
        self._field = Field(charges)

    def show_field(self, x_range, y_range, z_range):
        self._field.show(x_range, y_range, z_range)

    def field_at(self, position):
        return self._field.field_at(position)
