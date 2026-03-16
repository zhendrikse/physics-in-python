#Web VPython 3.2

from vpython import simple_sphere, rate, color, vec, arange, canvas, cylinder, box, label, sin, cos, slider, wtext, pi, radio, checkbox

title="""&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/waves/code/vibrating_membrane.py">vibrating_membrane.py</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; Visualization concept with spheres by <a href="https://jexpearce.github.io/jex/">Jex Pearce</a>

"""

Lx, Ly = 3 * pi, 3 * pi
dx, dy = 0.1, 0.1
animation = canvas(forward=vec(-2.5, -2.2, -2.2), center=vec(5.5, 4, 3),
                   up=vec(0, 0, 1), title=title, height=500,
                   background=color.gray(0.075), range=9)

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


class Membrane:
    def __init__(self, x, y, f_x_y_t):
        self._x, self._y, self._f_x_y_t = x, y, f_x_y_t
        self._hue = 0.
        self._radius = 0.075
        self._amplitude = 2.0
        self._omega = 2 * pi

        self._init_droplets()

    def _init_droplets(self):
        self._surface = []
        for i in range(len(self._x)):
            droplets_row = []
            for j in range(len(self._y)):
                colour = color.hsv_to_rgb(vec(self._hue, 1, 1))
                position = vec(self._x[i], self._y[j]-1, Lx/2)
                droplets_row.append(simple_sphere(pos=position, radius=self._radius, color=colour))
            self._surface.append(droplets_row)

    def update(self, t):
        for i in range(0, len(self._x)):
            for j in range(0, len(self._y)):
                self._surface[i][j].pos.z = Lx/2 + self._amplitude * self._f_x_y_t(self._x[i], self._y[j], self._omega, t)
                self._surface[i][j].color = color.hsv_to_rgb(vec(.05 * abs(self._surface[i][j].pos.z) + self._hue, 1, 1))

    def set_hue_value_to(self, new_hue_value):
        self._hue = new_hue_value

    def set_amplitude_to(self, new_value):
        self._amplitude = new_value

    def set_omega_to(self, new_value):
        self._omega = new_value

    def set_wave_function_to(self, normal_mode):
        self._f_x_y_t = normal_mode

    def set_droplet_radius_to(self, new_radius):
        self._radius = new_radius
        for i in range(len(self._x)):
            for j in range(len(self._y)):
                self._surface[i][j].radius = new_radius

class RadioButton:
    def __init__(self, button_, membrane_):
        self._button = button_
        self._membrane = membrane_

    def uncheck(self):
        self._button.checked = False

    def push(self, button_name):
        i = int(button_name[0])
        j = int(button_name[-1])
        self._membrane.set_wave_function_to(modes[i][j])

    def check(self):
        self._button.checked = True

    def name(self):
        return self._button.name

class RadioButtons:
    def __init__(self):
        self._radio_buttons = []
        self._selected_button = None

    def add(self, button_, membrane_):
        self._radio_buttons.append(RadioButton(button_, membrane_))

        if (len(self._radio_buttons) % 3) == 0:
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
        self._selected_button.push(button_name)

    def get_selected_button_name(self):
        return self._selected_button.name()


def mode_1_1(x, y, omega, t):
    return cos(omega * t) * sin(1 * x / 3) * sin(1 * y / 3)

def mode_2_1(x, y, omega, t):
    return cos(omega * t) * sin(2 * x / 3) * sin(1 * y / 3)

def mode_3_1(x, y, omega, t):
    return cos(omega * t) * sin(x) * sin(1 * y / 3)

def mode_1_2(x, y, omega, t):
    return cos(omega * t) * sin(1 * x / 3) * sin(2 * y / 3)

def mode_2_2(x, y, omega, t):
    return cos(omega * t) * sin(2 * x / 3) * sin(2 * y / 3)

def mode_3_2(x, y, omega, t):
    return cos(omega * t) * sin(x) * sin(2 * y / 3)

def mode_1_3(x, y, omega, t):
    return cos(omega * t) * sin(1 * x / 3) * sin(y)

def mode_2_3(x, y, omega, t):
    return cos(omega * t) * sin(2 * x / 3) * sin(y)

def mode_3_3(x, y, omega, t):
    return cos(omega * t) * sin(x) * sin(y)

x_range = arange(0, Lx + dx, dx)
y_range = arange(0, Ly + dy, dy)
modes = [[mode_1_1, mode_2_1, mode_3_1], [mode_1_2, mode_2_2, mode_3_2], [mode_1_3, mode_2_3, mode_3_3]]
membrane = Membrane(x_range, y_range, modes[0][0])
axis = Base(x_range, y_range, arange(-1, 1, dx), color.yellow, color.green, 10)

################
# GUI controls #
################

def adjust_offset():
    membrane.set_hue_value_to(offset_slider.value)
    hue_offset_text.text = "{:1.2f}".format(offset_slider.value, 2)


def adjust_amplitude():
    membrane.set_amplitude_to(amplitude_slider.value)
    amplitude_text.text = "{:1.2f}".format(amplitude_slider.value, 2)


def adjust_droplet_radius():
    membrane.set_droplet_radius_to(radius_slider.value * .01)
    droplet_radius_text.text = "{:1.2f}".format(radius_slider.value, 2)

def adjust_omega():
    membrane.set_omega_to(omega_slider.value)
    omega_slider_text.text = "= {:1.2f}".format(omega_slider.value / pi, 2) + " π"

_ = checkbox(text='Mesh ', bind=axis.mesh_visibility_is, checked=True)
_ = checkbox(text='Axis labels ', bind=axis.axis_labels_visibility_is, checked=True)
_ = checkbox(text='Tick marks ', bind=axis.tick_marks_visibility_is, checked=True)

def toggle(event):
    radio_buttons.toggle(event.name)

animation.append_to_caption("\n\n")
radius_slider = slider(min=1, max=10, value=7.5, step=.1, bind=adjust_droplet_radius)
animation.append_to_caption("droplet radius = ")
droplet_radius_text = wtext(text="7.50")

animation.append_to_caption("\n\n")
offset_slider = slider(min=0, max=1, value=0.0, bind=adjust_offset)
animation.append_to_caption("hue offset = ")
hue_offset_text = wtext(text="0.00")

animation.append_to_caption("\n\n")
omega_slider = slider(min=0, max=2 * pi, value=2 * pi, bind=adjust_omega)
omega_slider_text = wtext(text="omega = 2π")

animation.append_to_caption("\n\n")
amplitude_slider = slider(min=0.1, max=3, value=2, bind=adjust_amplitude)
animation.append_to_caption("amplitude = ")
amplitude_text = wtext(text="2.00")

animation.append_to_caption("\n\n")
radio_buttons = RadioButtons()
for i in range(3):
    for j in range(3):
        radio_buttons.add(radio(bind=toggle, text=" Mode " + str(i + 1) + "," + str(j + 1) + " ", name=str(i) + "_" + str(j)), membrane)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

time = 0
dt = 0.025
while True:
    rate(20)
    membrane.update(time)
    time += dt
