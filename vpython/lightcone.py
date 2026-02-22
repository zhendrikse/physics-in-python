# Web VPython 3.2
from vpython import points, vec, pi, box, color, rate, cone, canvas, label, arrow, cylinder, text, checkbox, vector, \
    sphere

title = """&#x2022; Click mouse to pause animation
&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/relativity/code/lightcone.py">lightcone.py</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>

"""

animation = canvas(title=title, forward=vec(-0.25, -0.48, -0.83), range=14, background=color.gray(0.075))
sphere(pos=vector(0, 0, 0), texture="https://i.imgur.com/1nVWbbd.jpg", radius=25, shininess=0, opacity=0.5)

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("x", "y", "z")


class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=20,
                 num_tick_marks=None, axis_labels=label_text, tick_mark_labels=True, mesh=False):

        num_tick_marks = length - 1 if not num_tick_marks else num_tick_marks
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200
        self._tick_marks, self._axis, self._arrows, self._arrow_labels, self._tick_labels = [], [], [], [], []
        self._position = position

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
                marker = label(pos=pos + offset[i], text=label_value, color=color.gray(0.5), box=False,
                               visible=tick_mark_labels)
                self._tick_labels.append(marker)
                a_box = box(pos=pos, width=2 * radius, height=0.5, length=2 * radius, color=tick_marks_color)
                if i == 1:
                    a_box.rotate(angle=0.5 * pi, axis=vec(0, 0, 1))
                self._tick_marks.append(a_box)

        self._xy_mesh, self._zx_mesh, self._xz_mesh, self._yx_mesh = [], [], [], []
        for j in range(num_tick_marks):
            self._xy_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y + j * tick_increment - length / 2, position.z),
                         axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=mesh)]
            self._yx_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y - length / 2, position.z),
                         axis=y_hat * length, color=color.gray(.5), radius=radius / 2, visible=mesh)]
            self._xz_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y, position.z - length / 2),
                         axis=z_hat * length, color=color.gray(0.4), radius=radius / 2, visible=mesh)]
            self._zx_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y, position.z - length / 2 + j * tick_increment),
                         axis=x_hat * length, color=color.gray(0.4), radius=radius / 2, visible=mesh)]

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


axis = Base(mesh=True, axis_labels=["x", "ct", "y"], tick_mark_labels=False)
axis.hide_xy_mesh()

light_cone_top = cone(pos=vec(0, 0, 0), radius=0, opacity=0.4, axis=vec(0, -1, 0))
light_cone_bottom = cone(pos=vec(0, -10, 0), radius=10, opacity=0.4, axis=vec(0, 10, 0))
spaceship = text(text="Spaceship", color=color.cyan, visible=False, height=.75)
photon = text(text="Photon", color=color.yellow, visible=False, height=.75)

animation.append_to_caption("\n")


def toggle_tick_marks(event):
    axis.tick_marks_visible(event.checked)


def toggle_tick_labels(event):
    axis.tick_labels_visible(event.checked)


def toggle_xz_mesh(event):
    axis.xz_mesh_visible(event.checked)


def toggle_xy_mesh(event):
    axis.xy_mesh_visible(event.checked)


def toggle_background(event):
    animation.background = color.black if event.checked else color.white


def on_mouse_click():
    pause_animation()


dt = 1


def pause_animation():
    global dt
    dt += 1
    dt %= 2


_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=True)
_ = checkbox(text='Tick labels', bind=toggle_tick_labels, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text="Dark background", bind=toggle_background, checked=True)

animation.bind("click", on_mouse_click)

height = 0
while height <= 11:
    rate(10)
    light_cone_top.pos = vec(0, height, 0)
    light_cone_top.radius = height
    light_cone_top.axis = vec(0, -height, 0)

    height += dt / 5

t = 0
photon.visible = True
spaceship.visible = True
while t < 7:
    rate(5)

    # Update photon
    points(pos=[vec(t * 1.5, t * 1.5, 0)], radius=5, color=color.yellow)
    photon.pos = vec(t * 1.5 + 1, t * 1.5, 0)

    # Update spaceship
    points(pos=[vec(-t * .5, t * 1.5, 0)], radius=3, color=color.cyan)
    spaceship.pos = vec(-t * .3 - 5, t * 1.5, 0)

    t += dt / 5

while True:
    rate(100)
