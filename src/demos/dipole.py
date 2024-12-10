##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py
#

from vpython import canvas, vec, sphere, arrow, mag, hat, cos, sin, exp
from toolbox.charge import Charge, ec
from toolbox.field import Field

def main():
    scene = canvas(width=1000, height=600, align='left', range=3E-13)
    charges = []
    
    radius = 1.2E-14
    charges.append(Charge(position=vec(10 * radius, 0, 0), radius=radius, coulomb=ec))
    charges.append(Charge(position=vec(-10 * radius, 0, 0), radius=radius, coulomb=ec))

    field = Field(charges)
    field.show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))

    while True:
        pass

if __name__=="__main__":
    main()
