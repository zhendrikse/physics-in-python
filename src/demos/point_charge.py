#
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/6_Point_Charge.py
#
from vpython import canvas, vec, color, arange, rate

from toolbox.charge import Positron
from toolbox.mouse import zoom_in_on


def on_mouse_click():
    zoom_in_on(scene)


scene = canvas(width=1000, height=600, align='left', range=3E-13)
scene.title = 'Select object to zoom in'
scene.bind('click', on_mouse_click)
charge = Positron(position=vec(0, 0, 0), radius=1.2E-14)
charge.show_field()

while True:
    pass
