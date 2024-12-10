from vpython import box, vec, color, mag, arrow, hat, exp
from functools import reduce    
from .charge import Charge, FieldArrow, k, ec

class Capacitor:
    def __init__(self, pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13)):
        # create two plates and create a capacitor 
        self._up_plate = box(pos=pos, size=size, color=color.blue)
        self._down_plate = box(pos=-pos, size=size, color=color.red)

        # fill the plates with charge
        self._charges = []
        for x in range(-20, 22, 2):
            for y in [self._up_plate.pos.y, self._down_plate.pos.y]:
                for z in range(-20, 22, 2):
                    # positive charge and negative charge locate at top plate and down plate
                    mu = 1 if y > 0  else -1
                    self._charges.append(Charge(position=vec(x*1E-14, y, z*1E-14), coulomb=mu * ec))

        # create field between plates
        field_arrows = []
        for x in range(-9, 9, 4):
            for y in range(-9, 9, 4):
                for z in range(-9, 9, 4):
                    point = vec(x*2E-14, y*1E-14, z*2E-14)
                    field_arrows.append(FieldArrow(point, self.field_at(point)))

    def field_at(self, position):
        return reduce(lambda x, y: x + y, [charge.field_at(position) for charge in self._charges])
