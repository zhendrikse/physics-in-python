##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py
#

from vpython import canvas, vec, arange, rate, color
from ..toolbox.charge import Charge, Q
from ..toolbox.field import Field
from ..toolbox.mouse import zoom_in_on


class Dipole:
    def __init__(self, radius=1.2E-14):
        position = vec(10 * radius, 0, 0)
        self._charges = [Charge(position=position, radius=radius, charge=Q),
                         Charge(position=-position, radius=radius, charge=-Q)]

    @property
    def field(self):
        return Field(self._charges)


def on_mouse_click():
    zoom_in_on(scene)


scene = canvas(width=1000, height=600, align='left', range=3E-13)
scene.title = "Click mouse to zoom in"
scene.bind('click', on_mouse_click)

dipole = Dipole()
dipole.field.show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))

while True:
    pass
