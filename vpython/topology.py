#Web VPython 3.2

from vpython import *

animation = canvas(height=500, background=color.gray(0.075), forward=vec(-1.0, -0.71, -.78))

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
        self._axis_labels += [label(pos=pos, text="Y-axis", color=axis_color, box=False)]
        pos = position + z_hat * (max_of_base + 2.5 * delta) + .5 * max_of_base * y_hat
        self._axis_labels += [label(pos=pos, text="Z-axis", color=axis_color, box=False)]
        pos = position + z_hat * (max_of_base + 2.5 * delta) + .5 * max_of_base * x_hat
        self._axis_labels += [label(pos=pos, text="X-axis", color=axis_color, box=False)]

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
        self._mesh += [box(pos=pos, length=max_of_base, width=radius, height=max_of_base,opacity=0.05)]
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

class ContourPlot(Plot):
    def __init__(self, xx, yy, zz):
        Plot.__init__(self, xx, yy, zz)
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
            self._x_contours.append(curve(pos=position_row, radius=self._max_range/250))

        for i in range(len(position_col)):
            self._y_contours.append(curve(pos=position_col[i], radius=self._max_range/250))

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
        vertex_.normal = cross(vec_1, vec_2)

    #        normal_total_ += cross(vec_1, vec_2)
    #        vertex_.normal = normal_total_/2

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
        self._hue_offset, self._hue_gradient, self._omega, self._opacity, self._shininess = .3, .5, pi, 1, .6
        self._axis_color, self._tick_marks_color, self._num_tick_marks = axis_color, tick_marks_color, num_tick_marks
        self._base = None
        self._tick_marks_visible, self._mesh_visible, self._axis_labels_visible, self._plot_contours = False, False, False, False
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
        self._canvas = canvas(x=0, y=0, height=600, background=color.gray(0.075), forward=vec(-1.0, -0.71, -.78))

    def plot_contours_is(self, bool_value):
        self._plot_contours = bool_value

    def add_subplot(self, x, y, z):
        if self._plot_contours:
            subplot = ContourPlot(x, y, z)
        else:
            subplot = SurfacePlot(x, y, z)

        subplot.set_hue_offset_to(self._hue_offset)
        subplot.set_hue_gradient_to(self._hue_gradient)
        subplot.set_omega_to(self._omega)
        subplot.set_opacity_to(self._opacity)
        subplot.set_shininess_to(self._shininess)
        self._subplots.append(subplot)

        if len(self._subplots) == 1:
            self._base = self._create_base(x, y, z)


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
        figure.add_subplot(xx, yy, zz) #
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

        if (len(self._radio_buttons) % 6) == 0:
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


###################################
# Topological / volumetric shapes #
###################################

arc_title = "Parametrization for arc $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) \\\\  \\sin(\\theta)+\\cos(\\phi) \\\\ 3\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, \\pi] \\\\ \\phi \\in [0, \\pi] \\end{cases}$"
def arc(resolution=50):
    def f_x(theta, _):
        return cos(theta)

    def f_y(theta, phi):
        return sin(theta) + cos(phi)

    def f_z(_, phi):
        return 3 * sin(phi)

    return NumpyWrapper(0, pi, 0, pi, resolution).get_plot_data(f_x, f_y, f_z)

bow_curve_title = "<a href=\"https://paulbourke.net/geometry/spiral/\">Paul Bourke&apos;s</a> parametrization for Bow curve $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (2 + T \\sin(2 \\pi \\theta)) \\sin(4 \\pi \\phi) \\\\  (2 + T \\sin(2 \\pi \\theta)) \\cos(4 \\pi \\phi) \\\\ T \\cos(2 \\pi \\theta) + 3 \\cos(2 \\pi \\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 1] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def bow_curve(resolution=100, t=1):
    def f_x(theta, phi):
        return (3 + t * sin(2 * pi * theta)) * sin(4 * pi * phi)

    def f_y(theta, phi):
        return (3 + t * sin(2 * pi * theta)) * cos(4 * pi * phi)

    def f_z(theta, phi):
       return t * cos(2 * pi * theta) + 3 * cos(2 * pi * phi)

    return NumpyWrapper(0, 1, 0, 1, resolution).get_plot_data(f_x, f_y, f_z)


