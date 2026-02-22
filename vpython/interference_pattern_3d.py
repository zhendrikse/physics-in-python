#Web VPython 3.2

from vpython import vertex, quad, canvas, rate, cos, color, vec, arange, vector, slider, wtext, cross, sqrt, checkbox, pi

title = """&#x2022; Original <a href="https://github.com/zhendrikse/science/blob/main/waves/code/interference_pattern_3d.py">interference_pattern_3d.py</a> by <a href="http://www.hendrikse.name/">Zeger Hendrikse</a>

"""

width = 600
height = 450
display = canvas(title=title, width=width, height=height, background=color.gray(0.075), forward=vec(-.82, -1., -.64), center=vec(13, -13, 5), range=60)

class NumpyWrapper:
    def __init__(self, start_1, stop_1, start_2, stop_2, resolution):
        self._resolution = resolution
        x = self._linspace(start_1, stop_1, resolution)
        y = self._linspace(start_2, stop_2, resolution)
        self._x, self._y = self._meshgrid(x, y)

    def _linspace(self, start, stop, num):
        return [x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop]

    def _meshgrid(self, x, y):
        # Create empty lists to hold the grid arrays
        X = []
        Y = []

        # Create the 2D grid arrays
        for i in range(len(y)):
            X.append(x)  # Repeat x for each row (to get the same x values)

        for j in range(len(x)):
            Y.append([y[i] for i in range(len(y))])  # Repeat y for each column (to get the same y values)

        # Transpose Y to match the structure of numpy's meshgrid
        Y = list(map(list, zip(*Y)))

        return X, Y

    def get_plot_data(self, f_x, f_y, f_z):
        x, y, z = [], [], []
        for i in range(len(self._x)):
            x_, y_, z_ = [], [], []
            for j in range(len(self._y[0])):
                x_ += [f_x(self._x[i][j], self._y[i][j])]
                y_ += [f_y(self._x[i][j], self._y[i][j])]
                z_ += [f_z(self._x[i][j], self._y[i][j])]
            x += [x_]
            y += [y_]
            z += [z_]

        return x, y, z


class Plot:
    def __init__(self, xx, yy, zz):
        self._xx, self._yy, self._zz = xx, yy, zz
        self._hue_offset, self._hue_gradient, self._omega, self._opacity, self._shininess = .3, .5, pi, 1, .6
        x_min, x_max = min(map(min, xx)), max(map(max, xx))
        y_min, y_max = min(map(min, yy)), max(map(max, yy))
        z_min, z_max = min(map(min, zz)), max(map(max, zz))
        range_x, range_y, range_z = x_max - x_min, y_max - y_min, z_max - z_min
        self._max_range = max(range_x, range_y, range_z)

    def _get_values_for_plot(self, x, y, t):
        value = self._zz[x][y] * (1 - cos(self._omega * t)) * .5
        new_position = vector(self._xx[x][y], value, self._yy[x][y])
        hue = self._hue_gradient * abs(new_position.y) / self._max_range + self._hue_offset
        return new_position, color.hsv_to_rgb(vec(hue, 1, 1.2))

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

class SurfacePlot(Plot):
    def __init__(self, xx, yy, zz):
        Plot.__init__(self, xx, yy, zz)
        self._vertices, self._quads = [], []
        self._create_vertices()
        self._create_quads()

    def _create_vertices(self, t=1):
        for x in range(len(self._xx)):
            for y in range(len(self._yy[0])):
                position, _ = self._get_values_for_plot(x, y, t)
                self._vertices.append(vertex(pos=position, normal=vec(0, 1, 0)))

    def _create_quad(self, x, y):
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (len(self._xx) - 1):
            _neighbor_increment_x = -x
        if y == (len(self._yy[0]) - 1):
            _neighbor_increment_y = -y

        v0 = self._get_vertex(x, y)
        v1 = self._get_vertex(x + _neighbor_increment_x, y)
        v2 = self._get_vertex(x + _neighbor_increment_x, y + _neighbor_increment_y)
        v3 = self._get_vertex(x, y + _neighbor_increment_y)
        self._quads.append(quad(vs=[v0, v1, v2, v3]))

    def _create_quads(self):
        for x in range(len(self._xx) - 2):
            for y in range(len(self._yy[0]) - 2):
                self._create_quad(x, y)

    def _set_vertex_normal_for(self, x, y):
        # OLD NORMAL ALGORITHM
        # if x == len(self._xx) - 1 or y == len(self._yy[0]) - 1: return
        # v = self._get_vertex(x, y)
        # a = self._get_vertex(x, y + 1).pos - v.pos
        # b = self._get_vertex(x + 1, y).pos - v.pos
        # v.normal = cross(a, b)

        # NEW NORMAL ALGORITH
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (len(self._xx) - 1):
            _neighbor_increment_x = -x
        if y == (len(self._yy[0]) - 1):
            _neighbor_increment_y = -y

        vertex_ = self._get_vertex(x, y)
        # # normal_total_ = self._get_vertex(x, y + _neighbor_increment_y).normal
        # # normal_total_ += self._get_vertex(x + _neighbor_increment_x, y).normal
        vec_1 = self._get_vertex(x, y + _neighbor_increment_y).pos - vertex_.pos
        vec_2 = self._get_vertex(x + _neighbor_increment_x, y).pos - vertex_.pos
        # """
        # Further work to focus on this area of the normal calculations
        # """
        vertex_.normal = cross(vec_1, vec_2)
        # # normal_total_ += cross(vec_1, vec_2)
        # # vertex_.normal = normal_total_/2

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        for x in range(len(self._xx) ):
            for y in range(len(self._yy[0])):
                self._set_vertex_normal_for(x, y)

    def _update_vertex(self, x, y, value, colour):
        vertex_ = self._get_vertex(x, y)
        vertex_.pos.y = value
        vertex_.color = colour
        vertex_.opacity = self._opacity
        vertex_.shininess = self._shininess

    def _update_vertices(self, t):
        for x in range(len(self._xx)):
            for y in range(len(self._yy[0])):
                position, colour = self._get_values_for_plot(x, y, t)
                self._update_vertex(x, y, position.y, colour)

    def _get_vertex(self, x, y):
        return self._vertices[x * len(self._yy[0]) + y]

    def render(self, t):
        self._update_vertices(t)
        self._make_normals()

