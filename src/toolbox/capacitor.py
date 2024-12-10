from vpython import box, vec, color, mag, arrow, hat, exp
from .charge import Charge, ec
from .field import Field

class Capacitor:
    def __init__(self, pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13)):
        # create two plates and create a capacitor 
        self._up_plate = box(pos=pos, size=size, color=color.blue)
        self._down_plate = box(pos=-pos, size=size, color=color.red)

        # fill the plates with charge
        charges = []
        for x in range(-20, 22, 2):
            for y in [self._up_plate.pos.y, self._down_plate.pos.y]:
                for z in range(-20, 22, 2):
                    # positive charge and negative charge locate at top plate and down plate
                    mu = 1 if y > 0  else -1
                    charges.append(Charge(position=vec(x*1E-14, y, z*1E-14), radius=1E-14, coulomb=mu * ec))

        self._field = Field(charges)

    def show_field(self, x_range, y_range, z_range):
        self._field.show(x_range, y_range, z_range)

    def field_at(self, position):
        return self._field.field_at(position)