# https://doc.sagemath.org/html/en/reference/plot3d/sage/plot/plot3d/parametric_plot3d.html
boys_surface_title = "With $K = \\dfrac{\\cos(\\theta)}{\\sqrt{2} - \\cos(2\\theta)\\sin(3\\phi)}$, $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} K (\\cos(\\theta)\\cos(2\\phi)+\\sqrt{2}\\sin(\\theta)\\cos(\\phi)) \\\\  K (\\cos(\\theta)\\sin(2\\phi)-\\sqrt{2}\\sin(\\theta)sin(\\phi)) \\\\ 3K \\cos(\\theta) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-2\\pi, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def boys_surface(resolution=100):
    def f_x(theta, phi):
        k = cos(theta) / (sqrt(2) - cos(2 * theta)*sin(3 * phi))
        return k * (cos(theta) * cos(2 * phi) + sqrt(2) * sin(theta) * cos(phi))

    def f_y(theta, phi):
        k = cos(theta) / (sqrt(2) - cos(2 * theta)*sin(3 * phi))
        return k * (cos(theta) * sin(2 * phi) - sqrt(2) * sin(theta) * sin(phi))

    def f_z(theta, phi):
        k = cos(theta) / (sqrt(2) - cos(2 * theta)*sin(3 * phi))
        return 1 * k * cos(theta)

    return NumpyWrapper(-2 * pi, 2 * pi, 0, pi, resolution).get_plot_data(f_x, f_y, f_z)

bubbles_title = "Parametrization for bubbles $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)\\sin(2\\phi) \\\\  \\sin(\\theta)\\sin(2\\phi) \\\\ \\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def bubbles(resolution=50):
    def f_x(theta, phi):
        return cos(theta) * sin(2 * phi)

    def f_y(theta, phi):
        return sin(theta) * sin(2 * phi)

    def f_z(_, phi):
        return sin(phi)

    return NumpyWrapper(-pi / 4, 3.01 * pi / 4, 0, 2 * pi, resolution).get_plot_data(f_x, f_y, f_z)


# https://paulbourke.net/geometry/spiral/
conchoidal_title = "<a href=\"https://paulbourke.net/geometry/spiral/\">Paul Bourke&apos;s</a> parametrization for a conchoidal$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} a\\left(1-\\dfrac{\\theta}{2\\pi}\\right)\\cos(n\\theta)(1+\\cos(\\phi))+c\\cos(n\\theta) \\\\  a\\left(1-\\dfrac{\\theta}{2\\pi}\\right)\\sin(n\\theta)(1+\\cos(\\phi))+c\\sin(n\\theta) \\\\ b\\dfrac{\\theta}{2\\pi}+a\\left(1-\\frac{\\theta}{2\\pi}\\right)\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def conchoidal(resolution=100, num_spirals=3, r_final=2, height=6.5, r_inner=.5):
    def f_x(s, t):
        return r_final * (1 - t / (2 * pi)) * cos(num_spirals * t) * (1 + cos(s)) + r_inner * cos(num_spirals * t)

    def f_y(s, t):
        return r_final * (1 - t / (2 * pi)) * sin(num_spirals * t) * (1 + cos(s)) + r_inner * sin(num_spirals * t)

    def f_z(s, t):
        return (height * t / (2 * pi)) + r_final * (1 - t / (2 * pi)) * sin(s)

    return NumpyWrapper(0, 2 * pi, 0, 2 * pi, resolution).get_plot_data(f_x, f_y, f_z)

