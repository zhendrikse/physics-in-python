from vpython import vector, vec, cylinder, arrow, points, label, radians, color
from ..toolbox.ball import Ball

x_hat = vector(1, 0, 0)
y_hat = vector(0, 1, 0)
z_hat = vector(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ["x", "y", "z"]

def obj_size(obj):
    if type(obj) == Ball:
        return vector(obj.radius, obj.radius, obj.radius)
    else:
        raise TypeError("Implement the obj_size() function in the axis module for type " + str(type(obj)))

class UnitVectors:
    def __init__(self, position=vec(0, 0, 0), base_color=color.yellow, scale=1):
        self._arrows = []
        self._arrow_labels = []
        self._position = position
        for i in range(len(base)):
            self._arrows += [arrow(pos=position, axis=base[i] * scale, color=base_color)]
            self._arrow_labels.append(label(pos=position + base[i] * scale, text=label_text[i], color=base_color, box=False))

    def reorient_with(self, other_object):
        other_objects_position = other_object.position
        shift = other_objects_position - self._position
        self._position = other_objects_position

        for i in range(len(self._arrows)):
            self._arrows[i].pos += shift
            self._arrow_labels[i].pos += shift


class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=10):

        num_tick_marks = 9
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200
        self._axis = []
        self._arrows = []
        self._arrow_labels = []
        self._tick_labels = []
        self._position = position

        for base_vec in base:
            self._axis += [cylinder(pos=position - length * base_vec / 2, axis=length * base_vec, radius=radius, color=axis_color)]
            self._arrows += [arrow(pos=position + length * base_vec / 2, axis=base_vec, color=axis_color, shaftwidth=radius)]

        for i in range(len(base)):
            self._arrow_labels.append(label(pos=position + base[i] * (length / 2 + tick_increment), text=label_text[i], color=tick_marks_color, box=False))

        offset = [-0.05 * length * y_hat, 0.05 * length * x_hat, -0.05 * length * y_hat]
        positions = []
        for i in range(len(base)):
            for j in range(num_tick_marks):
                pos = position - base[i] * (length  / 2 - j * tick_increment)
                positions.append(pos)
                label_value = pos.x - position.x if i == 0 else pos.y - position.y if i == 1 else pos.z - position.z
                label_value = "" if int(num_tick_marks / 2) == j else str(int(label_value))
                marker = label(pos=pos + offset[i], text=label_value, color=color.gray(0.5), box=False)
                self._tick_labels.append(marker)
        self._tick_marks = points(pos=positions, color=tick_marks_color, radius=radius * 100)


    def reorient_with(self, other_object):
        other_objects_position = other_object.position
        shift = other_objects_position - self._position
        self._position = other_objects_position

        for i in range(len(self._axis)):
            self._axis[i].pos += shift
            self._arrows[i].pos += shift
            self._arrow_labels[i].pos += shift

        for i in range(len(self._tick_labels)):
            self._tick_labels[i].pos += shift
            self._tick_marks.modify(i, pos=self._tick_marks.point(i)["pos"] + shift)

