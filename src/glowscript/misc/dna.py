#Web VPython 3.2

from vpython import canvas, vector, color, cos, sin, cylinder, sphere, pi, rate, slider

title_text ="""Simulation of a DNA molecule

&#x2022; <a href="https://trinket.io/glowscript/7ba54885924b">Original idea and code</a> by Francisco Adeil Gomes Araujo
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/physics-in-python/blob/main/src/glowscript/misc/dna.py">dna.py</a> 

"""

animation = canvas(title=title_text, width=800, height=600, range=4, center=vector(0, 3, 0),
                   background=color.gray(0.1))

# List of colours to represent the pairs of nucleotides
amino_colors = [color.red, color.blue, color.green, color.yellow]


class Nucleotide:
    def __init__(self, position, colour, radius=0.1):
        self._amino = sphere(pos=position, radius=radius, color=colour)

    def pos(self):
        return self._amino.pos

    def rotate(self, angle=0.01, axis=vector(0, 1, 0), origin=vector(0, 0, 0)):
        self._amino.rotate(angle=angle, axis=axis, origin=origin)


class NucleotidePair:
    def __init__(self, index, helix_angle, helix_radius, nucleotide_height):
        x, y, z = cos(index * helix_angle), index * nucleotide_height, sin(index * helix_angle)
        position_nucleotide_1 = helix_radius * vector(x, y, z)
        position_nucleotide_2 = helix_radius * vector(-x, y, -z)

        self._nucleotide_1 = Nucleotide(position_nucleotide_1, amino_colors[index % 4])
        self._nucleotide_2 = Nucleotide(position_nucleotide_2, amino_colors[(index + 2) % 4])
        self._connection = cylinder(pos=position_nucleotide_1, axis=self.distance(), radius=0.05, color=color.white)

    def rotate(self, angle=0.01, axis=vector(0, 1, 0), origin=vector(0, 0, 0)):
        self._nucleotide_1.rotate(angle=angle, axis=axis, origin=origin)
        self._nucleotide_2.rotate(angle=angle, axis=axis, origin=origin)
        self._connection.rotate(angle=angle, axis=axis, origin=origin)

    def nucleotide_1_pos(self):
        return self._nucleotide_1.pos()

    def nucleotide_2_pos(self):
        return self._nucleotide_2.pos()

    def distance(self):
        return self._nucleotide_2.pos() - self._nucleotide_1.pos()


class Dna:
    def __init__(self, number_of_pairs=12, omega=0.01, nucleotide_height=0.4, helix_radius=1.0, helix_angle=pi / 6):
        self._connections = []
        self._nucleotide_pairs = []
        self._omega = omega
        self._new_helix_with(number_of_pairs, nucleotide_height, helix_radius, helix_angle)

    def _new_connection_between(self, initial_position, final_position):
        return cylinder(pos=initial_position, axis=(final_position - initial_position), radius=0.05, color=color.white)

    def _new_helix_connection(self):
        last_pair = self._nucleotide_pairs[-1]
        pair_before_last_pair = self._nucleotide_pairs[-2]
        connection_1 = self._new_connection_between(last_pair.nucleotide_1_pos(),
                                                    pair_before_last_pair.nucleotide_1_pos())
        connection_2 = self._new_connection_between(last_pair.nucleotide_2_pos(),
                                                    pair_before_last_pair.nucleotide_2_pos())
        self._connections.append(connection_1)
        self._connections.append(connection_2)

    def _new_connected_pair_with(self, index, nucleotide_height, helix_radius, helix_angle):
        self._nucleotide_pairs.append(NucleotidePair(index, helix_angle, helix_radius, nucleotide_height))
        if index > 0: self._new_helix_connection()

    def _new_helix_with(self, number_of_pairs, nucleotide_height, helix_radius, helix_angle):
        for i in range(number_of_pairs):
            self._new_connected_pair_with(i, nucleotide_height, helix_radius, helix_angle)

    def rotate(self, axis=vector(0, 1, 0), origin=vector(0, 0, 0)):
        for pair in self._nucleotide_pairs:
            pair.rotate(angle=self._omega, axis=axis, origin=origin)
        for connection in self._connections:
            connection.rotate(angle=self._omega, axis=axis, origin=origin)

    def set_omega_to(self, value):
        self._omega = value


def change_rotation_speed():
    dna.set_omega_to(speed_slider.value)


animation.append_to_caption("\nRotation speed ")
dna = Dna(number_of_pairs=16, omega=0.01)
speed_slider = slider(bind=change_rotation_speed, value=0.01, min=0.0, max=.1)

while True:
    dna.rotate()
    rate(30)