conchoidal_2_title = "Conchoidal $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} a\\left(1-\\dfrac{\\theta}{2\\pi}\\right)\\cos(n\\theta)(1+\\cos(\\phi))+c\\cos(n\\theta) \\\\  a\\left(1-\\dfrac{\\theta}{2\\pi}\\right)\\sin(n\\theta)(1+\\cos(\\phi))+c\\sin(n\\theta) \\\\ b\\dfrac{\\theta}{2\\pi}+a\\left(1-\\frac{\\theta}{2\\pi}\\right)\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def conchoidal_2(resolution=100, k=1.2, k_2=1.2, a=1.5):
    def f_x(theta, phi):
        return k ** theta * (1 + cos(phi)) * cos(theta)

    def f_y(theta, phi):
        return k ** theta * (1 + cos(phi)) * sin(theta)

    def f_z(theta, phi):
        return k ** theta * sin(phi) - a * k_2 ** theta

    return NumpyWrapper(0, 6 * pi, 0, 2 * pi, resolution).get_plot_data(f_x, f_y, f_z)

cross_cap_title = "<a href=\"https://paulbourke.net/geometry/crosscap/\">Paul Bourke&apos;s parametrization</a> for a <a href=\"https://mathworld.wolfram.com/Cross-Cap.html\">cross cap</a> $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) \\sin(2\\phi) \\\\  \\sin(\\theta) \\sin(2\\phi) \\\\ \\cos(\\phi)\\cos(\\phi) - \\cos(\\theta)\\cos(\\theta)\\sin(\\phi)\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
def cross_cap(resolution=50):
    def f_x(theta, phi):
        return .5 * cos(theta) * sin(2 * phi)

    def f_y(theta, phi):
        return .5 * sin(theta) * sin(2 * phi)

    def f_z(theta, phi):
        return .5 * cos(phi) * cos(phi) -.5  * cos(theta) * cos(theta) * sin(phi) * sin(phi)

    return NumpyWrapper(-pi, pi, 0, pi/2, resolution).get_plot_data(f_x, f_y, f_z)

dented_title = "Parametrization for dented surface $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) \\\\  \\sin(\\theta)+\\cos(\\phi) \\\\ 3\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def dented(resolution=50):
    def f_x(theta, _):
        return cos(theta)

    def f_y(theta, phi):
        return sin(theta) + cos(phi)

    def f_z(_, phi):
        return 1.5 * sin(phi)

    return NumpyWrapper(-pi, pi, 0, 2 * pi, resolution).get_plot_data(f_x, f_y, f_z)

spiral_title = "Parametrization for <a href=\"https://en.wikipedia.org/wiki/Dini%27s_surface\">Dini&apos;s spiral</a> $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)\\sin(\\phi) \\\\  \\sin(\\theta)\\sin(\\phi) \\\\  \\cos(\\phi)+\\log(\\tan(\\phi/2)) + 0.2\\theta \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 12.4] \\\\ \\phi \\in [0.1, 2] \\end{cases}$"
def dinis_spiral(resolution=100, k=.5):
    def f_x(theta, phi):
        return 2 * cos(theta) * sin(phi)

    def f_y(theta, phi):
        return 2 * sin(theta) * sin(phi)

    def f_z(theta, phi):
        return cos(phi) + log(tan(k * phi)) + .2 * theta

    return NumpyWrapper(0, 12.4, 0.1, 2, resolution).get_plot_data(f_x, f_y, f_z)


elliptic_torus_title = "<a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for an elliptic torus $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (c + \\cos(\\phi)) \\cos(\\theta) \\\\  (c + \\cos(\\phi)) \\sin(\\theta) \\\\ \\sin(\\phi) + \\cos(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
def elliptic_torus(a=1.2, c=3.5, resolution=50):
    def f_x(theta, phi):
        return (a * cos(phi) + c) * cos(theta)

    def f_y(theta, phi):
        return (a * cos(phi) + c) * sin(theta)

    def f_z(_, phi):
        return a * (sin(phi) + cos(phi))

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)

