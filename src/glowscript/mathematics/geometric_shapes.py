# Web VPython 3.2

from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')
# get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

spiral_title = "<h3>Polar coordinates for Dini&apos;s spiral</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} \\cos(\\theta)\cdot\\sin(\\phi) \\\\  \\sin(\\theta)\\cdot\\sin(\\phi) \\\\ (\\cos(\\phi)+\\log(\\tan(\\phi/2)))) + 0.2\\theta \\end{pmatrix}\\text{, } \\begin{cases} 0 < \\theta < 12.4 \\\\ 0.1 < \\phi < 2\\end{cases}$"
torus_title = "<h3>Polar coordinates for torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (c + a \\cos(\\phi))\cdot\\cos(\\theta) \\\\  (c + a \\cos(\\phi))\cdot\\sin(\\theta) \\\\ a \\sin(\\phi) \\end{pmatrix}\\text{, } \\theta, \\phi \\in [-\\pi, \\pi]$"
twisted_torus_title = "<h3>Polar coordinates for twisted torus</h3>$\\begin{pmatrix}x \\\\ y \\\\ z\\end{pmatrix}=\\begin{pmatrix} (3 + \\sin(\\phi) + \\cos(\\theta)) \cdot \\cos(2\\phi) \\\\  (3 + \\sin(\\phi) + \\cos(\\theta))\cdot\\sin(2\\phi) \\\\ \\sin(\\theta)+2\\cos(\\phi) \\end{pmatrix}\\text{, } \\theta, \\phi \\in [-\\pi, \\pi]\\text{, } \\theta, \\phi \\in [-\\pi, \\pi]$"
caption = """
&#x2022; Source code can be found <a href="https://github.com/zhendrikse/physics-in-python/blob/main/src/glowscript/mathematics/geometric_shapes.py">here</a>
&#x2022; Inspired on <a href="https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Plot3D">Plot3D</a> by adding the following features: 
  &#x2022; Numpy linspace and meshgrid syntax
  &#x2022; Multiple subplots per figure
  &#x2022; Non-uniform coloring

"""

animation = canvas(align="top", width=700, height=700, center=vec(0, 5, 0),
                   forward=vec(-0.9, -0.5, -.8), title=twisted_torus_title + "\n", range=150)
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


class SubPlot:
    def __init__(self, xx, yy, zz, z_min=None, z_max=None):
        self._xx, self._yy, self._zz = xx, yy, zz

        self._z_min, self._z_max = self._z_min_and_z_max(z_min, z_max)
        self._hue_offset = 0.5
        self._omega = 0
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

    def hide_plot(self):
        for quad_ in self._quads:
            quad_.visible = False
        for vertex_ in self._vertices:
            vertex_.visible = False

    def _ranges(self):
        return self._xx.flatten().min(), self._xx.flatten().max(), self._yy.flatten().min(), self._yy.flatten().max()

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

    def _update_vertex(self, x, y, value):
        color_ = abs(value) / np.len(self._zz) + self._hue_offset
        self._get_vertex(x, y).pos.y = value
        self._get_vertex(x, y).color = color.hsv_to_rgb(vec(color_, color_, 1))

    def _update_vertices(self, t):
        range_z = self._z_max - self._z_min
        for x in range(np.len(self._xx)):
            for y in range(np.len(self._yy)):
                f_x_y = self._zz.get(x, y) * (cos(self._omega * t) + 1) * .5
                value = (np.len(self._xx) / range_z) * (f_x_y - self._z_min)
                self._update_vertex(x, y, value)

    def render(self, t):
        self._update_vertices(t)
        self._make_normals()

    def set_omega_to(self, omega):
        self._omega = omega

    def hue_offset_is(self, hue_offset):
        self._hue_offset = hue_offset

    def _get_vertex(self, x, y):
        return self._vertices[x * np.len(self._xx) + y]


