#Web VPython 3.2

from vpython import canvas, scene, arrow, color, vec, pi, floor, arange, cos, sin, rate, cylinder, box, label, checkbox, \
    wtext, slider, text, get_library

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')

title = """&#x2022; From <a href="https://www.amazon.com/Visualizing-Quantum-Mechanics-Python-Spicklemire/dp/1032569247">Visualizing Quantum Mechanics with Python</a>
&#x2022; Modified by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/quantumphysics/code/plane_wave.py">plane_wave.py</a>
&#x2022; The motion and x-axis represent the parameters $t$ and $x$ respectively
&#x2022; The colors represent the wave number $k$

"""

info = """
    <b>Concise derivation of the Schr&#246;dinger equation</b>

    According to <a href="https://en.wikipedia.org/wiki/Matter_wave">De Broglie</a> we have:

    $p = \dfrac{h}{\lambda} = \dfrac{h}{2\pi} \dfrac{2\pi}{\lambda} = \hbar k \Rightarrow \hbar k = \hbar \dfrac{\partial}{\partial x} \psi(x,t) = p \psi(x, t) \Rightarrow p = \hbar \dfrac{\partial}{\partial x}$

    The Kinetic energy can be expressed as:

    $K = \dfrac{p^2}{2m} = -\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2} \psi(x,t)$

    The total energy is given by the <a href="https://en.wikipedia.org/wiki/Planck_relation">Planck-Einstein relation</a>:

    $E = hf = \dfrac{h}{2\pi}\dfrac{2\pi}{T} = \hbar \omega \Rightarrow -i\hbar\dfrac{\partial}{\partial t} \psi(x,t) = E \psi(x,t) \Rightarrow E = -i\hbar\dfrac{\partial}{\partial t}$

    From this we arrive at the <a href="https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation">Schr&#246;dinger equation</a>:

    $(KE + PE)\Psi(x,,t) = E\Psi(x,t) = -i\hbar \dfrac{\partial}{\partial t}\Psi(x, t) = -\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2} \Psi(x,t) + V(x)\Psi(x,t)$
"""

animation = canvas(align="top", forward=vec(0.37, -0.55, -0.75), background=color.gray(0.075), title=title, range=11.5)


class Numpy:
    def __init__(self):
        self.array = self._array
        self.linspace = self._linspace
        self.len = self._len

    def _array(self, an_array):
        return nj.array(an_array)

    def _linspace(self, start, stop, num):
        return self._array([x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop])

    def _len(self, numpy_array): return numpy_array.shape[0]


np = Numpy()

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
label_text = ("X", "Re(ψ)", "Im(ψ)")


class Space:
    def __init__(self, linspace_x, linspace_y, linspace_z):
        self.linspace_x = linspace_x
        self.linspace_y = linspace_y
        self.linspace_z = linspace_z