limpet_torus_title = "<a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for a limpet torus $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) / (\\sqrt{2} + \\sin(\\phi)) \\\\  \\sin(\\theta) / (\\sqrt{2} + \\sin(\\phi)) \\\\ 1 / (\\sqrt{2} + \\cos(\\phi)) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
def limpet_torus(resolution=50):
    def f_x(theta, phi):
        return cos(theta) / (sin(phi) + sqrt(2))

    def f_y(x, y):
        return sin(x) / (sin(y) + sqrt(2))

    def f_z(_, y):
        return 1 / (cos(y) + sqrt(2))

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)

mobius_title = "Parametrization for <a href=\"https://en.wikipedia.org/wiki/M%C3%B6bius_strip\">Möbius strip</a> $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)(1+\\phi\\cos(\\theta/2)) \\\\  \\sin(\\theta)(1+\\phi\\cos(\\theta/2)) \\\\ 0.2\\phi\\sin(\\theta/2) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 4\\pi + 0.5] \\\\ \\phi \\in [0, 0.3] \\end{cases}$"
def mobius_strip(resolution=50):
    def f_x(theta, phi):
        return (cos(.5 * theta) * phi + 1) * cos(theta)

    def f_y(theta, phi):
        return (cos(.5 * theta) * phi + 1) * sin(theta)

    def f_z(theta, phi):
        return phi * sin(.5 * theta)

    return NumpyWrapper(-pi, pi, -1.001, 1.001, resolution).get_plot_data(f_x, f_y, f_z)

self_intersecting_disk_title = "Parametrization for a <a href=\"https://en.wikipedia.org/wiki/Real_projective_plane\">self-intersecting disk</a> $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} r\\phi\\cos(2\\theta) \\\\  r\\phi\\sin(2\\theta) \\\\ r\\phi\\cos(\\theta) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-\\pi, \\pi] \\end{cases}$"
def self_intersecting_disk(r=1, resolution=75):
    def f_x(x, y):
        return r * y * cos(2 * x)

    def f_y(x, y):
        return r * y * sin(2 * x)

    def f_z(x, y):
        return -r * y * cos(x)

    return NumpyWrapper(0, 2 * pi, 0, 1, resolution).get_plot_data(f_x, f_y, f_z)

star_of_david_title="Parametrization for a <a href=\"https://doc.sagemath.org/html/en/reference/plot3d/sage/plot/plot3d/parametric_plot3d.html\">Star of David</a> $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} K\\cos(\\theta) \\cos(\\phi) \\bigg(|\\cos(3\\phi/4)|^{500}+|\\sin(3\\phi/4)|^{500}\\bigg)^{-1/260} \\\\  K\\cos(\\theta) \\sin(\\phi)\\bigg(|\\cos(3\\phi/4)|^{500}+|\\sin(3\\phi/4)|^{500}\\bigg)^{-1/260} \\\\ K\\sin(\\theta) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
def star_of_david(resolution=100):
    def f_x(theta, phi):
        k = (abs(cos(theta))**200+abs(sin(theta))**200)**(-1.0/200)
        return cos(theta) * cos(phi) * (abs(cos(3*phi/4))**500+abs(sin(3*phi/4))**500)**(-1/260) * k

    def f_y(theta, phi):
        k = (abs(cos(theta))**200+abs(sin(theta))**200)**(-1.0/200)
        return cos(theta) * sin(phi) * (abs(cos(3*phi/4))**500+abs(sin(3*phi/4))**500)**(-1/260) * k

    def f_z(theta, phi):
        k = (abs(cos(theta))**200+abs(sin(theta))**200)**(-1.0/200)
        return k * sin(theta)

    return NumpyWrapper(-pi, pi, 0, 2 * pi, resolution).get_plot_data(f_x, f_y, f_z)

