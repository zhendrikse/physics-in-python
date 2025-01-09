from vpython import vec, color, rate, canvas, slider, wtext, label

from src.toolbox.capacitor import Capacitor
from src.toolbox.particle import Particle, Q


title = """Moving charge through electric field between two plates 

&#x2022; Based on <a href="https://github.com/Physics-Morris/Physics-Vpython/blob/master/8_Charge_Motion.py">8_Charge_Motion.py</a>
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Located in the <a href="https://github.com/zhendrikse/physics-in-python/">Physics in Python GitHub repository</a>

"""

ec = 1.6E-19  # electron charge
k = 9E9  # Coulomb constant

animation = canvas(width=1000, height=600, align='top', range=3E-13, title=title)
animation.append_to_caption("\n")


def adjust_velocity():
    moving_charge.set_initial_x_velocity(velocity_slider.value * 1E-13)
    velocity_slider_text.text = velocity_slider.value + " 1E-13 m/s"


def adjust_q():
    moving_charge.set_charge_to(charge_slider.value * ec * 5E-42)
    charge_slider_text.text = charge_slider.value + " electron charge(s)"


velocity_slider = slider(min=0.1, max=5, step=0.1, value=1.5, bind=adjust_velocity)
animation.append_to_caption(" Velocity in x-direction = ")
velocity_slider_text = wtext(text="1.5 E-13 m/s")
animation.append_to_caption("\n\n")

charge_slider = slider(min=0, max=5, step=0.1, value=1, bind=adjust_q)
animation.append_to_caption(" Q = ")
charge_slider_text = wtext(text="1 electron charge")
animation.append_to_caption("\n\n")

moving_charge = Particle(position=vec(-4E-13, 5E-14, 0),
                         velocity=vec(1.5E-13, 0, 0),
                         radius=1.2E-14,
                         charge=5E-42 * Q,
                         colour=color.green,
                         make_trail=True)

capacitor = Capacitor(pos=vec(0, 1E-13, 0),
                      plate_size=vec(4E-13, 4E-16, 4E-13))
capacitor.charge()
capacitor.show_field(x_range=range(-18, 18, 8),
                     y_range=range(-9, 9, 4),
                     z_range=range(-18, 18, 8))


dt = 0.01
pop_up = label(pos=vec(0, 2E-13, 0), text="Click mouse button to repeat", visible=False)
while True:
    while moving_charge.position().x < 6E-13:
        rate(1 / dt)
        field = capacitor.field_at(moving_charge.position())
        coulomb_force = moving_charge.coulomb_force_in(field)
        moving_charge.update(coulomb_force, dt)

    pop_up.visible = True
    animation.waitfor("click")
    pop_up.visible = False
    moving_charge.reset()
