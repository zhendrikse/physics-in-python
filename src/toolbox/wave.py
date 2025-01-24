from vpython import vec, pi, arrow, color, sin


class Wave:
    def __init__(self, position=vec(0, 0, 0), amplitude=2, wavelength=20, omega=0.1, colour=color.yellow, z_axis=False):
        self._position = position
        self._amplitude = amplitude
        self._omega = omega
        self._wavelength = wavelength
        self._on_z_axis = z_axis
        self._arrows = []
        self._create_wave(colour)

    def _create_wave(self, colour):
        for x in range(-self._wavelength, self._wavelength):
            self._create_wave_arrow_at(x, colour)

    def _create_wave_arrow_at(self, x, colour):
        k = self.wave_number()
        value = sin(k * x) * self._amplitude
        axis = vec(0, 0, value) if self._on_z_axis else vec(0, value, 0)
        self._arrows += [arrow(pos=vec(k * x, 0, 0) + self._position, axis=axis, shaftwidth=0.075, nbw=0, color=colour)]

    def wave_number(self):
        return 2 * pi / self._wavelength

    def update(self, t):
        for arrow_ in self._arrows:
            length = sin(arrow_.pos.x - self._omega * t) * self._amplitude
            arrow_.axis = vec(0, 0, length) if self._on_z_axis else vec(0, length, 0)


class ElectromagneticWave:
    def __init__(self, position=vec(0, 0, 0), amplitude=3, color_scheme=0):
        self._color_scheme = color_scheme

        self._electric_field = Wave(position=position, colour=self.electric_field_color_for(False, 0), z_axis=False)
        self._magnetic_field = Wave(position=position, colour=self.magnetic_field_color_for(False, 0), z_axis=True)

    def electric_field_color_for(self, dim, color_scheme):
        colours = [color.orange, vec(.4, 0, .0), color.yellow, vec(0, 1, 0)]
        return colours[color_scheme + (1 if dim else 0)]

    def magnetic_field_color_for(self, dim, color_scheme):
        colours = [color.cyan, vec(0, 0, .4), color.magenta, vec(1, 0., 1.0)]
        return colours[color_scheme + (1 if dim else 0)]

    def update(self, t):
        self._electric_field.update(t)
        self._magnetic_field.update(t)

