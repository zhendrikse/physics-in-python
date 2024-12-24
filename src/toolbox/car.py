from vpython import vec, box, color, label, arrow


class Car:
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), colour=color.green, draw=True):
        self._position = position
        self._velocity = velocity
        self._car = box(pos=position, length=2.5, height=1, width=1, color=colour) if draw else None
        self._label = label(pos=vec(position.x, position.y + 1.52, position.z), text="Select my perspective",
                            color=colour, line=True) if draw else None
        self._x_axis = arrow(pos=position, axis=vec(2, 0, 0), color=color.magenta, shaftwidth=0.15) if draw else None
        self._x_axis_label = label(pos=vec(position.x + 2, position.y, position.z), text="x",
                                   color=colour) if draw else None
        self._y_axis = arrow(pos=position, axis=vec(0, 2, 0), color=color.magenta, shaftwidth=0.15) if draw else None
        self._y_axis_label = label(pos=vec(position.x, position.y + 2, position.z), text="y",
                                   color=colour) if draw else None
        self._z_axis = arrow(pos=position, axis=vec(0, 0, 2), color=color.magenta, shaftwidth=0.15) if draw else None
        self._z_axis_label = label(pos=vec(position.x, position.y, position.z + 2), text="z",
                                   color=colour) if draw else None

    def show_axis(self):
        self._x_axis.visible = True
        self._y_axis.visible = True
        self._z_axis.visible = True
        self._x_axis_label.visible = True
        self._y_axis_label.visible = True
        self._z_axis_label.visible = True

    def hide_axis(self):
        self._x_axis.visible = False
        self._y_axis.visible = False
        self._z_axis.visible = False
        self._x_axis_label.visible = False
        self._y_axis_label.visible = False
        self._z_axis_label.visible = False

    def show_label(self):
        self._label.visible = True

    def hide_label(self):
        self._label.visible = False

    def _draw(self):
        if self._label:
            self._car.pos = self._position
            self._label.pos = vec(self._position.x, self.position.y + 1.5, self._position.z)
            self._x_axis.pos = self._position
            self._x_axis_label.pos = vec(self._position.x + 2, self._position.y, self._position.z)
            self._y_axis.pos = self._position
            self._y_axis_label.pos = vec(self._position.x, self._position.y + 2, self._position.z)
            self._z_axis.pos = self._position
            self._z_axis_label.pos = vec(self._position.x, self._position.y, self._position.z + 2)

    def move(self, dt):
        self._position += self._velocity * dt
        self._draw()

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity
