Web
VPython
3.2

from vpython import canvas, box, vector, sphere, sin, cos, rate, pi, arrow, slider, wtext, cross, color, vec, cylinder, \
    text, label, box, checkbox, radians

title = """Helical motion of charged particle in magnetic field

&#x2022; Based on <a href="https://towardsdatascience.com/simple-physics-animations-using-vpython-1fce0284606">Simple Physics Animations Using VPython</a> by Zhiheng Jiang
&#x2022; Refactored and maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

animation = canvas(width=800, height=600, title=title, range=40, forward=vec(-0.381663, -0.605187, -0.698629))

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("x", "y", "z")


class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=20,
                 num_tick_marks=None, axis_labels=label_text):
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


xlen, ylen, zlen = 100, 100, 100
boundaries = [
    box(pos=vector(0, -ylen / 2, 0), size=vector(xlen, .2, zlen), visible=False),
    box(pos=vector(0, ylen / 2, 0), size=vector(xlen, .2, zlen), visible=False),
    box(pos=vector(-xlen / 2, 0, 0), size=vector(.2, ylen, zlen), visible=False),
    box(pos=vector(xlen / 2, 0, 0), size=vector(.2, ylen, zlen), visible=False),
    box(pos=vector(0, 0, -zlen / 2), size=vector(xlen, ylen, .2), visible=False)
]

dt = .001  # time step


class MagneticField:
    def __init__(self, strength=3):
        self._magnetic_field = vector(0, -strength, 0)

    def field(self):
        return self._magnetic_field

    def strength_is(self, field_strength):
        self._magnetic_field = vector(0, -field_strength, 0)


class Proton:
    def __init__(self, position=vector(0, -ylen / 2 + 1, 0), v_mag=20, theta=10, charge=0.8):
        self._v_mag = v_mag
        self._angle = radians(theta)
        self._velocity = v_mag * vector(cos(self._angle), sin(self._angle), 0)
        self._initial_velocity = self._velocity
        self._initial_position = position
        self._proton = sphere(pos=position, color=color.red, radius=1, make_trail=True, trail_type="curve")
        self._charge = charge

    def move(self, magn_field):  # moves proton by small step
        acceleration = self._charge * cross(self._velocity, magn_field)  # F = ma = q v x B
        self._velocity += acceleration * dt  # a = dv/dt
        self._proton.pos += self._velocity * dt  # v = dx/dt

    def reset_proton(self):  # resets proton position and path
        self._proton.pos = self._initial_position
        self._velocity = self._initial_velocity
        self._proton.clear_trail()

    def charge_is(self, new_charge):
        self._charge = new_charge

    def angle_is(self, new_angle):
        self._angle = new_angle
        self._velocity = self._v_mag * vector(cos(self._angle), sin(self._angle), 0)

    def check_collision(self):  # checks for boundaries
        return ylen / 2 > self._proton.pos.y > -ylen / 2 and xlen / 2 > self._proton.pos.x > -xlen / 2 and -zlen / 2 < self._proton.pos.z < zlen / 2


def toggle_tick_marks(event):
    axis.tick_marks_visible(event.checked)


def toggle_tick_labels(event):
    axis.tick_labels_visible(event.checked)


def toggle_xz_mesh(event):
    axis.xz_mesh_visible(event.checked)


def toggle_xy_mesh(event):
    axis.xy_mesh_visible(event.checked)


def toggle_axis(event):
    axis.axis_visible(event.checked)


def toggle_box(event):
    for boundary in boundaries:
        boundary.visible = event.checked


axis = Base(length=int(xlen / 2.), num_tick_marks=20)
axis.hide_tick_labels()
axis.show_xz_mesh()

_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=True)
_ = checkbox(text='Tick labels', bind=toggle_tick_labels, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)
_ = checkbox(text="Show box", bind=toggle_box, checked=False)

pop_up = label(pos=vec(0, 32, 0), text="Click mouse button to start", visible=True, box=False)
proton = Proton()
magnetic_field = MagneticField()


def launch():
    pop_up.visible = False
    proton.reset_proton()
    while proton.check_collision():
        rate(1 / dt)
        proton.move(magnetic_field.field())
    pop_up.visible = True


animation.bind("click", launch)


def adjust_bfield():
    magnetic_field.strength_is(b_field_slider.value)
    b_field_text.text = str(b_field_slider.value) + " Tesla"


animation.append_to_caption("\n")
b_field_slider = slider(min=1, max=10, step=.5, value=5, bind=adjust_bfield)
animation.append_to_caption(" B-field Strength = ")
b_field_text = wtext(text="3 Tesla")
animation.append_to_caption("\n\n")


def adjust_q():
    proton.charge_is(charge_slide.value)
    charge_text.text = str(charge_slide.value) + " Coulumbs"


charge_slide = slider(min=0, max=1, step=.1, value=.8, bind=adjust_q)
animation.append_to_caption(" Q = ")
charge_text = wtext(text="0.8 Coulumbs")
animation.append_to_caption("\n\n")


def adjust_angle():
    proton.angle_is(radians(angle_slider.value))
    angle_text.text = str(angle_slider.value) + " degrees"


angle_slider = slider(min=0, max=90, step=1, value=10, bind=adjust_angle)
animation.append_to_caption(" Angle = ")
angle_text = wtext(text="10 degrees")

while True:
    rate(10)
