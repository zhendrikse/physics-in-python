# Web VPython 3.2

from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')
get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

# There is an L by L grid of vertex objects, numbered 0 through L-1 by 0 through L-1.
# Only the vertex operators numbered L-2 by L-2 are used to create quads.
# The extra row and extra column of vertex objects simplifies edge calculations.
# The stride length from y = 0 to y = 1 is L.

ricker_title = """<a href="https://en.wikipedia.org/wiki/Ricker_wavelet">Ricker / Mexican hat / Marr wavelet</a>

$\\psi(x,y,t) = \dfrac{1 + \sin(\\omega t)}{\pi\sigma^4} \\bigg(1 - \dfrac{1}{2} \\bigg( \dfrac{x^2 + y^2}{\sigma^2} \\bigg) \\bigg) e^{-\\dfrac{x^2+y^2}{2\sigma^2}}$
"""

sine_cosine_title = "<h2>$\\psi(x,y,t) = 0.7+0.2\\sin{(10x)}\\cos{(10y)}\\cos{(\omega t)}$</h2>"
exponential_title = "<h2>$\\psi(x, y, t) = \\sin(\omega t) \\sin(x^2 + y^2) e^{ -x^2 - y^2}$</h2>"
ripple_title = "<h2>$\\psi(x, y, t) = \\sin(\omega t) \\sin\\big(3 (x^2 + y^2)\\big)$</h2"
polynomial_title = "<h2>$\\psi(x, y, t) = \\sin(\omega t) (yx^3 - xy^3)$</h2>"
cosine_of_abs_title = "<h2>$\\psi(x, y, t) = \\sin(\omega t)\\cos(|x| + |y|)$</h2>"
sine_sqrt_title = "<h2>$\\psi(x, y, t) = \\sin(\\omega t)\sqrt{x^2+y^2}$</h2>"
caption = """
&#x2022; Based on <a href="https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Plot3D">Plot3D</a>
&#x2022; Rewritten by <a href="https://github.com/zhendrikse/physics-in-python">Zeger Hendrikse</a> to include: 
  &#x2022; Numpy linspace and meshgrid syntax
  &#x2022; Configurable base and mesh background
  &#x2022; Non-uniform coloring
"""

animation = canvas(align="top", width=600, height=600, center=vec(0, 5, 0),
                   forward=vec(-0.9, -0.5, -.8), title=ricker_title + "\n", range=75)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])


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
base = [x_hat, y_hat, z_hat]


class Base:
    def __init__(self, xx, yy, zz):
        axis_color = color.yellow
        tick_marks_color = vec(0.4, 0.8, 0.4)
        num_tick_marks = 10

        base_ = [np.linspace(0, np.len(xx), num_tick_marks + 1),
                 np.linspace(0, np.len(yy), num_tick_marks + 1),
                 np.linspace(0, np.len(zz), num_tick_marks + 1)]
        scale = .01 * (base_[0].get(-1) - base_[0].get(0))
        delta_ = [i.get(1) - i.get(0) for i in base_]
        range_ = [i.get(-1) - i.get(0) for i in base_]
        self._axis = self._make_axis(base_, delta_, axis_color, tick_marks_color, scale)
        self._tick_marks = self._make_tick_marks(base_, xx, yy, zz, tick_marks_color, scale, num_tick_marks)

        self._xy_mesh, self._xz_mesh, self._yz_mesh = [], [], []
        for j in range(np.len(base_[0])):
            pos_x_y = x_hat * base_[0].get(0) + y_hat * base_[1].get(0)
            pos_x_z = x_hat * base_[0].get(0) + z_hat * base_[2].get(0)
            pos_y_z = y_hat * base_[1].get(0) + z_hat * base_[2].get(0)
            self._xy_mesh += [cylinder(pos=pos_x_y + x_hat * j * delta_[0], axis=y_hat * range_[1])]
            self._xy_mesh += [cylinder(pos=pos_x_y + y_hat * j * delta_[1], axis=x_hat * range_[0])]
            self._xz_mesh += [cylinder(pos=pos_x_z + x_hat * j * delta_[0], axis=z_hat * range_[2])]
            self._xz_mesh += [cylinder(pos=pos_x_z + z_hat * j * delta_[2], axis=x_hat * range_[0])]
            self._yz_mesh += [cylinder(pos=pos_y_z + y_hat * j * delta_[1], axis=z_hat * range_[2])]
            self._yz_mesh += [cylinder(pos=pos_y_z + z_hat * j * delta_[2], axis=y_hat * range_[1])]

            pos = (base_[1].get(0) + .5 * range_[1]) * y_hat + (base_[2].get(0) + .5 * range_[2]) * z_hat
            self._yz_mesh += [
                box(pos=pos, length=scale, width=range_[2], height=range_[1], opacity=0.15, visible=False)]
            pos = (base_[0].get(0) + .5 * range_[0]) * x_hat + (base_[1].get(0) + .5 * range_[1]) * y_hat
            self._xy_mesh += [
                box(pos=pos, length=range_[0], width=scale, height=range_[1], opacity=0.15, visible=False)]
            pos = (base_[0].get(0) + .5 * range_[0]) * x_hat + (base_[2].get(0) + .5 * range_[2]) * z_hat
            self._xz_mesh += [
                box(pos=pos, length=range_[0], width=range_[2], height=scale, opacity=0.15, visible=False)]

            self._set_mesh_properties(self._xy_mesh, scale)
            self._set_mesh_properties(self._xz_mesh, scale)
            self._set_mesh_properties(self._yz_mesh, scale)

    def _set_mesh_properties(self, mesh, scale):
        for item_ in mesh:
            item_.color = color.gray(.5)
            item_.radius = scale * .5
            item_.visible = False

    def _make_axis(self, base_, delta_, axis_color, tick_marks_color, scale):
        c1 = cylinder(pos=x_hat * base_[0].get(0), axis=x_hat * (base_[0].get(-1) - base_[0].get(0)), color=axis_color,
                      radius=scale)
        c2 = cylinder(pos=y_hat * base_[1].get(0), axis=y_hat * (base_[0].get(-1) - base_[1].get(0)), color=axis_color,
                      radius=scale)
        c3 = cylinder(pos=z_hat * base_[2].get(0), axis=z_hat * (base_[0].get(-1) - base_[2].get(0)), color=axis_color,
                      radius=scale)
        a1 = arrow(pos=x_hat * base_[0].get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_[0] * x_hat,
                   round=True)
        a2 = arrow(pos=y_hat * base_[1].get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_[1] * y_hat,
                   round=True)
        a3 = arrow(pos=z_hat * base_[2].get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_[2] * z_hat,
                   round=True)
        pos = x_hat * (base_[0].get(-1) + 2.25 * delta_[0]) - vec(0, scale, 0)
        l1 = text(pos=pos, text="X", color=tick_marks_color, height=scale * 5, billboard=True, emissive=True)
        pos = y_hat * (base_[1].get(-1) + 2.25 * delta_[1]) - vec(0, scale, 0)
        l2 = text(pos=pos, text="Z", color=tick_marks_color, height=scale * 5, billboard=True, emissive=True)
        pos = z_hat * (base_[2].get(-1) + 2.25 * delta_[2]) - vec(0, scale, 0)
        l3 = text(pos=pos, text="Y", color=tick_marks_color, height=scale * 5, billboard=True, emissive=True)
        return [c1, c2, c3, a1, a2, a3, l1, l2, l3]

    def _make_tick_marks(self, base_, xx, yy, zz, tick_marks_color, scale, num_tick_marks):
        tick_marks = []
        increment = (yy.get(-1, -1) - yy.get(0, 0)) / num_tick_marks
        start_value = yy.get(0, 0)
        for i in range(0, np.len(base_[0]), 2):
            label_text = str(math.round(start_value + i * increment, 2))
            pos = x_hat * base_[0].get(i) + z_hat * (base_[2].get(-1) + 7 * scale)
            a_label = text(pos=pos, text=label_text, height=5 * scale, billboard=True, color=tick_marks_color)
            tick_marks.append(a_label)

        increment = (xx.get(-1, -1) - xx.get(0, 0)) / num_tick_marks
        start_value = xx.get(0, 0)
        for i in range(1, np.len(base_[2]), 2):
            label_text = str(math.round(start_value + i * increment, 2))
            pos = z_hat * base_[2].get(i) + x_hat * (base_[0].get(-1) + 5 * scale)
            a_label = text(pos=pos, text=label_text, height=5 * scale, billboard=True, color=tick_marks_color)
            tick_marks.append(a_label)

        increment = (zz.get(-1, -1) - zz.get(0, 0)) / num_tick_marks
        start_value = zz.get(0, 0)
        for i in range(0, np.len(base_[1]), 2):
            label_text = str(math.round(start_value + i * increment, 2))
            pos = y_hat * base_[1].get(i) + z_hat * (base_[2].get(-1) + 7 * scale)
            a_label = text(pos=pos, text=label_text, height=5 * scale, billboard=True, color=tick_marks_color)
            tick_marks.append(a_label)
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


