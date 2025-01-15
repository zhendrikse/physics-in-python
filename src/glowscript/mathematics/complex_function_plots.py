#Web VPython 3.2

from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')
get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

# There is an L by L grid of vertex objects, numbered 0 through L-1 by 0 through L-1.
# Only the vertex operators numbered L-2 by L-2 are used to create quads.
# The extra row and extra column of vertex objects simplifies edge calculations.
# The stride length from y = 0 to y = 1 is L.


z_2_title = "<h2>$\\psi(z, t) = \\big(z^2 + 2\\big)e^{2 \pi i t} \\text{ where } z \in \\mathbb{C}$, $t \in \\mathbb{R}$</h2>"
z_abs_squared_title = "<h2>$\\psi(x,y,t) = zz^* e^{i \pi t} \\text{ where } z \in \\mathbb{C}$, $t \in \\mathbb{R}$</h2>"
z_cubed_title = "<h2>$\\psi(z, t) = \\big(z^3 + 2\\big)e^{2 \pi i t} \\text{ where } z \in \\mathbb{C}$, $t \in \\mathbb{R}$</h2>"
z_plus_1_divided_by_z_min_1_title = "<h2>$\\psi(z, t) = \\bigg(\dfrac{z + 3/2}{z - 3/2} \\bigg)e^{2 \pi i t} \\text{ where } z \in \\mathbb{C}$, $t \in \\mathbb{R}$</h2>"
sine_z_title = "<h2>$\\psi(z,t) = \\sin{(z)}e^{2 \pi i t} \\text{ where } z \in \\mathbb{C}$, $t \in \\mathbb{R}$</h2>"

caption = """
&#x2022; Based on <a href="https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Plot3D">Plot3D</a>
&#x2022; Rewritten by <a href="https://github.com/zhendrikse/physics-in-python">Zeger Hendrikse</a> to include: 
  &#x2022; Numpy linspace and meshgrid syntax
  &#x2022; Configurable base and mesh background
"""

animation = canvas(align="top", width=600, height=600, center=vec(0, 5, 0),
                   forward=vec(-0.9, -0.5, -.8), title=z_2_title + "\n", range=75)


class Numpy:
    def __init__(self):
        self.array = self._array
        self.linspace = self._linspace
        self.len = self._len
        self.meshgrid = self._meshgrid

    def _len(self, numpy_array):
        return numpy_array.shape[0]

    def _array(self, an_array):
        return nj.array(an_array)

    def _linspace(self, start, stop, num):
        return self._array([x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop])

    def _meshgrid(self, linspace_1, linspace_2):
        xx = nj.stack([linspace_1 for _ in range(linspace_1.shape)])
        temp = []
        for i in range(linspace_2.shape[0]):
            for j in range(linspace_2.shape[0]):
                temp.append(linspace_2.get(i))
        yy = nj.array(temp).reshape(linspace_2.shape[0], linspace_2.shape[0])
        return xx, yy


np = Numpy()

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
label_text = ("Im(z)", "|Ψ(z,t)|", "Re(z)")


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
        scale = .01 * (x_.get(-1) - x_.get(0))
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


class Complex:
    def __init__(self, real, imaginary):
        self._real = real
        self._imaginary = imaginary

    def multiplied_by(self, factor):
        real = self._real * factor.real() - self._imaginary * factor.imaginary()
        imaginary = self._imaginary * factor.real() + self._real * factor.imaginary()
        return Complex(real, imaginary)

    def divided_by(self, denominator):
        r = denominator.real() * denominator.real() + denominator.imaginary() * denominator.imaginary()
        real = denominator.real() * self._real + denominator.imaginary() * self._imaginary
        imaginary = denominator.real() * self._imaginary - denominator.imaginary() * self._real
        return Complex(real, imaginary)

    def abs(self):
        return sqrt(self._real * self._real + self._imaginary * self._imaginary)

    def conjugate(self):
        return Complex(self._real, -self._imaginary)

    def add(self, term):
        return Complex(self._real + term.real(), self._imaginary + term.imaginary())

    def real(self):
        return self._real

    def sin(self, z):
        return Complex(sin(z.real()) * math.cosh(z.imaginary()), cos(z.real()) * math.sinh(z.imaginary()))

    def imaginary(self):
        return self._imaginary


