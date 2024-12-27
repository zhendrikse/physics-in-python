from vpython import canvas, color, vector, vec, curve, random, sqrt, pi, sphere, cos, sin, rate, mag2, graph, gcurve, \
    gvbars, dot, cross, norm, asin, exp

# Hard-sphere gas.
# Bruce Sherwood

#######################
### Rob Salgado modifications to calculate the pressure, appropriately scaled to represent the expected quantities in the ideal gas law.
### Zeger Hendrikse refactoring to gas class
###

cube_edge_in_meters = 1
RS_atomicMassNumberInKilograms = 4E-3
room_temperature_in_kelvin = 300
total_number_of_atoms = 200

###
RS_NatomsForCubicMeter = 200  # So that 200 particles (the default value of Natoms) represents the "number of particles in 1 m^3"

RS_Nav = 6.022E23
RS_Atm = 101325
RS_UniversalGasConstant = 8.314
RS_BoltzmannK = 1.3806E-23  # Boltzmann constant
RS_RoomK = 300

RS_MolesInCubicMeterRoom = (RS_Atm * 1) / (RS_UniversalGasConstant * RS_RoomK)
RS_NatomsFactor = RS_Nav * RS_MolesInCubicMeterRoom / RS_NatomsForCubicMeter

Natoms = total_number_of_atoms  # change this to have more or fewer atoms

RS_NrealAtoms = Natoms * RS_NatomsFactor
RS_NrealMoles = RS_NrealAtoms / RS_Nav

print(RS_MolesInCubicMeterRoom, "moles in 1 cubic meter")
print(RS_NrealAtoms, "atoms in 1 cubic meter")

# Typical values
L = cube_edge_in_meters  # container is a cube L on a side
gray = color.gray(0.7)  # color of edges of container
mass = RS_atomicMassNumberInKilograms / RS_Nav  # helium mass

Ratom = 0.03  # wildly exaggerated size of helium atom
k = RS_BoltzmannK  # Boltzmann constant
T = room_temperature_in_kelvin
dt = 1E-5

animation = canvas(width=500, height=500, align='left')
animation.range = L
animation.title = 'A "hard-sphere" gas'
s = """  Theoretical and averaged speed distributions (meters/sec).
  Initially all atoms have the same speed, but collisions
  change the speeds of the colliding atoms. One of the atoms is
  marked and leaves a trail so you can follow its path.

"""
animation.caption = s

class Box:
    def __init__(self, length=L, gas_atom_radius=Ratom, vertex_radius = 0.005):
        self._length = length
        dist = length / 2 + gas_atom_radius
        box_bottom = curve(color=gray, radius=vertex_radius)
        box_bottom.append([vector(-dist, -dist, -dist), vector(-dist, -dist, dist), vector(dist, -dist, dist), vector(dist, -dist, -dist), vector(-dist, -dist, -dist)])
        box_top = curve(color=gray, radius=vertex_radius)
        box_top.append([vector(-dist, dist, -dist), vector(-dist, dist, dist), vector(dist, dist, dist), vector(dist, dist, -dist), vector(-dist, dist, -dist)])
        vert1 = curve(color=gray, radius=vertex_radius)
        vert2 = curve(color=gray, radius=vertex_radius)
        vert3 = curve(color=gray, radius=vertex_radius)
        vert4 = curve(color=gray, radius=vertex_radius)
        vert1.append([vector(-dist, -dist, -dist), vector(-dist, dist, -dist)])
        vert2.append([vector(-dist, -dist, dist), vector(-dist, dist, dist)])
        vert3.append([vector(dist, -dist, dist), vector(dist, dist, dist)])
        vert4.append([vector(dist, -dist, -dist), vector(dist, dist, -dist)])

    def length(self):
        return self._length

