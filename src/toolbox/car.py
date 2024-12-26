from vpython import vec, box, color, label, arrow


class Car:
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), colour=color.green, draw=True):
        self._position = position
        self._velocity = velocity
        self._car = box(pos=position, length=2.5, height=1, width=1, color=colour) if draw else None
        self._label = label(pos=vec(position.x, position.y + 1.52, position.z), text="Select my perspective",
                            color=colour, line=True) if draw else None

    def show_label(self):
        self._label.visible = True

    def hide_label(self):
        self._label.visible = False

    def _draw(self):
        if self._label:
            self._car.pos = self._position
            self._label.pos = vec(self._position.x, self._position.y + 1.5, self._position.z)

    def move(self, dt):
        self._position += self._velocity * dt
        self._draw()

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity
