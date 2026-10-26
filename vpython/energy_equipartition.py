#Web VPython 3.2
from vpython import simple_sphere, color, vector, cylinder, mag, norm, dot, cross, rate, sqrt, vec, box, canvas, graph, gcurve, random

title = """&#x2022; Based on code shown in <a href="https://www.youtube.com/watch?v=tP5u-V-BLQo">this video</a> by Jordan Huang
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/thermodynamics/code/energy_equipartition.py">energy_equipartition.py</a>
&#x2022; The <span style="color: green">green curve</span> is the averaged kinetic energy of the center of mass
&#x2022; The <span style="color: red">red curve</span> is the averaged vibrational potential energy
&#x2022; The <span style="color: purple">purple curve</span> is the averaged vibrational kinetic energy
&#x2022; The <span style="color: blue">blue curve</span> is the averaged rotational kinetic energy

"""

display = canvas(title=title, width=600, height=600, background=color.gray(0.075), forward=vec(-.55, -.42, -.75), range=3.75E-10)

size, k_bond = 31E-12, 18600.0
d = 2.5 * size
N = 20
one_third = 1. / 3.
L = ((24.4E-3 / 6E23) * N) ** one_third / 50.  # 2L is the length of the cubic container box, the numer is made up

k, T = 1.38E-23, 298.0
mass_o = 16 / 6E23
mass_c = 12 / 6E23

class Atom:
    def __init__(self, position, initial_velocity, mass, radius, colour):
        self._atom = simple_sphere(pos=position, radius=radius, color=colour)
        self._mass = mass
        self._velocity = vector(random(), random(), random()) * initial_velocity

    def check_box_bounce(self):
        if abs(self._atom.pos.x) >= L - size and self._atom.pos.x * self._velocity.x >= 0:
            self._velocity.x = -self._velocity.x
        if abs(self._atom.pos.y) >= L - size and self._atom.pos.y * self._velocity.y >= 0:
            self._velocity.y = -self._velocity.y
        if abs(self._atom.pos.z) >= L - size and self._atom.pos.z * self._velocity.z >= 0:
            self._velocity.z = -self._velocity.z

    def time_lapse(self, bond_force, dt):
        acceleration_carbon = bond_force / self._mass
        self._velocity += acceleration_carbon * dt
        self._atom.pos += self._velocity * dt

    def pos(self):
        return self._atom.pos

    def momentum(self):
        return self._mass * self._velocity

    def mass(self):
        return self._mass

    def velocity(self):
        return self._velocity


class CarbonMonoxide:
    def __init__(self, oxygen_mass=mass_o, carbon_mass=mass_c, initial_v=sqrt(6E3 * k * T / (mass_c + mass_o))):
        pos = vector(random() - .5, random() - .5, random() - .5) * L
        axis = vector(1. * d, 0, 0)

        self._oxygen = Atom(pos, initial_v, oxygen_mass, size, color.red)
        self._carbon = Atom(pos + axis, initial_v, carbon_mass, size, color.blue)

        self._bond = cylinder(pos=pos, axis=axis, radius=size / 2., color=vec(0.975, .8, .55))
        self._bond_constant = k_bond

    def check_box_bounce(self):
        self._carbon.check_box_bounce()
        self._oxygen.check_box_bounce()

    def bond_force_on_oxygen(self):
        return self._bond_constant * (mag(self._bond.axis) - d) * norm(self._bond.axis)

    def check_collision_with(self, other):
        carbon_1, oxygen_1, carbon_2, oxygen_2 = self._carbon, self._oxygen, other._carbon, other._oxygen
        if mag(carbon_1.pos() - carbon_2.pos()) <= 2 * size and dot(carbon_1.pos() - carbon_2.pos(), carbon_1.velocity() - carbon_2.velocity()) <= 0:
            carbon_1._velocity, carbon_2._velocity = collision_between(carbon_1, carbon_2)
        if mag(oxygen_1.pos() - carbon_2.pos()) <= 2 * size and dot(oxygen_1.pos() - carbon_2.pos(), oxygen_1.velocity() - carbon_2.velocity()) <= 0:
            oxygen_1._velocity, carbon_2._velocity = collision_between(oxygen_1, carbon_2)
        if mag(carbon_1.pos() - oxygen_2.pos()) <= 2 * size and dot(carbon_1.pos() - oxygen_2.pos(), carbon_1.velocity() - oxygen_2.velocity()) <= 0:
            carbon_1._velocity, oxygen_2._velocity = collision_between(carbon_1, oxygen_2)
        if mag(oxygen_1.pos() - oxygen_2.pos()) <= 2 * size and dot(oxygen_1.pos() - oxygen_2.pos(), oxygen_1.velocity() - oxygen_2.velocity()) <= 0:
            oxygen_1._velocity, oxygen_2._velocity = collision_between(oxygen_1, oxygen_2)

    def time_lapse(self, dt):
        self._carbon.time_lapse(-self.bond_force_on_oxygen(), dt)
        self._oxygen.time_lapse(+self.bond_force_on_oxygen(), dt)

        self._bond.axis = self._carbon.pos() - self._oxygen.pos()
        self._bond.pos = self._oxygen.pos()

    def com(self):  # center of mass
        return (self._carbon.pos() * self._carbon.mass() + self._oxygen.pos() * self._oxygen.mass()) / self.mass()

    def com_v(self):
        return (self._carbon.momentum() + self._oxygen.momentum()) / self.mass()

    def v_P(self):
        return self._bond_constant * (mag(self._bond.axis) - d) * (mag(self._bond.axis) - d) / 2

    def v_K(self):
        C = self._carbon.mass() * (dot(self._carbon.velocity() - self.com_v(), self._bond.axis) / mag(self._bond.axis)) ** 2 / 2
        O = self._oxygen.mass() * (dot(self._oxygen.velocity() - self.com_v(), self._bond.axis) / mag(self._bond.axis)) ** 2 / 2
        return C + O

    def r_K(self):
        C = self._carbon.mass() * (mag(cross(self._carbon.velocity() - self.com_v(), self._bond.axis)) / mag(self._bond.axis)) ** 2 / 2
        O = self._oxygen.mass() * (mag(cross(self._oxygen.velocity() - self.com_v(), self._bond.axis)) / mag(self._bond.axis)) ** 2 / 2
        return C + O

    def com_K(self):
        return .5 * self.mass() * dot(self.com_v(), self.com_v())

    def mass(self):
        return self._carbon.mass() + self._oxygen.mass()


