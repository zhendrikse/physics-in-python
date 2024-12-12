from vpython import arrow, vec, hat, sphere, color, sin, cos, pi, canvas, exp, mag
from mathjax import MathJax

ec = 1.6E-19            # electron charge
k = 9E9                 # Coulomb constant

class FieldArrow:
    def __init__(self, position, field):
        color = self.mapping(field)
        arrow_length = 3E-14 
        arrow(pos=position, axis=hat(field) * arrow_length, color=vec(color, 0, 1))

    def mapping(self, field):
        a = 1E-17
        return 1 - exp(-a * mag(field))
        
class Charge:
    def __init__(self, mass=1.6E-27, position=vec(0, 0, 0), velocity=vec(0, 0, 0), radius=1.0, coulomb=ec, color=color.red, make_trail=False):
        colour = color 
        if colour is None:
          if coulomb > 0:
            colour = color.blue 
          else: 
            colour = color.red
          
        self._charge = sphere(mass=mass, pos=position, v=velocity, radius=radius, coulomb=coulomb, color=color, make_trail=make_trail)
        self._field_arrows = []
        
    def show_field(self):
        for r in range(1, 30, 5):
            for theta in range(0, 6):
                for phi in range(0, 6):
                    xyz = self.to_carthesian_coordinates(self._charge.radius * r, theta * pi/3, phi * pi/3)
                    self._field_arrows.append(FieldArrow(position=xyz, field=self.field_at(xyz)))
                    
    def to_carthesian_coordinates(self, r, theta, phi):
        x = r * sin(theta) * cos(phi)
        y = r * sin(theta) * sin(phi)
        z = r * cos(theta)
        return vec(x, y, z)
        
    def arrow(self, r, theta, phi):
      xyz = self.to_carthesian_coordinates(self._charge.radius * r, theta * pi/3, phi * pi/3)
      return FieldArrow(position=xyz, field=self.field_at(xyz))

    def field_at(self, position):
        return hat(position - self._charge.pos) * k * self._charge.coulomb / mag(position - self._charge.pos)**2
        
scene = canvas(width=1000, height=600, align='top', range=3E-13)
scene.caption = "Electric field \\( \\vec{E} ( \\vec{r} ) = \\dfrac {1} {4\\pi\\epsilon_0} \\dfrac {Q} {r^2} \\hat{r} \\), Electric force \\( \\vec{F}(\\vec{r}) = q \\vec{E} ( \\vec{r} ) =  \\dfrac {1} {4\\pi\\epsilon_0} \\dfrac {qQ} {r^2} \\hat{r} \\)"
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

charge = Charge(position=vec(0, 0, 0), radius=1.2E-14, coulomb=1 * ec)
charge.show_field()