class Gas:
    def __init__(self, atom_mass=mass, atom_radius = Ratom, number_of_atoms=Natoms):
        self._mass = atom_mass
        self._atom_radius = atom_radius
        self._atoms = []
        self._atom_momenta = []
        self._atom_positions = []
        self._average_kinetic_energy = sqrt(2 * atom_mass * 1.5 * k * T)  # average kinetic energy p**2/(2mass) = (3/2)kT

        for i in range(number_of_atoms):
            x = L * random() - L / 2
            y = L * random() - L / 2
            z = L * random() - L / 2
            atom_position = vec(x, y, z)
            self._atom_positions.append(atom_position)

            if i == 0:
                self._atoms.append(sphere(pos=atom_position, radius=atom_radius, color=color.cyan, make_trail=True, retain=100,
                                    trail_radius=0.3 * atom_radius))
            else:
                self._atoms.append(sphere(pos=atom_position, radius=atom_radius, color=gray))

            theta = pi * random()
            phi = 2 * pi * random()
            p_x = self._average_kinetic_energy * sin(theta) * cos(phi)
            p_y = self._average_kinetic_energy * sin(theta) * sin(phi)
            p_z = self._average_kinetic_energy * cos(theta)
            self._atom_momenta.append(vector(p_x, p_y, p_z))

    def average_kinetic_energy(self):
        return self._average_kinetic_energy

    def update_with_timestep(self, dt):
        for i in range(len(self._atoms)):
            self._atoms[i].pos = self._atom_positions[i] = self._atom_positions[i] + (self._atom_momenta[i] / self._mass) * dt

    def count_collisions_with(self, box):
        hit_counter = 0
        for index in range(len(self._atoms)):
            loc = self._atom_positions[index]
            if abs(loc.x) > box.length() / 2:
                if loc.x < 0:
                    self._atom_momenta[index].x = abs(self._atom_momenta[index].x)
                else:
                    self._atom_momenta[index].x = -abs(self._atom_momenta[index].x)
                    hit_counter += abs(2 * self._atom_momenta[index].x)

            if abs(loc.y) > box.length() / 2:
                if loc.y < 0:
                    self._atom_momenta[index].y = abs(self._atom_momenta[index].y)
                else:
                    self._atom_momenta[index].y = -abs(self._atom_momenta[index].y)
                    hit_counter += abs(2 * self._atom_momenta[index].y)

            if abs(loc.z) > box.length() / 2:
                if loc.z < 0:
                    self._atom_momenta[index].z = abs(self._atom_momenta[index].z)
                else:
                    self._atom_momenta[index].z = -abs(self._atom_momenta[index].z)
                    hit_counter += abs(2 * self._atom_momenta[index].z)

        return hit_counter

    def _check_collisions(self):
        hit_list = []
        r2 = 2 * self._atom_radius
        r2 *= r2
        for index in range(len(self._atoms)):
            for j in range(index):
                distance = self._atom_positions[index] - self._atom_positions[j]
                if mag2(distance) < r2:
                    hit_list.append([index, j])
        return hit_list

    def _collide(self, atom_index_1, atom_index_2):
        total_momentum = self._atom_momenta[atom_index_1] + self._atom_momenta[atom_index_2]
        position_i = self._atom_positions[atom_index_1]
        position_j = self._atom_positions[atom_index_2]
        velocity_i = self._atom_momenta[atom_index_1] / mass
        velocity_j = self._atom_momenta[atom_index_2] / mass
        vrel = velocity_j - velocity_i
        a = vrel.mag2
        if a == 0:
            return  # exactly same velocities
        rrel = position_i - position_j
        if rrel.mag > self._atom_radius:
            return  # one atom went all the way through another

        # theta is the angle between vrel and rrel:
        dx = dot(rrel, vrel.hat)  # rrel.mag*cos(theta)
        dy = cross(rrel, vrel.hat).mag  # rrel.mag*sin(theta)
        # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
        #   from the center of atom i to the center of atom j where atome j hits atom i:
        alpha = asin(dy / (2 * self._atom_radius))
        d = (2 * self._atom_radius) * cos(alpha) - dx  # distance traveled into the atom from first contact
        deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

        position_i = position_i - velocity_i * deltat  # back up to contact configuration
        position_j = position_j - velocity_j * deltat
        total_mass = 2 * mass

        # transform momenta to cm frame
        pcmi = self._atom_momenta[atom_index_1] - total_momentum * mass / total_mass
        pcmj = self._atom_momenta[atom_index_2] - total_momentum * mass / total_mass
        rrel = norm(rrel)

        # bounce in cm frame
        pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel
        pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
        self._atom_momenta[atom_index_1] = pcmi + total_momentum * mass / total_mass  # transform momenta back to lab frame
        self._atom_momenta[atom_index_2] = pcmj + total_momentum * mass / total_mass
        self._atom_positions[atom_index_1] = position_i + (self._atom_momenta[atom_index_1] / mass) * deltat  # move forward deltat in time
        self._atom_positions[atom_index_2] = position_j + (self._atom_momenta[atom_index_2] / mass) * deltat
        interchange(velocity_i.mag, self._atom_momenta[atom_index_1].mag / mass)
        interchange(velocity_j.mag, self._atom_momenta[atom_index_2].mag / mass)

    def update_momenta_of_colliding_atoms(self):
        for ij in self._check_collisions():
            self._collide(ij[0], ij[1])

gas = Gas()
box = Box()

deltav = 100  # binning for v histogram


def barx(v):
    return int(v / deltav)  # index into bars array


nhisto = int(4500 / deltav)
histo = []
for i in range(nhisto): histo.append(0.0)
histo[barx(gas.average_kinetic_energy() / mass)] = Natoms

gg = graph(width=500, height=0.4 * 500, xmax=3000, align='left',
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

    gas.update_with_timestep(dt)
    gas.update_momenta_of_colliding_atoms()
    hitcounter += gas.count_collisions_with(box)


    if (tcounter == tcountMax):
        #        P=(1/2)*(1/0.02242)*RS_NatomsFactor*(hitcounter/L**2)/(dt*tcountMax)
        P = (1 / 3) * RS_NatomsFactor * (hitcounter / L ** 2) / (dt * tcountMax)
        tcounter = 0
        hitcounter = 0

        print("[", Natoms, "(", RS_NrealMoles, ")", ",", T, ",", L ** 3, ",", P, "(", P / RS_Atm, ")", ",",
              P * L ** 3 / (RS_NrealAtoms * T), "]")
