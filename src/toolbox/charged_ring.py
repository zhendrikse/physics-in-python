from vpython import sin, cos, vec, box, sphere, rate, color, pi, vector

from toolbox.charge import Q, k

class ChargedRing:
    def __init__(self, number_of_ring_segments=60, radius=0.5e-10, draw=True, charge=-Q):
        self._segments = []  # array holding all the segments
        self._radius = radius
        self._charge = charge

        dx = 2 * pi * radius / number_of_ring_segments  # width of ring segment
        for i in range(0, number_of_ring_segments):
            theta = i * (2 * pi / number_of_ring_segments)  # angular position on ring
            x = radius * cos(theta)
            y = radius * sin(theta)
            if draw:
                self._segments.append(box(pos=vec(x, y, 0), size=vec(dx, dx, dx), color=color.green))
                self._segments[i].rotate(axis=vec(0, 0, 1), angle=theta)

    def field_at(self, position):
        dq = self._charge / len(self._segments)  # charge of ring segment
        E = vec(0, 0, 0)
        for segment in self._segments:
            r = segment.pos - position
            dE = k * dq * r.norm() / r.mag2
            E = E + dE
        return E

    @property
    def radius(self):
        return self._radius