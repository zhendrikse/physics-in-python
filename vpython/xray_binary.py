from vpython import vector, canvas, sphere, local_light, cylinder, rate, sin, cos

title="""&#x2022; Original <a href="https://www.mso.anu.edu.au/pfrancis/simulations/XRB.py">XRB.py</a> by <a href="http://www.mso.anu.edu.au/pfrancis/simulations/">Paul Francis</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/astrophysics/code/xray_binary.py">xray_binary.py</a>

"""

display = canvas(title=title, range=.5, width=650, height=400, forward=vector(0.2, 0.6, -1.0))
stars = sphere(pos=vector(0, 0, 0), texture="https://www.hendrikse.name/science/astrophysics/images/textures/universe.jpg", radius=3, shininess=0, opacity=0.5)

display.lights = []
display.ambient = 0.3 * vector(0.7, 0.5, 0.2)

class WhiteDwarf:
    def __init__(self, distance, position, colour=vector(0.8, 0.4, 1.0)):
        self._distance = distance
        self._light1 = local_light(pos=distance * position + vector(0.0, 0.01, 0.0), color=colour)
        self._light2 = local_light(pos=distance * position - vector(0.0, 0.01, 0.0), color=colour)
        self._sphere = sphere(pos=distance * position, radius=0.002, color=colour, emissive=True)

    def position(self):
        return self._sphere.pos

    def move(self, theta):
        wdpos = self._distance * vector(cos(theta), 0.0, sin(theta))
        self._sphere.pos = wdpos
        self._light1.pos = wdpos + vector(0.0, 0.01, 0.0)
        self._light2.pos = wdpos - vector(0.0, 0.01, 0.0)

class AccretionDisk:
    def __init__(self, distance, position):
        self._disk = cylinder(pos=distance * position, radius=0.08, axis=vector(0.0, 0.002, 0.0),
                        opacity=0.8, color=vector(0.7, 0.9, 1.0))

    def radius(self):
        return self._disk.radius

    def color(self):
        return self._disk.color

    def move(self, param):
        self._disk.pos = param


class Star:
    def __init__(self, distance, position):
        self._distance = distance
        self._star = sphere(pos=distance * position, radius=0.185, color=0.5 * vector(0.9, 0.5, 0.2))

    def move(self, theta):
        self._star.pos = self._distance * vector(cos(theta), 0.0, sin(theta))


class RocheBulge:
    def __init__(self, distance, position, radius):
        self._distance = distance
        self._bulge = sphere(pos=distance * position, radius=radius, color=0.5 * vector(0.9, 0.5, 0.2))

    def radius(self):
        return self._bulge.radius

    def move(self, theta):
        self._bulge.pos = self._distance * vector(cos(theta), 0.0, sin(theta))

class Stream:
    def __init__(self, colour, radius=0.002):
        self._stream = cylinder(color=colour, radius=radius)
        self._set_position_and_axis()

    def _set_position_and_axis(self, theta=0):
        spotangle = 0.15
        dstart = 0.05 - roche_bulge_2.radius() + 0.01
        streamstart = vector(-dstart * cos(theta), 0.0, -dstart * sin(theta))
        streamend = white_dwarf.position() - vector(accretion_disk.radius() * cos(theta - spotangle), 0.0,
                                                    accretion_disk.radius() * sin(theta - spotangle))
        self._stream.pos = streamstart
        self._stream.axis = streamend - streamstart

    def move(self, theta):
        self._set_position_and_axis(theta)


white_dwarf = WhiteDwarf(0.12, vector(cos(0), 0.0, sin(0)))
accretion_disk = AccretionDisk(0.12, vector(cos(0), 0.0, sin(0)))
main_star = Star(-0.2, vector(cos(0), 0.0, sin(0)))
roche_bulge_1 = RocheBulge(-0.09, vector(cos(0), 0.0, sin(0)), 0.085)
roche_bulge_2 = RocheBulge(-0.05, vector(cos(0), 0.0, sin(0)), 0.049)
stream_ = Stream(accretion_disk.color())

d_theta = -0.003
angle = 0.0
while 1:
    rate(100)
    angle += d_theta
    white_dwarf.move(angle)
    accretion_disk.move(white_dwarf.position())
    main_star.move(angle)
    roche_bulge_1.move(angle)
    roche_bulge_2.move(angle)
    stream_.move(angle)
