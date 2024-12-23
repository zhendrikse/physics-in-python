from vpython import vec, box, color, label, arrow

class Car:
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), colour=color.green, draw=True):
        self._position = position
        self._velocity = velocity
        self._car = box(pos=position, length=1.5, height=1, width=1, color=colour) if draw else None
        self._label = label(pos=vec(position.x,position.y + 1, position.z), text="From my perspective", color=colour, line=True) if draw else None
        self._x_axis = arrow(pos=position, axis=vec(2, 0, 0), color=color.cyan, shaftwidth=0.15)
        self._y_axis = arrow(pos=position, axis=vec(0, 2, 0), color=color.cyan, shaftwidth=0.15)
        self._z_axis = arrow(pos=position, axis=vec(0, 0, 2), color=color.cyan, shaftwidth=0.15)

    def _draw(self):
        if self._label:
            self._car.pos = self._position
            self._label.pos = vec(self._position.x, self.position.y + 1, self._position.z)
            self._x_axis.pos = self._position
            self._y_axis.pos = self._position
            self._z_axis.pos = self._position

    def move(self, dt):
        self._position += self._velocity * dt
        self._draw()

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity