# Web VPython 3.2

from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')
# get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

ricker_title = """<a href="https://en.wikipedia.org/wiki/Ricker_wavelet">Ricker / Mexican hat / Marr wavelet</a>

$F(x,y) = \dfrac{1}{\pi\sigma^4} \\bigg(1 - \dfrac{1}{2} \\bigg( \dfrac{x^2 + y^2}{\sigma^2} \\bigg) \\bigg) e^{-\\dfrac{x^2+y^2}{2\sigma^2}}$
"""

mexican_hat_title = "<h3>Polar coordinates for Mexican hat</h3>$\\begin{cases} x & = r\\cos(\\phi) \\\\ y & = r\\sin(\\phi)) \\\\ z & = (r^2 - 1)^2 \\end{cases}$"
spiral_title = "<h3>Polar coordinates for Dini&apos;s spiral</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)\cdot\\sin(\\phi) \\\\  \\sin(\\theta)\\cdot\\sin(\\phi) \\\\ (\\cos(\\phi)+\\log(\\tan(\\phi/2)))) + 0.2\\theta \\end{pmatrix}\\text{, } \\begin{cases} 0 < \\theta < 12.4 \\\\ 0.1 < \\phi < 2\\end{cases}$"
torus_title = "<h3>Polar coordinates for torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (c + a \\cos(\\phi))\cdot\\cos(\\theta) \\\\  (c + a \\cos(\\phi))\cdot\\sin(\\theta) \\\\ a \\sin(\\phi) \\end{pmatrix}\\text{, } \\theta, \\phi \\in [-\\pi, \\pi]$"
twisted_torus_title = "<h3>Polar coordinates for twisted torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (3 + \\sin(\\phi) + \\cos(\\theta)) \cdot \\cos(2\\phi) \\\\  (3 + \\sin(\\phi) + \\cos(\\theta))\cdot\\sin(2\\phi) \\\\ \\sin(\\theta)+2\\cos(\\phi) \\end{pmatrix}\\text{, } \\theta, \\phi \\in [-\\pi, \\pi]\\text{, } \\theta, \\phi \\in [-\\pi, \\pi]$"
sine_cosine_title = "<h2>$F(x, y) = \\sin{(\pi x)}\\cos{(\pi y)}}$</h2>"
exponential_title = "<h2>$F(x, y) = \\sin(x^2 + y^2) e^{ -x^2 - y^2}$</h2>"
ripple_title = "<h2>$F(x, y) =  \\sin\\big(3 (x^2 + y^2)\\big)$</h2"
polynomial_title = "<h2>$F(x, y) =  (yx^3 - xy^3)$</h2>"
cosine_of_abs_title = "<h2>F(x, y) = \\cos(|x| + |y|)$</h2>"
sine_sqrt_title = "<h2>$F(x, y) = \\sqrt{x^2+y^2}$</h2>"
caption = """
&#x2022; Source code can be found <a href="https://github.com/zhendrikse/physics-in-python/blob/main/src/glowscript/mathematics/3d_plots.py">here</a>
&#x2022; Inspired on <a href="https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Plot3D">Plot3D</a> by adding the following features: 
  &#x2022; Numpy linspace and meshgrid syntax
  &#x2022; Configurable base and mesh background
  &#x2022; Non-uniform coloring

"""

animation = canvas(align="top", width=700, height=700, center=vec(0, 5, 0),
                   forward=vec(-0.9, -0.5, -.8), title=ricker_title + "\n", range=75)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])


