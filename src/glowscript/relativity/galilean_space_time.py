#Web VPython 3.2

from vpython import vec, rate, graph, gcurve, color, label, vector, points, canvas, box, arrow, cylinder

#
# Zeger Hendrikse: https://github.com/zhendrikse
#
class Timer:

    def __init__(self, position=vector(0, 0, 0), use_scientific=False, relative_to=None, timer_color=color.white):
        self._use_scientific = use_scientific
        self._relative_to = relative_to
        self._distance_to_attached_object = relative_to.position - position if relative_to else 0
        if use_scientific:
            self._timer_label = label(pos=position, text='00E01', box=False, color=timer_color)
        else:
            self._timer_label = label(pos=position, text='00:00:00.00', box=False, color=timer_color)

    def update(self, t):
        # Basically just use sprintf formatting according to either stopwatch or scientific notation
        if self._relative_to:
            self._timer_label.pos = self._distance_to_attached_object + self._relative_to.position

        if self._use_scientific:
            self._timer_label.text = "%.4E".format(t)
            return

        hours = int(t / 3600)
        minutes = int((t / 60) % 60)
        secs = int(t % 60)
        frac = int(round(100 * (t % 1)))
        if frac == 100:
            frac = 0
            secs = secs + 1

        self._timer_label.text = "{:02d}:".format(hours) + "{:02d}:".format(minutes) + "{:02d}.".format(
            secs) + "{:02d}".format(frac)


class Axis:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, num_tick_marks=11,
                 length=10, orientation="x", label_orientation="down", offset=0):
        self._axis = vec(1, 0, 0) if orientation == "x" else vec(0, 1, 0)
        self._start = -self._axis * length / 2 + position
        self._end = self._axis * length / 2 + position

        self._num_tick_marks = num_tick_marks
        self._length = length
        self._offset = offset
        self._label_shifts = {
            "up": vector(0, -0.05 * self._length, 0),
            "down": vector(0, 0.05 * self._length, 0),
            "left": vector(-0.1 * self._length, 0, 0),
            "right": vector(0.1 * self._length, 0, 0)}

        self._label_shift = vector(0, -0.05 * self._length, 0)
        if label_orientation == "up":
            self._label_shift = vector(0, 0.05 * self._length, 0)
        elif label_orientation == "left":
            self._label_shift = vector(-0.1 * self._length, 0, 0)
        elif label_orientation == "right":
            self._label_shift = vector(0.1 * self._length, 0, 0)

        tick_positions = []
        self._tick_labels = []
        tick_increment = (self._end - self._start) / (num_tick_marks - 1)
        for i in range(num_tick_marks):
            tick_position = self._start + i * tick_increment
            tick_positions += [tick_position]
            label_value = offset + tick_position.x if orientation == "x" else tick_position.y
            label_text = str(round(label_value, 2))
            self._tick_labels += [label(pos=tick_position + self._label_shift, text=label_text, box=False)]

        self._ticks = points(pos=tick_positions, radius=10, color=tick_marks_color)
        self._cylinder = cylinder(pos=self._start, axis=self._end - self._start, radius=self._ticks.radius / 100,
                                  color=axis_color)

        self._x_axis = arrow(pos=position, axis=vec(2, 0, 0), color=axis_color, shaftwidth=0.15)
        self._y_axis = arrow(pos=position, axis=vec(0, 2, 0), color=axis_color, shaftwidth=0.15)
        self._z_axis = arrow(pos=position, axis=vec(0, 0, 2), color=axis_color, shaftwidth=0.15)
        self._x_axis_label = label(pos=position + vec(2, 0, 0), text="x", box=False, color=tick_marks_color)
        self._y_axis_label = label(pos=position + vec(0, 2, 0), text="y", box=False, color=tick_marks_color)
        self._z_axis_label = label(pos=position + vec(0, 0, 2), text="z", box=False, color=tick_marks_color)

    def reorient_with(self, other_object):
        other_objects_position = other_object.position()
        self._start = -self._axis * self._length / 2 + other_objects_position
        self._end = self._axis * self._length / 2 + other_objects_position
        tick_increment = (self._end - self._start) / (self._num_tick_marks - 1)
        for i in range(self._num_tick_marks):
            tick_position = self._start + i * tick_increment
            self._ticks.modify(i, pos=tick_position)
            self._tick_labels[i].pos = tick_position + self._label_shift

        self._cylinder.pos = self._start
        self._x_axis.pos = other_objects_position
        self._y_axis.pos = other_objects_position
        self._z_axis.pos = other_objects_position
        self._x_axis_label.pos = other_objects_position + vec(2, 0, 0)
        self._y_axis_label.pos = other_objects_position + vec(0, 2, 0)
        self._z_axis_label.pos = other_objects_position + vec(0, 0, 2)

    def show_unit_vectors(self):
        self._x_axis.visible = True
        self._y_axis.visible = True
        self._z_axis.visible = True
        self._x_axis_label.visible = True
        self._y_axis_label.visible = True
        self._z_axis_label.visible = True

    def hide_unit_vectors(self):
        self._x_axis.visible = False
        self._y_axis.visible = False
        self._z_axis.visible = False
        self._x_axis_label.visible = False
        self._y_axis_label.visible = False
        self._z_axis_label.visible = False


