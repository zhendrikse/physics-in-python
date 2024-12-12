##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/7_Dipole.py
#

from vpython import canvas, vec, hat, arrow, vector, sphere, color, exp, mag

ec = 1.6E-19            # electron charge
k = 9E9                 # Coulomb constant

class FieldArrow:
    def __init__(self, position, field):
        color = self.mapping(field)
        arrow_length = 3E-14 
        arrow(pos=position, axis=hat(field) * arrow_length, color=vec(1, color, 0))

    def mapping(self, field):
        a = 1E-17
        return 1 - exp(-a * mag(field))

class Field:
    def __init__(self, charges=[]):
        self._charges = charges
        self._field_arrows = []

    def show(self, x_range, y_range, z_range):
        self._field_arrows = []
        for x in x_range:
          for y in y_range:
            for z in z_range:
              self._field_arrows += [self._field_arrow(x, y, z)]

    def _field_arrow(self, x, y, z):
        point = vec(x, y, z) * self._charge_radius()
        return FieldArrow(position=point, field=self.field_at(point))

    def _charge_radius(self):
        return self._charges[0].radius() # Simply assuminging all charges in the field have same radius

    def field_at(self, position):
      field = vector(0, 0, 0)
      for charge in self._charges:
        field += charge.field_at(position)
      return field

class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec, colour=color.red, make_trail=False):

        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=coulomb, color=colour, make_trail=make_trail)
        self._field_arrows = []

    def field_at(self, position):
        return hat(position - self._charge.pos) * k * self._charge.coulomb / mag(position - self._charge.pos)**2
        
    def radius(self):
       return self._charge.radius

        
class Dipole:
    def __init__(self, radius=1.2E-14):
         position = vec(10 * radius, 0, 0)
         self._charges = []
         self._charges += [Charge(position=position, radius=radius, coulomb=ec, colour=color.blue)]
         self._charges += [Charge(position=-position, radius=radius, coulomb=-ec)]

    def field(self):
        return Field(charges=self._charges)

scene = canvas(width=1000, height=600, align='top', range=3E-13)

dipole = Dipole()
dipole.field().show(x_range=range(-22, 22, 5), y_range=range(-22, 22, 5), z_range=range(-12, 12, 5))

