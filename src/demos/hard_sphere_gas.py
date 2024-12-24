from vpython import canvas, color, vector, vec, curve, random, sqrt, pi, sphere, cos, sin, rate, mag2, graph, gcurve, \
    gvbars, dot, cross, norm, asin, exp

# Hard-sphere gas.

# Bruce Sherwood

#######################
### Rob Salgado modifications to calculate the pressure, appropriately scaled to represent the expected quantities in the ideal gas law.
###

RS_CubeEdgeInMeters = 1
RS_atomicMassNumberInKilograms = 4E-3
RS_TempK = 300

RS_Natoms = 200

###
RS_NatomsForCubicMeter = 200  # So that 200 particles (the default value of Natoms) represents the "number of particles in 1 m^3"

RS_Nav = 6.022E23
RS_Atm = 101325
RS_UniversalGasConstant = 8.314
RS_BoltzmannK = 1.3806E-23  # Boltzmann constant
RS_RoomK = 300

RS_MolesInCubicMeterRoom = (RS_Atm * 1) / (RS_UniversalGasConstant * RS_RoomK)
RS_NatomsFactor = RS_Nav * RS_MolesInCubicMeterRoom / RS_NatomsForCubicMeter

###
###
#######################

win = 500

Natoms = RS_Natoms  # change this to have more or fewer atoms

RS_NrealAtoms = Natoms * RS_NatomsFactor
RS_NrealMoles = RS_NrealAtoms / RS_Nav

print(RS_MolesInCubicMeterRoom, "moles in 1 cubic meter")
print(RS_NrealAtoms, "atoms in 1 cubic meter")

# Typical values
L = RS_CubeEdgeInMeters  # container is a cube L on a side
gray = color.gray(0.7)  # color of edges of container
mass = 4E-3 / 6E23  # helium mass
mass = RS_atomicMassNumberInKilograms / RS_Nav  # helium mass

Ratom = 0.03  # wildly exaggerated size of helium atom
k = 1.4E-23  # Boltzmann constant

k = RS_BoltzmannK  # Boltzmann constant

T = 300  # around room temperature
T = RS_TempK
dt = 1E-5

animation = canvas(width=win, height=win, align='left')
animation.range = L
animation.title = 'A "hard-sphere" gas'
s = """  Theoretical and averaged speed distributions (meters/sec).
  Initially all atoms have the same speed, but collisions
  change the speeds of the colliding atoms. One of the atoms is
  marked and leaves a trail so you can follow its path.

"""
animation.caption = s

d = L / 2 + Ratom
r = 0.005
boxbottom = curve(color=gray, radius=r)
boxbottom.append([vector(-d, -d, -d), vector(-d, -d, d), vector(d, -d, d), vector(d, -d, -d), vector(-d, -d, -d)])
boxtop = curve(color=gray, radius=r)
boxtop.append([vector(-d, d, -d), vector(-d, d, d), vector(d, d, d), vector(d, d, -d), vector(-d, d, -d)])
vert1 = curve(color=gray, radius=r)
vert2 = curve(color=gray, radius=r)
vert3 = curve(color=gray, radius=r)
vert4 = curve(color=gray, radius=r)
vert1.append([vector(-d, -d, -d), vector(-d, d, -d)])
vert2.append([vector(-d, -d, d), vector(-d, d, d)])
vert3.append([vector(d, -d, d), vector(d, d, d)])
vert4.append([vector(d, -d, -d), vector(d, d, -d)])

atoms = []
atom_momenta = []
atom_positions = []
pavg = sqrt(2 * mass * 1.5 * k * T)  # average kinetic energy p**2/(2mass) = (3/2)kT

for i in range(Natoms):
    x = L * random() - L / 2
    y = L * random() - L / 2
    z = L * random() - L / 2
    if i == 0:
        atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=color.cyan, make_trail=True, retain=100,
                            trail_radius=0.3 * Ratom))
    else:
        atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=gray))
    atom_positions.append(vec(x, y, z))
    theta = pi * random()
    phi = 2 * pi * random()
    px = pavg * sin(theta) * cos(phi)
    py = pavg * sin(theta) * sin(phi)
    pz = pavg * cos(theta)
    atom_momenta.append(vector(px, py, pz))

deltav = 100  # binning for v histogram


def barx(v):
    return int(v / deltav)  # index into bars array


nhisto = int(4500 / deltav)
histo = []
for i in range(nhisto): histo.append(0.0)
histo[barx(pavg / mass)] = Natoms

gg = graph(width=win, height=0.4 * win, xmax=3000, align='left',
           xtitle='speed, m/s', ytitle='Number of atoms', ymax=Natoms * deltav / 1000)

theory = gcurve(color=color.blue, width=2)
dv = 10
for v in range(0, 3001 + dv, dv):  # theoretical prediction
    theory.plot(v, (deltav / dv) * Natoms * 4 * pi * ((mass / (2 * pi * k * T)) ** 1.5) * exp(
        -0.5 * mass * (v ** 2) / (k * T)) * (v ** 2) * dv)

