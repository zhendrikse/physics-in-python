from vpython import arrow, arange, vec, color, pi, cos, sin, floor

class PlaneWave:
    def __init__(self, k=2 * pi / 5, omega=2 * pi, amplitude=3.):
        self._arrows = [arrow(pos=vec(x, 0, 0), axis=vec(0, amplitude, 0), color=color.red, shaftwidth=0.2) for x in
                        arange(-10, 10, 0.3)]
        self._amplitude = amplitude
        self._k = k
        self._omega = omega

    def set_k_to(self, value):
        self._k = value

    def set_omega_to(self, value):
        self._omega = value

    def set_amplitude_to(self, value):
        self._amplitude = value

    def update(self, t):
        for arrow_ in self._arrows:
            x = arrow_.pos.x
            k = self._k
            w = self._omega
            phase = k * x - w * t
            cycles = phase / (2 * pi)
            cycles -= floor(cycles)
            cphase = 2 * pi * cycles

            arrow_.axis.z = -cos(phase) * self._amplitude
            arrow_.axis.y = -sin(phase) * self._amplitude
            arrow_.color = color.hsv_to_rgb(vec(1.0 - cphase / (2 * pi), 1.0, 1.0))