class Numpy:
    def __init__(self):
        self.array = self._array
        self.linspace = self._linspace
        self.len = self._len
        self.meshgrid = self._meshgrid
        self.sqrt = self._sqrt
        self.cos = self._cos
        self.sin = self._sin
        self.tan = self._tan
        self.exp = self._exp
        self.log = self._log
        self.abs = self._abs

    def _abs(self, numpy_array):
        return nj.abs(numpy_array)

    def _exp(self, numpy_array):
        return nj.exp(numpy_array)

    def _log(self, numpy_array):
        return nj.log(numpy_array)

    def _cos(self, numpy_array):
        return nj.cos(numpy_array)

    def _sin(self, numpy_array):
        return nj.sin(numpy_array)

    def _tan(self, numpy_array):
        return nj.tan(numpy_array)

    def _sqrt(self, numpy_array):
        return nj.sqrt(numpy_array)

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
    def __init__(self, xx, yy, zz, axis_color, tick_marks_color, num_tick_marks):
        base_ = [np.linspace(0, np.len(xx), num_tick_marks + 1),
                 np.linspace(0, np.len(yy), num_tick_marks + 1),
                 np.linspace(0, np.len(zz), num_tick_marks + 1)]
        scale = .01 * (base_[0].get(-1) - base_[0].get(0))
        delta_ = [i.get(1) - i.get(0) for i in base_]
        self._tick_marks, self._xy_mesh, self._xz_mesh, self._yz_mesh = [], [], [], []
        self._make_tick_marks(base_, xx, yy, zz, delta_, tick_marks_color, axis_color, scale, num_tick_marks)
        self._make_mesh(base_, delta_, scale)

    def _make_mesh(self, base_, delta_, scale):
        range_ = [i.get(-1) - i.get(0) for i in base_]
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

    def _make_tick_marks(self, base_, xx, yy, zz, delta_, tick_marks_color, axis_color, scale, num_tick_marks):
        increment = (xx.get(-1, -1) - xx.get(0, 0)) / num_tick_marks
        start_value = xx.get(0, 0)
        for i in range(1, np.len(base_[2]), 2):
            label_text = '{:1.2f}'.format(start_value + i * increment, 2)
            pos = z_hat * base_[2].get(i) + x_hat * (base_[0].get(-1) + 5 * scale)
            x_label = text(pos=pos, text=label_text, height=5 * scale, billboard=True, color=tick_marks_color)
            self._tick_marks.append(x_label)

        increment = (yy.get(-1, -1) - yy.get(0, 0)) / num_tick_marks
        start_value = yy.get(0, 0)
        for i in range(0, np.len(base_[0]), 2):
            label_text = '{:1.2f}'.format(start_value + i * increment, 2)
            pos = x_hat * base_[0].get(i) + z_hat * (base_[2].get(-1) + 15 * scale)
            y_label = text(pos=pos, text=label_text, height=5 * scale, billboard=True, color=tick_marks_color)
            self._tick_marks.append(y_label)

        increment = (zz.get(-1, -1) - zz.get(0, 0)) / num_tick_marks
        start_value = zz.get(0, 0)
        for i in range(1, np.len(base_[1]), 2):
            label_text = '{:1.2f}'.format(start_value + i * increment, 2)
            pos = y_hat * base_[1].get(i) + z_hat * (base_[2].get(-1) + 15 * scale)
            z_label = text(pos=pos, text=label_text, height=5 * scale, billboard=True, color=tick_marks_color)
            self._tick_marks.append(z_label)

        pos = x_hat * (base_[0].get(-1) + 2 * delta_[0]) - vec(0, scale, -30)
        l_y = text(pos=pos, text="Y-axis", color=axis_color, height=scale * 4, billboard=True, emissive=True)
        pos = z_hat * (base_[2].get(-1) + 2 * delta_[2]) + y_hat * (.625 * base_[1].get(-1))
        l_z = text(pos=pos, text="Z-axis", color=axis_color, height=scale * 4, billboard=True, emissive=True)
        pos = x_hat * (base_[0].get(-1) / 2) + z_hat * (base_[2].get(-1) + 3 * delta_[2])
        l_x = text(pos=pos, text="X-axis", color=axis_color, height=scale * 4, billboard=True, emissive=True)
        c_x = cylinder(pos=x_hat * base_[0].get(0), axis=x_hat * (base_[0].get(-1) - base_[0].get(0)), color=axis_color,
                       radius=scale)
        c_y = cylinder(pos=z_hat * base_[2].get(0), axis=z_hat * (base_[2].get(-1) - base_[2].get(0)), color=axis_color,
                       radius=scale)
        c_z = cylinder(pos=y_hat * base_[1].get(0), axis=y_hat * (base_[1].get(-1) - base_[1].get(0)), color=axis_color,
                       radius=scale)
        self._tick_marks += [c_x, c_y, c_z, l_x, l_y, l_z]

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


