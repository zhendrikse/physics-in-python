# Web VPython 3.2

from vpython import canvas, scene, arrow, color, vec, pi, floor, arange, cos, sin, rate, cylinder, box, label, checkbox, \
    wtext, slider, text

title = """Visualization of plane waves $\psi(x, t) = A \cdot e^{i(k x - \omega t)}$

&#x2022; From <a href="https://www.amazon.com/Visualizing-Quantum-Mechanics-Python-Spicklemire/dp/1032569247">Visualizing Quantum Mechanics with Python</a>
&#x2022; Modified by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>, located in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; The motion and x-axis represent the parameters $t$ and $x$ respectively
&#x2022; The colors represent the wave number $k$

"""

info_1 = "De Broglie: $ p = \dfrac{h}{\lambda} = \dfrac{h}{2\pi} \dfrac{2\pi}{\lambda} = \hbar k \Rightarrow \hbar k = \hbar \dfrac{\partial}{\partial x} \psi(x,t) = p \psi(x, t) \Rightarrow p = \hbar \dfrac{\partial}{\partial x} $"
info_2 = "Kinetic energy: $ K = \dfrac{p^2}{2m} = -\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2} \psi(x,t) $"
info_3 = "Energy: $ E = hf = \dfrac{h}{2\pi}\dfrac{2\pi}{T} = \hbar \omega \Rightarrow -i\hbar\dfrac{\partial}{\partial t} \psi(x,t) = E \psi(x,t) \Rightarrow E = -i\hbar\dfrac{\partial}{\partial t} $"
info_4 = "Schr&#246;dinger equation: $ E\Psi(x,t) = -i\hbar \dfrac{\partial}{\partial t}\Psi(x, t) = -\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2} \Psi(x,t) + V(x)\Psi(x,t) $"

animation = canvas(forward=vec(0.37, -0.55, -0.75), width=600, height=450, align='top', background=color.black,
                   title=title, range=11.5)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

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


class PlaneWave:
    def __init__(self, k=2 * pi / 5, omega=2 * pi, amplitude=3.):
        self._arrows = [arrow(pos=vec(x, 0, 0), axis=vec(0, amplitude, 0), color=color.red, shaftwidth=0.2) for x in
                        arange(-10, 10, 0.3)]
        self._amplitude = amplitude
        self._k = k
        self._omega = omega

    def set_k_to(self, value):
        self._k = value

    def set_omega_to(self, value):
        self._omega = value

    def set_amplitude_to(self, value):
        self._amplitude = value

    def update(self, t):
        for arrow_ in self._arrows:
            x = arrow_.pos.x
            k = self._k
            w = self._omega
            phase = k * x - w * t
            cycles = phase / (2 * pi)
            cycles -= floor(cycles)
            cphase = 2 * pi * cycles

            arrow_.axis.z = -cos(phase) * self._amplitude
            arrow_.axis.y = -sin(phase) * self._amplitude
            arrow_.color = color.hsv_to_rgb(vec(1.0 - cphase / (2 * pi), 1.0, 1.0))


animation.append_to_caption("\n")


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


def adjust_k():
    complex_function.set_k_to(k_slider.value)
    k_slider_text.text = str(round(k_slider.value / pi)) + " * π"


def adjust_amplitude():
    complex_function.set_amplitude_to(amplitude_slider.value)
    amplitude_slider_text.text = str(amplitude_slider.value) + " units"


def adjust_omega():
    complex_function.set_omega_to(omega_slider.value)
    omega_slider_text.text = str(round(omega_slider.value / pi, 2)) + " * π"


omega_slider = slider(min=0, max=6 * pi, value=2 * pi, bind=adjust_omega)
animation.append_to_caption(" Omega = ")
omega_slider_text = wtext(text="2 * π")
animation.append_to_caption("\n\n")

k_slider = slider(min=-2 * pi / 3, max=2 * pi / 3, value=2 * pi / 5, bind=adjust_k)
animation.append_to_caption(" Wave number k = ")
k_slider_text = wtext(text="2 * π  / 5")
animation.append_to_caption("\n\n")

amplitude_slider = slider(min=1, max=6, value=3, bind=adjust_amplitude)
animation.append_to_caption(" Amplitude = ")
amplitude_slider_text = wtext(text="3 units")
animation.append_to_caption("\n\n")

_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=True)
_ = checkbox(text='Tick labels', bind=toggle_tick_labels, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)

animation.append_to_caption("\n\n" + info_1 + "\n\n" + info_2 + "\n\n" + info_3 + "\n\n" + info_4)

axis = Base(length=16)
axis.hide_tick_labels()
axis.show_xz_mesh()
complex_function = PlaneWave()

dt = 0.01
t = 0
while True:
    rate(30)
    complex_function.update(t)
    t += dt