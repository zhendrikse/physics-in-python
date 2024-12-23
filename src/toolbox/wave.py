from vpython import vec, pi, arrow, color, sin

class Wave:
    def __init__(self, position=vec(0, 0, 0), amplitude=2, wavelength=20, omega=0.1, color=color, z_axis=False):

        self._amplitude = amplitude
        self._omega = omega
        self._wavelength = wavelength
        self._on_z_axis = z_axis
        self._arrows = []

        for x in range(-wavelength, wavelength):
            k = self.wave_number()
            value = sin(k * x) * amplitude
            axis = vec(0, 0, value) if self._on_z_axis else vec(0, value, 0)
            self._arrows += [
                arrow(pos=vec(k * x + position.x, position.y, position.z), axis=axis, shaftwidth=0.075, nbw=0,
                      color=color)]

    def wave_number(self):
        return 2 * pi / self._wavelength

    def update(self, t):
        for arrow in self._arrows:
            length = sin(arrow.pos.x - self._omega * t) * self._amplitude
            arrow.axis = vec(0, 0, length) if self._on_z_axis else vec(0, length, 0)


class ElectromagneticWave:
    def __init__(self, position=vec(0, 0, 0), amplitude=3, color_scheme=0):
        self._color_scheme = color_scheme

        self._electric_field = Wave(position=position, color=self.electric_field_color_for(False, 0), z_axis=False)
        self._magnetic_field = Wave(position=position, color=self.magnetic_field_color_for(False, 0), z_axis=True)

    def electric_field_color_for(self, dim, color_scheme):
        colours = [color.orange, vec(.4, 0, .0), color.yellow, vec(0, 1, 0)]
        return colours[color_scheme + (1 if dim else 0)]

    def magnetic_field_color_for(self, dim, color_scheme):
        colours = [color.cyan, vec(0, 0, .4), color.magenta, vec(1, 0., 1.0)]
        return colours[color_scheme + (1 if dim else 0)]

    def update(self, t):
        self._electric_field.update(t)
        self._magnetic_field.update(t)

