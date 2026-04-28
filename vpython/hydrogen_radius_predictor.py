#Web VPython 3.2
from vpython import *
import random

# https://github.com/Alexander-Alford/Atom-Physics-Simulator/blob/main/main.py
# The purpose of this program is to demonstrate through user interaction that it is impossible for classical physics
# to account for the tested hydrogen atom radius by treating the problem as a 2-body problem. Regardless of how much
# the user tries, they will never be able to create an orbit that gives a radial graph similar to the tested
# graph it is compared against. This intuitively demonstrates the need for a more distinct treatment of the
# issue of quantum mechanics compared to that of classical mechanics.

# mathematical constants
h = 6.62607015e-34  # J/Hz
hbar = 1.054571817e-34  # J*s
elec_mass = 9.1093837015e-31  # kg
prot_mass = 1.6726219e-27  # kg
elem_charge = 1.602176634e-19  # C
coulombconst = 8.9875517923e9  # kg*m^3*s^2/C^2
a_0 = 5.29177210903e-11  # Bohr radius in m
v_light = 2.99792458e8  # m/s
pi = 3.14159265358979323846

# approximation constants
delta_t = 1e-19  # s
min_dist = 1e-15  # m
time = 0.0

graph_radBin = a_0 / 10
numRadHisto = 50
total_r_samples = 1000
counter = 0


class Particle:

    def __init__(self, velocity, mass, charge, position, color, radius):
        self.velocity = vector(velocity[0], velocity[1], velocity[2])
        self.position = vector(position[0], position[1], position[2])
        self.mass = mass
        self.charge = charge
        self.sphere = sphere(pos=self.position, radius=radius, color=color, make_trail=True, trail_type="points",
                             retain=200, interval=10)

    def updatePos(self):
        self.position += (self.velocity * delta_t)
        self.sphere.pos = self.position


particlelist = []

# flags and button functions
run_flag = True
electro_flag = True
magnet_flag = False


# selfinteractflag = False

def electroCheck(self):
    global electro_flag

    if electro_flag == True:
        electro_flag = False
    else:
        electro_flag = True


'''
def selfInteractCheck(self):
    global selfinteractflag

    if selfinteractflag == True:
        selfinteractflag = False
    else:
        selfinteractflag = True
'''


# Utility
def randSign():
    test = random.random()

    if (test < .50):
        return 1
    else:
        return -1


def genRandNormOrthVec(ref):
    retvec = [0, 0, 0]
    vecref = [ref.x, ref.y, ref.z]

    numofzeros = 0

    # print(ref)

    for i in range(3):
        if vecref[i] == 0:
            numofzeros += 1

    if numofzeros == 0:
        retvec[0] = random.random() * randSign()
        retvec[1] = random.random() * randSign()
        retvec[2] = (-retvec[0] * vecref[0] - retvec[1] * vecref[1]) / vecref[2]
    elif numofzeros == 1:
        retvec[0] = random.random() * randSign()

        if vecref[1] == 0:
            retvec[1] = random.random() * randSign()
            retvec[2] = (-retvec[1] * vecref[1]) / vecref[2]
        else:
            retvec[2] = random.random() * randSign()
            retvec[1] = (-retvec[2] * vecref[2]) / vecref[1]
    elif numofzeros == 2:
        for i in range(3):
            if vecref[i] == 0:
                retvec[i] = random.random() * randSign()
            else:
                retvec[i] = 0

    return norm(vec(retvec[0], retvec[1], retvec[2]))


# calulators
def getDistance(pos_1, pos_2):
    return mag(pos_1 - pos_2)


def getElectroForce(q1, q2, rad):
    return q1 * q2 * coulombconst / (rad ** 2)


'''
def getSelfForce(vel):
    # magnitude of velocity has to remain the same
    # calclulate inverse force that acts directly opposite of the velocity vector
    # cant go light speed
    # get randomized scalar vector that applies for perpendicular to velocity vector

    gamma = 1/sqrt( 1 - mag2(vel)/(v_light ** 2) ) #relativity factor from 1 to infinity

    velinv = -1*vel*(1 - 1/gamma) # reduction in forward velocity

    orthmag = sqrt( mag2(vel) - mag2( (vel + velinv) ) ) #magnitude of increase in orthogonal velocity 

    #print("orthmag = " + str(orthmag) + ", vel " + str(mag(vel)) + ", gamma " + str(gamma) + ", inv " + str(mag(velinv)))

    ret_vel = vel + velinv + genRandNormOrthVec(vel)*orthmag

    return ret_vel
'''


def addForce(force, p1, p2):
    p1.velocity += (norm(p1.position - p2.position) * force * delta_t) / p1.mass
    p2.velocity += (norm(p2.position - p1.position) * force * delta_t) / p2.mass


