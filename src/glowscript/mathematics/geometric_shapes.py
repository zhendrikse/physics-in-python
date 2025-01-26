# Web VPython 3.2

from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdnjs.cloudflare.com/ajax/libs/numjs/0.16.1/numjs.min.js')
# get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

spiral_title = "<h3>Parametrization for <a href=\"https://en.wikipedia.org/wiki/Dini%27s_surface\">Dini&apos;s spiral</a></h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)\cdot\\sin(\\phi) \\\\  \\sin(\\theta)\\cdot\\sin(\\phi) \\\\  \\cos(\\phi)+\\log(\\tan(\\phi/2))) + 0.2\\theta \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 12.4] \\\\ \\phi \\in [0.1, 2] \\end{cases}$"
torus_title = "<h3>Parametrization for torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (c + a \\cos(\\phi))\cdot\\cos(\\theta) \\\\  (c + a \\cos(\\phi))\cdot\\sin(\\theta) \\\\ a \\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-\\pi, \\pi] \\end{cases}$"
twisted_torus_title = "<h3>Parametrization for twisted torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (3 + \\sin(\\phi) + \\cos(\\theta)) \cdot \\cos(2\\phi) \\\\  (3 + \\sin(\\phi) + \\cos(\\theta))\cdot\\sin(2\\phi) \\\\ \\sin(\\theta)+2\\cos(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-\\pi, \\pi] \\end{cases}$"
mobius_title = "<h3>Parametrization for <a href=\"https://en.wikipedia.org/wiki/M%C3%B6bius_strip\">Möbius strip</a></h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)(1+\\phi\\cos(\\theta/2)) \\\\  \\sin(\\theta)(1+\\phi\\cos(\\theta/2)) \\\\ 0.2\\phi\\sin(\\theta/2) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 4\\pi + 0.5] \\\\ \\phi \\in [0, 0.3] \\end{cases}$"
bubbles_title = "<h3>Parametrization for bubbles</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)\\sin(2\\phi) \\\\  \\sin(\\theta)\\sin(2\\phi) \\\\ \\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
trefoil_knot_title = "<h3>Parametrization for the <a href=\"https://en.wikipedia.org/wiki/Trefoil_knot\">trefoil knot</a></h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (4(1+0.25\\sin(3\\phi))+\\cos(\\theta))\\cos(2\\phi) \\\\  \\sin(\\theta)(1+\\phi\\cos(\\theta/2)) \\\\ 0.2\\phi\\sin(\\theta/2) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 4\\pi + 0.5] \\\\ \\phi \\in [0, 0.3] \\end{cases}$"
arc_title = "<h3>Parametrization for arc</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) \\\\  \\sin(\\theta)+\\cos(\\phi) \\\\ 3\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, \\pi] \\\\ \\phi \\in [0, \\pi] \\end{cases}$"
dented_title = "<h3>Parametrization for dented surface</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) \\\\  \\sin(\\theta)+\\cos(\\phi) \\\\ 3\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
conchoid_title = "<h3><a href=\"https://paulbourke.net/geometry/spiral/\">Paul Bourke&apos;s</a> parametrization for a conchoid</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} a\\left(1-\\dfrac{\\theta}{2\\pi}\\right)\\cos(n\\theta)(1+\\cos(\\phi))+c\\cos(n\\theta) \\\\  a\\left(1-\\dfrac{\\theta}{2\\pi}\\right)\\sin(n\\theta)(1+\\cos(\\phi))+c\\sin(n\\theta) \\\\ b\\dfrac{\\theta}{2\\pi}+a\left(1-\\frac{\\theta}{2\\pi}\\right)\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"
self_intersecting_disk_title = "<h3>Parametrization for a <a href=\"https://en.wikipedia.org/wiki/Real_projective_plane\">self-intersecting disk</a></h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} r\\phi\\cos(2\\theta) \\\\  r\\phi\\sin(2\\theta) \\\\ r\\phi\\cos(\\theta) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
cross_cap_title = "<h3><a href=\"https://paulbourke.net/geometry/crosscap/\">Paul Bourke&apos;s parametrization</a> for a <a href=\"https://mathworld.wolfram.com/Cross-Cap.html\">cross cap</a></h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) \\sin(2\\phi) \\\\  \\sin(\\theta) \\sin(2\\phi) \\\\ \\cos(\\phi)\\cos(\\phi) - \\cos(\\theta)\\cos(\\theta)\\sin(\\phi)\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
limpet_torus_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for a limpet torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) / (\\sqrt{2} + \\sin(\\phi)) \\\\  \\sin(\\theta) / (\\sqrt{2} + \\sin(\\phi)) \\\\ 1 / (\\sqrt{2} + \\cos(\\phi)) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
elliptic_torus_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for an elliptic torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (c + \\cos(\\phi)) \\cos(\\theta) \\\\  (c + \\cos(\\phi)) \\sin(\\theta) \\\\ \\sin(\\phi) + \\cos(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [-\\pi, \\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
figure_8_klein_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for a figure-8 Klein bottle</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) (a + \\sin(\\phi) \\cos(\\theta/2) - \\sin(2\\phi) \\sin(\\theta/2)/2) \\\\ \\sin(\\theta) (a + \\sin(\\phi) \\cos(\\theta/2) - \\sin(2\\phi) \\sin(\\theta/2)/2) \\\\ \\sin(\\theta/2) \\sin(\\phi) + \\cos(\\theta/2) \\sin(2\\phi)/2 \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
grays_klein_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for Gray&apos;s Klein bottle</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta) (a + \\cos(n\\theta/2) \\sin(\\phi) - \\sin(n\\theta/2) \\sin(2\\phi))\\cos(m\\theta/2) \\\\ (a + \\cos(n\\theta/2) \\sin(\\phi) - \\sin(n\\theta/2) \\sin(2\\phi))\\sin(m\\theta/2) \\\\ \\sin(n\\theta/2) \\sin(\\phi) + \\cos(n\\theta/2) \\sin(2\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 4\\pi] \\\\ \\phi \\in [-pi, \\pi] \\end{cases}$"
klein_title = "<h3><a href=\"https://paulbourke.net/geometry/toroidal/\">Paul Bourke&apos;s parametrization</a> for Klein&apos;s bottle</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\begin{cases} 6\\cos(\\theta)(1+\\sin(\\theta)) + r\\cos(\\theta)\\cos(\\phi), 0 \\leq \\theta &lt; \\pi \\\\ 6\\cos(\\theta)(1+\\sin(\\theta)) + r\\cos(\\phi+\\pi), \\pi &lt; \\theta \\leq 2\\pi \\end{cases} \\\\ \\begin{cases} 16\\sin(\\theta)+r\\sin(\\theta)\\cos(\\phi), 0 \\leq \\theta &lt; \\pi  \\\\\ 16\\sin(\\theta), \\pi &lt; \\theta \\leq 2\\pi \\end{cases} \\\\  r\\sin(\\phi) \\end{pmatrix}\\text{, } \\begin{cases} \\theta \\in [0, 2\\pi] \\\\ \\phi \\in [0, 2\\pi] \\end{cases}$"