class Figure:
    def __init__(self, canvas_):
        self._subplots = []
        self._hue_offset, self._hue_gradient, self._omega, self._opacity, self._shininess = .3, 1, pi, 1, .6
        self._canvas = canvas_

    def render(self, t):
        for subplot in self._subplots:
            subplot.render(t)

    def render_contour(self, t):
        for subplot in self._subplots:
            subplot.render_contour(t)

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
        self._subplots = []
        self._canvas.delete()
        self._canvas = canvas(x=0, y=0, width=width, height=height, range=60, background=color.gray(0.075), forward=vec(-.82, -1., -.64), center=vec(13, -13, 5))

    def add_subplot(self, x, y, z):
        subplot = SurfacePlot(x, y, z)
        subplot.set_hue_offset_to(self._hue_offset)
        subplot.set_hue_gradient_to(self._hue_gradient)
        subplot.set_omega_to(self._omega)
        subplot.set_opacity_to(self._opacity)
        subplot.set_shininess_to(self._shininess)
        self._subplots.append(subplot)

def interference(resolution=150, wavelength=10.0):
    k = 2 * pi / wavelength  # Wave number
    distance_between_sources = 20.0  # Distance between the two sources
    intensity = 1  # Intensity of the sources
    def f_x(x, _):
        return x

    def f_y(_, y):
        return y

    def f_z(x, y):
        d1 = sqrt((x - distance_between_sources / 2) ** 2 + y ** 2)
        d2 = sqrt((x + distance_between_sources / 2) ** 2 + y ** 2)
        return intensity * (cos(k * d1) + cos(k * d2)) * (cos(k * d1) + cos(k * d2))
    return NumpyWrapper(-50, 50, -50, 50, resolution).get_plot_data(f_x, f_y, f_z)

################
# GUI controls #
################

def adjust_opacity(event):
    figure.set_opacity_to(event.value)
    opacity_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_shininess(event):
    figure.set_shininess_to(event.value)
    shininess_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_wavelength(event):
    figure.reset()  # To make the GUI controls appear on top
    x_, y_, z_ = interference(wavelength=event.value)
    figure.add_subplot(x_, y_, z_)
    wavelength_slider_text.text = "= {:1.2f}".format(event.value)

def adjust_gradient(event):
    figure.set_hue_gradient_to(event.value)
    gradient_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_offset(event):
    figure.set_hue_offset_to(event.value)
    offset_slider_text.text = "= {:1.2f}".format(event.value, 2)

display.append_to_caption("\nHue offset  ")
_ = slider(min=0, max=1, step=0.01, value=.3, bind=adjust_offset)
offset_slider_text = wtext(text="= 0.3")

display.append_to_caption("\n\nHue gradient  ")
_ = slider(min=0, max=1, step=0.01, value=.5, bind=adjust_gradient)
gradient_slider_text = wtext(text="= 0.5")

display.append_to_caption("\n\nWavelength ")
_ = slider(min=5, max=20, value=10, bind=adjust_wavelength)
wavelength_slider_text = wtext(text="= 10")

display.append_to_caption("\n\nOpacity ")
_ = slider(min=0, max=1, step=0.01, value=1, bind=adjust_opacity)
opacity_slider_text = wtext(text="= 1")

display.append_to_caption("\n\nShininess ")
_ = slider(min=0, max=1, step=0.01, value=0.6, bind=adjust_shininess)
shininess_slider_text = wtext(text="= 0.6")
display.append_to_caption("\n\n")

#################################
# COMMENT OUT IN LOCAL VPYTHON  #
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

figure = Figure(display)
figure.reset() # To make the GUI controls appear on top

xx_, yy_, zz_ = interference()
figure.add_subplot(xx_, yy_, zz_)

dt = 0.0
time = 1
while True:
    rate(10)
    figure.render(time)
    time += dt
