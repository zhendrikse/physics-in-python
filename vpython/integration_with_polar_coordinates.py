#Web VPython 3.2

from vpython import label, vec, vector, canvas, rate, color, cylinder, box, arange, pi, cos, sin, wtext, slider, sign, checkbox

display = canvas(background=color.gray(0.075), height=500, forward=vec(-.4, -.7, -.6), up=vec(0, 0, 1), center=vec(0, .35, -.40))

x_hat = vec(0, 1, 0)
y_hat = vec(0, 0, 1)
z_hat = vec(1, 0, 0)
base = [x_hat, y_hat, z_hat]

class Base:
    def __init__(self, xx, yy, zz, axis_color, tick_marks_color, num_tick_marks):
        x_min, x_max = min(xx), max(xx)
        y_min, y_max = min(yy), max(yy)
        z_min, z_max = min(zz), max(zz)
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

        pos = position + (x_hat + z_hat) * .5 * max_of_base
        self._mesh += [box(pos=pos, length=max_of_base, width=radius, height=max_of_base,opacity=0.05)]
        pos = position + (z_hat + y_hat) * .5 * max_of_base
        self._mesh += [box(pos=pos, length=max_of_base, width=max_of_base, height=radius, opacity=0.05)]
        pos = position + (y_hat + x_hat) * .5 * max_of_base
        self._mesh += [box(pos=pos, length=radius, width=max_of_base, height=max_of_base, opacity=0.05)]

    def tick_marks_visibility_is(self, event):
        for tick_mark in self._tick_marks:
            tick_mark.visible = event.checked

    def mesh_visibility_is(self, event):
        for i in range(len(self._mesh)):
            self._mesh[i].visible = event.checked

    def axis_labels_visibility_is(self, event):
        for i in range(len(self._axis_labels)):
            self._axis_labels[i].visible = event.checked

x_range = arange(-1.25, 1.25, .1)
y_range = arange(-1.25, 1.25, .1)
axis = Base(x_range, y_range, arange(-1, 1, .1), color.yellow, color.green, 10)


phi_max = 2 * pi
da = 0.05


def f(theta, phi):
    #f = 1
    #    f = t
    #    f = p
    #    f = (p-pi)**2
    return theta * theta * (phi - pi) * (phi -pi)


R = 1

class Element:
    def __init__(self, position, size, opacity, theta, phi, f_theta_phi):
        self._element = box(pos=position, opacity=opacity, size=size)
        self._theta = theta
        self._phi = phi
        self._f_theta_phi = f_theta_phi

    def update(self, theta_min, theta_max, phi_min, phi_max):
        if theta_min <= self._theta <= theta_max and phi_min <= self._phi <= phi_max:
            self._element.visible = True
        elif theta_min >= self._theta >= theta_max and phi_min >= self._phi >= phi_max:
            self._element.visible = True
        else:
            self._element.visible = False

    def f_theta_phi(self):
        return self._f_theta_phi

    def value(self):
        return self._f_theta_phi * sin(self._theta) if self._element.visible else 0

    def set_color(self, colour):
        self._element.color = colour

    def set_opacity_to(self, value):
        self._element.opacity = value