# double_torus_title = ""


caption = """
&#x2022; Written by <a href="http://www.hendrikse.name/">Zeger Hendrikse</a> and <a href="https://www.glowscript.org/#/user/X9Z3/">Maximillian DeMarr</a>
&#x2022; Source code can be found <a href="https://github.com/zhendrikse/physics-in-python/blob/main/src/glowscript/mathematics/geometric_shapes.py">here</a>
&#x2022; Inspired on <a href="https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Plot3D">Plot3D</a> by adding the following features: 
  &#x2022; Numpy linspace and meshgrid syntax
  &#x2022; Multiple subplots per figure
  &#x2022; Non-uniform coloring

"""

animation = canvas(align="top", background=color.gray(0), width=800, height=600, center=vec(0, 5, 0),
                   forward=vec(-0.9, -0.5, -.8), title=arc_title + "\n\n")

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
            suplot.set_shininess_to(shininess)

    def reset(self):
        for subplot in self._subplots:
            subplot.hide_plot()

        self._subplots = []

    def add_subplot(self, xx, yy, zz):
        subplot = SubPlot(xx, yy, zz)
        subplot.set_omega_to(self._omega)
        subplot.set_opacity_to(self._opacity)
        subplot.set_hue_offset_to(self._hue_offset)
        subplot.set_hue_gradient_to(self._hue_gradient)
        self._subplots.append(subplot)