class Plot3D:
    """
    A class to make 3D plots.

    The x-axis is labeled y, the z axis is labeled x, and the y-axis is
    labeled z. This is done to mimic fairly standard practive for plotting
    the z value of a function of x and y.

    A plot is typically made like so:

    resolution = 75
    x = y = np.linspace(-2 * pi, 2 * pi, resolution)
    xx, yy = np.meshgrid(x, y)
    zz = np.cos(np.abs(xx).add(np.abs(yy)))
    Plot3D(xx, yy, zz)


    Attributes
    ----------
    xx : array
        Numpy array containing the x-values, typically generated by
        the np.meshgrid() function
    yy : array
        Numpy array containing the y-values, typically generated by
        the np.meshgrid() function
    zz : array
        Numpy array containing the function values
    z_min: float
        Optional minimum z-axis boundary
    z_max: float
        Optional maximum z-axis boundary


    Methods
    -------
    render(t):
        Render the plot with a new time.
    """

    def __init__(self, xx, yy, zz, z_min=None, z_max=None, axis_color=color.yellow, tick_marks_color=vec(0.4, 0.8, 0.4),
                 num_tick_marks=10):
        self._xx = xx
        self._yy = yy
        self._zz = zz

        self._z_min, self._z_max = self._z_min_and_z_max(z_min, z_max)
        self._hue_offset = 0.5
        self._omega = 0
        self._axis_color = axis_color
        self._tick_marks_color = tick_marks_color
        self._num_tick_marks = num_tick_marks
        self._axis = self._create_base()
        self._vertices, self._quads = [], []
        self._create_vertices()
        self._create_quads()
        self.render(0)

    def reinitialize(self, xx, yy, zz, z_min=None, z_max=None):
        self._xx = xx
        self._yy = yy
        self._zz = zz

        self._z_min, self._z_max = self._z_min_and_z_max(z_min, z_max)
        self._hide_plot()  # Hide previous shizzle before creating new stuff
        self._hide_axis()  # Hide previous stizzle before creating new stuff
        self._axis = self._create_base()
        self._vertices, self._quads = [], []
        self._create_vertices()
        self._create_quads()
        self.render(0)

    def _z_min_and_z_max(self, z_min, z_max):
        # Has user has already defined the boundaries for us?
        # Otherwise, we fall back to automatic boundary creation
        if z_min and z_max:
            return z_min, z_max

        return self._zz.flatten().min(), self._zz.flatten().max()

    def _hide_axis(self):
        self._axis.tick_marks_visibility_is(False)
        self._axis.xy_mesh_visibility_is(False)
        self._axis.xz_mesh_visibility_is(False)
        self._axis.yz_mesh_visibility_is(False)

    def _hide_plot(self):
        for quad_ in self._quads:
            quad_.visible = False
        for vertex_ in self._vertices:
            vertex_.visible = False

    def _create_base(self):
        x_min, x_max, y_min, y_max = self._ranges()
        xx = np.linspace(x_min, x_max, np.len(self._xx))
        yy = np.linspace(y_min, y_max, np.len(self._yy))
        zz = np.linspace(self._z_min, self._z_max, np.len(self._zz))
        axis = Base(xx, yy, zz, self._axis_color, self._tick_marks_color, self._num_tick_marks)
        axis.xy_mesh_visibility_is(True)
        axis.xz_mesh_visibility_is(True)
        axis.yz_mesh_visibility_is(True)
        return axis

    def _ranges(self):
        x_min = self._xx.flatten().min()
        x_max = self._xx.flatten().max()
        y_min = self._yy.flatten().min()
        y_max = self._yy.flatten().max()
        return x_min, x_max, y_min, y_max

    def _create_vertices(self):
        x_min, x_max, y_min, y_max = self._ranges()
        range_x = x_max - x_min
        range_y = y_max - y_min

        for x in range(np.len(self._xx)):
            for y in range(np.len(self._yy)):
                x_ = (self._xx.get(x, y) - x_min) * np.len(self._xx) / range_x
                y_ = (self._yy.get(x, y) - y_min) * np.len(self._yy) / range_y
                self._vertices.append(vertex(pos=vec(x_, 0, y_), normal=vec(0, 1, 0)))

    # Create the quad objects, based on the vertex objects already created.
    def _create_quads(self):
        for x in range(np.len(self._xx) - 2):
            for y in range(np.len(self._yy) - 2):
                v0 = self._get_vertex(x, y)
                v1 = self._get_vertex(x + 1, y)
                v2 = self._get_vertex(x + 1, y + 1)
                v3 = self._get_vertex(x, y + 1)
                self._quads.append(quad(vs=[v0, v1, v2, v3]))

    def _set_vertex_normal_for(self, x, y):
        # if x == np.len(self._xx) - 1 or y == np.len(self._yy) - 1: return
        vertex_ = self._get_vertex(x, y)
        vec_1 = self._get_vertex(x, y + 1).pos - vertex_.pos
        vec_2 = self._get_vertex(x + 1, y).pos - vertex_.pos
        vertex_.normal = cross(vec_1, vec_2)

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        for x in range(np.len(self._xx) - 2):
            for y in range(np.len(self._yy) - 2):
                self._set_vertex_normal_for(x, y)

    def _value_to_plot(self, x, y, t, range_z):
        f_x_y = self._zz.get(x, y) * (cos(self._omega * t) + 1) * .5
        return (np.len(self._xx) / range_z) * (f_x_y - self._z_min)

    def _update_vertex(self, x, y, t, range_z):
        value = self._value_to_plot(x, y, t, range_z)
        self._get_vertex(x, y).pos.y = value
        color_ = abs(value) / np.len(self._zz) + self._hue_offset
        self._get_vertex(x, y).color = color.hsv_to_rgb(vec(color_, color_, 1))

    def render(self, t):
        range_z = self._z_max - self._z_min
        for x in range(np.len(self._xx)):
            for y in range(np.len(self._yy)):
                self._update_vertex(x, y, t, range_z)

        self._make_normals()

    def set_omega_to(self, omega):
        self._omega = omega

    def hue_offset_is(self, hue_offset):
        self._hue_offset = hue_offset

    def _get_vertex(self, x, y):
        return self._vertices[x * np.len(self._xx) + y]

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


