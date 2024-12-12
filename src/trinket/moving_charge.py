#
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/8_Charge_Motion.py
#

from vpython import arrow, hat, vec, exp, mag, sphere, mag, color, box, canvas, rate

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
        

class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec, charge_color=None, make_trail=False):
        colour = charge_color 
        if colour is None:
          if coulomb > 0:
            colour = color.blue 
          else: 
            colour = color.red
          
        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=coulomb, color=colour, make_trail=make_trail)

    def field_at(self, position):
        return hat(position - self._charge.pos) * k * self._charge.coulomb / mag(position - self._charge.pos)**2
        
    def radius(self):
       return self._charge.radius
    
    def position(self):
       return self._charge.pos

    def coulomb_force_in(self, electric_field):
        return electric_field * self._charge.coulomb

    def update(self, coulomb_force, dt):
        # use formula: s = v0*t + 1/2*a*t^2
        self._charge.v += coulomb_force / self._charge.mass * dt
        self._charge.pos += self._charge.v * dt
        
class Field:
    def __init__(self, charges=[]):
        self._charges = charges
        self._field_arrows = []

    def show(self, x_range, y_range, z_range):
        self._field_arrows = []
        for x in x_range:
          for y in y_range:
            for z in z_range:
              self._field_arrows.append(self._field_arrow(x, y, z))

    def _field_arrow(self, x, y, z):
        point = vec(x, y, z) * self._charge_radius()
        return FieldArrow(position=point, field=self.field_at(point))

    def _charge_radius(self):
        return self._charges[0].radius() # Simply assuminging all charges in the field have same radius

    def field_at(self, position):
      field = vec(0, 0, 0)
      for charge in self._charges:
        field += charge.field_at(position)
      return field

class Capacitor:
    def __init__(self, pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13)):
      # fill the plates with charge
      top_plate_y_pos = vec(0, 1E-13, 0).y
      bottom_plate_y_pos = -vec(0, 1E-13, 0).y
      charges = []
      for x in range(-20, 22, 2):
          for y in [top_plate_y_pos, bottom_plate_y_pos]:
              for z in range(-20, 22, 2):
                  # positive charge and negative charge locate at top plate and down plate
                  mu = 1 if y > 0  else -1
                  charges.append(Charge(position=vec(x*1E-14, y, z*1E-14), radius=1E-14, coulomb=mu * ec))
          
      self._field = Field(charges)
      self._field.show(x_range=range(-18, 18, 8), y_range=range(-9, 9, 4), z_range=range(-18, 18, 8))
      
    def show_field(self, x_range, y_range, z_range):
        self._field.show(x_range, y_range, z_range)

    def field_at(self, position):
        return self._field.field_at(position)
        
              
scene = canvas(width=1000, height=600, align='left', range=3E-13)
capacitor = Capacitor(pos=vec(0, 1E-13, 0), size=vec(4E-13, 4E-16, 4E-13))
#capacitor.show_field(x_range=range(-18, 18, 8), y_range=range(-9, 9, 4), z_range=range(-18, 18, 8))
moving_charge = Charge(position=vec(-4E-13, 5E-14, 0), velocity=vec(1.5E-13, 0, 0), radius=1.2E-14, coulomb=5E-42*ec, charge_color=color.green, make_trail=True)

dt = 0.01
for t in range(0, 600):
    rate(1/dt)
    field = capacitor.field_at(moving_charge.position())
    coulomb_force = moving_charge.coulomb_force_in(field)
    moving_charge.update(coulomb_force, dt)