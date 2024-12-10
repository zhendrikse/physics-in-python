from vpython import vec, sphere, color, mag, hat, arrow, exp, sin, cos, pi
from .field import PointChargeField

# parameter setting
ec = 1.6E-19            # electron charge
k = 9E9                 # Coulomb constant
    
class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1E-14, coulomb=ec, colour=None, make_trail=False):
        colour = colour if colour is not None else color.blue if coulomb > 0 else color.red
        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=coulomb, color=colour, make_trail=make_trail)
        self._field = PointChargeField(self)

    def show_field(self):
        self._field.show_field()        

    def field_at(self, position):
        return hat(position - self._charge.pos) * k * self._charge.coulomb / mag(position - self._charge.pos)**2

    @property
    def coulomb(self):
        return self._charge.coulomb
    
    @property
    def position(self):
        return self._charge.pos
    
    @property
    def radius(self):
        return self._charge.radius
    
    def delete(self):
        self._charge.clear_trail()
        self._charge.visible = False
        del self._charge
    
    def coulomb_force_in(self, electric_field):
        return electric_field * self._charge.coulomb

    def update(self, coulomb_force, dt):
        '''given a charge and position and update position'''
        # use formula: s = v0*t + 1/2*a*t^2
        self._charge.v += coulomb_force / self._charge.mass * dt
        self._charge.pos += self._charge.v * dt