def applyForce(plist):
    global electro_flag
    global selfinteractflag

    for p1 in range(len(plist)):
        for p2 in range(p1 + 1, len(plist)):
            if p2 <= len(plist):
                if (electro_flag == True):
                    addForce(getElectroForce(plist[p1].charge, plist[p2].charge,
                                             getDistance(plist[p1].position, plist[p2].position)), plist[p1], plist[p2])
                # if(selfinteractflag == True):
                # plist[p1].velocity = getSelfForce(plist[p1].velocity)


# def setMinElecRad(n, k):
#    if n == k:


# def setMaxElecVel(k, rad):
#    return ((k*hbar)/(rad*elec_mass))


# def setPrincQuantNum(num):
#    if num == 1:


primescene = canvas(title="<b>Atomic Physics Simulator</b>", width=500, height=500, center=vector(0, 0, 0),
                    align="none")
primescene.userspin = False
primescene.resizable = False


# primescene.userpan = False

# Button code.
# def setPositions(n, k):


def resetBut():
    global coulombconst
    coulombconst = 8.9875517923e9
    primescene.autoscale = False
    particlelist[0].position = vector(0, 0, 0)
    particlelist[0].velocity = vector(0, 0, 0)
    particlelist[1].position = vector(a_0, 0, 0)
    particlelist[1].velocity = vector(0, 2.18e6, 0)
    primescene.center = vector(0, 0, 0)
    primescene.range = a_0 * 1.1
    primescene.autoscale = True
    slide.value = coulombconst


def pauseBut(self):
    global run_flag

    if run_flag == False:
        run_flag = True
        self.text = "Pause"
    else:
        run_flag = False
        self.text = "Run"


def coulombSlider(self):
    global coulombconst
    coulombconst = self.value


button(text="Pause", pos=primescene.caption_anchor, bind=pauseBut)
button(text="Reset", pos=primescene.caption_anchor, bind=resetBut)
primescene.append_to_caption('\n')
slide = slider(value=coulombconst, pos=primescene.caption_anchor, min=6e9, max=8e10, bind=coulombSlider)
wtext(text="Attractive Force", pos=primescene.caption_anchor)
# checkbox(text = "Electrostatic Force", bind = electroCheck, checked = True, id = 0)
# checkbox(text = "Magnetic Force", checked = False)
# checkbox(text = "Particle Self interaction", checked = False, bind = selfInteractCheck)

# graphing
distgraph = graph(width=500, height=300, xmin=0, ymin=0, xmax=5, ymax=1, title="probability",
                  xtitle="Radius (a0)", ytitle="relative probability", align="none")

r_histo = list(range(numRadHisto))
snapshot_rhisto = list(range(total_r_samples))
vrad = gvbars(color=color.red, delta=0.1)

hydOrbTheory = gcurve(color=color.blue)
for r in range(0, 500, 1):
    hydOrbTheory.plot((r / 100), (4) * ((r / 100) ** 2) * exp(-2 * (r / 100)))

for i in range(len(r_histo)):
    r_histo[i] = 0.0

for i in range(len(snapshot_rhisto)):
    snapshot_rhisto[i] = 0


def snap_radius(dist):
    bin = int(round(dist / graph_radBin))

    if bin < 50:
        r_histo[bin] += 10 / total_r_samples
        snapshot_rhisto.insert(0, bin)

        if snapshot_rhisto[total_r_samples - 1] > 0:
            r_histo[snapshot_rhisto[total_r_samples - 1]] -= 10 / total_r_samples

        snapshot_rhisto.pop(total_r_samples - 1)


def graph_radius():
    accum = []

    for r in range(numRadHisto):
        accum.append([r / 10, r_histo[r]])

    vrad.data = accum


# sphere(pos=vector(1.29e-11,0,0), color=color.red, radius=1e-12)

particlelist.append(Particle([0, 0, 0], prot_mass, elem_charge, [0, 0, 0], color.purple, 1e-12))
particlelist.append(Particle([0, 2.18e6, 0], elec_mass, -elem_charge, [a_0, 0, 0], color.yellow, 1e-12))

while True:
    rate(2000)

    if run_flag:

        if electro_flag == True:
            applyForce(particlelist)

        for p in range(len(particlelist)):
            particlelist[p].updatePos()

        # print("velocity ", mag(particlelist[1].velocity)/1e8, " m/s")
        # print("distance ", getDistance(particlelist[1].position, particlelist[0].position)*10/a_0, " a_0 ", int(round(getDistance(particlelist[1].position, particlelist[0].position)*10/a_0)))
        # print("position ", particlelist[1].position)
        # print("force ", getElectroForce(particlelist[0].charge, particlelist[1].charge, getDistance(particlelist[0].position, particlelist[1].position)))
        if counter % 20 == 0:
            snap_radius(getDistance(particlelist[1].position, particlelist[0].position))

        counter = counter + 1

        graph_radius()

        time = time + delta_t

