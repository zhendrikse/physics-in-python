#Web VPython 3.2

from vpython import *

animation = canvas(height=500, background=color.gray(0.075), forward=vec(-1.0, -0.71, -.78))

class ComplexNumber:
    def __init__(self, re, im):
        self._re = re
        self._im = im

    def re(self): return self._re
    def im(self): return self._im
    def phase(self): return atan2(self.im(), self.re())
    def abs(self): return sqrt(self.re() * self.re() + self.im() * self.im())

class MathWrapper:
    def __init__(self):
      self.complex = self._complex
      self.add, self.subtract, self.multiply, self.divide = self._add, self._subtract, self._multiply, self._divide
      self.sqrt, self.log, self.exp, self.sin, self.cos = self._sqrt, self._log, self._exp, self._sin, self._cos

    def _complex(self, re, im):
      return ComplexNumber(re, im)
    def _add(self, z1, z2):
      return ComplexNumber(z1.re() + z2.re(), z1.im() + z2.im())
    def _subtract(self, z1, z2):
      return ComplexNumber(z1.re() - z2.re(), z1.im() - z2.im())
    def _log(self, z):
      return ComplexNumber(log(z.abs()), atan2(z.im(), z.re()))
    def _exp(self, z):
      return ComplexNumber(exp(z.re()) * cos(z.im()), exp(z.re()) * sin(z.im()))
    def _sin(self, z):
        i_z = self.multiply(z, ComplexNumber(0, 1))
        min_i_z = self.multiply(z, ComplexNumber(0, -1))
        return math.multiply(ComplexNumber(0, -.5), self.exp(self.subtract(i_z, min_i_z)))

    def _cos(self, z):
        i_z = self.multiply(z, ComplexNumber(0, 1))
        min_i_z = self.multiply(z, ComplexNumber(0, -1))
        return math.multiply(ComplexNumber(.5, 0), self.exp(self.add(i_z, min_i_z)))

    def _multiply(self, z1, z2):
        return ComplexNumber(z1.re() * z2.re() - z1.im() * z2.im(), z1.im() * z2.re() + z1.re() * z2.im())

    def _divide(self, z1, z2):
        denominator = z2.re() * z2.re() + z2.im() * z2.im()
        re = z1.re() * z2.re() + z1.im() * z2.im()
        im = z1.im() * z2.re() - z1.re() * z2.im()
        return ComplexNumber(re / denominator, im / denominator)

    def _sqrt(self, z):
        factor = sqrt((z.abs() + z.re())/2)
        return ComplexNumber(factor, factor * (z.im() / abs(z.im())))

math = MathWrapper()


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


x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]