# The x axis is labeled y, the z axis is labeled x, and the y axis is labeled z.
# This is done to mimic fairly standard practive for plotting
#     the z value of a function of x and y.
class plot3D:
    def __init__(self, xx, yy, zz, f):
        self._f = f
        self._xx = xx
        self._yy = yy
        self._zz = zz
        self._hue_offset = 0.
        self._omega = pi
        self._axis = self._create_base()
        self._vertices, self._quads = [], []
        self._create_vertices()
        self._create_quads()
        self.render(0)

    def reinitialize(self, xx, yy, zz, f):
        self._f = f
        self._xx = xx
        self._yy = yy
        self._zz = zz
        self._hide_plot()  # Hide previous shizzle before creating new stuff
        self._hide_axis()  # Hide previous stizzle before creating new stuff
        self._axis = self._create_base()
        self._vertices, self._quads = [], []
        self._create_vertices()
        self._create_quads()
        self.render(0)

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
        axis = Base(self._xx, self._yy, self._zz)
        axis.xy_mesh_visibility_is(True)
        axis.xz_mesh_visibility_is(True)
        axis.yz_mesh_visibility_is(True)
        return axis

    def _create_vertices(self):
        for i in range(np.len(self._xx) * np.len(self._yy)):
            x, y = self._get_x_and_y_for(i)
            self._vertices.append(vertex(pos=vec(y, 0, x), normal=vec(0, 1, 0)))

    def _get_x_and_y_for(self, index):
        return int(index / np.len(self._xx)), index % np.len(self._yy)

    # Create the quad objects, based on the vertex objects already created.
    def _create_quads(self):
        for x in range(np.len(self._xx) - 2):
            for y in range(np.len(self._yy) - 2):
                v0 = self._get_vertex(x, y)
                v1 = self._get_vertex(x + 1, y)
                v2 = self._get_vertex(x + 1, y + 1)
                v3 = self._get_vertex(x, y + 1)
                self._quads.append(quad(vs=[v0, v1, v2, v3]))

    def _set_vertex_normal_for(self, index):
        x, y = self._get_x_and_y_for(index)
        if x == np.len(self._xx) - 1 or y == np.len(self._yy) - 1: return
        v = self._vertices[index]
        a = self._vertices[index + np.len(self._xx)].pos - v.pos
        b = self._vertices[index + 1].pos - v.pos
        v.normal = cross(a, b)

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        for i in range(np.len(self._xx) * np.len(self._yy)):
            self._set_vertex_normal_for(i)

    def _update_vertex_with_index(self, i, t):
        z_min = self._zz.get(0)
        range_z = self._zz.get(-1) - self._zz.get(0)

        x, y = self._get_x_and_y_for(i)
        f_x_y = self._f(self._xx.get(x, y), self._yy.get(x, y), self._omega, t)
        value = np.len(self._zz) / range_z * (f_x_y - z_min)

        self._vertices[i].pos.y = value
        color_ = (abs(value) - z_min) / (range_z * 20) + self._hue_offset

        self._vertices[i].color = color.hsv_to_rgb(vec(color_, color_, 1))

    def render(self, t):
        for i in range(np.len(self._xx) * np.len(self._yy)):
            self._update_vertex_with_index(i, t)

        self._make_normals()

    def set_omega_to(self, omega):
        self._omega = omega

    def hue_offset_is(self, hue_offset):
        self._hue_offset = hue_offset

    def _get_vertex(self, x, y):
        return self._vertices[x * np.len(self._xx) + y]

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


def sine_sqrt():
    xx, yy = np.meshgrid(np.linspace(-2 * pi, 2 * pi, 50), np.linspace(-2 * pi, 2 * pi, 50))
    zz = np.linspace(-2, 2, 50)

    def f(x, y, omega, t):
        return sin(omega * t) * sin(sqrt(x * x + y * y))

    return xx, yy, zz, f


def ricker():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    zz = np.linspace(-1, 3, 50)
    sigma = .7

    def f(x, y, omega, t):
        return (1 + sin(omega * t)) / (pi * sigma ** 4) * (1 - 0.5 * ((x * x + y * y)) / (sigma * sigma)) * exp(
            -1 * ((x * x + y * y) / (2 * sigma * sigma)))

    return xx, yy, zz, f


def cosine_of_abs():
    xx, yy = np.meshgrid(np.linspace(-2 * pi, 2 * pi, 75), np.linspace(-2 * pi, 2 * pi, 75))
    zz = np.linspace(-2, 2, 75)

    def f(x, y, omega, t):
        return sin(omega * t) * cos(abs(x) + abs(y))

    return xx, yy, zz, f


def polynomial():
    xx, yy = np.meshgrid(np.linspace(-1.75, 1.75, 50), np.linspace(-1.75, 1.75, 50))
    zz = np.linspace(-4, 4, 50)

    def f(x, y, omega, t):
        return sin(omega * t) * (y * x * x * x - x * y * y * y)

    return xx, yy, zz, f


