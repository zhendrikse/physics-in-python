#
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/8_Charge_Motion.py
#
from vpython import canvas, box, vec, sphere, color, rate, mag, arrow, hat, exp

# parameter setting
ec = 1.6E-19            # electron charge

class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, C=1, colour=None, make_trail=False):
        colour = colour if colour is not None else color.blue if C > 0 else color.red
        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=C * ec, color=colour, make_trail=make_trail)
        
    @property
    def coulomb(self):
        return self._charge.coulomb
    
    @property
    def position(self):
        return self._charge.pos
    
    def coulomb_force(self, electric_field):
        return electric_field * self._charge.coulomb

    def update(self, coulomb_force, dt):
        '''given a charge and position and update position'''
        # use formula: s = v0*t + 1/2*a*t^2
        self._charge.v += coulomb_force / self._charge.mass * dt
        self._charge.pos += self._charge.v * dt
    
class FieldArrow:
    def __init__(self, position, E):        
        color = self._mapping(E)
        arrow_length = 3E-14    # length of arrow
        arrow(pos=position, axis=hat(E) * arrow_length, color=vec(1, color, 0))

    def _mapping(self, E):
        '''mapping from (Inf, 0) to (1, 0) as the rgb color value'''
        a = 1E-17
        return 1 - exp(-a * mag(E))


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
                    self._charges.append(Charge(position=vec(x*1E-14, y, z*1E-14), C=mu))

        # create field between plates
        field_arrows = []
        for x in range(-9, 9, 4):
            for y in range(-9, 9, 4):
                for z in range(-9, 9, 4):
                    point = vec(x*2E-14, y*1E-14, z*2E-14)
                    field_arrows.append(FieldArrow(point, self.field_at(point)))

    def field_at(self, position):
        electric_field = vec(0, 0, 0)
        k = 9E9 # Coulomb constant
        # superposition quality
        for charge in self._charges:
            distance = position - charge.position
            electric_field += k * charge.coulomb * distance / mag(distance)**3

        return electric_field


def main():
    # create scene
    scene = canvas(width=1000, height=600, align='left', range=3E-13)
    capacitor = Capacitor(pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13))
    moving_charge = Charge(position=vec(-4E-13, 5E-14, 0), velocity=vec(1.5E-13, 0, 0), radius=1.2E-14, C=5E-42, colour=color.green, make_trail=True)

    # simulation
    dt = 0.01  # update time interval
    for t in range(0, 600):
        rate(1/dt)
        coulomb_force = moving_charge.coulomb_force(capacitor.field_at(moving_charge.position))
        moving_charge.update(coulomb_force, dt)


main()
