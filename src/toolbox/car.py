from vpython import vec, box, color, cylinder, compound, color

from ..toolbox.moveable import Moveable

class Car(Moveable):
    def __init__(self, pos=vec(0, 0, 0), velocity=vec(0, 0, 0), mass=1.0, scale=1.0, colour=color.green, render=True):
        Moveable.__init__(self, pos=pos, velocity=velocity, mass=mass)

        self._car = self._vpython_car(scale, colour) if render else None
        self.move_to(pos)

    @staticmethod
    def _vpython_car(scale, colour):
        parts = []
        parts += [box(pos=vec(0, 0, 0), width=7 * scale, height=3.5 * scale, length=18 * scale, color=colour)]
        parts += [box(pos=vec(1.5, 3.0, 0) * scale, width=7 * scale, height=3 * scale, length=9 * scale, color=colour)]
        parts += [cylinder(pos=vec(-6.5, -2, -3.75) * scale, radius=1.75 * scale, axis=vec(0, 0, 1) * scale,
                           color=color.yellow)]
        parts += [cylinder(pos=vec(-6.5, -2, +2.75) * scale, radius=1.75 * scale, axis=vec(0, 0, 1) * scale,
                           color=color.yellow)]
        parts += [cylinder(pos=vec(+7, -2, -3.75) * scale, radius=1.75 * scale, axis=vec(0, 0, 1) * scale,
                           color=color.yellow)]
        parts += [cylinder(pos=vec(+7, -2, +2.75) * scale, radius=1.75 * scale, axis=vec(0, 0, 1) * scale,
                           color=color.yellow)]
        return compound(parts)

    def render(self):
        if self._car:
            self._car.pos = self._position
