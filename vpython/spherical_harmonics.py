# Web VPython 3.2

from vpython import *

animation = canvas(height=500, align="top", center=vec(0, -10, 0), background=color.gray(0.075),
                   forward=vec(-0.9, -0.85, -.8), range=150)


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
    def __init__(self, button_, function_):
        self._button = button_
        self._function = function_

    def uncheck(self):
        self._button.checked = False

    def push(self, spherical_harmonic_parameters):
        # Update spherical harmonic parameters
        parameter_index = int(self.name().split(",")[0])
        parameter_value = int(self.name().split(",")[1])
        spherical_harmonic_parameters.coefficients[parameter_index] = parameter_value

        # Update plot with new updated parameters
        create_title(spherical_harmonic_parameters)
        xx, yy, zz = self._function(spherical_harmonic_parameters)
        figure.reset()
        figure.add_subplot(xx, yy, zz)
        animation.range = 1.5 * len(xx)
        ##########################
        # COMMENT OUT IN VPYTHON #
        ##########################
        #MathJax.Hub.Queue(["Typeset", MathJax.Hub])

    def check(self):
        self._button.checked = True

    def name(self):
        return self._button.name


class RadioButtons:
    def __init__(self, spherical_harmonic_parameters):
        self._radio_buttons = []
        self._selected_button = None
        self._spherical_harmonic_parameters = spherical_harmonic_parameters

    def add(self, button_, function_):
        self._radio_buttons.append(RadioButton(button_, function_))

        if (len(self._radio_buttons) % 7) == 0:
            animation.append_to_caption("\n\n")

        # By default, all spherical parameters are set to 4
        # So the index of that parameter, number 5, should be checked
        if (len(self._radio_buttons)) == 5:
            self._radio_buttons[4].check()
            self._selected_button = self._radio_buttons[4]

    def _uncheck_buttons_except(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() != button_name: button_.uncheck()

    def _get_button_by(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() == button_name: return button_

    def toggle(self, button_name):
        self._uncheck_buttons_except(button_name)
        self._selected_button = self._get_button_by(button_name)
        self._selected_button.push(self._spherical_harmonic_parameters)

    def get_selected_button_name(self):
        return self._selected_button.name()

class SphericalHarmonicParameters:
    def __init__(self):
        self.coefficients = [4, 4, 4, 4, 4, 4, 4, 4]
        self.resolution = 100

def spherical_harmonics(spherical_harmonic, resolution=100):
    m = spherical_harmonic.coefficients
    def r(theta, phi):
        return sin(m[0] * theta) ** m[1] + cos(m[2] * theta) ** m[3] + sin(m[4] * phi) ** m[5] + cos(m[6] * phi) ** m[7]

    def f_x(theta, phi):
        return r(theta, phi) * sin(theta) * cos(phi)

    def f_y(theta, phi):
        return r(theta, phi) * cos(theta)

    def f_z(theta, phi):
        return r(theta, phi) * sin(theta) * sin(phi)

    return NumpyWrapper(-1.1 * pi, pi, 0, 1.01 * pi, resolution).get_plot_data(f_x, f_y, f_z)

def create_title(spherical_parameters):
    animation_title = "$\\rho = \\sin(m_0\\phi)^{m_1} + \\cos(m_2\\phi)^{m_3} + \\sin(m_4\\theta)^{m_5} + \\cos(m_6\\theta)^{m_7}$\n\n"
    animation_title += "$\\begin{pmatrix} x \\\\ y \\\\ z \\end{pmatrix} = \\begin{pmatrix} \\rho\\sin(\\phi)\\cos(\\theta) \\\\ \\rho\\cos(\\phi) \\\\ \\rho\\sin(\\phi)\\sin(\\theta)\\end{pmatrix}$"
    animation_title += "\n\nwhere\n\n$"
    for i in range(len(spherical_parameters.coefficients)):
        animation_title += "m_" + str(i) + "=" + str(spherical_parameters.coefficients[i])
        animation_title += "" if i == len(spherical_parameters.coefficients) - 1 else ", "
    animation.title = animation_title + "$\n\n"

    ##########################
    # COMMENT OUT IN VPYTHON #
    ##########################
    # MathJax.Hub.Queue(["Typeset", MathJax.Hub])

#
# GUI controls
#
def adjust_opacity(event):
    figure.set_opacity_to(event.value)


def adjust_shininess(event):
    figure.set_shininess_to(event.value)


def adjust_omega(event):
    figure.set_omega_to(event.value)
    omega_slider_text.text = "= {:1.2f}".format(event.value / pi, 2) + " π"


def adjust_gradient(event):
    figure.set_hue_gradient_to(event.value)


def adjust_offset(event):
    figure.set_hue_offset_to(event.value)


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
    parameters.resolution = 50 if event.checked else 100

animation.append_to_caption("\n")
_ = checkbox(text="Contour", bind=toggle_plot_type, checked=False)
_ = checkbox(text='Mesh ', bind=toggle_mesh, checked=False)
_ = checkbox(text='Axis labels ', bind=toggle_axis_labels, checked=False)
_ = checkbox(text='Tick marks ', bind=toggle_tick_marks, checked=False)
_ = checkbox(text='Animate ', bind=toggle_animate, checked=False)

animation.append_to_caption("\n\nHue offset  ")
_ = slider(min=0, max=1, value=.8, bind=adjust_offset)

animation.append_to_caption("\n\nHue gradient  ")
_ = slider(min=0, max=1, value=.5, bind=adjust_gradient)

animation.append_to_caption("\n\nAnimation speed ")
_ = slider(min=0, max=2 * pi, value=pi, bind=adjust_omega)
omega_slider_text = wtext(text="= π")

animation.append_to_caption("\n\nOpacity ")
_ = slider(min=0, max=1, step=0.01, value=1, bind=adjust_opacity)

animation.append_to_caption("\n\nShininess ")
_ = slider(min=0, max=1, step=0.01, value=0.6, bind=adjust_shininess)

parameters = SphericalHarmonicParameters()

def toggle_parameter(event):
    button_array_index = int(event.name.split(",")[0])
    radio_button_array[button_array_index].toggle(event.name)

animation.append_to_caption("\n\n")
radio_button_array = []
for row in range(len(parameters.coefficients)):
    animation.append_to_caption("Choose $m_" + str(row) + "=$")
    radio_buttons = RadioButtons(parameters)
    for column in range(7):
        radio_button = radio(bind=toggle_parameter, text=str(column) + " ", name=str(row) + "," + str(column))
        radio_buttons.add(radio_button, spherical_harmonics)
    radio_button_array += [radio_buttons]

##########################
# COMMENT OUT IN VPYTHON #
##########################
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

create_title(parameters)
figure = Figure(animation)
figure.reset() # To make the GUI controls appear on top
xx_, yy_, zz_ = spherical_harmonics(parameters)
figure.add_subplot(xx_, yy_, zz_)

dt = 0.0
time = 1
while True:
    rate(10)
    figure.render(time)
    time += dt
