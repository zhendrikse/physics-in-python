# Web VPython 3.2

from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdnjs.cloudflare.com/ajax/libs/numjs/0.16.1/numjs.min.js')
# get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

animation = canvas(background=color.gray(0.1))


class Numpy:
    def __init__(self):
        self.array = self._array
        self.linspace = self._linspace
        self.len = self._len
        self.meshgrid = self._meshgrid
        self.concatenate = self._concatenate
        self.sqrt = self._sqrt
        self.cos = self._cos
        self.sin = self._sin
        self.tan = self._tan
        self.exp = self._exp
        self.log = self._log
        self.abs = self._abs
        self.ones = self._ones
        self.zeros = self._zeros
        self.random = self._random

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

    def _ones(self, shape_array):
        return nj.ones(shape_array)

    def _zeros(self, shape_array):
        return nj.zeros(shape_array)

    def _random(self, shape_array):
        return nj.random(shape_array)

    def _concatenate(self, numpy_array_1, numpy_array_2):
        return nj.concatenate(numpy_array_1, numpy_array_2)

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


# This class is only meant to be used from within the Figure class.
class SubPlot:
    def __init__(self, xx, yy, zz):
        self._xx, self._yy, self._zz = xx, yy, zz
        self._hue_offset = .2
        self._opacity = 1
        self._shininess = 0.6
        self._hue_gradient = .25
        self._omega = 0
        self._vertices, self._quads = [], []
        self._create_vertices()
        self._create_quads()
        self.render(0)

    def hide_plot(self):
        for quad_ in self._quads:
            quad_.visible = False
        for vertex_ in self._vertices:
            vertex_.visible = False

    def _create_vertex(self, x, y):
        x_ = self._xx.get(x, y) * self._xx.shape[0]
        y_ = self._yy.get(x, y) * self._yy.shape[1]
        self._vertices.append(vertex(pos=vec(x_, 0, y_), normal=vec(0, 1, 0)))

    def _create_vertices(self):
        for x in range(self._xx.shape[0]):
            for y in range(self._yy.shape[1]):
                self._create_vertex(x, y)

    def _create_quad(self, x, y):
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (self._xx.shape[0] - 1):
            _neighbor_increment_x = -x
        if y == (self._yy.shape[1] - 1):
            _neighbor_increment_y = -y

        v0 = self._get_vertex(x, y)
        v1 = self._get_vertex(x + _neighbor_increment_x, y)
        v2 = self._get_vertex(x + _neighbor_increment_x, y + _neighbor_increment_y)
        v3 = self._get_vertex(x, y + _neighbor_increment_y)
        self._quads.append(quad(vs=[v0, v1, v2, v3]))

    # Create the quad objects, based on the vertex objects already created.
    def _create_quads(self):
        for x in range(self._xx.shape[0] - 1):
            for y in range(self._yy.shape[1] - 1):
                self._create_quad(x, y)

    def _set_vertex_normal_for(self, x, y):
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (self._xx.shape[0] - 1):
            _neighbor_increment_x = -x
        if y == (self._yy.shape[1] - 1):
            _neighbor_increment_y = -y
        vertex_ = self._get_vertex(x, y)
        #        normal_total_ = self._get_vertex(x, y + _neighbor_increment_y).normal
        #        normal_total_ += self._get_vertex(x + _neighbor_increment_x, y).normal
        vec_1 = self._get_vertex(x, y + _neighbor_increment_y).pos - vertex_.pos
        vec_2 = self._get_vertex(x + _neighbor_increment_x, y).pos - vertex_.pos
        """
        Further work to focus on this area of the normal calculations
        """
        vertex_.normal = cross(vec_1, vec_2)

    #        normal_total_ += cross(vec_1, vec_2)
    #        vertex_.normal = normal_total_/2

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        for x in range(self._xx.shape[0]):
            for y in range(self._yy.shape[1]):
                self._set_vertex_normal_for(x, y)

    def _update_vertex(self, x, y, value):
        hue = .5 / self._yy.shape[1] * self._hue_gradient * abs(value) + self._hue_offset
        vertex_ = self._get_vertex(x, y)
        vertex_.pos.y = value
        vertex_.color = color.hsv_to_rgb(vec(hue, 1, 1))
        vertex_.opacity = self._opacity
        vertex_.shininess = self._shininess

    def _update_vertices(self, t):
        for x in range(self._xx.shape[0]):
            for y in range(self._yy.shape[1]):
                f_x_y = self._zz.get(x, y) * (cos(self._omega * t) + 1) * .5
                value = self._zz.shape[0] * f_x_y
                self._update_vertex(x, y, value)

    def _get_vertex(self, x, y):
        return self._vertices[x * self._yy.shape[1] + y]

    def render(self, t):
        self._update_vertices(t)
        self._make_normals()

    def set_omega_to(self, omega):
        self._omega = omega

    def set_hue_offset_to(self, offset):
        self._hue_offset = offset

    def set_hue_gradient_to(self, gradient):
        self._hue_gradient = gradient

    def set_opacity_to(self, opacity):
        self._opacity = opacity

    def set_shininess_to(self, shininess):
        self._shininess = shininess