torus_title = "Parametrization for torus $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (c + a \\cos(\\phi))\\cos(\\theta) \\\\  (c + a \\cos(\\phi))\\sin(\\theta) \\\\ a \\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-\\pi, \\pi] \\end{cases}$"
def torus(a=.7, c=2, height=2, resolution=75):
    def f_x(theta, phi):
        return (c + a * cos(phi)) * cos(theta)

    def f_y(theta, phi):
        return (c + a * cos(phi)) * sin(theta)

    def f_z(_, phi):
        return height * a * sin(phi)

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)


trefoil_knot_title = "Parametrization for the <a href=\"https://en.wikipedia.org/wiki/Trefoil_knot\">trefoil knot</a> $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (4(1+0.25\\sin(3\\phi))+\\cos(\\theta))\\cos(2\\phi) \\\\  \\sin(\\theta)(1+\\phi\\cos(\\theta/2)) \\\\ 0.2\\phi\\sin(\\theta/2) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 4\\pi + 0.5] \\\\ \\phi \\in [0, 0.3] \\end{cases}$"
def trefoil_knot(resolution=50):
    def f_x(x, y):
        factor = 4* (.25 * sin(3 * y) + 1) + cos(x)
        return factor * cos(2 * y)

    def f_y(x, y):
        factor = 4* (.25 * sin(3 * y) + 1) + cos(x)
        return factor * sin(2 * y)

    def f_z(x, y):
        return sin(x) + 2 * cos(3 * y)

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)

# https://www.mattiagiuri.com/2020/11/20/plotting-a-torus-with-python/
# https://en.wikipedia.org/wiki/Real_projective_plane
# figure_8_klein_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for a figure-8 Klein bottle</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) (a + \\sin(\\phi) \\cos(\\theta/2) - \\sin(2\\phi) \\sin(\\theta/2)/2) \\\\ \\sin(\\theta) (a + \\sin(\\phi) \\cos(\\theta/2) - \\sin(2\\phi) \\sin(\\theta/2)/2) \\\\ \\sin(\\theta/2) \\sin(\\phi) + \\cos(\\theta/2) \\sin(2\\phi)/2 \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
# grays_klein_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for Gray&apos;s Klein bottle</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) (a + \\cos(n\\theta/2) \\sin(\\phi) - \\sin(n\\theta/2) \\sin(2\\phi))\\cos(m\\theta/2) \\\\ (a + \\cos(n\\theta/2) \\sin(\\phi) - \\sin(n\\theta/2) \\sin(2\\phi))\\sin(m\\theta/2) \\\\ \\sin(n\\theta/2) \\sin(\\phi) + \\cos(n\\theta/2) \\sin(2\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 4\\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"

twisted_torus_title = "Parametrization for twisted torus $\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (3 + \\sin(\\phi) + \\cos(\\theta)) \\cos(2\\phi) \\\\  (3 + \\sin(\\phi) + \\cos(\\theta))\\sin(2\\phi) \\\\ \\sin(\\theta)+2\\cos(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-\\pi, \\pi] \\end{cases}$"
def twisted_torus(resolution=100):
    def f_x(theta, phi):
        return (3 + sin(phi) + cos(theta)) * cos(2 * phi)

    def f_y(theta, phi):
        return (3 + sin(phi) + cos(theta)) * sin(2 * phi)

    def f_z(theta, phi):
        return 2 * (cos(phi) + sin(theta))

    return NumpyWrapper(-pi, pi, -pi, pi, resolution).get_plot_data(f_x, f_y, f_z)

################
# GUI controls #
################

def toggle(event):
    radio_buttons.toggle(event.name)

