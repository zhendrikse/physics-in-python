from vpython import sin, cos, vec, box, sphere, rate, color, pi, vector

from toolbox.charge import Q, k, Charge
from toolbox.field import Field


class ChargedRing:
    def __init__(self, number_of_ring_segments=60, radius=0.5e-10, charge=-Q, draw=True):
        self._segment_positions = []  # array holding all the segments
        self._radius = radius
        self._charge = charge

        dx = 2 * pi * radius / number_of_ring_segments  # width of ring segment
        for i in range(0, number_of_ring_segments):
            theta = i * (2 * pi / number_of_ring_segments)  # angular position on ring
            x = radius * cos(theta)
            y = radius * sin(theta)
            self._segment_positions.append(vec(x, y, 0))
            if draw:
                a_box = box(pos=vec(x, y, 0), size=vec(dx, dx, dx), color=color.green)
                a_box.rotate(axis=vec(0, 0, 1), angle=theta)

        dq = self._charge / len(self._segment_positions)  # charge of ring segment
        charges = [Charge(position=position, charge=dq, radius=radius, draw=False) for position in self._segment_positions]
        self._field = Field(charges)

    def field_at(self, position):
        dq = self._charge / len(self._segment_positions)  # charge of ring segment
        E = vec(0, 0, 0)
        for segment_position in self._segment_positions:
            r = segment_position - position
            dE = k * dq * r.norm() / r.mag2
            E = E + dE
        return E

    def show_field(self, x_range, y_range, z_range):
        self._field.show(x_range, y_range, z_range)

    @property
    def radius(self):
        return self._radius