class Base:
    def __init__(self, xx, yy, zz, axis_color, tick_marks_color, num_tick_marks):
        x_min, x_max = min(map(min, xx)), max(map(max, xx))
        y_min, y_max = min(map(min, yy)), max(map(max, yy))
        z_min, z_max = min(map(min, zz)), max(map(max, zz))
        range_x, range_y, range_z = x_max - x_min, y_max - y_min, z_max - z_min
        max_of_base = max(range_x, range_y, range_z)
        delta = max_of_base / num_tick_marks
        position = vec(x_min, z_min, y_min)
        radius = max_of_base / 200

        self._mesh = []
        self._create_mesh(delta, max_of_base, num_tick_marks, position, radius)

        self._tick_marks = []
        self._create_tick_marks(delta, max_of_base, num_tick_marks, position, tick_marks_color, x_min, y_min, z_min)

        self._axis_labels = []
        pos = position + x_hat * (max_of_base + 2.5 * delta) + .5 * max_of_base * z_hat
        self._axis_labels += [label(pos=pos, text="Im(z)", color=axis_color, box=False)]
        pos = position + z_hat * (max_of_base + 2.5 * delta) + .5 * max_of_base * y_hat
        self._axis_labels += [label(pos=pos, text="|F(z)|", color=axis_color, box=False)]
        pos = position + z_hat * (max_of_base + 2.5 * delta) + .5 * max_of_base * x_hat
        self._axis_labels += [label(pos=pos, text="Re(z)", color=axis_color, box=False)]

    def _create_tick_marks(self, delta, max_of_base, num_tick_marks, position, tick_marks_color, x_min, y_min, z_min):
        increment = max_of_base / num_tick_marks
        for i in range(1, num_tick_marks, 2):
            # Tick marks X
            label_text = '{:1.2f}'.format(x_min + i * increment, 2)
            pos = position + x_hat * i * delta + z_hat * (max_of_base + .75 * delta)
            self._tick_marks.append(label(pos=pos, text=label_text, color=tick_marks_color, box=False))
            # Tick marks Y
            label_text = '{:1.2f}'.format(y_min + i * increment, 2)
            pos = position + z_hat * i * delta + x_hat * (max_of_base + .75 * delta)
            self._tick_marks.append(label(pos=pos, text=label_text, color=tick_marks_color, box=False))
            # Tick marks Z
            label_text = '{:1.2f}'.format(z_min + i * increment, 2)
            pos = position + y_hat * i * delta + z_hat * (max_of_base + .75 * delta)
            self._tick_marks.append(label(pos=pos, text=label_text, color=tick_marks_color, box=False))

    def _create_mesh(self, delta, max_of_base, num_tick_marks, position, radius):
        for i in range(num_tick_marks + 1):
            # XY-mesh (lies in VPython xz-plane)
            self._mesh += [cylinder(pos=position + z_hat * delta * i, axis=max_of_base * x_hat)]
            self._mesh += [cylinder(pos=position + x_hat * delta * i, axis=max_of_base * z_hat)]
            # YZ-mesh (lies in VPython zy-plane)
            self._mesh += [cylinder(pos=position + z_hat * delta * i, axis=max_of_base * y_hat)]
            self._mesh += [cylinder(pos=position + y_hat * delta * i, axis=max_of_base * z_hat)]
            # XZ-mesh (lies in VPython xy-plane)
            self._mesh += [cylinder(pos=position + x_hat * delta * i, axis=max_of_base * y_hat)]
            self._mesh += [cylinder(pos=position + y_hat * delta * i, axis=max_of_base * x_hat)]
        for item in self._mesh:
            item.color = color.gray(.5)
            item.radius = radius

        pos = position + (x_hat + y_hat) * .5 * max_of_base
        self._mesh += [box(pos=pos, length=max_of_base, width=radius, height=max_of_base, opacity=0.05)]
        pos = position + (x_hat + z_hat) * .5 * max_of_base
        self._mesh += [box(pos=pos, length=max_of_base, width=max_of_base, height=radius, opacity=0.05)]
        pos = position + (y_hat + z_hat) * .5 * max_of_base
        self._mesh += [box(pos=pos, length=radius, width=max_of_base, height=max_of_base, opacity=0.05)]

    def tick_marks_visibility_is(self, visible):
        for tick_mark in self._tick_marks:
            tick_mark.visible = visible

    def mesh_visibility_is(self, visible):
        for i in range(len(self._mesh)):
            self._mesh[i].visible = visible

    def axis_labels_visibility_is(self, visible):
        for i in range(len(self._axis_labels)):
            self._axis_labels[i].visible = visible


class Plot:
    def __init__(self, xx, yy, abs_z, phase_z):
        self._xx, self._yy, self._abs_z, self._phase_z = xx, yy, abs_z, phase_z
        self._omega, self._opacity, self._shininess = pi, 1, .6
        x_min, x_max = min(map(min, xx)), max(map(max, xx))
        y_min, y_max = min(map(min, yy)), max(map(max, yy))
        z_min, z_max = min(map(min, abs_z)), max(map(max, abs_z))
        range_x, range_y, range_z = x_max - x_min, y_max - y_min, z_max - z_min
        self._max_range = max(range_x, range_y, range_z)

    def _get_values_for_plot(self, x, y, t):
        phase = self._phase_z[x][y] + self._omega * t
        phase += 2 * pi if phase < 0 else 0
        phase /= 2 * pi
        colour = color.hsv_to_rgb(vec(phase, 1, 1.2))

        new_position = vector(self._xx[x][y], self._abs_z[x][y], self._yy[x][y])
        return new_position, colour

    def set_omega_to(self, omega):
        self._omega = omega

    def set_opacity_to(self, opacity):
        self._opacity = opacity

    def set_shininess_to(self, shininess):
        self._shininess = shininess


