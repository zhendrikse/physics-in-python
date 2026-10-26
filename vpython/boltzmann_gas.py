#Web VPython 3.2
from vpython import canvas, color, vector, vec, curve, random, sqrt, pi, simple_sphere, cos, sin, rate, mag2, graph, gcurve, \
    gvbars, dot, cross, norm, asin, exp

L = cube_edge_in_meters = 1
atomic_mass = 4E-3
T = room_temperature_in_kelvin = 300
total_number_of_atoms = 200
atoms_per_cubic_meter = 200  # So that 200 particles represents the "number of particles in 1 m^3"

avogadro_number = 6.022E23
size_helium_atom = 101325
universal_gas_constant = 8.314
k = boltzmann_constant = 1.3806E-23  # Boltzmann constant

moles_per_cubic_meter_at_room_temp = (size_helium_atom * 1) / (universal_gas_constant * room_temperature_in_kelvin)
conversion_factor_to_real_number_of_atoms = avogadro_number * moles_per_cubic_meter_at_room_temp / atoms_per_cubic_meter

real_number_of_atoms = total_number_of_atoms * conversion_factor_to_real_number_of_atoms
real_mole_amount = real_number_of_atoms / avogadro_number

#print(moles_per_cubic_meter_at_room_temp, "moles in 1 cubic meter")
#print(real_number_of_atoms, "atoms in 1 cubic meter")

# Typical values
gray = color.gray(0.7)  # color of edges of container
mass = atomic_mass / avogadro_number  # helium mass

animation = canvas(range=L, background=color.gray(0.075), align='top', height="500")
animation.title = """&#x2022; A "hard-sphere" gas, written by Bruce Sherwood, modified by Rob Salgado
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/thermodynamics/code/boltzmann_gas.py">boltzmann_gas.py</a>

"""

class Box:
    def __init__(self, length=L, gas_atom_radius=0.03, vertex_radius=0.005):
        self._length = length
        dist = length / 2 + gas_atom_radius
        box_bottom = curve(color=gray, radius=vertex_radius)
        box_bottom.append([vector(-dist, -dist, -dist), vector(-dist, -dist, dist), vector(dist, -dist, dist),
                           vector(dist, -dist, -dist), vector(-dist, -dist, -dist)])
        box_top = curve(color=gray, radius=vertex_radius)
        box_top.append(
            [vector(-dist, dist, -dist), vector(-dist, dist, dist), vector(dist, dist, dist), vector(dist, dist, -dist),
             vector(-dist, dist, -dist)])
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
    def __init__(self, atom_mass=mass, atom_radius=0.03, number_of_atoms=200):
        self._mass = atom_mass
        self._number_of_atoms = number_of_atoms
        self._atom_radius = atom_radius
        self._atoms = []
        self._atom_momenta = []
        self._atom_positions = []
        self._average_kinetic_energy = sqrt(
            2 * atom_mass * 1.5 * k * T)  # average kinetic energy p**2/(2mass) = (3/2)kT

    def is_confined_to_a(self, cube):
        for i in range(self._number_of_atoms):
            x = cube.length() * random() - cube.length() / 2
            y = cube.length() * random() - cube.length() / 2
            z = cube.length() * random() - cube.length() / 2
            atom_position = vec(x, y, z)
            self._atom_positions.append(atom_position)

            if i == 0:
                self._atoms.append(
                    simple_sphere(pos=atom_position, radius=self._atom_radius, color=color.cyan, make_trail=True, retain=100,
                           trail_radius=0.3 * self._atom_radius))
            else:
                self._atoms.append(simple_sphere(pos=atom_position, radius=self._atom_radius, color=gray))

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
            self._atoms[i].pos = self._atom_positions[i] = self._atom_positions[i] + (
                        self._atom_momenta[i] / self._mass) * dt

    def count_collisions_with(self, cube):
        hit_count = 0
        for index in range(len(self._atoms)):
            atom_position = self._atom_positions[index]
            atom_momentum = self._atom_momenta[index]
            if abs(atom_position.x) > cube.length() / 2:
                if atom_position.x < 0:
                    atom_momentum.x = abs(atom_momentum.x)
                else:
                    atom_momentum.x = -abs(atom_momentum.x)
                    hit_count += abs(2 * atom_momentum.x)

            if abs(atom_position.y) > cube.length() / 2:
                if atom_position.y < 0:
                    atom_momentum.y = abs(atom_momentum.y)
                else:
                    atom_momentum.y = -abs(atom_momentum.y)
                    hit_count += abs(2 * atom_momentum.y)

            if abs(atom_position.z) > cube.length() / 2:
                if atom_position.z < 0:
                    atom_momentum.z = abs(atom_momentum.z)
                else:
                    atom_momentum.z = -abs(atom_momentum.z)
                    hit_count += abs(2 * atom_momentum.z)

        return hit_count

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

        difference_in_velocity = velocity_j - velocity_i
        if difference_in_velocity.mag2 == 0:
            return

        atoms_distance = position_i - position_j
        if atoms_distance.mag > self._atom_radius:
            return  # one atom went all the way through another

        # theta is the angle between difference_in_velocity and atoms_distance:
        dx = dot(atoms_distance, difference_in_velocity.hat)  # atoms_distance.mag*cos(theta)
        dy = cross(atoms_distance, difference_in_velocity.hat).mag  # atoms_distance.mag*sin(theta)
        # alpha is the angle of the triangle composed of atoms_distance, path of atom j, and a line
        #   from the center of atom i to the center of atom j where atoms_distance j hits atom i:
        alpha = asin(dy / (2 * self._atom_radius))
        d = (2 * self._atom_radius) * cos(alpha) - dx  # atoms_distance traveled into the atom from first contact
        deltat = d / difference_in_velocity.mag  # time spent moving from first contact to position inside atom

        position_i = position_i - velocity_i * deltat  # back up to contact configuration
        position_j = position_j - velocity_j * deltat
        total_mass = 2 * mass

        # transform momenta to cm frame
        pcmi = self._atom_momenta[atom_index_1] - total_momentum * mass / total_mass
        pcmj = self._atom_momenta[atom_index_2] - total_momentum * mass / total_mass

        # bounce in cm frame
        pcmi = pcmi - 2 * pcmi.dot(norm(atoms_distance)) * norm(atoms_distance)
        pcmj = pcmj - 2 * pcmj.dot(norm(atoms_distance)) * norm(atoms_distance)
        self._atom_momenta[
            atom_index_1] = pcmi + total_momentum * mass / total_mass  # transform momenta back to lab frame
        self._atom_momenta[atom_index_2] = pcmj + total_momentum * mass / total_mass
        self._atom_positions[atom_index_1] = position_i + (
                    self._atom_momenta[atom_index_1] / mass) * deltat  # move forward deltat in time
        self._atom_positions[atom_index_2] = position_j + (self._atom_momenta[atom_index_2] / mass) * deltat
        swap_between_bins(velocity_i.mag, self._atom_momenta[atom_index_1].mag / mass)
        swap_between_bins(velocity_j.mag, self._atom_momenta[atom_index_2].mag / mass)

    def update_momenta_of_colliding_atoms(self):
        for ij in self._check_collisions():
            self._collide(ij[0], ij[1])


