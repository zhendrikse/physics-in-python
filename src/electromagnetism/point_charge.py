from vpython import canvas, vec, color, arange, rate

from src.toolbox.particle import Positron
from src.toolbox.mouse import zoom_in_on

title = """Electric field of a point charge 

&#x2022; Based on <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/6_Point_Charge.py">6_Point_Charge.py</a>
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; Select an object with mouse to zoom in

"""

def on_mouse_click():
    zoom_in_on(animation)

animation = canvas(width=1000, height=600, align='left', range=3E-13, title = title, forward = vec(-0.492668, -0.285952, -0.821894))
animation.bind('click', on_mouse_click)
charge = Positron(position=vec(0, 0, 0), radius=1.2E-14)
charge.show_field()

while True:
    rate(10)