class ContourPlot(Plot):
    def __init__(self, xx, yy, abs_z, phase_z):
        Plot.__init__(self, xx, yy, abs_z, phase_z)
        self._x_contours, self._y_contours = [], []
        self._initialize_contour_curves()

    def _initialize_contour_curves(self, t=1):
        positions = []
        position_col = [[] for _ in range(len(self._yy[0]))]
        for i in range(len(self._xx)):
            position_row = []
            for j in range(len(self._yy[0])):
                position, _ = self._get_values_for_plot(i, j, t)
                position_row.append(position)
                position_col[j].append(position)
            positions.append(position_row)
            self._x_contours.append(curve(pos=position_row, radius=self._max_range / 250))

        for i in range(len(position_col)):
            self._y_contours.append(curve(pos=position_col[i], radius=self._max_range / 250))

    def _render_contours(self, x, y, t):
        position, colour = self._get_values_for_plot(x, y, t)
        self._x_contours[x].modify(y, color=colour)
        self._y_contours[y].modify(x, color=colour)
        self._x_contours[x].modify(y, pos=position)
        self._y_contours[y].modify(x, pos=position)

    def render(self, t):
        for x in range(len(self._xx)):
            for y in range(len(self._yy[0])):
                self._render_contours(x, y, t)


# This class is only meant to be used from within the Figure class.
class SurfacePlot(Plot):
    def __init__(self, xx, yy, abs_z, phase_z):
        Plot.__init__(self, xx, yy, abs_z, phase_z)
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

    # Create the quad objects, based on the vertex objects already created.
    #
    # When removing the "-1", opposite ends will be glued together
    #
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
        for x in range(len(self._xx)):
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
    def __init__(self, canvas_, axis_color=color.yellow, tick_marks_color=vec(0.4, 0.8, 0.4), num_tick_marks=10):
        self._subplots = []
        self._omega, self._opacity, self._shininess = pi, 1, .6
        self._axis_color, self._tick_marks_color, self._num_tick_marks = axis_color, tick_marks_color, num_tick_marks
        self._base = None
        self._tick_marks_visible, self._mesh_visible, self._axis_labels_visible, self._plot_contours = True, True, False, False
        self._canvas = canvas_

    def _create_base(self, xx, yy, zz):
        axis = Base(xx, yy, zz, self._axis_color, self._tick_marks_color, self._num_tick_marks)
        axis.mesh_visibility_is(self._mesh_visible)
        axis.axis_labels_visibility_is(self._axis_labels_visible)
        axis.tick_marks_visibility_is(self._tick_marks_visible)
        return axis

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

    def set_opacity_to(self, opacity):
        self._opacity = opacity
        for subplot in self._subplots:
            subplot.set_opacity_to(opacity)

    def set_shininess_to(self, shininess):
        self._shininess = shininess
        for subplot in self._subplots:
            subplot.set_shininess_to(shininess)

    def tick_marks_visibility_is(self, visible):
        self._tick_marks_visible = visible
        self._base.tick_marks_visibility_is(visible)

    def mesh_visibility_is(self, visible):
        self._mesh_visible = visible
        self._base.mesh_visibility_is(visible)

    def axis_labels_visibility_is(self, visible):
        self._axis_labels_visible = visible
        self._base.axis_labels_visibility_is(visible)

    def reset(self):
        self._subplots = []
        self._canvas.delete()
        self._canvas = canvas(x=0, y=0, height=500, center=vec(0, 1, 0), background=color.gray(0.075), forward=vec(-1.0, -0.71, -.78))

    def plot_contours_is(self, bool_value):
        self._plot_contours = bool_value

    def _transform(self, z):
        abs_z, phase_z = [], []
        for i in range(len(z)):
            abs_temp, phase_temp = [], []
            for j in range(len(z[0])):
                abs_temp.append(z[i][j].abs())
                phase_temp.append(z[i][j].phase())
            abs_z.append(abs_temp)
            phase_z.append(phase_temp)
        return abs_z, phase_z

    def add_subplot(self, x, y, z):
        abs_z, phase_z = self._transform(z)

        if self._plot_contours:
            subplot = ContourPlot(x, y, abs_z, phase_z)
        else:
            subplot = SurfacePlot(x, y, abs_z, phase_z)

        subplot.set_omega_to(self._omega)
        subplot.set_opacity_to(self._opacity)
        subplot.set_shininess_to(self._shininess)
        self._subplots.append(subplot)

        if len(self._subplots) == 1:
            self._base = self._create_base(x, y, abs_z)


