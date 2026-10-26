#Web VPython 3.2
from vpython import canvas, helix, sphere, color, mag, norm, cos, sin, pi, rate, arrow, acos, dot, vector, radio, button

title="""&#x2022; Original <a href="https://www.mso.anu.edu.au/pfrancis/simulations/co2.py">co2.py</a> by <a href="http://www.mso.anu.edu.au/pfrancis/simulations/">Paul Francis</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/molecularphysics/code/carbon_dioxide.py">carbon_dioxide.py</a>

"""

spacing = 1.0E-10
k = 8.0E-4  # Tension compression constant
kt = 3.0E-5  # Torsion constant
u = 1.660E-27
ion_charge = 1.0 * 1.602E-19
rad = 3.0E-11

scale = 2.0 * spacing
display = canvas(range=scale * .65, width=600, height=400, background=color.gray(0.075), center=vector(scale * .2, 0, 0), title=title)

class Atom:
    def __init__(self, position, mass, colour, radius, charge, momentum=vector(0., 0., 0.)):
        self._atom = sphere(pos=position, color=colour, radius=radius)
        self._mass = mass
        self._charge = charge
        self._momentum = momentum

    def pos(self):
        return self._atom.pos

    def coulomb(self, electric_field):
        return self._charge * electric_field.field()

    def update(self, force, dt):
        self._momentum += dt * force
        self._atom.pos += dt * self._momentum / self._mass

    def reset(self, position):
        self._atom.pos = position
        self._momentum = vector(0., 0., 0.)


class Oxygen(Atom):
    def __init__(self, position):
        Atom.__init__(self, position=position, mass=16.0 * u, colour=color.green, radius=rad, charge=ion_charge)


class Carbon(Atom):
    def __init__(self, position=vector(0, 0, 0)):
        Atom.__init__(self, position=position, mass=12 * u, colour=color.red, radius=0.8 * rad, charge=-2.0 * ion_charge)


class CarbonDioxide:
    def __init__(self):
        self._theta = 30. * pi / 180.0
        self._oxy1 = Oxygen(position=vector(spacing * cos(self._theta), spacing * sin(self._theta), 0.))
        self._oxy2 = Oxygen(position=-1.0 * self._oxy1.pos())
        self._carb1 = Carbon(position=vector(0., 0.0 * spacing, 0.))

        self._spring1 = helix(pos=self._carb1.pos(), axis=self._oxy1.pos() - self._carb1.pos(), radius=0.3 * rad,
                        thickness=0.1 * rad, color=color.yellow, coils=10)

        self._spring2 = helix(pos=self._carb1.pos(), axis=self._oxy2.pos() - self._carb1.pos(), radius=0.3 * rad,
                        thickness=0.1 * rad, color=color.yellow, coils=10)

    def reset(self):
        self._oxy1.reset(position=vector(spacing * cos(self._theta), spacing * sin(self._theta), 0.))
        self._oxy2.reset(position=-1 * vector(spacing * cos(self._theta), spacing * sin(self._theta), 0.))
        self._carb1.reset(position=vector(0., 0.0 * spacing, 0.))
        self._spring1.pos = self._carb1.pos()
        self._spring1.axis = self._oxy1.pos() - self._carb1.pos()
        self._spring2.pos = self._carb1.pos()
        self._spring2.axis = self._oxy2.pos() - self._carb1.pos()

    def update(self, electric_field, dt):
        v1 = self._oxy1.pos() - self._carb1.pos()
        v2 = self._oxy2.pos() - self._carb1.pos()

        angle = acos(dot(v1, -1.0 * v2) / (v1.mag * v2.mag))

        # Oxy1 forces
        coulomb_force = self._oxy1.coulomb(electric_field)
        stretch_force = -1.0 * k * (mag(v1) - spacing) * norm(v1)
        torque_force = -1.0 * kt * spacing * angle * norm(v1 + v2)
        self._oxy1.update(coulomb_force + stretch_force + torque_force, dt)

        # Oxy2 forces
        coulomb_force = self._oxy2.coulomb(electric_field)
        stretch_force = -1.0 * k * (mag(v2) - spacing) * norm(v2)
        torque_force = -1.0 * kt * spacing * angle * norm(v1 + v2)
        self._oxy2.update(coulomb_force + stretch_force + torque_force, dt)

        # Carb1 forces
        coulomb_force = self._carb1.coulomb(electric_field)
        stretch_force = k * (mag(v1) - spacing) * norm(v1) + k * (mag(v2) - spacing) * norm(v2)
        torque_force = 2.0 * kt * spacing * angle * norm(v1 + v2)
        self._carb1.update(coulomb_force + stretch_force + torque_force, dt)

        # Update springs
        self._spring1.pos = self._carb1.pos()
        self._spring1.axis = v1

        self._spring2.pos = self._carb1.pos()
        self._spring2.axis = v2

    def pos(self):
        return self._carb1.pos()

class ElectricField:
    def __init__(self, position, magnitude=0.0, frequency=8.0):
        self._magnitude = magnitude
        self._frequency = frequency
        self._evector = arrow(pos=position, axis=vector(0, 0, 0), shaftwidth=0.1 * spacing, color=color.magenta)
        self._field = vector(0., 0., 0.)

    def update(self, time):
        frequency = self._frequency * 2.0 * pi * 1.00001E10
        self._evector.axis = 0.5 * spacing * cos(time * frequency) * vector(0., 1., 0.)
        self._field = self._magnitude * cos(time * frequency) * vector(0., 1., 0.)

    def field(self):
        return self._field

    def set_frequency_to(self, frequency):
        self._frequency = frequency


carbon_dioxide = CarbonDioxide()
field = ElectricField(position=vector(1.7 * spacing, 0., 0.), magnitude=200, frequency=8.0)

def toggle_frequency(event):
    if event.name == "8": # Nothing happens
        field.set_frequency_to(8.0)
        radio_2.checked = radio_3.checked = radio_4.checked = False
    if event.name == "5.291": # Linear vibrations
        field.set_frequency_to(5.291)
        radio_1.checked = radio_3.checked = radio_4.checked = False
    if event.name == "1.5": # Bending
        field.set_frequency_to(1.5)
        radio_1.checked = radio_2.checked = radio_4.checked = False
    if event.name == "2.76": # non-active sym
        field.set_frequency_to(2.76)
        radio_1.checked = radio_2.checked = radio_3.checked = False


display.append_to_caption("Frequency: ")
radio_1 = radio(text="8  ", name="8", bind=toggle_frequency, checked=True)
radio_2 = radio(text="5.291  ", name="5.291", bind=toggle_frequency)
radio_3 = radio(text="1.5  ", name="1.5", bind=toggle_frequency)
radio_4 = radio(text="2.76  ", name="2.76", bind=toggle_frequency)
_ = button(text="Reset", bind=carbon_dioxide.reset)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

time = 0
timestep = 1.0E-13
while 1:
    rate(500)
    time += timestep
    field.update(time)
    carbon_dioxide.update(field, timestep)
