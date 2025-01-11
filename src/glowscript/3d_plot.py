from vpython import *

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')

animation = canvas(title="Axis componen")


class Numpy:
    def __init__(self):
        self.array = self._array
        self.linspace = self._linspace
        self.len = self._len

    def _array(self, an_array):
        return nj.array(an_array)

    def _linspace(self, start, stop, num):
        return self._array([x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop])

    def _len(self, numpy_array): return numpy_array.shape[0]


np = Numpy()

L = 50
animation = canvas(width=600, height=600, center=vec(0.05 * L, 0.2 * L, 0), range=1.3 * L)

# There is an L by L grid of vertex objects, numbered 0 through L-1 by 0 through L-1.
# Only the vertex operators numbered L-2 by L-2 are used to create quads.
# The extra row and extra column of vertex objects simplifies edge calculations.
# The stride length from y = 0 to y = 1 is L.

## The next line contains LaTeX math notation. See http://www.glowscript.org/docs/VPythonDocs/MathJax.html
# scene.caption = """\\( f(x,y,t) = 0.7+0.2\\sin{(10x)}\\cos{(10y)}\\cos{(2t)} \\)
scene.caption = """<i>f</i>(<i>x,y,t</i>) = 0.7+0.2sin(10<i>x</i>)cos(10<i>y</i>)cos(2<i>t</i>)
<b>Click to toggle between pausing or running.</b>
   To rotate "camera", drag with right button or Ctrl-drag.
   To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
     On a two-button mouse, middle is left + right.
   To pan left/right and up/down, Shift-drag.
   Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""

# MathJax.Hub.Queue(["Typeset",MathJax.Hub]) # format the LaTeX; see http://www.glowscript.org/docs/VPythonDocs/MathJax.html

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
label_text = ("x", "y", "z")


class Space:
    def __init__(self, linspace_x, linspace_y, linspace_z):
        self.linspace_x = linspace_x
        self.linspace_y = linspace_y
        self.linspace_z = linspace_z


class Base:
    def __init__(self, space, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red,
                 axis_labels=label_text):
        x_ = space.linspace_x
        y_ = space.linspace_y
        z_ = space.linspace_z
        scale = .01 * (x_.get(-1) - x_.get(0))
        delta_x = x_.get(1) - x_.get(0)
        delta_y = y_.get(1) - y_.get(0)
        delta_z = z_.get(1) - z_.get(0)
        range_x = x_.get(-1) - x_.get(0)
        range_y = y_.get(-1) - y_.get(0)
        range_z = z_.get(-1) - z_.get(0)
        self._axis = self._make_axis(x_, y_, z_, delta_x, delta_y, delta_z, axis_color, axis_labels, scale)
        self._tick_marks = self._make_tick_marks(x_, y_, z_, tick_marks_color, scale)

        self._xy_mesh, self._xz_mesh, self._yz_mesh = [], [], []
        for j in range(np.len(x_)):
            pos_x_y = x_hat * x_.get(0) + y_hat * y_.get(0)
            pos_x_z = x_hat * x_.get(0) + z_hat * z_.get(0)
            pos_y_z = y_hat * y_.get(0) + z_hat * z_.get(0)
            self._xy_mesh += [
                cylinder(pos=position + pos_x_y + x_hat * j * delta_x, axis=y_hat * range_y, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            self._xy_mesh += [
                cylinder(pos=position + pos_x_y + y_hat * j * delta_y, axis=x_hat * range_x, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            pos = position + (x_.get(0) + .5 * range_x) * x_hat + (y_.get(0) + .5 * range_y) * y_hat
            self._xy_mesh += [box(pos=pos, length=range_x, width=scale, height=range_y, opacity=0.15, visible=False)]
            self._xz_mesh += [
                cylinder(pos=position + pos_x_z + x_hat * j * delta_x, axis=z_hat * range_z, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            self._xz_mesh += [
                cylinder(pos=position + pos_x_z + z_hat * j * delta_z, axis=x_hat * range_x, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            pos = position + (x_.get(0) + .5 * range_x) * x_hat + (z_.get(0) + .5 * range_z) * z_hat
            self._xz_mesh += [box(pos=pos, length=range_x, width=range_z, height=scale, opacity=0.15, visible=False)]
            self._yz_mesh += [
                cylinder(pos=position + pos_y_z + y_hat * j * delta_y, axis=z_hat * range_z, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            self._yz_mesh += [
                cylinder(pos=position + pos_y_z + z_hat * j * delta_z, axis=y_hat * range_y, color=color.gray(.5),
                         radius=scale * .5, visible=False)]
            pos = position + (y_.get(0) + .5 * range_y) * y_hat + (z_.get(0) + .5 * range_z) * z_hat
            self._yz_mesh += [box(pos=pos, length=scale, width=range_z, height=range_y, opacity=0.15, visible=False)]

    def _make_axis(self, x_, y_, z_, delta_x, delta_y, delta_z, axis_color, axis_labels, scale):
        c1 = cylinder(pos=x_hat * x_.get(0), axis=x_hat * (x_.get(-1) - x_.get(0)), color=axis_color, radius=scale)
        c2 = cylinder(pos=y_hat * y_.get(0), axis=y_hat * (y_.get(-1) - y_.get(0)), color=axis_color, radius=scale)
        c3 = cylinder(pos=z_hat * z_.get(0), axis=z_hat * (z_.get(-1) - z_.get(0)), color=axis_color, radius=scale)
        a1 = arrow(pos=x_hat * x_.get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_x * x_hat, round=True)
        a2 = arrow(pos=y_hat * y_.get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_y * y_hat, round=True)
        a3 = arrow(pos=z_hat * z_.get(-1), color=axis_color, shaftwidth=scale * 2, axis=2 * delta_z * z_hat, round=True)
        l1 = text(pos=x_hat * (x_.get(-1) + 2 * delta_x) - vec(0, scale, 0), text=axis_labels[0],
                  color=axis_color, height=scale * 7, billboard=True, emissive=True)
        l2 = text(pos=y_hat * (y_.get(-1) + 2 * delta_y) - vec(0, scale, 0), text=axis_labels[1],
                  color=axis_color, height=scale * 7, billboard=True, emissive=True)
        l3 = text(pos=z_hat * (z_.get(-1) + 2 * delta_z) - vec(0, scale, 0), text=axis_labels[2],
                  color=axis_color, height=scale * 7, billboard=True, emissive=True)
        return [c1, c2, c3, a1, a2, a3, l1, l2, l3]

    def _make_tick_marks(self, x_dim, y_dim, z_dim, tick_marks_color, scale):
        tick_marks = []
        for i in range(np.len(x_dim)):
            a_box = box(pos=x_hat * x_dim.get(i), width=scale * 2, height=scale * 5, length=scale * 2,
                        color=tick_marks_color)
            tick_marks.append(a_box)
        for i in range(np.len(z_dim)):
            a_box = box(pos=z_hat * z_dim.get(i), width=scale * 2, height=scale * 5, length=scale * 2,
                        color=tick_marks_color)
            tick_marks.append(a_box)
        for i in range(np.len(y_dim)):
            a_box = box(pos=y_hat * y_dim.get(i), width=scale * 2, height=scale * 5, length=scale * 2,
                        color=tick_marks_color)
            a_box.rotate(angle=0.5 * pi, axis=vec(0, 0, 1))
            tick_marks.append(a_box)
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


class plot3D:
    def __init__(self, f, xmin, xmax, ymin, ymax, zmin, zmax):
        # The x axis is labeled y, the z axis is labeled x, and the y axis is labeled z.
        # This is done to mimic fairly standard practive for plotting
        #     the z value of a function of x and y.
        self.f = f
        self.xmin = xmin if xmin else 0
        self.xmax = xmax if xmax else 0
        self.ymin = ymin if ymin else 0
        self.ymax = ymax if ymax else 0
        self.zmin = zmin if zmin else 0
        self.zmax = zmax if zmax else 0

        R = L / 100
        d = L - 2

        self.vertices = []
        values = self.f_values()
        for i in range(L * L):
            x = int(i / L)
            y = i % L
            self.vertices.append(self.make_vertex(x, y, values[i]))

        self.make_quads()
        self.make_normals()

    def f_values(self):
        function_values = []
        for i in range(L * L):
            x = int(i / L)
            y = i % L
            function_values.append(self.evaluate(self.f_x_y(x, y)))
        return function_values

    def f_x_y(self, x, y):
        d = L - 2
        x_ = self.xmin + x * (self.xmax - self.xmin) / d
        y_ = self.ymin + y * (self.ymax - self.ymin) / d
        return self.f(x_, y_)

    def evaluate(self, f_x_y):
        d = L - 2
        return (d / (self.zmax - self.zmin)) * (f_x_y - self.zmin)

    def make_quads(self):
        # Create the quad objects, based on the vertex objects already created.
        for x in range(L - 2):
            for y in range(L - 2):
                v0 = self.get_vertex(x, y)
                v1 = self.get_vertex(x + 1, y)
                v2 = self.get_vertex(x + 1, y + 1)
                v3 = self.get_vertex(x, y + 1)
                quad(vs=[v0, v1, v2, v3])

    def make_normals(self):
        # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
        # The vectors a and b point to the right and up around a vertex in the xy plane.
        for i in range(L * L):
            x = int(i / L)
            y = i % L
            if x == L - 1 or y == L - 1: continue
            v = self.vertices[i]
            a = self.vertices[i + L].pos - v.pos
            b = self.vertices[i + 1].pos - v.pos
            v.normal = cross(a, b)

    def replot(self):
        values = self.f_values()
        for i in range(L * L):
            self.vertices[i].pos.y = values[i]

        self.make_normals()

    def make_vertex(self, x, y, value):
        return vertex(pos=vec(y, value, x), color=color.cyan, normal=vec(0, 1, 0))

    def get_vertex(self, x, y):
        return self.vertices[x * L + y]

    def get_pos(self, x, y):
        return self.get_vertex(x, y).pos


def toggle_tick_marks(event):
    axis.tick_marks_visibility_is(event.checked)


def toggle_xz_mesh(event):
    axis.xz_mesh_visibility_is(event.checked)


def toggle_xy_mesh(event):
    axis.xy_mesh_visibility_is(event.checked)


def toggle_yz_mesh(event):
    axis.yz_mesh_visibility_is(event.checked)


def toggle_axis(event):
    axis.axis_visibility_is(event.checked)


animation.append_to_caption("\n")
_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=True)
_ = checkbox(text='YZ mesh', bind=toggle_yz_mesh, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=False)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)

space = Space(np.linspace(-0, L, 11), np.linspace(0, L * .8, 11), np.linspace(0, L, 11))
axis = Base(space)

t = 0
dt = 0.02


def f(x, y):
    # Return the value of the function of x and y:
    return 0.4 + 0.2 * sin(10 * x) * cos(10 * y) * sin(5 * t)


p = plot3D(f, 0, 1, 0, 1, 0, 1)  # function, xmin, xmax, ymin, ymax (defaults 0, 1, 0, 1, 0, 1)

run = True


def running(ev):
    global run
    run = not run


animation.bind('mousedown', running)
animation.forward = vec(-0.7, -0.5, -1)

while True:
    # print("scene.forward=" + str(animation.forward))
    # print("scene.range=" + str(animation.range))
    rate(30)
    if run:
        p.replot()
        t += dt