accum = []
for i in range(int(3000 / deltav)): accum.append([deltav * (i + .5), 0])
vdist = gvbars(color=color.red, delta=deltav)


def interchange(v1, v2):  # remove from v1 bar, add to v2 bar
    barx1 = barx(v1)
    barx2 = barx(v2)
    if barx1 == barx2:  return
    if barx1 >= len(histo) or barx2 >= len(histo): return
    histo[barx1] -= 1
    histo[barx2] += 1


def check_collisions():
    hitlist = []
    r2 = 2 * Ratom
    r2 *= r2
    for i in range(Natoms):
        ai = atom_positions[i]
        for j in range(i):
            aj = atom_positions[j]
            dr = ai - aj
            if mag2(dr) < r2: hitlist.append([i, j])
    return hitlist


nhisto = 0  # number of histogram snapshots to average

tcounter = 0
tcountMax = 1000  ## sample size
hitcounter = 0

print("N,T,V,P, PV/(NT)")

while True:
    rate(300)

    tcounter += 1

    # Accumulate and average histogram snapshots
    for i in range(len(accum)): accum[i][1] = (nhisto * accum[i][1] + histo[i]) / (nhisto + 1)
    if nhisto % 10 == 0:
        vdist.data = accum
    nhisto += 1

    # Update all positions
    for i in range(Natoms): atoms[i].pos = atom_positions[i] = atom_positions[i] + (atom_momenta[i] / mass) * dt

    # Check for collisions
    hitlist = check_collisions()

    # If any collisions took place, update momenta of the two atoms
    for ij in hitlist:
        i = ij[0]
        j = ij[1]
        ptot = atom_momenta[i] + atom_momenta[j]
        posi = atom_positions[i]
        posj = atom_positions[j]
        vi = atom_momenta[i] / mass
        vj = atom_momenta[j] / mass
        vrel = vj - vi
        a = vrel.mag2
        if a == 0: continue;  # exactly same velocities
        rrel = posi - posj
        if rrel.mag > Ratom: continue  # one atom went all the way through another

        # theta is the angle between vrel and rrel:
        dx = dot(rrel, vrel.hat)  # rrel.mag*cos(theta)
        dy = cross(rrel, vrel.hat).mag  # rrel.mag*sin(theta)
        # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
        #   from the center of atom i to the center of atom j where atome j hits atom i:
        alpha = asin(dy / (2 * Ratom))
        d = (2 * Ratom) * cos(alpha) - dx  # distance traveled into the atom from first contact
        deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

        posi = posi - vi * deltat  # back up to contact configuration
        posj = posj - vj * deltat
        mtot = 2 * mass
        pcmi = atom_momenta[i] - ptot * mass / mtot  # transform momenta to cm frame
        pcmj = atom_momenta[j] - ptot * mass / mtot
        rrel = norm(rrel)
        pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel  # bounce in cm frame
        pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
        atom_momenta[i] = pcmi + ptot * mass / mtot  # transform momenta back to lab frame
        atom_momenta[j] = pcmj + ptot * mass / mtot
        atom_positions[i] = posi + (atom_momenta[i] / mass) * deltat  # move forward deltat in time
        atom_positions[j] = posj + (atom_momenta[j] / mass) * deltat
        interchange(vi.mag, atom_momenta[i].mag / mass)
        interchange(vj.mag, atom_momenta[j].mag / mass)

    for i in range(Natoms):
        loc = atom_positions[i]
        if abs(loc.x) > L / 2:
            if loc.x < 0:
                atom_momenta[i].x = abs(atom_momenta[i].x)
            else:
                atom_momenta[i].x = -abs(atom_momenta[i].x)
                hitcounter += abs(2 * atom_momenta[i].x)

        if abs(loc.y) > L / 2:
            if loc.y < 0:
                atom_momenta[i].y = abs(atom_momenta[i].y)
            else:
                atom_momenta[i].y = -abs(atom_momenta[i].y)
                hitcounter += abs(2 * atom_momenta[i].y)

        if abs(loc.z) > L / 2:
            if loc.z < 0:
                atom_momenta[i].z = abs(atom_momenta[i].z)
            else:
                atom_momenta[i].z = -abs(atom_momenta[i].z)
                hitcounter += abs(2 * atom_momenta[i].z)

    if (tcounter == tcountMax):
        #        P=(1/2)*(1/0.02242)*RS_NatomsFactor*(hitcounter/L**2)/(dt*tcountMax)
        P = (1 / 3) * RS_NatomsFactor * (hitcounter / L ** 2) / (dt * tcountMax)
        tcounter = 0
        hitcounter = 0

        print("[", Natoms, "(", RS_NrealMoles, ")", ",", T, ",", L ** 3, ",", P, "(", P / RS_Atm, ")", ",",
              P * L ** 3 / (RS_NrealAtoms * T), "]")
