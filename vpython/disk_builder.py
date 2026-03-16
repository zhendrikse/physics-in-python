#Web VPython 3.2

from vpython import scene, curve, color, vector, arrow, arange, ring, pi, vec, box, label, cylinder, text

title = """Add electric field of concentric rings to get E of disk on axis

&#x2022; Original <a href="https://lectdemo.github.io/virtual/15_E_disk_add_rings.html">15_E_disk_add_rings.py</a> by Ruth Chabay 2004
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; add charged rings one mouse click at a time

"""

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("x", "y", "z")


class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=20, num_tick_marks=None, axis_labels=label_text):
        self._position = position
        num_tick_marks = length - 1 if not num_tick_marks else num_tick_marks
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200

        self._axis, self._arrows, self._arrow_labels, self._tick_marks, self._tick_labels = [], [], [], [], []
        for base_vec in base:
            self._axis += [
                cylinder(pos=position - length * base_vec / 2, axis=length * base_vec, radius=radius, color=axis_color)]
            self._arrows += [
                arrow(pos=position + length * base_vec / 2, axis=base_vec, color=axis_color, shaftwidth=radius)]

        for i in range(len(base)):
            pos = position + base[i] * (length / 2 + tick_increment)
            self._arrow_labels.append(
                text(pos=pos, text=axis_labels[i], color=axis_color, height=radius * 10, align='center', billboard=True,
                     emissive=True))

        offset = [-0.05 * length * y_hat, 0.05 * length * x_hat, -0.05 * length * y_hat]
        positions = []
        for i in range(len(base)):
            for j in range(num_tick_marks):
                pos = position - base[i] * (length / 2 - j * tick_increment)
                positions.append(pos)
                label_value = pos.x - position.x if i == 0 else pos.y - position.y if i == 1 else pos.z - position.z
                label_value = "" if int(num_tick_marks / 2) == j else str(int(label_value))
                marker = label(pos=pos + offset[i], text=label_value, color=color.gray(0.5), box=False)
                self._tick_labels.append(marker)
                a_box = box(pos=pos, width=2 * radius, height=0.5, length=2 * radius, color=tick_marks_color)
                if i == 1:
                    a_box.rotate(angle=0.5 * pi, axis=vec(0, 0, 1))
                self._tick_marks.append(a_box)

        self._xy_mesh, self._zx_mesh, self._xz_mesh, self._yx_mesh = [], [], [], []
        for j in range(num_tick_marks):
            self._xy_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y + j * tick_increment - length / 2, position.z),
                         axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            self._yx_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y - length / 2, position.z),
                         axis=y_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            self._xz_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y, position.z - length / 2),
                         axis=z_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            self._zx_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y, position.z - length / 2 + j * tick_increment),
                         axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]

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


def toggle_background():
    animation.background = color.gray(0.075) if animation.background == color.white else color.white


def on_key_press(event):
    if event.key == " ":
        toggle_background()
    if event.key == 's':
        animation.capture("electric_field_of_charged_disk")


animation.title = title
animation.background = color.gray(0.075)
animation.forward = vector(-0.5, -0.60, -0.65)
animation.range = 8.0
# scene.autoscale = 0
##scene.caption = "\\(  \\)"
animation.bind('keydown', on_key_press)

axes = Base(length=10)
axes.show_xz_mesh()
axes.hide_tick_marks()
axes.hide_tick_labels()
observer_location = vector(0, 0, 0)
scale_factor = 1
electric_field_arrow = arrow(pos=observer_location, axis=vector(0, 0, 0), shaftwidth=0.3, color=color.orange)
for ring_radius in arange(0.2, 5, 0.2):
    animation.waitfor("click")
    ring(pos=vector(-3, 0, 0), radius=ring_radius, color=color.red, thickness=0.09)
    x = observer_location.x
    electric_field_magnitude = 2 * pi * ring_radius / (ring_radius * ring_radius + (x + 2) * (x + 2)) ** 1.5
    electric_field_arrow.axis += scale_factor * electric_field_magnitude * vector(1, 0, 0)