box = Box()
gas = Gas(number_of_atoms=total_number_of_atoms)
gas.is_confined_to_a(box)

velocity_binning = 100  # binning for velocity histogram
def bin_number_of(velocity):
    return int(velocity / velocity_binning)  # index into bars array


total_bins = int(4500 / velocity_binning)
histogram = [0.0] * total_bins
histogram[bin_number_of(gas.average_kinetic_energy() / mass)] = total_number_of_atoms

gg = graph(width=500, height=0.4 * 500, xmax=3000, align='left', background=color.black,
           xtitle='speed, m/s', ytitle='Number of atoms', ymax=total_number_of_atoms * velocity_binning / 1000)

theoretical_curve = gcurve(color=color.blue, width=2)
dv = 10
for v in range(0, 3001 + dv, dv):  # theoretical prediction
    theoretical_curve.plot(v, (velocity_binning / dv) * total_number_of_atoms * 4 * pi * ((mass / (2 * pi * k * T)) ** 1.5) * exp(
        -0.5 * mass * (v ** 2) / (k * T)) * (v ** 2) * dv)

accum = []
for i in range(int(3000 / velocity_binning)):
    accum.append([velocity_binning * (i + .5), 0])
vdist = gvbars(color=color.red, delta=velocity_binning)


def swap_between_bins(velocity_1, velocity_2):  # remove from v1 bar, add to v2 bar
    bin_1 = bin_number_of(velocity_1)
    bin_2 = bin_number_of(velocity_2)
    if bin_1 == bin_2:
        return
    if bin_1 >= len(histogram) or bin_2 >= len(histogram):
        return
    histogram[bin_1] -= 1
    histogram[bin_2] += 1

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

total_bins = 0  # number of histogram snapshots to average
time_counter = 0
sample_size = 1000
hit_counter = 0

#print("N,T,V,P, PV/(NT)")
dt = 1E-5

while True:
    rate(300)

    time_counter += 1

    # Accumulate and average histogram snapshots
    for accumulator in accum:
        accumulator[1] = (total_bins * accum[i][1] + histogram[i]) / (total_bins + 1)
    if total_bins % 10 == 0:
        vdist.data = accum
    total_bins += 1

    gas.update_with_timestep(dt)
    gas.update_momenta_of_colliding_atoms()
    hit_counter += gas.count_collisions_with(box)

    if time_counter == sample_size:
        #        P=(1/2)*(1/0.02242)*RS_NatomsFactor*(hitcounter/L**2)/(dt*tcountMax)
        P = (1 / 3) * conversion_factor_to_real_number_of_atoms * (hit_counter / L ** 2) / (dt * sample_size)
        time_counter = 0
        hit_counter = 0

#        print("[", total_number_of_atoms, "(", round(real_mole_amount, 4), ")", ",", T, ",", L ** 3, ",", round(P, 4), "(",
#              round(P / size_helium_atom, 4), ")", ",",
#              P * L ** 3 / (real_number_of_atoms * T), "]")