class Car:
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), colour=color.green, draw=True):
        self._position = self._start_position = position
        self._velocity = velocity
        self._car = box(pos=position, length=2.5, height=1, width=1, color=colour) if draw else None
        self._label = label(pos=vec(position.x, position.y + 1.52, position.z), text="Select my perspective",
                            color=colour, line=True) if draw else None

    def reset(self):
        self._position = self._start_position

    def show_label(self):
        self._label.visible = True

    def hide_label(self):
        self._label.visible = False

    def _draw(self):
        if self._label:
            self._car.pos = self._position
            self._label.pos = vec(self._position.x, self._position.y + 1.5, self._position.z)

    def move(self, dt):
        self._position += self._velocity * dt
        self._draw()

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity


animation_time = 15  # seconds

scene = canvas(width="800", height="600")
scene.title = "Relative motion: click on car to change perspective!"
scene.center = vec(0, 0, 0)
scene.forward = vec(0, -0.35, -1)
scene.range = 11
scene.caption = "Galilean transformation \\(  \\begin{pmatrix} x' \\\\ t'\\end{pmatrix} = \\begin{pmatrix} 1 & -v \\\\ 0 & 1 \\end{pmatrix} \\begin{pmatrix} x \\\\ t \\end{pmatrix} \\)"
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

green_car = Car(position=vec(-10, 0, -5), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 5), colour=color.red)
red_car.hide_label()

axis_green_car = Axis(num_tick_marks=11, length=30, position=vec(-10, 0, -5), offset=10)  # , label_orientation="down")
axis_red_car = Axis(num_tick_marks=11, length=30, position=vec(0, 0, 5), offset=0)  # , label_orientation="down")
axis_green_car.hide_unit_vectors()

space_time_graph_red = graph(width=350, height=150, title="Space-time graph for red inertial frame", xtitle="Position",
                             ytitle="Time", ymax=2 * animation_time,
                             xmin=-animation_time, xmax=animation_time)
red_curve_green_car = gcurve(graph=space_time_graph_red, color=color.green)
red_curve_red_car = gcurve(graph=space_time_graph_red, color=color.red)

space_time_graph_green = graph(width=350, height=150, title="Space-time for green inertial frame", xtitle="Position",
                               ytitle="Time", ymax=2 * animation_time,
                               xmin=-animation_time, xmax=animation_time)
green_curve_green_car = gcurve(graph=space_time_graph_green, color=color.green)
green_curve_red_car = gcurve(graph=space_time_graph_green, color=color.red)


def select_car_in(my_scene):
    selected_object = my_scene.mouse.pick
    if selected_object is None:
        return
    my_scene.camera.follow(selected_object)
    if selected_object.color == color.green:
        # scene.forward = vec(-0.00101513, -0.770739, 0.637151)
        scene.range = 17
        green_car.hide_label()
        red_car.show_label()
        axis_green_car.show_unit_vectors()
        axis_red_car.hide_unit_vectors()
    elif selected_object.color == color.red:
        # scene.forward = vec(0.00813912, -0.581035, -0.813838)
        scene.range = 11
        red_car.hide_label()
        green_car.show_label()
        axis_red_car.show_unit_vectors()
        axis_green_car.hide_unit_vectors()


def on_mouse_click():
    select_car_in(scene)

scene.bind('click', on_mouse_click)

timer = Timer(position=vec(0, 5, 0))
dt = 0.01
while True:
    t = 0

    while green_car.position().x <= animation_time:
        rate(1 / dt)
        green_car.move(dt)
        red_curve_green_car.plot(green_car.position().x, t)
        red_curve_red_car.plot(red_car.position().x, t)

        green_curve_red_car.plot(-green_car.position().x, t)
        green_curve_green_car.plot(-red_car.position().x, t)

        timer.update(t)
        axis_green_car.reorient_with(green_car)

        t += dt

    label(pos=vec(0, 7, 0), text="Click mouse to restart", color=color.yellow)
    scene.waitfor('click')
    green_car.reset()
    red_car.reset()
    axis_green_car.reorient_with(green_car)
    axis_red_car.reorient_with(red_car)


