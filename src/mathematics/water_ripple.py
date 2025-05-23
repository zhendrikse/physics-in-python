
# Web VPython 3.2

from vpython import *
import numpy as np

animation = canvas()

class NumpyWrapper:
    def __init__(self, start_1, stop_1, start_2, stop_2, resolution):
        self._resolution = resolution
        x = np.linspace(start_1, stop_1, resolution)
        y = np.linspace(start_2, stop_2, resolution)
        self._x, self._y = np.meshgrid(x, y)
        self._convert_back_to_python_arrays()

    def get_plot_data(self, f_x, f_y, f_z):
        x, y, z = [], [], []
        for i in range(len(self._x)):
            x_, y_, z_ = [], [], []
            for j in range(len(self._y[0])):
                x_ += [f_x(self._x, self._y, i, j)]
                y_ += [f_y(self._x, self._y, i, j)]
                z_ += [f_z(self._x, self._y, i, j)]
            x += [x_]
            y += [y_]
            z += [z_]

        return x, y, z

    @staticmethod
    def _convert_back_to_python_array(numpy_array):
        result = []
        for x in range(numpy_array.shape[0]):
            temp = []
            for y in range(numpy_array.shape[1]):
                temp += [numpy_array[x, y]]
            result += [temp]
        return result

    def _convert_back_to_python_arrays(self):
        self._x = self._convert_back_to_python_array(self._x)
        self._y = self._convert_back_to_python_array(self._y)

    def get_x_y(self):
        return self._x, self._y

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
        self.render(zz)

    def hide_plot(self):
        for quad_ in self._quads:
            quad_.visible = False
        for vertex_ in self._vertices:
            vertex_.visible = False

    def _create_vertex(self, x, y):
        x_ = self._xx[x][y] * len(self._xx)
        y_ = self._yy[x][y] * len(self._yy[0])
        self._vertices.append(vertex(pos=vec(x_, 0, y_), normal=vec(0, 1, 0)))

    def _create_vertices(self):
        for x in range(len(self._xx)):
            for y in range(len(self._yy[1])):
                self._create_vertex(x, y)

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

    # Create the quad objects, based on the vertex objects already created.
    def _create_quads(self):
        for x in range(len(self._xx) - 1):
            for y in range(len(self._yy[0]) - 1):
                self._create_quad(x, y)

    def _set_vertex_normal_for(self, x, y):
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (len(self._xx) - 1):
            _neighbor_increment_x = -x
        if y == (len(self._yy[0]) - 1):
            _neighbor_increment_y = -y
        vertex_ = self._get_vertex(x, y)
        #        normal_total_ = self._get_vertex(x, y + _neighbor_increment_y).normal
        #        normal_total_ += self._get_vertex(x + _neighbor_increment_x, y).normal
        vec_1 = self._get_vertex(x, y + _neighbor_increment_y).pos - vertex_.pos
        vec_2 = self._get_vertex(x + _neighbor_increment_x, y).pos - vertex_.pos
        """
        Further work to focus on this area of the normal calculations
        """
        vertex_.gauss = cross(vec_1, vec_2)

    #        normal_total_ += cross(vec_1, vec_2)
    #        vertex_.normal = normal_total_/2

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        for x in range(len(self._xx)):
            for y in range(len(self._yy[1])):
                self._set_vertex_normal_for(x, y)

    def _update_vertex(self, x, y, value):
        hue = .025 / len(self._yy[0]) * self._hue_gradient * abs(value) + self._hue_offset
        vertex_ = self._get_vertex(x, y)
        vertex_.pos.y = value
        vertex_.color = color.hsv_to_rgb(vec(hue, 1, 1))
        vertex_.opacity = self._opacity
        vertex_.shininess = self._shininess

    def _update_vertices(self, new_values):
        for x in range(len(self._xx)):
            for y in range(len(self._yy[0])):
                x_ = self._xx[x][y]
                y_ = self._yy[x][y]
                value = len(self._zz) * new_values[x][y]
                self._update_vertex(x, y, value)

    def _get_vertex(self, x, y):
        return self._vertices[x * len(self._yy[0]) + y]

    def render(self, new_values):
        self._update_vertices(new_values)
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

    def render(self, new_values):
        for subplot in self._subplots:
            subplot.render(new_values)

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


