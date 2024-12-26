from vpython import vector, vec, cylinder, arrow, points, label, curve, color, box, pyramid, sphere
from dataclasses import dataclass


def obj_size(obj):
    if type(obj) == Ball:
        return vector(obj._ball.radius, obj._ball.radius, obj._ball.radius)
    else:
        raise TypeError("Implement the obj_size() function in the axis module for type " + str(type(obj)))


@dataclass
class Interval:
    start: vector
    end: vector

    def distance(self):
        return self.end - self.start


class Axis:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, num_tick_marks=10,
                 length=10, orientation="x", label_orientation="down", offset=0):
        self._axis = vec(1, 0, 0) if orientation == "x" else vec(0, 1, 0)
        self._num_tick_marks = num_tick_marks
        self._length = length
        self._offset = offset
        self._label_shifts = {
            "up": vector(0, -0.05 * self._length, 0),
            "down": vector(0, 0.05 * self._length, 0),
            "left": vector(-0.1 * self._length, 0, 0),
            "right": vector(0.1 * self._length, 0, 0)}

        self._axis_interval = Interval(-self._axis * length / 2 + position, self._axis * length / 2 + position)

        self._label_shift = vector(0, -0.05 * self._length, 0)
        if label_orientation == "up":
            self._label_shift = vector(0, 0.05 * self._length, 0)
        elif label_orientation == "left":
            self._label_shift = vector(-0.1 * self._length, 0, 0)
        elif label_orientation == "right":
            self._label_shift = vector(0.1 * self._length, 0, 0)

        tick_positions = []
        self._tick_labels = []
        tick_increment = self._axis_interval.distance() / (self._num_tick_marks - 1)
        for i in range(num_tick_marks):
            tick_position = self._axis_interval.start + i * tick_increment
            tick_positions += [tick_position]
            label_value = offset + tick_position.x if orientation == "x" else tick_position.y
            label_text = str(round(label_value, 2))
            self._tick_labels += [label(pos=tick_position + self._label_shift, text=label_text, box=False)]

        self._ticks = points(pos=tick_positions, radius=10, color=tick_marks_color)
        self._cylinder = cylinder(pos=self._axis_interval.start, axis=self._axis_interval.distance(),
                                  radius=self._ticks.radius / 100, color=axis_color)

        self._x_axis = arrow(pos=position, axis=vec(2, 0, 0), color=axis_color, shaftwidth=0.15)
        self._y_axis = arrow(pos=position, axis=vec(0, 2, 0), color=axis_color, shaftwidth=0.15)
        self._z_axis = arrow(pos=position, axis=vec(0, 0, 2), color=axis_color, shaftwidth=0.15)
        self._x_axis_label = label(pos=vec(2, 0, 0), text="x", box=False, color=tick_marks_color)
        self._y_axis_label = label(pos=vec(0, 2, 0), text="y", box=False, color=tick_marks_color)
        self._z_axis_label = label(pos=vec(0, 0, 2), text="z", box=False, color=tick_marks_color)

    def reorient_with(self, other_object):
        other_objects_position = other_object.position
        start = -self._axis * self._length / 2 + other_objects_position
        end = self._axis * self._length / 2 + other_objects_position
        self._axis_interval = Interval(start, end)
        tick_increment = self._axis_interval.distance() / (self._num_tick_marks - 1)
        for i in range(self._num_tick_marks):
            tick_position = self._axis_interval.start + i * tick_increment
            self._ticks.modify(i, pos=tick_position)
            self._tick_labels[i].pos = tick_position + self._label_shift

        self._cylinder.pos = self._axis_interval.start
        self._x_axis.pos = other_objects_position
        self._y_axis.pos = other_objects_position
        self._z_axis.pos = other_objects_position
        self._x_axis_label.pos = other_objects_position + vec(2, 0, 0)
        self._y_axis_label.pos = other_objects_position + vec(0, 2, 0)
        self._z_axis_label.pos = other_objects_position + vec(0, 0, 2)

    def show_unit_vectors(self):
        self._x_axis.visible = True
        self._y_axis.visible = True
        self._z_axis.visible = True
        self._x_axis_label.visible = True
        self._y_axis_label.visible = True
        self._z_axis_label.visible = True

    def hide_unit_vectors(self):
        self._x_axis.visible = False
        self._y_axis.visible = False
        self._z_axis.visible = False
        self._x_axis_label.visible = False
        self._y_axis_label.visible = False
        self._z_axis_label.visible = False