class RadioButton:
    def __init__(self, button, function_, title_text):
        self._button = button
        self._function = function_
        self._explanation = title_text

    def uncheck(self):
        self._button.checked = False

    def push(self):
        xx, yy, zz = self._function()
        figure.reset()
        figure.add_subplot(xx, yy, zz)
        animation.title = self._explanation + "\n\n"
        MathJax.Hub.Queue(["Typeset", MathJax.Hub])

    def check(self):
        self._button.checked = True

    def name(self):
        return self._button.name


class RadioButtons:
    def __init__(self):
        self._radio_buttons = []
        self._selected_button = None

    def add(self, button, function_, title_text):
        self._radio_buttons.append(RadioButton(button, function_, title_text))

        if (len(self._radio_buttons) % 6) == 0:
            animation.append_to_caption("\n\n")

        if (len(self._radio_buttons)) == 1:
            self._radio_buttons[0].check()
            self._selected_button = self._radio_buttons[0]

    def _uncheck_buttons_except(self, button_name):
        for button in self._radio_buttons:
            if button.name() != button_name: button.uncheck()

    def _get_button_by(self, button_name):
        for button in self._radio_buttons:
            if button.name() == button_name: return button

    def toggle(self, button_name):
        self._uncheck_buttons_except(button_name)
        self._selected_button = self._get_button_by(button_name)
        self._selected_button.push()

    def get_selected_button_name(self):
        return self._selected_button.name()


