from vpython import *
from random import randint

# Excitation of atoms by electron beam
# Bruce Sherwood, March 2003

title=""""
https://lectdemo.github.io/virtual/06_absorb_emit.html

Click to randomly excite an atom or emit a photon.
Build up spectrum of emitted photons.
When all lines in spectrum have been displayed,
  electron beam is turned off, and eventually
  all atoms end up in ground state again.
"""

Nlevels = 5  # number of discrete energy levels
Eexcite = 3  # electron beam energy (Nlevels-1 corresponds to top level)
# If Eexcite < Nlevels-1, upper levels are not excited
Eset = [0, 2.8, 4, 4.7, 5]  # energy levels measured up from ground state
Natoms = 30  # number of atoms

scene.width = scene.height = 600
scene.background = color.white
scene.foreground = color.black
Nlines = Eexcite * (Eexcite + 1) / 2  # number of possible photon emission lines
greyintensity = 0.8
grey = (greyintensity, greyintensity, greyintensity)
Escale = 1  # sets scale of display
L = Nlevels * Escale
Rlevel = Escale / 30  # radius of horizontal line representing an energy level
Ratom = Escale / 10  # radius of atom
levels = []  # list of energy level lines
for N in range(Nlevels):
    levels.append(cylinder(pos=vector(-L / 2, Eset[N] * Escale, 0), axis=vector(L, 0, 0), radius=Rlevel, color=color.gray(0.4)))
atoms = []  # list of atoms
photons = []  # list of already-emitted photons that have been displayed in spectrum
sx1 = -L / 2  # spectrum displayed in rectangle bounded by (sx1,sy1) and (sx2,sy2)
sx2 = -sx1
sy1 = levels[0].pos.y - 1.5 * Escale
sy2 = sy1 + Escale
emitarr = arrow(visible=0, shaftwidth=2 * Ratom)  # display energy emitted as photon
absorbarr = arrow(visible=0, shaftwidth=2 * Ratom, color=color.gray(0.4))  # display energy absorbed from electron beam
beam = label(pos=vector(0, 0.5 * (levels[0].pos.y + sy2), 0), box=0,
             text='Electron beam is turned on', opacity=0)
beam.on = 1

def hsv_to_rgb(hue, saturation, value):
    if saturation:
        if hue == 1.0: hue = 0.0
        i = int(hue * 6.0)
        f = hue * 6.0 - i

        w = value * (1.0 - saturation)
        q = value * (1.0 - saturation * f)
        t = value * (1.0 - saturation * (1.0 - f))

        if i == 0: return value, t, w
        if i == 1: return q, value, w
        if i == 2: return w, value, t
        if i == 3: return w, q, value
        if i == 4: return t, w, value
        if i == 5: return value, w, q
    else:
        return value, value, value

def Ecolor(Ephoton):  # convert photon energy to color (hue)
    Erange = levels[-1].pos.y - levels[0].pos.y
    hue = (5 / 6) * Ephoton / Erange
    rbg_values = hsv_to_rgb(hue, 1, 1)
    return vector(rbg_values[0], rbg_values[1], rbg_values[2])


class atom(object):  # atom has energy level, can absorb energy from electron beam or emit photon
    def __init__(self, x, energy):
        self.ball = sphere(pos=vector(x, 0, 0), radius=Ratom, color=color.yellow)
        self.E = energy

    def getE(self):
        return self.__E

    def setE(self, energy):
        self.__E = energy
        self.ball.y = levels[energy].pos.y

    E = property(getE, setE)

    def emit(self, Efinal):
        Einitial = self.E
        Ephoton = levels[Einitial].pos.y - levels[Efinal].pos.y
        emitarr.pos = self.ball.pos
        self.E = Efinal
        emitarr.axis = self.ball.pos - emitarr.pos
        emitarr.color = Ecolor(Ephoton)
        emitarr.visible = 1
        for photon in photons:
            if Ephoton == photon.E: return
        Erange = levels[-1].pos.y - levels[0].pos.y
        x1 = sx1 + (sx2 - sx1) * Ephoton / Erange
        photons.append(box(pos=vector(x1, (sy1 + sy2) / 2, 0), size=vector(Ratom, sy2 - sy1, 0), color=Ecolor(Ephoton), E=Ephoton))

    def absorb(self, Efinal):
        absorbarr.pos = self.ball.pos
        self.E = Efinal
        absorbarr.axis = self.ball.pos - absorbarr.pos
        absorbarr.visible = 1


def wait():
    scene.waitfor("click")  # comment out this line to run fast
    rate(5) # comment in this line to run fast
    pass


scene.center = vector(0, (sy1 + levels[-1].pos.y) / 2, 0)
for N in range(Natoms):  # put all atoms in ground state initially
    atoms.append(atom(-L / 2 + (N + 1) * L / (Natoms + 1), 0))
wait()
while 1:
    Na = randint(0, Natoms - 1)  # randomly choose one of the atoms
    aa = atoms[Na]
    # If in ground state, and not all emission lines have been displayed yet,
    #   absorb energy from electron beam:
    if aa.E == 0 and len(photons) < Nlines:
        aa.absorb(randint(1, Eexcite))
        wait()  # show arrow indicating absorption of energy
        absorbarr.visible = 0
    Na = randint(0, Natoms - 1)  # randomly choose one of the atoms
    aa = atoms[Na]
    # If in excited state, emit a photon:
    if aa.E > 0:
        Efinal = randint(0, aa.E - 1)  # randomly choose a lower energy level
        aa.emit(Efinal)
        wait()  # show arrow indicating photon emission
        emitarr.visible = 0
    if len(photons) == Nlines and beam.on:
        beam.on = 0
        beam.text = 'Electron beam has been turned OFF'
        wait()