def sine_sqrt():
    resolution = 50
    x = y = np.linspace(-2 * pi, 2 * pi, resolution)
    xx, yy = np.meshgrid(x, y)
    x_2_plus_y_2 = xx.multiply(xx).add(yy.multiply(yy))
    zz = np.sin(np.sqrt(x_2_plus_y_2)).multiply(5)

    z_min = -9
    z_max = 9
    return xx, yy, zz, z_min, z_max


def mexican_hat():
    # https://matplotlib.org/stable/gallery/mplot3d/surface3d_radial.html#sphx-glr-gallery-mplot3d-surface3d-radial-py
    r = np.linspace(0, 1.25, 50)
    p = np.linspace(-pi, 1.05 * pi, 50)
    R, P = np.meshgrid(r, p)
    Z = R.multiply(R).subtract(1).multiply(R.multiply(R).subtract(1))
    X, Y = np.cos(P).multiply(R), np.sin(P).multiply(R)

    return X, Y, Z, None, None


def torus():
    # https://www.mattiagiuri.com/2020/11/20/plotting-a-torus-with-python/

    resolution = 75
    c = 3
    a = 1
    xx = yy = np.linspace(-pi, 1.05 * pi, resolution)
    U, V = np.meshgrid(xx, yy)
    X = (np.cos(V).multiply(a).add(c)).multiply(np.cos(U))
    Y = (np.cos(V).multiply(a).add(c)).multiply(np.sin(U))
    Z = np.sin(V).multiply(a)
    return X, Y, Z, -2, 2