def exp_sine():
    xx, yy = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
    zz = np.linspace(-4, 4, 100)

    def f(x, y, omega, t):
        return 10 * sin(omega * t) * sin(x * x + y * y) * exp(-(x * x + y * y))

    return xx, yy, zz, f


def sine_cosine():
    xx, yy = np.meshgrid(np.linspace(0, pi, 50), np.linspace(0, pi, 50))
    zz = np.linspace(0, 3, 50)

    def f(x, y, omega, t):
        return 1 + sin(1.25 * pi * x) * cos(1.25 * pi * y) * sin(omega * t)

    return xx, yy, zz, f


def ripple():
    xx, yy = np.meshgrid(np.linspace(-2 * pi / 3, 2 * pi / 3, 100), np.linspace(-2 * pi / 3, 2 * pi / 3, 100))
    zz = np.linspace(-7, 7, 100)

    def f(x, y, omega, t):
        return sin(omega * t) * sin(3 * (x * x + y * y))

    return xx, yy, zz, f


def adjust_color():
    plot.hue_offset_is(color_slider.value)


def switch_function(event):
    xx, yy, zz, f = None, None, None, None
    if event.index < 0:
        return
    elif event.index == 0:
        xx, yy, zz, f = ricker()
        animation.title = ricker_title + "\n"
        animation.range = 75
    elif event.index == 1:
        xx, yy, zz, f = sine_sqrt()
        animation.title = sine_sqrt_title + "\n"
        animation.range = 75
    elif event.index == 2:
        xx, yy, zz, f = sine_cosine()
        animation.title = sine_cosine_title + "\n"
        animation.range = 75
    elif event.index == 3:
        xx, yy, zz, f = ripple()
        animation.range = 150
        animation.title = ripple_title + "\n\n"
    elif event.index == 4:
        xx, yy, zz, f = exp_sine()
        animation.range = 150
        animation.title = exponential_title + "\n"
    elif event.index == 5:
        xx, yy, zz, f = polynomial()
        animation.range = 75
        animation.title = polynomial_title + "\n"
    elif event.index == 6:
        xx, yy, zz, f = cosine_of_abs()
        animation.range = 115
        animation.title = cosine_of_abs_title + "\n"

    plot.reinitialize(xx, yy, zz, f)
    MathJax.Hub.Queue(["Typeset", MathJax.Hub])


def adjust_omega():
    plot.set_omega_to(omega_slider.value)
    omega_slider_text.text = str(round(omega_slider.value / pi, 2)) + " * π"


animation.append_to_caption("\n")
wave_choices = ["Ricker wavelet", "f(x,y) = sqrt(x*x + y*y)", "f(x,y) = sin(10x) cos(10y)", "Ripple",
                "f(x,y) = sin(x*x + y*y) exp(-x*x - y*y)", "f(x,y) = y*x*x*x - x*y*y*y", "f(x,y) = cos(|x| + |y|)"]
_ = menu(choices=wave_choices, bind=switch_function)
animation.append_to_caption("\n\n")
_ = checkbox(text='YZ mesh ', bind=toggle_yz_mesh, checked=True)
_ = checkbox(text='XZ mesh ', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh ', bind=toggle_xy_mesh, checked=True)
_ = checkbox(text='Axis ', bind=toggle_axis, checked=True)
_ = checkbox(text='Tick marks ', bind=toggle_tick_marks, checked=True)
animation.append_to_caption("\n\nHue offset  ")
color_slider = slider(min=0, max=1, step=.01, value=0, bind=adjust_color)

animation.append_to_caption("\n\nOmega = ")
omega_slider = slider(min=0, max=3 * pi, value=pi, bind=adjust_omega)
omega_slider_text = wtext(text="1 * π")
animation.append_to_caption("\n" + caption + "\n")


def on_key_press(key):
    if key == "b":
        animation.background = color.white if animation.background == color.black else color.black
    if key == 's':
        animation.capture("3d_complex_function_plot")
    if key == 'v':
        print("scene.center=" + str(animation.center))
        print("scene.forward=" + str(animation.forward))
        print("scene.range=" + str(animation.range))


def key_pressed(event):
    key = event.key
    on_key_press(key)


animation.bind('keydown', key_pressed)


def running(ev):
    global run
    run = not run
    # print("scene.center=" + str(animation.center))
    # print("scene.forward=" + str(animation.forward))
    # print("scene.range=" + str(animation.range))


animation.bind('mousedown', running)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

time = 0
dt = 0.02
run = True
plot = plot3D(ricker()[0], ricker()[1], ricker()[2], ricker()[3])
while True:
    rate(30)
    if run:
        plot.render(time)
        time += dt