class Base:
    def __init__(self, space, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red,
                 axis_labels=label_text):
        x_ = space.linspace_x
        y_ = space.linspace_y
        z_ = space.linspace_z
        scale = .005 * (x_.get(-1) - x_.get(0))
        delta_x = x_.get(1) - x_.get(0)
        delta_y = y_.get(1) - y_.get(0)
        delta_z = z_.get(1) - z_.get(0)
        range_x = x_.get(-1) - x_.get(0)
        range_y = y_.get(-1) - y_.get(0)
        range_z = z_.get(-1) - z_.get(0)
        self._axis = self._make_axis(x_, y_, z_, delta_x, delta_y, delta_z, axis_color, axis_labels, scale)
        self._tick_marks = self._make_tick_marks(x_, y_, z_, tick_marks_color, scale)

        self._xy_mesh, self._xz_mesh, self._yz_mesh = [], [], []
        for j in range(np.len(x_)):
            pos_x_y = x_hat * x_.get(0) + y_hat * y_.get(0)
            pos_x_z = x_hat * x_.get(0) + z_hat * z_.get(0)
            pos_y_z = y_hat * y_.get(0) + z_hat * z_.get(0)
            self._xy_mesh += [
                cylinder(pos=position + pos_x_y + x_hat * j * delta_x, axis=y_hat * range_y, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            self._xy_mesh += [
                cylinder(pos=position + pos_x_y + y_hat * j * delta_y, axis=x_hat * range_x, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            pos = position + (x_.get(0) + .5 * range_x) * x_hat + (y_.get(0) + .5 * range_y) * y_hat
            self._xy_mesh += [box(pos=pos, length=range_x, width=scale, height=range_y, opacity=0.15, visible=False)]
            self._xz_mesh += [
                cylinder(pos=position + pos_x_z + x_hat * j * delta_x, axis=z_hat * range_z, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            self._xz_mesh += [
                cylinder(pos=position + pos_x_z + z_hat * j * delta_z, axis=x_hat * range_x, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            pos = position + (x_.get(0) + .5 * range_x) * x_hat + (z_.get(0) + .5 * range_z) * z_hat
            self._xz_mesh += [box(pos=pos, length=range_x, width=range_z, height=scale, opacity=0.15, visible=False)]
            self._yz_mesh += [
                cylinder(pos=position + pos_y_z + y_hat * j * delta_y, axis=z_hat * range_z, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            self._yz_mesh += [
                cylinder(pos=position + pos_y_z + z_hat * j * delta_z, axis=y_hat * range_y, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            pos = position + (y_.get(0) + .5 * range_y) * y_hat + (z_.get(0) + .5 * range_z) * z_hat
            self._yz_mesh += [box(pos=pos, length=scale, width=range_z, height=range_y, opacity=0.15, visible=False)]

    def _make_axis(self, x_, y_, z_, delta_x, delta_y, delta_z, axis_color, axis_labels, scale):
        c1 = cylinder(pos=x_hat * x_.get(0), axis=x_hat * (x_.get(-1) - x_.get(0)), color=axis_color, radius=scale)
        c2 = cylinder(pos=y_hat * y_.get(0), axis=y_hat * (y_.get(-1) - y_.get(0)), color=axis_color, radius=scale)
        c3 = cylinder(pos=z_hat * z_.get(0), axis=z_hat * (z_.get(-1) - z_.get(0)), color=axis_color, radius=scale)
        a1 = arrow(pos=x_hat * x_.get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_x * x_hat, round=True)
        a2 = arrow(pos=y_hat * y_.get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_y * y_hat, round=True)
        a3 = arrow(pos=z_hat * z_.get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_z * z_hat, round=True)
        l1 = text(pos=x_hat * (x_.get(-1) + 2 * delta_x) - vec(0, scale, 0), text=axis_labels[0],
                  color=axis_color, height=scale * 7, billboard=True, emissive=True)
        l2 = text(pos=y_hat * (y_.get(-1) + 2 * delta_y) - vec(0, scale, 0), text=axis_labels[1],
                  color=axis_color, height=scale * 7, billboard=True, emissive=True)
        l3 = text(pos=z_hat * (z_.get(-1) + 2 * delta_z) - vec(0, scale, 0), text=axis_labels[2],
                  color=axis_color, height=scale * 7, billboard=True, emissive=True)
        return [c1, c2, c3, a1, a2, a3, l1, l2, l3]

    def _make_tick_marks(self, x_dim, y_dim, z_dim, tick_marks_color, scale):
        tick_marks = []
        for i in range(np.len(x_dim)):
            a_box = box(pos=x_hat * x_dim.get(i), width=scale * 2, height=scale * 5, length=scale * 2,
                        color=tick_marks_color)
            tick_marks.append(a_box)
        for i in range(np.len(z_dim)):
            a_box = box(pos=z_hat * z_dim.get(i), width=scale * 2, height=scale * 5, length=scale * 2,
                        color=tick_marks_color)
            tick_marks.append(a_box)
        for i in range(np.len(y_dim)):
            a_box = box(pos=y_hat * y_dim.get(i), width=scale * 2, height=scale * 5, length=scale * 2,
                        color=tick_marks_color)
            a_box.rotate(angle=0.5 * pi, axis=vec(0, 0, 1))
            tick_marks.append(a_box)
        return tick_marks

    def axis_visibility_is(self, visible):
        for i in range(len(self._axis)):
            self._axis[i].visible = visible

    def tick_marks_visibility_is(self, visible):
        for tick_mark in self._tick_marks:
            tick_mark.visible = visible

    def xy_mesh_visibility_is(self, visible):
        for i in range(len(self._xy_mesh)):
            self._xy_mesh[i].visible = visible

    def xz_mesh_visibility_is(self, visible):
        for i in range(len(self._xz_mesh)):
            self._xz_mesh[i].visible = visible

    def yz_mesh_visibility_is(self, visible):
        for i in range(len(self._xz_mesh)):
            self._yz_mesh[i].visible = visible


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
    axis.tick_marks_visibility_is(event.checked)


def toggle_yz_mesh(event):
    axis.yz_mesh_visibility_is(event.checked)


def toggle_xz_mesh(event):
    axis.xz_mesh_visibility_is(event.checked)


def toggle_xy_mesh(event):
    axis.xy_mesh_visibility_is(event.checked)


def toggle_axis(event):
    axis.axis_visibility_is(event.checked)


def toggle_info(event):
    if event.checked:
        # animation.width = 1200
        animation.caption = info
        MathJax.Hub.Queue(["Typeset", MathJax.Hub])  # , animation.title])  # LaTeX formatting
    else:
        # animation.width = 600
        animation.caption = ""
        MathJax.Hub.Queue(["Typeset", MathJax.Hub])  # , animation.title])  # LaTeX formatting


def adjust_k():
    complex_function.set_k_to(k_slider.value)
    k_slider_text.text = str(round(k_slider.value / pi, 2)) + " * π"


def adjust_amplitude():
    complex_function.set_amplitude_to(amplitude_slider.value)
    amplitude_slider_text.text = str(amplitude_slider.value) + " units"


def adjust_omega():
    complex_function.set_omega_to(omega_slider.value)
    omega_slider_text.text = str(round(omega_slider.value / pi, 2)) + " * π"


omega_slider = slider(pos=animation.title_anchor, min=0, max=6 * pi, value=2 * pi, bind=adjust_omega)
animation.append_to_title(" Omega = ")
omega_slider_text = wtext(pos=animation.title_anchor, text="2 * π")
animation.append_to_title("\n\n")

k_slider = slider(pos=animation.title_anchor, min=-2 * pi / 3, max=2 * pi / 3, value=2 * pi / 5, bind=adjust_k)
animation.append_to_title(" Wave number k = ")
k_slider_text = wtext(pos=animation.title_anchor, text="2 * π  / 5")
animation.append_to_title("\n\n")

amplitude_slider = slider(pos=animation.title_anchor, min=1, max=6, value=3, bind=adjust_amplitude)
animation.append_to_title(" Amplitude = ")
amplitude_slider_text = wtext(pos=animation.title_anchor, text="3 units")
animation.append_to_title("\n\n")

_ = checkbox(pos=animation.title_anchor, text='Tick marks', bind=toggle_tick_marks, checked=False)
_ = checkbox(pos=animation.title_anchor, text='YZ mesh', bind=toggle_yz_mesh, checked=False)
_ = checkbox(pos=animation.title_anchor, text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(pos=animation.title_anchor, text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(pos=animation.title_anchor, text='Axis', bind=toggle_axis, checked=True)
_ = checkbox(pos=animation.title_anchor, text="Show info", bind=toggle_info, checked=False)
animation.append_to_title("\n\n")

MathJax.Hub.Queue(["Typeset", MathJax.Hub])

space = Space(np.linspace(-10, 10, 11), np.linspace(-6, 6, 11), np.linspace(-6, 6, 11))
axis = Base(space)
axis.tick_marks_visibility_is(False)
axis.xz_mesh_visibility_is(True)
complex_function = PlaneWave()

dt = 0.01
t = 0
while True:
    rate(30)
    complex_function.update(t)
    t += dt

