from vpython import vector, mag, norm, helix, color

zero_force = vector(0, 0, 0)


class Spring:
    def __init__(self,
                 position=vector(0, 0, 0),
                 axis=vector(1.0, 0, 0),
                 spring_constant=1,
                 equilibrium_size=None,
                 radius=0.5,
                 thickness=0.03,
                 coils=10,
                 colour = color.yellow,
                 draw=True):
        self._spring = self._vpython_helix(position, axis, spring_constant, radius, thickness, coils, colour) if draw else None
        self._position = position
        self._axis = axis
        self._spring_constant = spring_constant
        self._equilibrium_size = equilibrium_size if equilibrium_size else mag(axis)

    @staticmethod
    def _vpython_helix(position, axis, spring_constant, radius, thickness, coils, colour):
        spring = helix(pos=position,
                       axis=axis,
                       radius=radius,
                       thickness=thickness,
                       spring_constant=spring_constant,
                       color=colour,
                       coils=coils)

        return spring

    def _draw(self):
        if self._spring:
            self._spring.axis = self._axis
            self._spring.pos = self._position

    def update(self, axis, position=None):
        self._axis = axis
        self._position = position if position else self._position
        self._draw()

    def is_stretched_or_compressed(self):
        return abs(self.stretch) >= 0

    # https://en.wikipedia.org/wiki/Hooke%27s_law
    def _hookes_law(self):
        c = self._spring_constant
        u = self.stretch
        force = -c * u
        return force * norm(self._axis)

    @property
    def force(self):
        return self._hookes_law() if self.is_stretched_or_compressed() else zero_force

    @property
    def axis(self):
        return self._axis

    @property
    def position(self):
        return self._position

    @property
    def stretch(self):
        return mag(self._axis) - self._equilibrium_size