# The x axis is labeled y, the z axis is labeled x, and the y axis is labeled z.
# This is done to mimic fairly standard practive for plotting
#     the z value of a function of x and y.
class plot3D:
    def __init__(self, xx, yy, zz, f):
        self._f = f
        self._xx = xx
        self._yy = yy
        self._zz = zz
        self._vertices = self._create_vertices()
        self._quads = self._create_quads()
        self._make_normals()
        self._axis = self._create_base()

    def reinitialize(self, xx, yy, zz, f):
        self._f = f
        self._xx = xx
        self._yy = yy
        self._zz = zz
        self._hide_plot()
        self._hide_axis()
        self._vertices = self._create_vertices()
        self._quads = self._create_quads()
        self._make_normals()
        self._axis = self._create_base()

    def _hide_axis(self):
        self._axis.tick_marks_visibility_is(False)
        self._axis.axis_visibility_is(False)
        self._axis.xy_mesh_visibility_is(False)
        self._axis.xz_mesh_visibility_is(False)
        self._axis.yz_mesh_visibility_is(False)

    def _hide_plot(self):
        for quad_ in self._quads:
            quad_.visible = False
        for vertex_ in self._vertices:
            vertex_.visible = False

    def _create_base(self):
        space = Space(np.linspace(-0, np.len(self._xx), 11), np.linspace(0, np.len(self._yy), 11),
                      np.linspace(0, np.len(self._zz), 11))
        axis = Base(space)
        axis.xy_mesh_visibility_is(True)
        axis.xz_mesh_visibility_is(True)
        axis.yz_mesh_visibility_is(True)
        return axis

    def _create_vertices(self):
        vertices = []
        for i in range(np.len(self._xx) * np.len(self._yy)):
            x, y = self._get_x_and_y_for(i)
            value, phase = self._evaluate(x, y, 0)
            colour = color.hsv_to_rgb(vec(phase, 1, 1.25))
            vertices.append(vertex(pos=vec(y, value, x), color=colour, normal=vec(0, 1, 0)))
        return vertices

    def _get_x_and_y_for(self, index):
        return int(index / np.len(self._xx)), index % np.len(self._yy)

    def _evaluate(self, z_re, z_im, t):
        f_x_y = self._f(Complex(self._xx.get(z_re, z_im), self._yy.get(z_re, z_im)), t)
        range_z = self._zz.get(-1) - self._zz.get(0)
        phase = atan2(f_x_y.imaginary(), f_x_y.real())
        phase += 2 * pi if phase < 0 else 0
        phase /= 2 * pi
        return np.len(self._zz) / range_z * (f_x_y.abs() - self._zz.get(0)), phase

        # Create the quad objects, based on the vertex objects already created.

    def _create_quads(self):
        quads = []
        for x in range(np.len(self._xx) - 2):
            for y in range(np.len(self._yy) - 2):
                v0 = self.get_vertex(x, y)
                v1 = self.get_vertex(x + 1, y)
                v2 = self.get_vertex(x + 1, y + 1)
                v3 = self.get_vertex(x, y + 1)
                quads.append(quad(vs=[v0, v1, v2, v3]))
        return quads

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        for i in range(np.len(self._xx) * np.len(self._yy)):
            x, y = self._get_x_and_y_for(i)
            if x == np.len(self._xx) - 1 or y == np.len(self._yy) - 1: continue
            v = self._vertices[i]
            a = self._vertices[i + np.len(self._xx)].pos - v.pos
            b = self._vertices[i + 1].pos - v.pos
            v.normal = cross(a, b)

    def replot(self, t):
        for i in range(np.len(self._xx) * np.len(self._yy)):
            x, y = self._get_x_and_y_for(i)
            value, phase = self._evaluate(x, y, t)
            self._vertices[i].pos.y = value
            colour = color.hsv_to_rgb(vec(phase, 1, 1.25))
            self._vertices[i].color = colour

        self._make_normals()

    def get_vertex(self, x, y):
        return self._vertices[x * np.len(self._xx) + y]

    def get_pos(self, x, y):
        return self.get_vertex(x, y).pos

    def axis_visibility_is(self, visible):
        self._axis.axis_visibility_is(visible)

    def tick_marks_visibility_is(self, visible):
        self._axis.tick_marks_visibility_is(visible)

    def xy_mesh_visibility_is(self, visible):
        self._axis.xy_mesh_visibility_is(visible)

    def xz_mesh_visibility_is(self, visible):
        self._axis.xz_mesh_visibility_is(visible)

    def yz_mesh_visibility_is(self, visible):
        self._axis.yz_mesh_visibility_is(visible)