# def adjust_opacity():
#     figure.set_opacity_to(opacity_slider.value)
#
#
# def adjust_shininess():
#     figure.set_shininess_to(shininess_slider.value)
#
#
# def adjust_omega():
#     figure.set_omega_to(omega_slider.value)
#     omega_slider_text.text = "= sin({:1.2f}".format(omega_slider.value / pi, 2) + " π)"
#
#
# def adjust_gradient():
#     figure.set_hue_gradient_to(gradient_slider.value)
#
#
# def adjust_offset():
#     figure.set_hue_offset_to(offset_slider.value)
#
#
# animation.append_to_caption("\nHue offset  ")
# offset_slider = slider(min=0, max=1, value=.25, bind=adjust_offset)
#
# animation.append_to_caption("\n\nHue gradient  ")
# gradient_slider = slider(min=0, max=1, value=.25, bind=adjust_gradient)
#
# animation.append_to_caption("\n\nAnimation speed ")
# omega_slider = slider(min=0, max=3 * pi, value=0, bind=adjust_omega)
# omega_slider_text = wtext(text="= 0")
#
# animation.append_to_caption("\n\nOpacity ")
# opacity_slider = slider(min=0, max=1, step=0.01, value=1, bind=adjust_opacity)
#
# animation.append_to_caption("\n\nShininess ")
# shininess_slider = slider(min=0, max=1, step=0.01, value=0.6, bind=adjust_shininess)
#
# animation.append_to_caption("\n\n")


# def f_x(theta, phi, i, j):
#     return cos(theta[i][j])
#
# def f_y(theta, phi, i, j):
#     return sin(theta[i][j]) + cos(phi[i][j])
#
# def f_z(theta, phi, i, j):
#     return 3 * sin(phi[i][j])
#
# x, y, z = NumpyWrapper(0, pi, 0, pi, 50).get_plot_data(f_x, f_y, f_z)
# figure = Figure()
# figure.add_subplot(SubPlot(x, y, z))


# xx, yy = NumpyWrapper(-2 * pi, 2 * pi, -2 * pi, 2 * pi, 50).get_x_y()
# figure = Figure()
#
# def f_x_y_t(x, y, t):
#     return sin(sqrt(x * x + y * y)) * (cos(t) + 1)
#
# figure.add_subplot(FiniteDifferencePlot(xx, yy, f_x_y_t))
#



# dt = 0.01
# time = 0
# while True:
#     rate(30)
#     figure.render(time)
#     time += dt