# t = theta, azimuthal angle
# p = phi, planar angle
class Sphere:
    def __init__(self, theta_min, theta_max, phi_min, phi_max):
        self._opacity = 0.35
        self._theta_min, self._theta_max, self._phi_min, self._phi_max = theta_min, theta_max, phi_min, phi_max
        self._cells = []

        f_values = []
        theta = theta_min
        while theta <= theta_max:
            phi = phi_min
            while phi <= phi_max:
                f_values.append(f(theta, phi))
                pos = R * vector(R * sin(theta) * cos(phi), R * sin(theta) * sin(phi), R * cos(theta))
                self._cells.append(Element(pos, da * vector(1, 1, 1), self._opacity, theta, phi, f(theta, phi)))
                phi += da
            theta += da

        f_max = max(f_values)
        f_min = min(f_values)
        df = f_max - f_min
        if df == 0:
            df = 1
            f_max = 1
            f_min = 0
        for cell in self._cells:
            # Red --> maximum value
            # Blue --> minimum value
            cell.set_color(vector(f_max - cell.f_theta_phi(), cell.f_theta_phi() - f_min, 0) / df)


    def _update_cells(self):
        for cell in self._cells:
            cell.update(self._theta_min, self._theta_max, self._phi_min, self._phi_max)
        #    for r in riemann:
        #        if (xmin_sl.value < r.pos.x < xmax_sl.value and ymin_sl.value < r.pos.z < ymax_sl.value):
        #            r.color = vector(0.8,0.8,0.8)
        #            r.opacity = 1
        #        else if (xmin_sl.value > r.pos.x > xmax_sl.value and ymin_sl.value > r.pos.z > ymax_sl.value):
        #            r.color = color.red
        #            r.opacity = 1
        #        else:
        #            r.opacity = 0

    def set_phi_max_to(self, value):
        self._phi_max = value
        self._update_cells()

    def set_phi_min_to(self, value):
        self._phi_min = value
        self._update_cells()

    def set_theta_max_to(self, value):
        self._theta_max = value
        self._update_cells()

    def set_theta_min_to(self, value):
        self._theta_min = value
        self._update_cells()

    def integrate(self):
        integral = 0
        for cell in self._cells:
            integral += cell.value()
        return integral * R ** 2 * da ** 2 * sign(self._theta_max - self._theta_min) * sign(self._phi_max - self._phi_min)

    def set_opacity_to(self, value):
        self._opacity = value
        for element in self._cells:
            element.set_opacity_to(value)


sphere_ = Sphere(0, pi, 0, 2 * pi)

def set_theta_min(event):
    sphere_.set_theta_min_to(event.value)
    theta_min_text.text = 'θ_min = ' + '{:1.2f}'.format(event.value) + "\n\n"
    make_caption()

def set_theta_max(event):
    sphere_.set_theta_max_to(event.value)
    theta_max_text.text = 'θ_max = ' + '{:1.2f}'.format(event.value) + "\n\n"
    make_caption()

def set_phi_min(event):
    sphere_.set_phi_min_to(event.value)
    phi_min_text.text = 'φ_min = ' + '{:1.2f}'.format(event.value) + "\n\n"
    make_caption()

def set_phi_max(event):
    sphere_.set_phi_max_to(event.value)
    phi_max_text.text = 'φ_max = ' + '{:1.2f}'.format(event.value) + "\n\n"
    make_caption()


def integrate():
    return sphere_.integrate()

def adjust_opacity(event):
    sphere_.set_opacity_to(event.value)
    opacity_slider_text.text = "= {:1.2f}".format(event.value, 2)

_ = checkbox(text='Mesh ', bind=axis.mesh_visibility_is, checked=True)
_ = checkbox(text='Axis labels ', bind=axis.axis_labels_visibility_is, checked=True)
_ = checkbox(text='Tick marks ', bind=axis.tick_marks_visibility_is, checked=True)

display.append_to_caption("\n\nOpacity")
_ = slider(min=0, max=1, step=0.01, value=.35, bind=adjust_opacity)
opacity_slider_text = wtext(text="= 0.35")

def make_caption():
    int_text.text = 'Integral = ' + '{:1.2f}'.format(integrate())
    return


display.append_to_caption("\n\nSet the integration range below.\n\n")

_ = slider(min=0, max=pi, value=0, length=220, bind=set_theta_min, right=15)
theta_min_text = wtext(text='θ_min = ' + '{:1.2f}'.format(0) + "\n\n")
_ = slider(min=0, max=pi, value=pi, length=220, bind=set_theta_max, right=15)
theta_max_text = wtext(text='θ_max = ' + '{:1.2f}'.format(pi) + "\n\n")
_ = slider(min=0, max=2 * pi, value=0, length=220, bind=set_phi_min, right=15)
phi_min_text = wtext(text='φ_min = ' + '{:1.2f}'.format(0) + "\n\n")
_ = slider(min=0, max=2 * pi, value=2 * pi, length=220, bind=set_phi_max, right=15)
phi_max_text = wtext(text='φ_max = ' + '{:1.2f}'.format(2 * pi) + "\n\n")

int_text = wtext(text='Integral = ' + '{:1.2f}'.format(integrate()))
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

# make_caption()
while True:
    rate(10)
