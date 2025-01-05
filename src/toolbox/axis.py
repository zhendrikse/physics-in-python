from vpython import vector, vec, cylinder, arrow, box, label, color, pi, text

from ..toolbox.ball import Ball

x_hat = vector(1, 0, 0)
y_hat = vector(0, 1, 0)
z_hat = vector(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("x", "y", "z")


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
            self._arrow_labels.append(
                label(pos=position + base[i] * scale, text=label_text[i], color=base_color, box=False))

    def reorient_with(self, other_object):
        other_objects_position = other_object.position()
        shift = other_objects_position - self._position
        self._position = other_objects_position

        for i in range(len(self._arrows)):
            self._arrows[i].pos += shift
            self._arrow_labels[i].pos += shift


class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=20,
                 num_tick_marks=None, axis_labels=label_text):
        num_tick_marks = length - 1 if not num_tick_marks else num_tick_marks
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200

        self._position = position
        self._xy_mesh, self._zx_mesh, self._xz_mesh, self._yx_mesh, self._axis, self._arrows, self._arrow_labels, self._tick_marks, self._tick_labels = [], [], [], [], [], [], [], [], []
        self._create_axis(position, tick_increment, length, radius, axis_labels, axis_color, tick_marks_color)
        self._create_tick_marks_and_labels(position, num_tick_marks, tick_increment, length, radius, tick_marks_color)
        self._create_mesh(position, num_tick_marks, tick_increment, length, radius)

    def _create_axis(self, position, tick_increment, length, radius, axis_labels, axis_color, tick_marks_color):
        for base_vec in base:
            pos = position - length * base_vec / 2
            self._axis += [cylinder(pos=pos, axis=length * base_vec, radius=radius, color=axis_color)]
            self._arrows += [arrow(pos=pos, axis=base_vec, color=axis_color, shaftwidth=radius)]

        for i in range(len(base)):
            pos = position + base[i] * (length / 2 + tick_increment)
            self._arrow_labels.append(label(pos=pos, text=axis_labels[i], color=tick_marks_color, box=False))

    def _create_tick_marks_and_labels(self, position, num_tick_marks, tick_increment, length, radius, colour):
        offset = [-0.05 * length * y_hat, 0.05 * length * x_hat, -0.05 * length * y_hat]
        for i in range(len(base)):
            for j in range(num_tick_marks):
                pos = position - base[i] * (length / 2 - j * tick_increment)
                label_value = pos.x - position.x if i == 0 else pos.y - position.y if i == 1 else pos.z - position.z
                label_value = "" if int(num_tick_marks / 2) == j else str(int(label_value))
                marker = label(pos=pos + offset[i], text=label_value, color=color.gray(0.5), height=radius * 100, box=False)
                self._tick_labels.append(marker)
                a_box = box(pos=pos, width=2 * radius, height=0.5, length=2 * radius, color=colour)
                if i == 1:
                    a_box.rotate(angle=0.5 * pi, axis=vec(0, 0, 1))
                self._tick_marks.append(a_box)

    def _create_mesh(self, position, num_tick_marks, tick_increment, length, radius):
        for j in range(num_tick_marks):
            pos = vec(position.x - length / 2, position.y + j * tick_increment - length / 2, position.z)
            self._xy_mesh += [
                cylinder(pos=pos, axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            pos = vec(position.x - length / 2 + j * tick_increment, position.y - length / 2, position.z)
            self._yx_mesh += [
                cylinder(pos=pos, axis=y_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            pos = vec(position.x - length / 2 + j * tick_increment, position.y, position.z - length / 2)
            self._xz_mesh += [
                cylinder(pos=pos, axis=z_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            pos = vec(position.x - length / 2, position.y, position.z - length / 2 + j * tick_increment)
            self._zx_mesh += [
                cylinder(pos=pos, axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]

    def show_axis(self):
        self.axis_visible(True)

    def hide_axis(self):
        self.axis_visible(False)

    def show_tick_labels(self):
        self.tick_labels_visible(True)

    def hide_tick_labels(self):
        self.tick_labels_visible(False)

    def show_tick_marks(self):
        self.tick_marks_visible(True)

    def hide_tick_marks(self):
        self.tick_marks_visible(False)

    def axis_visible(self, visible):
        for i in range(len(base)):
            self._arrow_labels[i].visible = visible
            self._arrows[i].visible = visible
            self._axis[i].visible = visible
        self.tick_labels_visible(visible)
        self.tick_marks_visible(visible)

    def tick_labels_visible(self, visible):
        for a_label in self._tick_labels:
            a_label.visible = visible

    def tick_marks_visible(self, visible):
        for tick_mark in self._tick_marks:
            tick_mark.visible = visible

    def xy_mesh_visible(self, visible):
        for i in range(len(self._xy_mesh)):
            self._xy_mesh[i].visible = visible
            self._yx_mesh[i].visible = visible

    def xz_mesh_visible(self, visible):
        for i in range(len(self._xz_mesh)):
            self._xz_mesh[i].visible = visible
            self._zx_mesh[i].visible = visible

    def show_xy_mesh(self):
        self.xy_mesh_visible(True)

    def hide_xy_mesh(self):
        self.xy_mesh_visible(False)

    def show_xz_mesh(self):
        self.xz_mesh_visible(True)

    def hide_xz_mesh(self):
        self.xz_mesh_visible(False)

    def reorient(self, new_position):
        shift = new_position - self._position
        self._position = new_position

        for i in range(len(self._axis)):
            self._axis[i].pos += shift
            self._arrows[i].pos += shift
            self._arrow_labels[i].pos += shift

        for i in range(len(self._tick_labels)):
            self._tick_labels[i].pos += shift
            self._tick_marks[i].pos += shift

        for i in range(len(self._xy_mesh)):
            self._xy_mesh[i].pos += shift
            self._yx_mesh[i].pos += shift

        for i in range(len(self._xz_mesh)):
            self._xz_mesh[i].pos += shift
            self._zx_mesh[i].pos += shift

    @property
    def position(self):
        return self._position
