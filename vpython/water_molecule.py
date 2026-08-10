from vpython import sin, cos, canvas, sphere, rotate, vector, vec, rate, color, pi, helix, acos, dot, mag, norm, arrow, button

title="""&#x2022; Original <a href="https://www.mso.anu.edu.au/pfrancis/simulations/h2o.py">h2o.py</a> by <a href="http://www.mso.anu.edu.au/pfrancis/simulations/">Paul Francis</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/molecularphysics/code/water.py">water.py</a>

"""

spacing = 1.0E-10
k = 5.0E-6  # Tension compression constant
kt = 5.0E-6  # Torsion constant
u = 1.660E-27
ion_charge = 1.0 * 1.602E-19
rad = 3.0E-11
scale = 1.25 * spacing

display = canvas(range=scale * 1.25, width=600, height=400, background=color.gray(0.075), center=vector(scale * .3, 0, 0), title=title)


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
        Atom.__init__(self, position=position, mass=16.0 * u, colour=color.red, radius=1.2 * rad, charge=-2 * ion_charge)


class Hydrogen(Atom):
    def __init__(self, position=vector(0, 0, 0)):
        Atom.__init__(self, position=position, mass=1.0 * u, colour=color.blue, radius=0.4 * rad, charge=-ion_charge)


class WaterDioxide:
    def __init__(self, bond_angle=105. * pi / 180.0):
        self._bond_angle = bond_angle

        oxy_pos, h1_pos, h2_pos = self._get_positions()
        self._oxy1 = Oxygen(position=oxy_pos)
        self._hy1 = Hydrogen(position=h1_pos)
        self._hy2 = Hydrogen(position=h2_pos)

        self._spring1 = helix(pos=self._oxy1.pos(), axis=self._hy1.pos() - self._oxy1.pos(), radius=0.3 * rad,
                        thickness=0.1 * rad, color=color.yellow, coils=10)

        self._spring2 = helix(pos=self._oxy1.pos(), axis=self._hy2.pos() - self._oxy1.pos(), radius=0.3 * rad,
                        thickness=0.1 * rad, color=color.yellow, coils=10)

    def update(self, E, dt):
        v1 = self._hy1.pos() - self._oxy1.pos()
        v2 = self._hy2.pos() - self._oxy1.pos()
        angle = acos(dot(v1, v2) / (v1.mag * v2.mag))

        # hy1 forces
        coulomb_force = self._hy1.coulomb(E)
        stretch_force = -1.0 * k * (mag(v1) - spacing) * norm(v1)
        torque_force = kt * spacing * (angle - self._bond_angle) * norm(v1 + v2)
        self._hy1.update(coulomb_force + stretch_force + torque_force, dt)

        # hy2 forces
        coulomb_force = self._hy2.coulomb(E)
        stretch_force = -1.0 * k * (mag(v2) - spacing) * norm(v2)
        torque_force = kt * spacing * (angle - self._bond_angle) * norm(v1 + v2)
        self._hy2.update(coulomb_force + stretch_force + torque_force, dt)

        # Oxy1 forces
        coulomb_force = self._oxy1.coulomb(E)
        stretch_force = k * (mag(v1) - spacing) * norm(v1) + k * (mag(v2) - spacing) * norm(v2)
        torque_force = -2.0 * kt * spacing * (angle - self._bond_angle) * norm(v1 + v2)
        self._oxy1.update(coulomb_force + stretch_force + torque_force, dt)

        # Update springs
        self._spring1.pos = self._oxy1.pos()
        self._spring1.axis = v1

        self._spring2.pos = self._oxy1.pos()
        self._spring2.axis = v2

    def _get_positions(self, theta=0.0 * pi / 180.0, tilt=20.0 * pi / 180.0):
        oxy_pos = vector(0., 0.0 * spacing, 0.)
        h1_pos = rotate(spacing * vector(cos(theta), sin(theta), 0.), angle=tilt, axis=vec(1, 0, 0))
        angle = self._bond_angle + theta
        h2_pos = rotate(spacing * vector(cos(angle), sin(angle), 0.), angle=tilt, axis=vec(1, 0, 0))
        return oxy_pos, h1_pos, h2_pos

    def reset(self):
        oxy_pos, h1_pos, h2_pos = self._get_positions()
        self._oxy1.reset(position=oxy_pos)
        self._hy1.reset(position=h1_pos)
        self._hy2.reset(position=h2_pos)
        self._spring1.pos = self._oxy1.pos()
        self._spring1.axis = self._hy1.pos() - self._oxy1.pos()
        self._spring2.pos = self._oxy1.pos()
        self._spring2.axis = self._hy2.pos() - self._oxy1.pos()

    def pos(self):
        return self._oxy1.pos()


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

    def reset(self):
        self._evector.axis = vector(0, 0, 0)
        self._field = vector(0., 0., 0.)

field = ElectricField(position=vec(1.7 * spacing, 0., 0.), magnitude=120.0, frequency=0.25)
hydrogen_dioxide = WaterDioxide()

def reset():
    global time
    time = 0.
    hydrogen_dioxide.reset()
    field.reset()

_ = button(text="Reset", bind=reset)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

timestep = 5.0E-13
time = 0
while 1:
    rate(600)
    field.update(time)
    time += timestep
    hydrogen_dioxide.update(field, timestep)

