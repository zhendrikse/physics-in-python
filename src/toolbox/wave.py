from vpython import vec, pi, arrow, color, sin

step_range = 20
omega = 0.1
wavelength = step_range
k = 2 * pi / wavelength


class Wave:
    def __init__(self, position=vec(0, 0, 0), amplitude=2, color=color, z_axis=False):

        self._amplitude = amplitude
        self._on_z_axis = z_axis
        self._arrows = []

        positions = []
        for x in range(-step_range, step_range):
            positions.append(k * x)

        for x in positions:
            value = sin(x) * amplitude
            axis = vec(0, 0, value) if self._on_z_axis else vec(0, value, 0)
            self._arrows += [
                arrow(pos=vec(x + position.x, position.y, position.z), axis=axis, shaftwidth=0.075, nbw=0, color=color)]

    def update(self, t):
        for arrow in self._arrows:
            ampere = sin(arrow.pos.x - omega * t) * self._amplitude
            arrow.axis = vec(0, 0, ampere) if self._on_z_axis else vec(0, ampere, 0)


class ElectromagneticWave:
    def __init__(self, position=vec(0, 0, 0), amplitude=3, color_scheme=0):
        self._color_scheme = color_scheme
        self._electric_field_colors = [color.orange, vec(.4, 0, .0), color.yellow, vec(0, 1, 0)]
        self._magnetic_field_colors = [color.cyan, vec(0, 0, .4), color.magenta, vec(1, 0., 1.0)]

        self._electric_field = Wave(position=position, color=self._electric_field_colors[0], z_axis=False)
        self._magnetic_field = Wave(position=position, color=self._magnetic_field_colors[0], z_axis=True)

    def update(self, t):
        self._electric_field.update(t)
        self._magnetic_field.update(t)