class RadioButton:
    def __init__(self, button_, function_, title_text):
        self._button = button_
        self._function = function_
        self._explanation = title_text

    def uncheck(self):
        self._button.checked = False

    def push(self):
        xx, yy, zz = self._function()
        figure.reset()
        figure.add_subplot(xx, yy, zz)  #
        animation.title = self._explanation + "\n\n"

        #################################
        # COMMENT OUT IN LOCAL VPYTHON  #
        #MathJax.Hub.Queue(["Typeset", MathJax.Hub])

    def check(self):
        self._button.checked = True

    def name(self):
        return self._button.name


class RadioButtons:
    def __init__(self):
        self._radio_buttons = []
        self._selected_button = None

    def add(self, button_, function_, title_text):
        self._radio_buttons.append(RadioButton(button_, function_, title_text))

        if (len(self._radio_buttons) % 5) == 0:
            animation.append_to_caption("\n\n")

        if (len(self._radio_buttons)) == 1:
            self._radio_buttons[0].check()
            self._selected_button = self._radio_buttons[0]

    def _uncheck_buttons_except(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() != button_name: button_.uncheck()

    def _get_button_by(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() == button_name: return button_

    def toggle(self, button_name):
        self._uncheck_buttons_except(button_name)
        self._selected_button = self._get_button_by(button_name)
        self._selected_button.push()

    def get_selected_button_name(self):
        return self._selected_button.name()


###############################
# Complex functions F(z) => C #
###############################

z_squared_plus_2_title = "$\\psi(z) = \\big(z^2 + 2\\big)$"
def z_squared_plus_2(resolution=40):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.multiply(math.add(math.multiply(z, z), math.complex(2, 0)), math.complex(.5, 0))

    return NumpyWrapper(-2, 2, -2, 2, resolution).get_plot_data(f_x, f_y, f_z)


z_abs_squared_title = "$\\psi(z) = z\\bar{z}$"
def z_abs_squared(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.multiply(math.multiply(z, ComplexNumber(z.re(), -z.im())), math.complex(0.5, 0))

    return NumpyWrapper(-2, 2, -2, 2, resolution).get_plot_data(f_x, f_y, f_z)

z_cubed_title = "$\\psi(z) = \\big(z^3 + 2\\big)$"
def z_cubed(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.multiply(math.add(math.multiply(z, math.multiply(z, z)), ComplexNumber(2, 0)), math.complex(0.2, 0))

    return NumpyWrapper(-2, 2, -2, 2, resolution).get_plot_data(f_x, f_y, f_z)

log_z_title = "$\\psi(z) = \\log{(z)}$"
def log_z(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.multiply(ComplexNumber(2, 0), math.log(z))

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)

exp_z_title = "$\\psi(z) = e^{-z^2}$"
def exp_z(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.exp(math.multiply(math.multiply(z, z), math.complex(-1, 0)))

    return NumpyWrapper(-1, 1, -1, 1, resolution).get_plot_data(f_x, f_y, f_z)

sqrt_z_title = "$\\psi(z) = \\sqrt{z}$"
def sqrt_z(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.sqrt(z)

    return NumpyWrapper(-1, 1, -1, 1, resolution).get_plot_data(f_x, f_y, f_z)

sine_z_title = "$\\psi(z) = \\sin{(z)}$"
def sin_z(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.multiply(ComplexNumber(.025, 0), math.sin(z))

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)

z_plus_one_over_z_title = "$\\psi(z) = z + \\bigg(\\dfrac{1}{z}\\bigg)$"
def z_plus_one_over_z(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        return math.multiply(math.complex(.5, 0), math.add(z, math.divide(math.complex(1, 0), z)))

    return NumpyWrapper(-3, 3, -3, 3, resolution).get_plot_data(f_x, f_y, f_z)

z_plus_1_divided_by_z_min_1_title = "$\\psi(z) = \\bigg(\\dfrac{z + 1}{z - 1} \\bigg)$"
def z_plus_1_divided_by_z_min_1(resolution=50):
    def f_x(re, _):
        return re

    def f_y(_, im):
        return im

    def f_z(re, im):
        z = math.complex(re, im)
        value = math.add(math.complex(1, 0), z)
        return math.multiply(ComplexNumber(0.4, 0), math.divide(value, math.add(math.complex(-1, 0), z)))

    return NumpyWrapper(-4, 4, -4, 4, resolution).get_plot_data(f_x, f_y, f_z)

################
# GUI controls #
################

def toggle(event):
    radio_buttons.toggle(event.name)


radio_buttons = RadioButtons()
radio_buttons.add(radio(bind=toggle, text=" $z^2 + 2$ ", name="z_squared_plus_2"), z_squared_plus_2, z_squared_plus_2_title)
radio_buttons.add(radio(bind=toggle, text=" $z\\bar{z}$ ", name="z_abs_squared"), z_abs_squared, z_abs_squared_title)
radio_buttons.add(radio(bind=toggle, text=" $z^3 + 2$ ", name="z_cubed"), z_cubed, z_cubed_title)
radio_buttons.add(radio(bind=toggle, text=" $\\dfrac{z + 1}{z - 1}$ ", name="z_plus_1_divided_by_z_min_1"), z_plus_1_divided_by_z_min_1, z_plus_1_divided_by_z_min_1_title)
radio_buttons.add(radio(bind=toggle, text=" $z + \\dfrac{1}{z}$", name="z_plus_one_over_z"), z_plus_one_over_z, z_plus_one_over_z_title)
radio_buttons.add(radio(bind=toggle, text=" $\\sin(z)$ ", name="sine"), sin_z, sine_z_title)
radio_buttons.add(radio(bind=toggle, text=" $\\log(z)$ ", name="log"), log_z, log_z_title)
radio_buttons.add(radio(bind=toggle, text=" $\\exp(z)$ ", name="exp"), exp_z, exp_z_title)
radio_buttons.add(radio(bind=toggle, text=" $\\sqrt{z}$ ", name="sqrt"), sqrt_z, sqrt_z_title)


def adjust_opacity(event):
    figure.set_opacity_to(event.value)
    opacity_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_shininess(event):
    figure.set_shininess_to(event.value)
    shininess_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_omega(event):
    figure.set_omega_to(event.value)
    omega_slider_text.text = "= {:1.2f}".format(event.value / pi, 2) + " π"

animation.append_to_caption("\n\nAnimation speed ")
_ = slider(min=0, max=2 * pi, value=pi, bind=adjust_omega)
omega_slider_text = wtext(text="= π")

animation.append_to_caption("\n\nOpacity ")
_ = slider(min=0, max=1, step=0.01, value=1, bind=adjust_opacity)
opacity_slider_text = wtext(text="= 1")

animation.append_to_caption("\n\nShininess ")
_ = slider(min=0, max=1, step=0.01, value=0.6, bind=adjust_shininess)
shininess_slider_text = wtext(text="= 0.6")


def toggle_tick_marks(event):
    figure.tick_marks_visibility_is(event.checked)


def toggle_axis_labels(event):
    figure.axis_labels_visibility_is(event.checked)


def toggle_mesh(event):
    figure.mesh_visibility_is(event.checked)


def toggle_animate(event):
    global dt
    dt = 0.01 if event.checked else 0


def toggle_plot_type(event):
    figure.plot_contours_is(event.checked)


animation.append_to_caption("\n\n")
_ = checkbox(text="Contour", bind=toggle_plot_type, checked=False)
_ = checkbox(text='Mesh ', bind=toggle_mesh, checked=True)
_ = checkbox(text='Axis labels ', bind=toggle_axis_labels, checked=False)
_ = checkbox(text='Tick marks ', bind=toggle_tick_marks, checked=True)
_ = checkbox(text='Animate ', bind=toggle_animate, checked=False)
animation.append_to_caption("\n\n")

animation.title = z_squared_plus_2_title + "\n\n"
#################################
# COMMENT OUT IN LOCAL VPYTHON  #
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

figure = Figure(animation)
figure.reset() # To make the GUI controls appear on top

xx_, yy_, zz_ = z_squared_plus_2()
figure.add_subplot(xx_, yy_, zz_)

dt = 0.0
time = 1
while True:
    rate(10)
    figure.render(time)
    time += dt
