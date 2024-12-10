#
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/8_Charge_Motion.py
#
from vpython import vec, color, rate, canvas, button
from toolbox.capacitor import Capacitor
from toolbox.charge import Charge, ec     


scene = canvas(width=1000, height=600, align='left', range=3E-13)

def main():
    dt = 0.01
    moving_charge = Charge(position=vec(-4E-13, 5E-14, 0), 
                           velocity=vec(1.5E-13, 0, 0), 
                           radius=1.2E-14, 
                           coulomb=5E-42*ec, 
                           colour=color.green, 
                           make_trail=True)
    
    capacitor = Capacitor(pos=vec(0, 1E-13, 0), 
                          size=vec(4E-13, 4E-16, 4E-13))
    
    capacitor.show_field(x_range=range(-18, 18, 8), 
                         y_range=range(-9, 9, 4), 
                         z_range=range(-18, 18, 8))
    
    for t in range(0, 600):
        rate(10/dt)
        field = capacitor.field_at(moving_charge.position)
        coulomb_force = moving_charge.coulomb_force_in(field)
        moving_charge.update(coulomb_force, dt)
    
    while True:
        pass

main()
