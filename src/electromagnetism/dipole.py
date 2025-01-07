##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py
#

from vpython import canvas, vec, rate

from src.toolbox.charge import Charge, Q
from src.toolbox.field import Field
from src.toolbox.mouse import zoom_in_on

title = """Electric field of a dipole 

    &#x2022; Based on <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py">7_Dipole.py</a>
    &#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
    &#x2022; Select an object with mouse to zoom in'

"""

animation = canvas(width=1000, height=600, align='top', range=3E-13, title = title)

class Dipole:
    def __init__(self, radius=1.2E-14):
        position = vec(10 * radius, 0, 0)
        self._charges = [Charge(position=position, radius=radius, charge=Q),
                         Charge(position=-position, radius=radius, charge=-Q)]

    def show_field(self):
        Field(self._charges).show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))


def on_mouse_click():
    zoom_in_on(animation)

animation.bind('click', on_mouse_click)

Dipole().show_field()

while True:
    rate(10)