radio_buttons = RadioButtons()
radio_buttons.add(radio(bind=toggle, text=" Arc ", name="arc"), arc, arc_title)
radio_buttons.add(radio(bind=toggle, text=" Bow curve ", name="bow_curve"), bow_curve, bow_curve_title)
radio_buttons.add(radio(bind=toggle, text=" Boy&apos;s surface ", name="boys_surface"), boys_surface, boys_surface_title)
radio_buttons.add(radio(bind=toggle, text=" Bubbles ", name="bubbles"), bubbles, bubbles_title)
radio_buttons.add(radio(bind=toggle, text=" Conchoid ", name="conchoid"), conchoidal, conchoidal_title)
radio_buttons.add(radio(bind=toggle, text=" Conchoid 2 ", name="conchoid_2"), conchoidal_2, conchoidal_2_title)
radio_buttons.add(radio(bind=toggle, text=" Cross cap ", name="cross_cap"), cross_cap, cross_cap_title)
radio_buttons.add(radio(bind=toggle, text=" Dented surface ", name="dented"), dented, dented_title)
radio_buttons.add(radio(bind=toggle, text=" Dini&apos;s spiral ", name="dinis_spiral"), dinis_spiral, spiral_title)
radio_buttons.add(radio(bind=toggle, text=" Elliptic torus ", name="elliptic_torus"), elliptic_torus, elliptic_torus_title)
# radio_buttons.add(radio(bind=toggle, text=" Figure-8 Klein bottle ", name="figure_8_klein_bottle"), figure_8_klein_bottle, figure_8_klein_title)
# radio_buttons.add(radio(bind=toggle, text=" Grays Klein bottle ", name="grays_klein_bottle"), grays_klein_bottle, grays_klein_title)
radio_buttons.add(radio(bind=toggle, text=" Limpet torus ", name="limpet_torus"), limpet_torus, limpet_torus_title)
radio_buttons.add(radio(bind=toggle, text=" Mobius strip ", name="mobius"), mobius_strip, mobius_title)
radio_buttons.add(radio(bind=toggle, text=" Self-intersecting disk ", name="self_intersecting_disk"), self_intersecting_disk, self_intersecting_disk_title)
radio_buttons.add(radio(bind=toggle, text=" Star of David ", name="star_of_david"), star_of_david, star_of_david_title)
radio_buttons.add(radio(bind=toggle, text=" Torus ", name="torus"), torus, torus_title)
radio_buttons.add(radio(bind=toggle, text=" Trefoil Knot ", name="trefoil_knot"), trefoil_knot, trefoil_knot_title)
radio_buttons.add(radio(bind=toggle, text=" Twisted torus ", name="twisted_torus"), twisted_torus, twisted_torus_title)

def adjust_opacity(event):
    figure.set_opacity_to(event.value)
    opacity_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_shininess(event):
    figure.set_shininess_to(event.value)
    shininess_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_omega(event):
    figure.set_omega_to(event.value)
    omega_slider_text.text = "= {:1.2f}".format(event.value / pi, 2) + " π"


def adjust_gradient(event):
    figure.set_hue_gradient_to(event.value)
    gradient_slider_text.text = "= {:1.2f}".format(event.value, 2)


def adjust_offset(event):
    figure.set_hue_offset_to(event.value)
    offset_slider_text.text = "= {:1.2f}".format(event.value, 2)

animation.append_to_caption("\n\nHue offset  ")
_ = slider(min=0, max=1, step=0.01, value=.3, bind=adjust_offset)
offset_slider_text = wtext(text="= 0.3")

animation.append_to_caption("\n\nHue gradient  ")
_ = slider(min=0, max=1, step=0.01, value=.5, bind=adjust_gradient)
gradient_slider_text = wtext(text="= 0.5")

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
_ = checkbox(text='Mesh ', bind=toggle_mesh, checked=False)
_ = checkbox(text='Axis labels ', bind=toggle_axis_labels, checked=False)
_ = checkbox(text='Tick marks ', bind=toggle_tick_marks, checked=False)
_ = checkbox(text='Animate ', bind=toggle_animate, checked=False)
animation.append_to_caption("\n\n")

animation.title = arc_title + "\n\n"
#################################
# COMMENT OUT IN LOCAL VPYTHON  #
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

figure = Figure(animation)
figure.reset() # To make the GUI controls appear on top

xx_, yy_, zz_ = arc()
figure.add_subplot(xx_, yy_, zz_)

dt = 0.0
time = 1
while True:
    rate(10)
    figure.render(time)
    time += dt
