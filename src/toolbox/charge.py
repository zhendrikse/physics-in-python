from vpython import vec, sphere, color

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