# Web VPython 3.2

from vpython import canvas, box, vector, sphere, sin, cos, rate, pi, arrow, slider, wtext, cross, color, vec, cylinder, \
    text, label, box, checkbox, radians, get_library

title = """Helical motion of charged particle in magnetic field

&#x2022; Based on <a href="https://towardsdatascience.com/simple-physics-animations-using-vpython-1fce0284606">Simple Physics Animations Using VPython</a> by Zhiheng Jiang
&#x2022; Refactored and maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

animation = canvas(width=800, height=600, title=title, range=40, forward=vec(-0.381663, -0.605187, -0.698629))

# https://github.com/nicolaspanel/numjs
get_library('https://cdn.jsdelivr.net/gh/nicolaspanel/numjs@0.15.1/dist/numjs.min.js')


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


xlen, ylen, zlen = 100, 100, 100
boundaries = [
    box(pos=vector(0, -ylen / 2, 0), size=vector(xlen, .2, zlen), visible=False),
    box(pos=vector(0, ylen / 2, 0), size=vector(xlen, .2, zlen), visible=False),
    box(pos=vector(-xlen / 2, 0, 0), size=vector(.2, ylen, zlen), visible=False),
    box(pos=vector(xlen / 2, 0, 0), size=vector(.2, ylen, zlen), visible=False),
    box(pos=vector(0, 0, -zlen / 2), size=vector(xlen, ylen, .2), visible=False)
]

dt = .001  # time step


class MagneticField:
    def __init__(self, strength=3):
        self._magnetic_field = vector(0, -strength, 0)

    def field(self):
        return self._magnetic_field

    def strength_is(self, field_strength):
        self._magnetic_field = vector(0, -field_strength, 0)


class Proton:
    def __init__(self, position=vector(0, -ylen / 2 + 1, 0), v_mag=20, theta=10, charge=0.8):
        self._v_mag = v_mag
        self._angle = radians(theta)
        self._velocity = v_mag * vector(cos(self._angle), sin(self._angle), 0)
        self._initial_velocity = self._velocity
        self._initial_position = position
        self._proton = sphere(pos=position, color=color.red, radius=1, make_trail=True, trail_type="curve")
        self._charge = charge

    def move(self, magn_field):  # moves proton by small step
        acceleration = self._charge * cross(self._velocity, magn_field)  # F = ma = q v x B
        self._velocity += acceleration * dt  # a = dv/dt
        self._proton.pos += self._velocity * dt  # v = dx/dt

    def reset_proton(self):  # resets proton position and path
        self._proton.pos = self._initial_position
        self._velocity = self._initial_velocity
        self._proton.clear_trail()

    def charge_is(self, new_charge):
        self._charge = new_charge

    def angle_is(self, new_angle):
        self._angle = new_angle
        self._velocity = self._v_mag * vector(cos(self._angle), sin(self._angle), 0)

    def check_collision(self):  # checks for boundaries
        return ylen / 2 > self._proton.pos.y > -ylen / 2 and xlen / 2 > self._proton.pos.x > -xlen / 2 and -zlen / 2 < self._proton.pos.z < zlen / 2


space = Space(np.linspace(-xlen / 4, xlen / 4, 11), np.linspace(-xlen / 4, xlen / 4, 11),
              np.linspace(-xlen / 4, xlen / 4, 11))
axis = Base(space)
axis.xz_mesh_visibility_is(True)
axis.tick_marks_visibility_is(False)


def toggle_box(event):
    for boundary in boundaries:
        boundary.visible = event.checked


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
_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=False)
_ = checkbox(text='YZ mesh', bind=toggle_yz_mesh, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)

_ = checkbox(text="Show box", bind=toggle_box, checked=False)

pop_up = label(pos=vec(0, 32, 0), text="Click mouse button to start", visible=True, box=False)
proton = Proton()
magnetic_field = MagneticField()


def launch():
    pop_up.visible = False
    proton.reset_proton()
    while proton.check_collision():
        rate(1 / dt)
        proton.move(magnetic_field.field())
    pop_up.visible = True


animation.bind("click", launch)


def adjust_bfield():
    magnetic_field.strength_is(b_field_slider.value)
    b_field_text.text = str(b_field_slider.value) + " Tesla"


animation.append_to_caption("\n")
b_field_slider = slider(min=1, max=10, step=.5, value=5, bind=adjust_bfield)
animation.append_to_caption(" B-field Strength = ")
b_field_text = wtext(text="3 Tesla")
animation.append_to_caption("\n\n")


def adjust_q():
    proton.charge_is(charge_slide.value)
    charge_text.text = str(charge_slide.value) + " Coulumbs"


charge_slide = slider(min=0, max=1, step=.1, value=.8, bind=adjust_q)
animation.append_to_caption(" Q = ")
charge_text = wtext(text="0.8 Coulumbs")
animation.append_to_caption("\n\n")


def adjust_angle():
    proton.angle_is(radians(angle_slider.value))
    angle_text.text = str(angle_slider.value) + " degrees"


angle_slider = slider(min=0, max=90, step=1, value=10, bind=adjust_angle)
animation.append_to_caption(" Angle = ")
angle_text = wtext(text="10 degrees")

while True:
    rate(10)

