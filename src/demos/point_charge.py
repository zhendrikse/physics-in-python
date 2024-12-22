#
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/6_Point_Charge.py
#
from vpython import canvas, vec

from toolbox.charge import Positron

scene = canvas(width=1000, height=600, align='left', range=3E-13)
charge = Positron(position=vec(0, 0, 0), radius=1.2E-14)
charge.show_field()

while True:
    pass