def toggle_tick_marks(event):
    plot.tick_marks_visibility_is(event.checked)


def toggle_xz_mesh(event):
    plot.xz_mesh_visibility_is(event.checked)


def toggle_xy_mesh(event):
    plot.xy_mesh_visibility_is(event.checked)


def toggle_yz_mesh(event):
    plot.yz_mesh_visibility_is(event.checked)


def toggle_axis(event):
    plot.axis_visibility_is(event.checked)


def phase(omega, t):
    return Complex(cos(omega * t), sin(omega * t))


def z_squared():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    zz = np.linspace(0, 8, 50)

    def f(z, t):
        return z.multiplied_by(z).add(Complex(2, 0)).multiplied_by(phase(2 * pi, t))

    return xx, yy, zz, f


def z_abs_squared():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    zz = np.linspace(0, 10, 50)

    def f(z, t):
        return z.multiplied_by(z.conjugate()).multiplied_by(phase(pi, t))

    return xx, yy, zz, f


def z_cubed():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    zz = np.linspace(0, 24, 50)

    def f(z, t):
        return z.multiplied_by(z).multiplied_by(z).add(Complex(2, 0)).multiplied_by(phase(2 * pi, t))

    return xx, yy, zz, f


def z_plus_1_divided_by_z_min_1():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 75), np.linspace(-2, 2, 75))
    zz = np.linspace(0, 10, 75)

    def f(z, t):
        return z.add(Complex(3 / 2, 0)).divided_by(z.add(Complex(-3 / 2, 0))).multiplied_by(phase(2 * pi, t))

    return xx, yy, zz, f


def sine_z():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    zz = np.linspace(0, 4, 50)

    def f(z, t):
        # return Complex(sin(z.real(), z.imaginary()).multiplied_by(phase(2 * pi, t))
        sine_z = Complex(sin(z.real()) * math.cosh(z.imaginary()), cos(z.real()) * math.sinh(z.imaginary()))
        return sine_z.multiplied_by(phase(2 * pi, t))

    return xx, yy, zz, f


def switch_function(event):
    xx, yy, zz, f = None, None, None, None
    if event.index < 0:
        return
    elif event.index == 0:
        xx, yy, zz, f = z_squared()
        animation.title = z_2_title + "\n"
        animation.range = 75
    elif event.index == 1:
        xx, yy, zz, f = z_abs_squared()
        animation.title = z_abs_squared_title + "\n"
        animation.range = 75
    elif event.index == 2:
        xx, yy, zz, f = z_cubed()
        animation.range = 75
        animation.title = z_cubed_title + "\n\n"
    elif event.index == 3:
        xx, yy, zz, f = z_plus_1_divided_by_z_min_1()
        animation.range = 115
        animation.title = z_plus_1_divided_by_z_min_1_title + "\n"
    elif event.index == 4:
        xx, yy, zz, f = sine_z()
        animation.range = 75
        animation.title = sine_z_title + "\n"

    plot.reinitialize(xx, yy, zz, f)
    MathJax.Hub.Queue(["Typeset", MathJax.Hub])


wave_choices = ["f(z, t) = z * z + 2", "f(z, t) = |z| * |z|", "f(z, t) = z * z * z + 2", "f(z, t) = z + 1.5 / z - 1.5",
                "f(z, t) = sin(z)"]
_ = menu(choices=wave_choices, bind=switch_function)
animation.append_to_caption("  ")
_ = checkbox(text='YZ mesh', bind=toggle_yz_mesh, checked=True)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=True)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)
_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=True)
animation.append_to_caption("\n" + caption + "\n")


def running(ev):
    global run
    run = not run
    # print("scene.center=" + str(animation.center))
    # print("scene.forward=" + str(animation.forward))
    # print("scene.range=" + str(animation.range))


animation.bind('mousedown', running)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

time = 0
dt = 0.01
run = True
plot = plot3D(z_squared()[0], z_squared()[1], z_squared()[2], z_squared()[3])
while True:
    rate(1 / dt)
    if run:
        plot.replot(time)
        time += dt