def knot():
    resolution = 50

    theta = np.linspace(-pi, pi, resolution)
    phi = np.linspace(0, 2.1 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    xx = np.cos(theta)
    yy = np.sin(theta).add(np.cos(phi))
    zz = np.sin(phi)

    return xx, yy, zz, None, None


def arc():
    resolution = 50

    theta = np.linspace(0, 1.05 * pi, resolution)
    phi = np.linspace(0, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    xx = np.cos(theta)
    yy = np.sin(theta).add(np.cos(phi))
    zz = np.sin(phi)

    return xx, yy, zz, None, None


def bubbles():
    resolution = 75

    theta = np.linspace(0, 1.02 * pi, resolution)
    phi = np.linspace(0, 2.02 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    xx = np.cos(theta).multiply(np.sin(phi.multiply(2)))
    yy = np.sin(theta).multiply(np.sin(phi.multiply(2)))
    zz = np.sin(phi)

    return xx, yy, zz, -1, 1.1


def mobius_strip():
    resolution = 100

    theta = np.linspace(-pi, 1.03 * pi, resolution)
    phi = np.linspace(-1, 1, resolution)
    theta, phi = np.meshgrid(theta, phi)

    factor = np.cos(theta.multiply(.5)).multiply(phi.multiply(.5)).add(1)
    xx = factor.multiply(np.cos(theta))
    yy = factor.multiply(np.sin(theta))
    zz = np.sin(theta.multiply(.5)).multiply(phi.multiply(.5))
    return xx, yy, zz, -0.5, 1


def twisted_torus():
    resolution = 100

    theta = np.linspace(-pi, pi * 1.05, resolution)
    phi = np.linspace(-pi, pi * 1.03, resolution)
    theta, phi = np.meshgrid(theta, phi)

    factor = np.sin(phi).add(np.cos(theta)).add(3)
    xx = np.cos(phi.multiply(2)).multiply(factor)
    yy = np.sin(phi.multiply(2)).multiply(factor)
    zz = np.sin(theta).add(np.cos(phi).multiply(2))

    return xx, yy, zz, None, None


def dinis_spiral():
    resolution = 100

    u = np.linspace(0, 12.4, resolution)
    v = np.linspace(0.1, 2, resolution)
    u, v = np.meshgrid(u, v)

    xx = np.cos(u).multiply(np.sin(v))
    yy = np.sin(u).multiply(np.sin(v))
    term = np.log(np.tan(v.multiply(0.5))).add(np.cos(v))
    zz = u.multiply(0.2).add(term)

    return xx, yy, zz, -2, 3


def ricker():
    resolution = 50

    x = y = np.linspace(-1.25, 1.25, resolution)
    xx, yy = np.meshgrid(x, y)

    sigma = .7
    sigma_2 = sigma * sigma
    x_2_plus_y_2 = xx.multiply(xx).add(yy.multiply(yy))
    x_2_plus_y_2_div_sigma_2 = x_2_plus_y_2.divide(-0.5 * sigma_2)
    factor_1 = 1 / (pi * sigma_2 * sigma_2)
    factor_2 = x_2_plus_y_2_div_sigma_2.add(1)
    zz = np.exp(x_2_plus_y_2_div_sigma_2).multiply(factor_2).multiply(factor_1)

    z_min = -.25
    z_max = 2
    return xx, yy, zz, z_min, z_max


def cosine_of_abs():
    resolution = 75
    x = y = np.linspace(-2 * pi, 2 * pi, resolution)
    xx, yy = np.meshgrid(x, y)
    zz = np.cos(np.abs(xx).add(np.abs(yy)))

    z_min = -2.5
    z_max = 2.5
    return xx, yy, zz, z_min, z_max


def polynomial():
    resolution = 50
    x = y = np.linspace(-1.75, 1.75, resolution)
    xx, yy = np.meshgrid(x, y)

    uu = yy.multiply(yy).multiply(yy).multiply(xx)
    zz = yy.multiply(xx).multiply(xx).multiply(xx).subtract(uu)

    z_min = z_max = None
    return xx, yy, zz, z_min, z_max


def exp_sine():
    resolution = 100
    x = y = np.linspace(-pi, pi, resolution)
    xx, yy = np.meshgrid(x, y)

    x_2_plus_y_2 = xx.multiply(xx).add(yy.multiply(yy))
    sin_x_2_plus_y_2 = np.sin(x_2_plus_y_2).multiply(10)
    exp_min_x_2_plus_y_2 = np.exp(x_2_plus_y_2.multiply(-1))
    zz = sin_x_2_plus_y_2.multiply(exp_min_x_2_plus_y_2)

    z_min = -.5
    z_max = 5
    return xx, yy, zz, z_min, z_max


def sine_cosine():
    resolution = 50
    x = y = np.linspace(-2 * pi / 3, 2 * pi / 3., resolution)
    xx, yy = np.meshgrid(x, y)
    zz = np.sin(xx.multiply(pi)).multiply(np.cos(yy.multiply(pi)))

    z_min = -2.5
    z_max = 2.5
    return xx, yy, zz, z_min, z_max


def ripple():
    resolution = 125
    x = y = np.linspace(-4 * pi / 3, 4 * pi / 3, resolution)
    xx, yy = np.meshgrid(x, y)

    x_2_plus_y_2 = xx.multiply(xx).add(yy.multiply(yy))
    zz = np.sin(x_2_plus_y_2.multiply(.75)).multiply(5)

    z_min = -20
    z_max = 20
    return xx, yy, zz, z_min, z_max


def adjust_color():
    plot.hue_offset_is(color_slider.value)


def sync_radio_buttons(event):
    if event.name != "ricker": ricker_button.checked = False
    if event.name != "torus": torus_button.checked = False
    if event.name != "twisted_torus": twisted_torus_button.checked = False
    if event.name != "mexican_hat": mexican_button.checked = False
    if event.name != "ripple": ripple_button.checked = False
    if event.name != "polynomial": polynomial_button.checked = False
    if event.name != "spiral": spiral_button.checked = False
    if event.name != "sin_cos": sin_cos_button.checked = False
    if event.name != "abs_cos": abs_cos_button.checked = False
    if event.name != "exp_sin": exp_sin_button.checked = False
    if event.name != "sin_sqrt": sin_sqrt_button.checked = False
    if event.name != "mobius": mobius_button.checked = False
    if event.name != "bubbles": bubbles_button.checked = False
    if event.name != "knot": knot_button.checked = False
    if event.name != "arc": arc_button.checked = False


def switch_function(event):
    sync_radio_buttons(event)
    xx, yy, zz, z_min, z_max = None, None, None, None, None

    if event.name == "mexican_hat":
        xx, yy, zz, z_min, z_max = mexican_hat()
        animation.title = mexican_hat_title + "\n\n"
    elif event.name == "ricker":
        xx, yy, zz, z_min, z_max = ricker()
        animation.title = ricker_title + "\n"
    elif event.name == "torus":
        xx, yy, zz, z_min, z_max = torus()
        animation.title = torus_title + "\n"
    elif event.name == "twisted_torus":
        xx, yy, zz, z_min, z_max = twisted_torus()
        animation.title = twisted_torus_title + "\n"
    elif event.name == "ripple":
        xx, yy, zz, z_min, z_max = ripple()
        animation.title = ripple_title + "\n\n"
    elif event.name == "spiral":
        xx, yy, zz, z_min, z_max = dinis_spiral()
        animation.title = spiral_title + "\n\n"
    elif event.name == "sin_sqrt":
        xx, yy, zz, z_min, z_max = sine_sqrt()
        animation.title = sine_sqrt_title + "\n"
    elif event.name == "polynomial":
        xx, yy, zz, z_min, z_max = polynomial()
        animation.title = polynomial_title + "\n"
    elif event.name == "sin_cos":
        xx, yy, zz, z_min, z_max = sine_cosine()
        animation.title = sine_cosine_title + "\n"
    elif event.name == "abs_cos":
        xx, yy, zz, z_min, z_max = cosine_of_abs()
        animation.title = cosine_of_abs_title + "\n"
    elif event.name == "exp_sin":
        xx, yy, zz, z_min, z_max = exp_sine()
        animation.title = exponential_title + "\n"
    elif event.name == "mobius":
        xx, yy, zz, z_min, z_max = mobius_strip()
        animation.title = exponential_title + "\n"
    elif event.name == "bubbles":
        xx, yy, zz, z_min, z_max = bubbles()
        animation.title = exponential_title + "\n"
    elif event.name == "arc":
        xx, yy, zz, z_min, z_max = arc()
        animation.title = exponential_title + "\n"
    elif event.name == "knot":
        xx, yy, zz, z_min, z_max = knot()
        animation.title = exponential_title + "\n"

    animation.range = 1.5 * np.len(xx)
    plot.reinitialize(xx, yy, zz, z_min, z_max)
    time = 0.5
    MathJax.Hub.Queue(["Typeset", MathJax.Hub])


def adjust_omega():
    plot.set_omega_to(omega_slider.value)
    omega_slider_text.text = "{:1.2f}".format(omega_slider.value / pi, 2) + " * π"


animation.append_to_caption("\n")
_ = checkbox(text='YZ mesh ', bind=toggle_yz_mesh, checked=True)
_ = checkbox(text='XZ mesh ', bind=toggle_xy_mesh, checked=True)
_ = checkbox(text='XY mesh ', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='Tick marks ', bind=toggle_tick_marks, checked=True)
animation.append_to_caption("\n\nHue offset  ")
color_slider = slider(min=0, max=1, step=.01, value=0.5, bind=adjust_color)

animation.append_to_caption("\n\nOmega = ")
omega_slider = slider(min=0, max=3 * pi, value=0, bind=adjust_omega)
omega_slider_text = wtext(text="1 * π")

animation.append_to_caption("\n\n")
ricker_button = radio(bind=switch_function, checked=True, text='Ricker wavelet', name='ricker')
mexican_button = radio(bind=switch_function, text='Mexican hat', name='mexican_hat')
torus_button = radio(bind=switch_function, text="Torus", name="torus")
twisted_torus_button = radio(bind=switch_function, text="Twisted torus", name="twisted_torus")
ripple_button = radio(bind=switch_function, text="Ripple", name="ripple")
spiral_button = radio(bind=switch_function, text="Spiral", name="spiral")
animation.append_to_caption("\n\n")
mobius_button = radio(bind=switch_function, text="Mobius strip ", name="mobius")
bubbles_button = radio(bind=switch_function, text="Bubbles ", name="bubbles")
arc_button = radio(bind=switch_function, text="Arc ", name="arc")
knot_button = radio(bind=switch_function, text="Knot ", name="knot")
animation.append_to_caption("\n\n")
sin_sqrt_button = radio(bind=switch_function, text="F=sin(sqrt(x*x+y*y)) ", name="sin_sqrt")
polynomial_button = radio(bind=switch_function, text="F=y*y*y*x-y*x*x*x ", name="polynomial")
sin_cos_button = radio(bind=switch_function, text="F=sin(x)*cos(y) ", name="sin_cos")
animation.append_to_caption("\n\n")
abs_cos_button = radio(bind=switch_function, text="F=cos(abs(x)+abs(y)) ", name="abs_cos")
exp_sin_button = radio(bind=switch_function, text="F=(x*x+y*y)exp(sin(-x*x-y*y)) ", name="exp_sin")

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


animation.bind('mousedown', running)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

time = 0
dt = 0.02
run = True
xx, yy, zz, z_min, z_max = ricker()
plot = Plot3D(xx, yy, zz, z_min, z_max)
while True:
    rate(30)
    plot.render(time)
    if run:
        time += dt

