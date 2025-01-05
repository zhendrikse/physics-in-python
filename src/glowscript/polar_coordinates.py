#Web VPython 3.2

title = """Frequently used objects

&#x2022; Created by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> 
&#x2022; Maintained in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

from vpython import sphere, vec, arrow, color, sin, cos, ring, curve, cross, label, canvas, text, cylinder, norm, slider, radians, rate, checkbox, pi, box

animation = canvas(forward=vec(0.37, -0.55, -0.75), range=8., title=title)

theta = 45
phi = 45
radius = 4

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
            self._arrow_labels.append(label(pos=position + base[i] * (length / 2 + tick_increment), text=axis_labels[i],
                                            color=tick_marks_color, box=False))

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


def to_cartesian(r_, phi_, theta_):
    return vec(r_ * sin(radians(theta_)) * cos(radians(phi_)), r_ * sin(radians(theta_)) * sin(radians(phi_)), r_ * cos(radians(theta_)))

axis = Base(length=10)
axis.hide_tick_labels()
axis.show_xz_mesh()

dome = sphere(radius=radius, opacity=0.5, color=color.orange)
intersection = ring(radius=radius, color=color.gray(0.5), axis=y_hat, thickness=1/(radius * 5))

point_on_sphere = to_cartesian(radius, phi, theta)
radial_arrow = arrow(pos=point_on_sphere, axis=norm(point_on_sphere), color=color.green)
radial_axis = curve(pos=[vec(0, 0, 0), point_on_sphere], color=color.green)
theta_arrow = arrow(pos=point_on_sphere, axis=norm(point_on_sphere - y_hat * radius), color=color.red)
phi_arrow = arrow(pos=point_on_sphere, axis=cross(theta_arrow.axis, radial_arrow.axis), color=color.cyan)
radial_label = text(pos=to_cartesian(radius * .5, phi, theta), text="r", height=radius / 5, color=color.green)

def set_tangent_vectors():
    theta_arrow.axis = norm(to_cartesian(radius, phi, theta) - y_hat * radius)
    theta_arrow.pos = to_cartesian(radius, phi, theta)
    radial_arrow.axis = norm(to_cartesian(radius, phi, theta))
    radial_arrow.pos = to_cartesian(radius, phi, theta)
    radial_axis.modify(1, pos=to_cartesian(radius, phi, theta))
    phi_arrow.pos = to_cartesian(radius, phi, theta)
    phi_arrow.axis = cross(theta_arrow.axis, radial_arrow.axis)
    radial_label.pos=to_cartesian(radius * .5, phi, theta)

def set_phi():
    global phi
    phi = phi_slider.value
    set_tangent_vectors()

def set_theta():
    global theta
    theta = theta_slider.value
    set_tangent_vectors()

animation.append_to_caption("\nAdjust theta using the slider\n")
theta_slider = slider(bind = set_theta, value = theta, min = 0, max = 360)
animation.append_to_caption("\nAdjust phi using the slider\n")
phi_slider = slider(bind = set_phi, value = phi, min = 0, max = 360)


animation.append_to_caption("\n\n")

show_tick_marks = True
def toggle_tick_marks(btn):
    nonlocal show_tick_marks, axis
    show_tick_marks = not show_tick_marks
    axis.tick_marks_visible(show_tick_marks)

show_tick_labels = False
def toggle_tick_labels(btn):
    nonlocal show_tick_labels, axis
    show_tick_labels = not show_tick_labels
    axis.tick_labels_visible(show_tick_labels)

show_xz_mesh = True
def toggle_xz_mesh(btn):
    nonlocal show_xz_mesh, axis
    show_xz_mesh = not show_xz_mesh
    axis.xz_mesh_visible(show_xz_mesh)

show_xy_mesh = False
def toggle_xy_mesh(btn):
    nonlocal show_xy_mesh, axis
    show_xy_mesh = not show_xy_mesh
    axis.xy_mesh_visible(show_xy_mesh)

tick_marks_button = checkbox(text = 'Tick marks', bind = toggle_tick_marks, checked=True)
tick_labels_button = checkbox(text = 'Tick labels', bind = toggle_tick_labels, checked=False)
show_xz_button = checkbox(text = 'XZ mesh', bind = toggle_xz_mesh, checked=True)
show_xy_button = checkbox(text = 'XY mesh', bind = toggle_xy_mesh, checked=False)

while True:
    rate(60)