class SubPlotFxyt(SubPlot):
    def __init__(self, xx, yy, f_x_y_t):
        SubPlot.__init__(self, xx, yy, None)
        self._f_x_y_t = f_x_y_t

    def _update_vertices(self, t):
        for x in range(self._xx.shape[0]):
            for y in range(self._yy.shape[1]):
                x_ = self._xx.get(x, y)
                y_ = self._yy.get(x, y)
                value = self._xx.shape[0] * self._f_x_y_t(x_, y_, t)
                self._update_vertex(x, y, value)


class Figure:
    """
    A class to make 3D figures.

    The x-axis is labeled y, the z axis is labeled x, and the y-axis is
    labeled z. This is done to mimic fairly standard practive for plotting
    the z value of a function of x and y.

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

    Methods
    -------
    render(t):
        Render the plot with a new time.
    """

    def __init__(self):
        self._subplots = []
        self._hue_offset = .25
        self._hue_gradient = .25
        self._omega = 0
        self._opacity = 1
        self._shininess = 0.6

    def render(self, t):
        for subplot in self._subplots:
            subplot.render(t)

    def set_omega_to(self, omega):
        self._omega = omega
        for subplot in self._subplots:
            subplot.set_omega_to(omega)

    def set_hue_offset_to(self, offset):
        self._hue_offset = offset
        for subplot in self._subplots:
            subplot.set_hue_offset_to(offset)

    def set_hue_gradient_to(self, gradient):
        self._hue_gradient = gradient
        for subplot in self._subplots:
            subplot.set_hue_gradient_to(gradient)

    def set_opacity_to(self, opacity):
        self._opacity = opacity
        for subplot in self._subplots:
            subplot.set_opacity_to(opacity)

    def set_shininess_to(self, shininess):
        self._shininess = shininess
        for subplot in self._subplots:
            subplot.set_shininess_to(shininess)

    def reset(self):
        for subplot in self._subplots:
            subplot.hide_plot()

        self._subplots = []

    def add_subplot(self, subplot):
        subplot.set_omega_to(self._omega)
        subplot.set_opacity_to(self._opacity)
        subplot.set_hue_offset_to(self._hue_offset)
        subplot.set_hue_gradient_to(self._hue_gradient)
        self._subplots.append(subplot)


def adjust_opacity():
    figure.set_opacity_to(opacity_slider.value)


def adjust_shininess():
    figure.set_shininess_to(shininess_slider.value)


def adjust_omega():
    figure.set_omega_to(omega_slider.value)
    omega_slider_text.text = "= sin({:1.2f}".format(omega_slider.value / pi, 2) + " π)"


def adjust_gradient():
    figure.set_hue_gradient_to(gradient_slider.value)


def adjust_offset():
    figure.set_hue_offset_to(offset_slider.value)


animation.append_to_caption("\nHue offset  ")
offset_slider = slider(min=0, max=1, value=.25, bind=adjust_offset)

animation.append_to_caption("\n\nHue gradient  ")
gradient_slider = slider(min=0, max=1, value=.25, bind=adjust_gradient)

animation.append_to_caption("\n\nAnimation speed ")
omega_slider = slider(min=0, max=3 * pi, value=0, bind=adjust_omega)
omega_slider_text = wtext(text="= 0")

animation.append_to_caption("\n\nOpacity ")
opacity_slider = slider(min=0, max=1, step=0.01, value=1, bind=adjust_opacity)

animation.append_to_caption("\n\nShininess ")
shininess_slider = slider(min=0, max=1, step=0.01, value=0.6, bind=adjust_shininess)

animation.append_to_caption("\n\n")

resolution = 50
x = y = np.linspace(-2 * pi, 2 * pi, resolution)
x, y = np.meshgrid(x, y)


def f_x_y_t(x, y, t):
    return sin(sqrt(x * x + y * y)) * (cos(t) + 1)


# resolution = 50
# theta = np.linspace(0, 1.05 * pi, resolution)
# phi = np.linspace(0, pi, resolution)
# theta, phi = np.meshgrid(theta, phi)

# x = np.cos(theta)
# y = np.sin(theta).add(np.cos(phi))
# z = np.sin(phi).multiply(3)


figure = Figure()
# plot = figure.add_subplot(x, y, z, type="f(x,y,z)")
figure.add_subplot(SubPlotFxyt(x, y, f_x_y_t))

dt = 0.05
time = 0
while True:
    rate(30)
    figure.render(time)
    time += dt