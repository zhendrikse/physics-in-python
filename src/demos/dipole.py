##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py
#

from vpython import canvas, vec
from toolbox.charge import Charge, ec
from toolbox.field import Field

class Dipole:
    def __init__(self, radius=1.2E-14):
        position = vec(10 * radius, 0, 0)
        self._charges = [Charge(position=position, radius=radius, coulomb=ec),
                         Charge(position=-position, radius=radius, coulomb=ec)]

    @property
    def field(self):
        return Field(self._charges)

def main():
    scene = canvas(width=1000, height=600, align='left', range=3E-13)
    dipole = Dipole()
    dipole.field.show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))

    while True:
        pass

if __name__=="__main__":
    main()
