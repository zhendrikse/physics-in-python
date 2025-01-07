#Web VPython 3.2

from vpython import canvas, box, vector, sphere, sin, cos, rate, pi, button, slider, wtext, cross, color

title = """Helical motion of charged particle in magnetic field

&#x2022; Based on <a href="https://towardsdatascience.com/simple-physics-animations-using-vpython-1fce0284606">Simple Physics Animations Using VPython</a> by Zhiheng Jiang
&#x2022; Refactored and maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

animation = canvas(width=800, height=600, title=title)

xlen, ylen, zlen = 100, 100, 100
boundaries = [
    box(pos=vector(0, -ylen / 2, 0), size=vector(xlen, .2, zlen)),
    box(pos=vector(0, ylen / 2, 0), size=vector(xlen, .2, zlen)),
    box(pos=vector(-xlen / 2, 0, 0), size=vector(.2, ylen, zlen)),
    box(pos=vector(xlen / 2, 0, 0), size=vector(.2, ylen, zlen)),
    box(pos=vector(0, 0, -zlen / 2), size=vector(xlen, ylen, .2))
]

dt = .001  # time step
Bfield = 5  # strength of magnetic field
v_mag = 20  # magnitude of velocity of proton
proton_charge = 0.5  # charge of proton in arbitrary units
theta = pi / 4  # angle of launch of proton
#v = vector(v_mag * cos(theta), v_mag * sin(theta), 0)  # velocity vector
magnetic_field = vector(0, -Bfield, 0)  # vector of magnetic field
starting_point = vector(0, -ylen / 2 + 1, 0)  # starting position vector of proton


class Proton:
    def __init__(self, position=vector(0, -ylen / 2 + 1, 0), velocity=v_mag * vector(cos(theta), sin(theta), 0)):  # v is a vector representing velocity
        self.velocity = velocity
        self._initial_velocity = velocity
        self._initial_position = position
        self.proton = sphere(pos=starting_point, color=color.red, radius=1, make_trail=True, trail_type="curve")
        self.acceleration = vector(0, 0, 0)

    def move(self):  # moves proton by small step
        self.acceleration = proton_charge * cross(self.velocity, magnetic_field)  # F = ma = q v x B
        self.velocity += self.acceleration * dt  # a = dv/dt
        self.proton.pos += self.velocity * dt  # v = dx/dt

    def reset_proton(self):  # resets proton position and path
        self.proton.pos = self._initial_position
        self.velocity = self._initial_velocity
        self.proton.clear_trail()
        self.acceleration = vector(0, 0, 0)

    def check_collision(self):  # checks for boundaries
        return ylen / 2 > self.proton.pos.y > -ylen / 2 and xlen / 2 > self.proton.pos.x > -xlen / 2 and -zlen / 2 < self.proton.pos.z < zlen / 2


proton = Proton()
def launch():
    proton.reset_proton()
    while proton.check_collision():
        rate(1 / dt)
        proton.move()


button(text="Launch!", bind=launch)  # link the button and function
animation.append_to_caption("\n\n")  # newlines for aesthetics

def adjust_bfield():
    global Bfield, magnetic_field  # to update global value
    Bfield = BfieldSlider.value
    magnetic_field = vector(0, -Bfield, 0)  # B directed downwards
    BfieldSliderReadout.text = BfieldSlider.value + " Tesla"


BfieldSlider = slider(min=1, max=10, step=.5, value=5, bind=adjust_bfield)
animation.append_to_caption(" B-field Strength = ")
BfieldSliderReadout = wtext(text="5 Tesla")
animation.append_to_caption("\n\n")

def adjust_q():
    global proton_charge
    proton_charge = QSlider.value
    QSliderReadout.text = QSlider.value + " Coulumbs"

QSlider = slider(min=0, max=1, step=.1, value=.5, bind=adjust_q)
animation.append_to_caption(" Q = ")
QSliderReadout = wtext(text="0.5 Coulumbs")
animation.append_to_caption("\n\n")

def adjust_angle():
    global theta
    theta = angleSlider.value * pi / 180  # degree - radian conversion
    angleSliderReadout.text = str(angleSlider.value) + " degrees"
    proton.velocity = v_mag * vector(cos(theta), sin(theta), 0)

angleSlider = slider(min=0, max=90, step=1, value=45, bind=adjust_angle)
animation.append_to_caption(" Angle = ")
angleSliderReadout = wtext(text="45 degrees")

while True:
    rate(10)