def arc(resolution=50):
    theta = np.linspace(0, 1.05 * pi, resolution)
    phi = np.linspace(0, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    xx = np.cos(theta)
    yy = np.sin(theta).add(np.cos(phi))
    zz = np.sin(phi).multiply(3)

    return xx, yy, zz


def breather(resolution=100):
    pass


# K = sqrt(0.84)
# G = (0.4*((K*cosh(0.4*u))^2 + (0.4*sin(K*v))^2))
# f_x = (2*K*cosh(0.4*u)*(-(K*cos(v)*cos(K*v)) - sin(v)*sin(K*v)))/G
# f_y = (2*K*cosh(0.4*u)*(-(K*sin(v)*cos(K*v)) + cos(v)*sin(K*v)))/G
# f_z = -u + (2*0.84*cosh(0.4*u)*sinh(0.4*u))/G

def bubbles(resolution=75):
    theta = np.linspace(0, 1.02 * pi, resolution)
    phi = np.linspace(0, 2.02 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    xx = np.cos(theta).multiply(np.sin(phi.multiply(2)))
    yy = np.sin(theta).multiply(np.sin(phi.multiply(2)))
    zz = np.sin(phi)

    return xx, yy, zz


def conchoid(resolution=100, num_spirals=3, r_final=2, height=6.5, r_inner=.5):
    theta = phi = np.linspace(0, 2 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    factor_1 = np.cos(phi).add(1)
    factor_2 = theta.divide(-2 * pi).add(1).multiply(r_final).multiply(np.cos(theta.multiply(num_spirals)))

    xx = factor_1.multiply(factor_2).add(np.cos(theta.multiply(num_spirals)).multiply(r_inner))
    factor_2 = theta.divide(-2 * pi).add(1).multiply(r_final).multiply(np.sin(theta.multiply(num_spirals)))
    yy = factor_1.multiply(factor_2).add(np.sin(theta.multiply(num_spirals)).multiply(r_inner))
    term = np.sin(phi).multiply(r_final).multiply(theta.divide(-2 * pi).add(1))
    zz = theta.multiply(height / (2 * pi)).add(term)

    return xx, yy, zz


def cross_cap(resolution=100):
    u = np.linspace(0, pi, resolution)
    v = np.linspace(0, pi, resolution)
    u, v = np.meshgrid(u, v)

    x = np.cos(u).multiply(np.sin(v.multiply(2)))
    y = np.sin(u).multiply(np.sin(v.multiply(2)))
    term = np.cos(u).multiply(np.cos(u)).multiply(np.sin(v)).multiply(np.sin(v))
    z = np.cos(v).multiply(np.cos(v)).subtract(term)

    return x, y, z


def dinis_spiral(resolution=100):
    u = np.linspace(0, 12.4, resolution)
    v = np.linspace(0.1, 2, resolution)
    u, v = np.meshgrid(u, v)

    xx = np.cos(u).multiply(np.sin(v))
    yy = np.sin(u).multiply(np.sin(v))
    term = np.log(np.tan(v.multiply(0.5))).add(np.cos(v))
    zz = u.multiply(0.2).add(term)

    return xx, yy, zz


def dented(resolution=50):
    theta = np.linspace(-pi, pi, resolution)
    phi = np.linspace(0, 2 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    x = np.cos(theta)
    y = np.sin(theta).add(np.cos(phi))
    z = np.sin(phi).multiply(1.5)

    return x, y, z


#
# Double torus parametrization found on:
# https://doc.sagemath.org/html/en/reference/plot3d/sage/plot/plot3d/parametric_plot3d.html
#
def double_torus_1(a=1, b=1, resolution=50):
    theta = phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = np.cos(phi).add(a).multiply(np.sin(theta)).add(b)
    y = np.cos(phi).add(a).multiply(np.cos(theta)).add(b)
    z = np.sin(phi).add(b)

    return x, y, z


def double_torus_2(a=1, b=1, resolution=50):
    theta = phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = np.cos(phi).add(a).multiply(np.cos(theta)).add(2 * b)
    y = np.sin(phi).add(a)
    z = np.cos(phi).add(a).multiply(np.sin(theta)).add(b)

    return x, y, z


def double_torus(resolution=50):
    x1, y1, z1 = double_torus_1(resolution)
    x2, y2, z2 = double_torus_2(resolution)
    x_stitch, y_stitch, z_stitch = np.concatenate(x1, x2), np.concatenate(y1, y2), np.concatenate(z1, z2)
    return x_stitch, y_stitch, z_stitch


def elliptic_torus(a=1, c=2.5, resolution=50):
    theta = phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = (np.cos(phi).multiply(a).add(c)).multiply(np.cos(theta))
    y = (np.cos(phi).multiply(a).add(c)).multiply(np.sin(theta))
    z = np.sin(phi).add(np.cos(phi)).multiply(a)
    return x, y, z


def figure_8_klein_bottle(a=1.50, resolution=100):
    theta = phi = np.linspace(0, 2 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    term_1 = np.sin(phi).multiply(np.cos(theta.multiply(0.5)))
    term_2 = np.sin(phi.multiply(2)).multiply(np.sin(theta.multiply(0.5))).multiply(0.5)
    factor = term_1.subtract(term_2).add(a)
    x = np.cos(theta).multiply(factor)
    y = np.sin(theta).multiply(factor)
    term = np.cos(theta.multiply(0.5)).multiply(np.sin(phi.multiply(2))).multiply(.5)
    z = np.sin(theta.multiply(0.5)).multiply(np.sin(phi)).add(term)
    return x, y, z


def grays_klein_bottle(resolution=75, a=1.5, n=2, m=1):
    theta = np.linspace(0, 4 * pi, resolution)
    phi = np.linspace(0, 2 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    term_1 = np.sin(phi).multiply(np.cos(theta.multiply(n / 2.0)))
    term_2 = np.sin(phi.multiply(2)).multiply(np.sin(theta.multiply(n / 2.0)))
    factor = term_1.subtract(term_2).add(a)
    x = np.cos(theta.multiply(m / 2.0)).multiply(factor)
    y = np.sin(theta.multiply(m / 2.0)).multiply(factor)
    term = np.cos(theta.multiply(n / 2.0)).multiply(np.sin(phi.multiply(2)))
    z = np.sin(theta.multiply(n / 2.0)).add(np.cos(theta.multiply(n / 2.0)).multiply(np.sin(phi.multiply(2))))
    return x, y, z


#
# Paul Bourke's parametrization of the Klein bottle
# https://paulbourke.net/geometry/toroidal/
#
def klein_bottle_part_1(resolution=50):
    # theta = np.linspace(0, pi * (1 - 1/(2 * resolution)), resolution)
    # phi = np.linspace(0, 2 * pi * ( 1 - 1/resolution), resolution)
    theta = np.linspace(0, pi + .1, resolution)
    phi = np.linspace(0, 2 * pi + .2, resolution)

    theta, phi = np.meshgrid(theta, phi)

    r = np.cos(theta).multiply(-0.5).add(1).multiply(4)
    term2 = np.cos(theta).multiply(np.cos(phi)).multiply(r)
    term1 = np.sin(theta).add(1).multiply(np.cos(theta)).multiply(6)
    x = term1.add(term2)
    y = np.sin(theta).multiply(16).add(np.sin(theta).multiply(r).multiply(np.cos(phi)))
    z = np.sin(phi).multiply(r)

    return x, y, z


def klein_bottle_part_2(resolution=50):
    # theta = np.linspace(pi * (1 + 1/(2 * resolution)), 2 * pi, resolution)
    # phi = np.linspace(0, 2 * pi * ( 1 - 1/resolution), resolution)
    theta = np.linspace(pi, 2 * pi, resolution)
    phi = np.linspace(0, 2 * pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    r = np.cos(theta).multiply(-0.5).add(1).multiply(4)
    term2 = np.cos(phi.add(pi)).multiply(r)
    term1 = np.sin(theta).add(1).multiply(np.cos(theta)).multiply(6)
    x = term1.add(term2)
    y = np.sin(theta).multiply(16)
    z = np.sin(phi).multiply(r)

    return x, y, z


def klein_bottle(resolution=56):
    x1, y1, z1 = klein_bottle_part_1(resolution)
    x2, y2, z2 = klein_bottle_part_2(resolution)
    x_stitch_, y_stitch_, z_stitch_ = np.concatenate(x1, x2), np.concatenate(y1, y2), np.concatenate(z1, z2)
    return x_stitch_, y_stitch_, z_stitch_


def limpet_torus(resolution=100):
    theta = phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = np.cos(theta).divide(np.sin(phi).add(sqrt(2)))
    y = np.sin(theta).divide(np.sin(phi).add(sqrt(2)))
    z = np.ones([resolution, resolution]).divide(np.cos(phi).add(sqrt(2)))
    return x, y, z


def mobius_strip(resolution=100):
    theta = np.linspace(-pi, pi, resolution)
    phi = np.linspace(-1, 1, resolution)
    theta, phi = np.meshgrid(theta, phi)

    factor = np.cos(theta.multiply(.5)).multiply(phi.multiply(.5)).add(1)
    xx = factor.multiply(np.cos(theta))
    yy = factor.multiply(np.sin(theta))
    zz = np.sin(theta.multiply(.5)).multiply(phi.multiply(.5))
    return xx, yy, zz


# https://en.wikipedia.org/wiki/Real_projective_plane
def self_intersecting_disk(r=1, resolution=100):
    theta = np.linspace(0, 2 * pi, resolution)
    phi = np.linspace(0, 1, resolution)
    theta, phi = np.meshgrid(theta, phi)
    X = np.cos(theta.multiply(2)).multiply(phi).multiply(r)
    Y = np.sin(theta.multiply(2)).multiply(phi).multiply(r)
    Z = np.cos(theta).multiply(phi).multiply(-r)
    return X, Y, Z


# https://www.mattiagiuri.com/2020/11/20/plotting-a-torus-with-python/
def torus(a=.7, c=2, resolution=50):
    theta = phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = (np.cos(phi).multiply(a).add(c)).multiply(np.cos(theta))
    y = (np.cos(phi).multiply(a).add(c)).multiply(np.sin(theta))
    z = np.sin(phi).multiply(a)
    return x, y, z


def trefoil_knot(resolution=100):
    theta = phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    factor = np.sin(phi.multiply(3)).multiply(0.25).add(1).multiply(4).add(np.cos(theta))
    xx = factor.multiply(np.cos(phi.multiply(2)))
    yy = factor.multiply(np.sin(phi.multiply(2)))
    zz = np.sin(theta).add(np.cos(phi.multiply(3)).multiply(2))

    return xx, yy, zz


def twisted_torus(resolution=100):
    theta = np.linspace(-pi, pi, resolution)
    phi = np.linspace(-pi, pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    factor = np.sin(phi).add(np.cos(theta)).add(3)
    xx = np.cos(phi.multiply(2)).multiply(factor)
    yy = np.sin(phi.multiply(2)).multiply(factor)
    zz = np.sin(theta).add(np.cos(phi).multiply(2))

    return xx, yy, zz


def toggle(event):
    radio_buttons.toggle(event.name)


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
radio_buttons = RadioButtons()
radio_buttons.add(radio(bind=toggle, text="Arc ", name="arc"), arc, arc_title)
radio_buttons.add(radio(bind=toggle, text="Bubbles ", name="bubbles"), bubbles, bubbles_title)
radio_buttons.add(radio(bind=toggle, text="Conchoid ", name="conchoid"), conchoid, conchoid_title)
radio_buttons.add(radio(bind=toggle, text="Cross cap ", name="cross_cap"), cross_cap, cross_cap_title)
radio_buttons.add(radio(bind=toggle, text="Dented surface ", name="dented"), dented, dented_title)
radio_buttons.add(radio(bind=toggle, text="Dini&apos;s spiral", name="dinis_spiral"), dinis_spiral, spiral_title)
# radio_buttons.add(radio(bind=toggle, text="Double torus", name="double_torus"), double_torus, double_torus_title)
radio_buttons.add(radio(bind=toggle, text="Elliptic torus ", name="elliptic_torus"), elliptic_torus,
                  elliptic_torus_title)
radio_buttons.add(radio(bind=toggle, text="Figure-8 Klein bottle ", name="figure_8_klein_bottle"),
                  figure_8_klein_bottle, figure_8_klein_title)
radio_buttons.add(radio(bind=toggle, text="Grays Klein bottle ", name="grays_klein_bottle"), grays_klein_bottle,
                  grays_klein_title)
radio_buttons.add(radio(bind=toggle, text="Klein bottle ", name="klein_bottle"), klein_bottle, klein_title)
radio_buttons.add(radio(bind=toggle, text="Limpet torus ", name="limpet_torus"), limpet_torus, limpet_torus_title)
radio_buttons.add(radio(bind=toggle, text="Mobius strip ", name="mobius"), mobius_strip, mobius_title)
radio_buttons.add(radio(bind=toggle, text="Self-intersecting disk ", name="self_intersecting_disk"),
                  self_intersecting_disk, self_intersecting_disk_title)
radio_buttons.add(radio(bind=toggle, text="Torus", name="torus"), torus, torus_title)
radio_buttons.add(radio(bind=toggle, text="Trefoil Knot ", name="trefoil_knot"), trefoil_knot, trefoil_knot_title)
radio_buttons.add(radio(bind=toggle, text="Twisted torus", name="twisted_torus"), twisted_torus, twisted_torus_title)

animation.append_to_caption("\n" + caption + "\n")


def on_key_press(key):
    if key == "b":
        animation.background = color.white if animation.background == color.black else color.black
    if key == 's':
        animation.capture(radio_buttons.get_selected_button_name())
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

x, y, z = arc()
figure = Figure()
figure.add_subplot(x, y, z)

time = 0
dt = 0.02
run = True
while True:
    rate(30)
    figure.render(time)
    if run:
        time += dt