def collision_between(atom_1, atom_2):
    distance = atom_2.pos() - atom_1.pos()
    distance_squared = dot(distance, distance)
    v1prime = atom_1.velocity() - 2 * atom_2.mass() / (atom_1.mass() + atom_2.mass()) * -distance * dot(atom_1.velocity() - atom_2.velocity(), -distance) / distance_squared
    v2prime = atom_2.velocity() - 2 * atom_1.mass() / (atom_1.mass() + atom_2.mass()) * distance * dot(atom_2.velocity() - atom_1.velocity(), distance) / distance_squared
    return v1prime, v2prime


# if __name__ == "__main__":
#     a = CarbonMonoxide(pos=vector(0, 0, 0), axis = vector(2.6 * size, 0, 0))
#     a.O.v = vector(1, 1, 0)
#     a.C.v = vector(2, -1, 0)
#     a.time_lapse(dt)
#     print(a.bond_force_on_O(), a.com(), a.v_P(), a.v_K(), a.r_K(), a.com_K())

container = box(length=2 * L, height=2 * L, width=2 * L, opacity=.4, color=vec(.5, 1, .5))
display.append_to_caption("\n")
energies = graph(width=600, align="left", ymin=0, background=color.black, title="Average energies")
c_avg_com_K = gcurve(color=color.green)
c_avg_v_P = gcurve(color=color.red)
c_avg_v_K = gcurve(color=color.purple)
c_avg_r_K = gcurve(color=color.blue)

co_molecules = []
for _ in range(N):
    co_molecules += [CarbonMonoxide()]

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

times = 0  # number of loops that has been run
dt = 5E-16
t = 0
total_com_K, total_v_K, total_v_P, total_r_K = 0, 0, 0, 0
while True:
    rate(300)
    for molecule in co_molecules:
        molecule.time_lapse(dt)
        molecule.check_box_bounce()

    for i in range(N - 1):  # The first N - 1 molecules
        for j in range(i + 1, N):  # From i + 1 to the last molecules, to avoid double-checking
            co_molecules[i].check_collision_with(co_molecules[j])

    for co_molecule in co_molecules:
        total_com_K += co_molecule.com_K()
        total_v_K += co_molecule.v_K()
        total_v_P += co_molecule.v_P()
        total_r_K += co_molecule.r_K()

    t += dt
    times += 1
    c_avg_com_K.plot(times, total_com_K / times)
    c_avg_v_P.plot(times, total_v_P / times)
    c_avg_v_K.plot(times, total_v_K / times)
    c_avg_r_K.plot(times, total_r_K / times)