class Figure:
    """
    A class to make 3D figures.

    The x-axis is labeled y, the z axis is labeled x, and the y-axis is
    labeled z. This is done to mimic fairly standard practive for plotting
    the z value of a function of x and y.

    A plot is typically made like so:

    resolution = 75
    x = y = np.linspace(-2 * pi, 2 * pi, resolution)
    xx, yy = np.meshgrid(x, y)
    zz = np.cos(np.abs(xx).add(np.abs(yy)))
    figure = Figure()
    figure.add_subplot(xx, yy, zz)


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

    def __init__(self):
        self._subplots = []
        self._hue_offset = 0.5
        self._omega = 0

    def render(self, t):
        for subplot in self._subplots:
            subplot.render(t)

    def set_omega_to(self, omega):
        self._omega = omega
        for subplot in self._subplots:
            subplot.set_omega_to(omega)

    def hue_offset_is(self, hue_offset):
        self._hue_offset = hue_offset
        for subplot in self._subplots:
            subplot.hue_offset_is(hue_offset)

    def reset(self):
        for subplot in self._subplots:
            subplot.hide_plot()

        self._subplots = []

    def add_subplot(self, xx, yy, zz, z_min=None, z_max=None):
        subplot = SubPlot(xx, yy, zz, z_min, z_max)
        subplot.set_omega_to(self._omega)
        subplot.hue_offset_is(self._hue_offset)
        self._subplots.append(subplot)


def torus(a=1, c=3):
    # https://www.mattiagiuri.com/2020/11/20/plotting-a-torus-with-python/

    resolution = 50
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


def adjust_color():
    figure.hue_offset_is(color_slider.value)


def sync_radio_buttons(event):
    if event.name != "torus": torus_button.checked = False
    if event.name != "twisted_torus": twisted_torus_button.checked = False
    if event.name != "spiral": spiral_button.checked = False
    if event.name != "mobius": mobius_button.checked = False
    if event.name != "bubbles": bubbles_button.checked = False
    if event.name != "knot": knot_button.checked = False
    if event.name != "arc": arc_button.checked = False


def switch_function(event):
    sync_radio_buttons(event)
    xx, yy, zz, z_min, z_max = None, None, None, None, None

    if event.name == "torus":
        xx, yy, zz, z_min, z_max = torus()
        animation.title = torus_title + "\n"
    elif event.name == "twisted_torus":
        xx, yy, zz, z_min, z_max = twisted_torus()
        animation.title = twisted_torus_title + "\n"
    elif event.name == "spiral":
        xx, yy, zz, z_min, z_max = dinis_spiral()
        animation.title = spiral_title + "\n\n"
    elif event.name == "mobius":
        xx, yy, zz, z_min, z_max = mobius_strip()
        animation.title = twisted_torus_title + "\n"
    elif event.name == "bubbles":
        xx, yy, zz, z_min, z_max = bubbles()
        animation.title = twisted_torus_title + "\n"
    elif event.name == "arc":
        xx, yy, zz, z_min, z_max = arc()
        animation.title = twisted_torus_title + "\n"
    elif event.name == "knot":
        xx, yy, zz, z_min, z_max = knot()
        animation.title = twisted_torus_title + "\n"

    figure.reset()
    figure.add_subplot(xx, yy, zz, z_min, z_max)
    animation.range = 1.5 * np.len(xx)
    MathJax.Hub.Queue(["Typeset", MathJax.Hub])


def adjust_omega():
    figure.set_omega_to(omega_slider.value)
    omega_slider_text.text = "= sin({:1.2f}".format(omega_slider.value / pi, 2) + " π)"


animation.append_to_caption("\nHue offset  ")
color_slider = slider(min=0, max=1, step=.01, value=0.5, bind=adjust_color)

animation.append_to_caption("\n\nAnimation speed ")
omega_slider = slider(min=0, max=3 * pi, value=0, bind=adjust_omega)
omega_slider_text = wtext(text="= 0")

animation.append_to_caption("\n\n")
torus_button = radio(bind=switch_function, text="Torus", name="torus")
twisted_torus_button = radio(bind=switch_function, text="Twisted torus", name="twisted_torus", checked=True)
spiral_button = radio(bind=switch_function, text="Spiral", name="spiral")
mobius_button = radio(bind=switch_function, text="Mobius strip ", name="mobius")
bubbles_button = radio(bind=switch_function, text="Bubbles ", name="bubbles")
arc_button = radio(bind=switch_function, text="Arc ", name="arc")
knot_button = radio(bind=switch_function, text="Knot ", name="knot")

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
xx, yy, zz, z_min, z_max = twisted_torus()

figure = Figure()
figure.add_subplot(xx, yy, zz, z_min, z_max)

while True:
    rate(30)
    figure.render(time)
    if run:
        time += dt



