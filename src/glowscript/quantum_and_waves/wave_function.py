# Web VPython 3.2

title = """Visualization of free particle wave functions

&#x2022; From <a href="https://www.amazon.com/Visualizing-Quantum-Mechanics-Python-Spicklemire/dp/1032569247">Visualizing Quantum Mechanics with Python</a>
&#x2022; Modified by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>, located in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; The motion and x-axis represent the parameters t and x respectively

"""

animation = canvas(width=800, height=600, align='top', title=title, range=9, forward=vec(0.39581, -0.452886, -0.798892))

# For complex numbers
get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")


def linspace(start, end, total):
    return arange(start, end, (end - start) / total)


x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("X", "Re(ψ)", "Im(ψ)")


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
                text(pos=pos, text=axis_labels[i], color=axis_color, height=radius * 5, align='center', billboard=True,
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


class Wave:
    def __init__(self, psi, L=20, N=40):
        self._x = linspace(-L / 2, L / 2, N)
        self._arrows = []
        self._psi = psi
        for xval in self._x:
            a = arrow(pos=vec(xval, 0, 0), axis=vec(0, 1, 0), color=color.red)
            self._arrows.append(a)

    def update_for(self, t):
        psi_array = []
        for xval in self._x:
            psi_array.append(self._psi.value_at(xval, t))

        for i in range(len(psi_array)):
            self._arrows[i].axis = vec(0, psi_array[i].re, psi_array[i].im)


class PsiFreeParticle:
    def __init__(self, k, omega):
        self._k = k
        self._omega = omega

    def value_at(self, x, t):
        k = self._k
        omega = self._omega
        return math.complex(cos(k * x - omega * t), sin(k * x - omega * t))


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


animation.append_to_caption("\n")
_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=False)
_ = checkbox(text='Tick labels', bind=toggle_tick_labels, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=False)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)

axis = Base(length=10)
axis.hide_tick_labels()
axis.hide_tick_marks()

T = 0.5
omega = 2 * pi / T
k = 1  # particle is stationary, so k=0

t = 0
dt = 0.02
psi = PsiFreeParticle(k, omega)
wave = Wave(psi)

while t < 5:  # simulate for 5 seconds
    rate(1 / dt)
    wave.update_for(t)
    t += dt