class Wave:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._time = 0
        self._initialize_wave_data()
        self._old, self._new, self._now = [], [], []

    def _initialize_wave_data(self):
        self._old = [[0 for j in range(len(self._y))] for i in range(len(self._x))]
        self._now = [[0 for j in range(len(self._y))] for i in range(len(self._x))]
        self._new = [[0 for j in range(len(self._y))] for i in range(len(self._x))]

    def reset(self):
        self._initialize_wave_data()
        self._time = 0

    def update_by(self, dt):
        c = 1.5
        r = (c * dt / dx) * (c * dt / dx)
        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._new[i][j] = (2 * self._now[i][j] - self._old[i][j] +
                                   r * (self._now[i + 1][j] + self._now[i - 1][j] + self._now[i][j + 1] + self._now[i][
                            j - 1] - 4 * self._now[i][j]))
                self._old[i][j] = self._now[i][j]

        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._y) - 1):
                self._now[i][j] = self._new[i][j]

        if abs(self._time - 0.25) < dt:  # introducing a disturbance
            disturbance_magnitude = 20
            self._now[len(self._x) // 2][len(self._y) // 2] += disturbance_magnitude

        self._time += dt

    def current_values(self):
        return self._now

    def get_time(self):
        return self._time

class Pool:
    def __init__(self, x, y):
        self._x, self._y = x, y
        self._surface = [[0. for _ in range(len(self._y))] for _ in range(len(self._x))]
        self._hue = .55
    #     self._init_pool()
    #
    # def _init_pool(self):
    #     water = box(pos=vec(Lx / 2, Ly / 2, -.1), width=.15, length=Lx, height=Ly, color=vec(0, .6, 1), opacity=0.6)
    #     back = box(pos=vec(dx, Ly / 2 + dy, 0), width=.4, length=.04, height=Ly, color=color.yellow)
    #     left = box(pos=vec(Lx / 2, 0, 0), width=.4, length=.04, height=Ly + dy, color=color.yellow)
    #     left.rotate(angle=radians(90), axis=vec(0, 0, 1))
    #     right = box(pos=vec(Lx / 2, Ly, 0), width=.4, length=.04, height=Ly + dy, color=color.yellow)
    #     right.rotate(angle=radians(90), axis=vec(0, 0, 1))
    #     bottom = box(pos=vec(Lx / 2, Ly / 2, -.2), width=0.04, length=Lx + dx, height=Ly + dy, color=color.yellow)

    def reset(self):
        self._surface = [[0. for _ in range(len(self._y))] for _ in range(len(self._x))]

    def update_by(self, dt):
        new_values = wave.current_values()
        for i in range(1, len(self._x) - 1):
            for j in range(1, len(self._x) - 1):
                self._surface[i][j] = new_values[i][j]  # Updating the z position of the surface points

    def set_hue_value_to(self, new_hue_value):
        self._hue = new_hue_value

    def get_current_values(self):
        return self._surface


def adjust_offset():
    figure.set_hue_offset_to(offset_slider.value)
    hue_offset_text.text = "{:1.2f}".format(offset_slider.value, 2)


Lx, Ly = 2, 2  # TODO: non-square!!


animation.append_to_caption("\n")
offset_slider = slider(min=0, max=1, value=.6, bind=adjust_offset)
animation.append_to_caption("hue offset = ")
hue_offset_text = wtext(text="0.55")
#popup = text(text="Click mouse to start", pos=vec(-Lx / 2, 0, Ly / 3), billboard=True, color=color.yellow, height=.3)
animation_duration = 5  # seconds

animation.append_to_caption("\n\n  Remaining animation time = ")
clock = wtext(text="{:1.2f}".format(animation_duration, 2))


dx, dy = 0.1, 0.1
x_range = arange(0, Lx + dx, dx)
y_range = arange(0, Ly + dy, dy)
wave = Wave(x_range, y_range)
pool = Pool(x_range, y_range)

# x, y, z = NumpyWrapper(0, pi, 0, pi, 50).get_plot_data(f_x, f_y, f_z)
def f_x(theta, phi, i, j):
    return 200 * theta[i][j]

def f_y(theta, phi, i, j):
    return 200 * phi[i][j]

def f_z(theta, phi, i, j):
    return 0
#
x, y, z = NumpyWrapper(0, Lx + dx, 0, Ly + dy, 41).get_plot_data(f_x, f_y, f_z)

#x, y = NumpyWrapper(0, Lx + dx, 0, Ly + dy , 41).get_x_y()
#z = pool.get_current_values()
figure = Figure()
figure.add_subplot(SubPlot(x, y, z))

# The Time-loop
dt = 0.01
while True:
    #popup.visible = True
    animation.waitfor("click")
    #popup.visible = False
    wave.reset()
    pool.reset()
    for _ in range(int(animation_duration / dt)):
        rate(20)#rate(1 / (2 * dt))
        wave.update_by(dt)
        pool.update_by(dt)
        figure.render(pool.get_current_values())
        clock.text = "{:1.2f}".format(animation_duration - wave.get_time(), 2)