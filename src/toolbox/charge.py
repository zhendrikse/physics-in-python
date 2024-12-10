from vpython import vec, sphere, color, mag, hat, arrow, exp, sin, cos, pi

# parameter setting
ec = 1.6E-19            # electron charge
k = 9E9                 # Coulomb constant

class FieldArrow:
    def __init__(self, position, E, point_charge=False):
        # create electric field using arrow
        color = FieldArrow.mapping(E)
        arrow_length = 3E-14    # length of arrow
        colour = vec(color, 0, 1) if point_charge else vec(1, color, 0)
        arrow(pos=position, axis=hat(E) * arrow_length, color=colour)

    # mapping from (Inf, 0) to (1, 0)
    @staticmethod
    def mapping(E):
        a = 1E-17
        return 1 - exp(-a * mag(E))
    
class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec, colour=None, make_trail=False):
        colour = colour if colour is not None else color.blue if coulomb > 0 else color.red
        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=coulomb, color=colour, make_trail=make_trail)
        self._field = []              # store electric field arrow

    def show_field(self):
        # generate electric field
        for r in range(1, 30, 5):
            for theta in range(0, 6):
                for phi in range(0, 6):
                    xyz = Charge.to_carthesian_coordinates(self._charge.radius * r, theta * pi/3, phi * pi/3)
                    E = k * self._charge.coulomb * (xyz - self._charge.pos) / mag(xyz - self._charge.pos)**3
                    self._field.append(FieldArrow(xyz, E, True))

    @staticmethod
    def to_carthesian_coordinates(r, theta, phi):
        x = r * sin(theta) * cos(phi)
        y = r * sin(theta) * sin(phi)
        z = r * cos(theta)
        return vec(x, y, z)

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