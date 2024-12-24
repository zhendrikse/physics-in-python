from vpython import vec, rate, graph, gcurve, color, scene, label, vector, points, curve, box, pyramid, sphere, arrow

def obj_size(obj):
    if type(obj) == box or type(obj) == pyramid:
        return obj.size
    elif type(obj) == sphere:
        return vector(obj.radius, obj.radius, obj.radius)


class Axis:

    def __init__(self, attached_to, num_labels, axis_type="x", axis=vector(1, 0, 0), start_pos=None, length=None,
                 labels=None, label_orientation="down", axis_color=color.yellow, label_color=color.white):
        # attached_to - Object which axis is oriented based on by default
        # numLabels - number of labels on axis
        # axisType - sets whether this is a default axis of x or y, or an arbitrary axis
        # axis - unit vector defining the orientation of the axis to be created IF axisType = "arbitrary"
        # startPos - start position for the axis - defaults to (-obj_size(obj).x/2,-4*obj_size(obj).y,0)
        # length - length of the axis - defaults to obj_size(obj).x
        # labelOrientation - how labels are placed relative to axis markers - "up", "down", "left", or "right"

        self.interval_markers = []
        self.interval_labels = []
        self.labelText = labels
        self.obj = attached_to
        self.lastPos = vector(attached_to.pos.x, attached_to.pos.y, attached_to.pos.z)
        self.numLabels = num_labels
        self.axisType = axis_type
        self.axis = axis if axis_type != "y" else vector(0, 1, 0)
        self.length = length if (length is not None) else obj_size(attached_to).x
        self.startPos = start_pos if (start_pos is not None) else vector(-obj_size(attached_to).x / 2,
                                                                         -4 * obj_size(attached_to).y, 0)
        self.axisColor = axis_color
        self.labelColor = label_color

        if label_orientation == "down":
            self.labelShift = vector(0, -0.05 * self.length, 0)
        elif label_orientation == "up":
            self.labelShift = vector(0, 0.05 * self.length, 0)
        elif label_orientation == "left":
            self.labelShift = vector(-0.1 * self.length, 0, 0)
        elif label_orientation == "right":
            self.labelShift = vector(0.1 * self.length, 0, 0)

        self.__reorient()

    def update(self):
        # Determine if reference obj. has shifted since last update, if so shift us too
        if self.obj.pos != self.lastPos:
            diff = self.obj.pos - self.lastPos

            for i in range(len(self.interval_markers)):
                self.interval_markers[i].pos += diff
                self.interval_labels[i].pos += diff
            self.axisCurve.pos = [x + diff for x in self.axisCurve.pos]

            self.lastPos = vector(self.obj.pos.x, self.obj.pos.y, self.obj.pos.z)

    def reorient(self, axis=None, start_pos=None, length=None, labels=None, label_orientation=None):
        # Determine which, if any, parameters are being modified
        self.axis = axis if axis is not None else self.axis
        self.startPos = start_pos if start_pos is not None else self.startPos
        self.length = length if length is not None else self.length
        self.labelText = labels if labels is not None else self.labels

        # Re-do label orientation as well, if it has been set
        if label_orientation == "down":
            self.labelShift = vector(0, -0.05 * self.length, 0)
        elif label_orientation == "up":
            self.labelShift = vector(0, 0.05 * self.length, 0)
        elif label_orientation == "left":
            self.labelShift = vector(-0.1 * self.length, 0, 0)
        elif label_orientation == "right":
            self.labelShift = vector(0.1 * self.length, 0, 0)

        self.__reorient()

    def __reorient(self):
        # Actual internal axis setup code... determines first whether we are creating or updating
        updating = True if len(self.interval_markers) > 0 else False

        # Then determines the endpoint of the axis and the interval
        final = self.startPos + (self.length * self.axis)
        interval = (self.length / (self.numLabels - 1)) * self.axis

        # Loop for each interval marker, setting up or updating the markers and labels
        i = 0
        while i < self.numLabels:
            interval_pos = self.startPos + (i * interval)

            # Determine text for this label
            if self.labelText is not None:
                label_text = self.labelText[i]
            elif self.axisType == "y":
                label_text = str(round(interval_pos.y, 2))
            else:
                label_text = str(round(interval_pos.x, 2))

            if updating:
                self.interval_markers[i].pos = interval_pos
                self.interval_labels[i].pos = interval_pos + self.labelShift
                self.interval_labels[i].text = str(label_text)
            else:
                self.interval_markers.append(points(pos=interval_pos, color=self.axisColor, radius=5))
                self.interval_labels.append(
                    label(pos=interval_pos + self.labelShift, text=str(label_text), box=False, height=10,
                          color=self.labelColor))
            i = i + 1

        # Finally, create / update the line itself!
        if updating:
            self.axisCurve.pos = [self.startPos, final]
        else:
            self.axisCurve = curve(pos=[self.startPos, final], color=self.axisColor)


class PhysTimer:

    def __init__(self, x, y, use_scientific=False, timer_color=color.white):
        # x,y - world coordinates for the timer location
        # use_scientific - bool to turn off/on scientific notation for time
        # timer_color - attribute controlling the color of the text

        self.use_scientific = use_scientific
        self.timerColor = timer_color
        if use_scientific is False:
            self.timerLabel = label(pos=vector(x, y, 0), text='00:00:00.00', box=False)
        else:
            self.timerLabel = label(pos=vector(x, y, 0), text='00E01', box=False)

    def update(self, t):
        # Basically just use sprintf formatting according to either stopwatch or scientific notation
        if self.use_scientific:
            self.timerLabel.text = "%.4E" % t
        else:
            hours = int(t / 3600)
            mins = int((t / 60) % 60)
            secs = int(t % 60)
            frac = int(round(100 * (t % 1)))
            if frac == 100:
                frac = 0
                secs = secs + 1
            self.timerLabel.text = "{:02d}:".format(hours) + "{:02d}:".format(mins) + "{:02d}.".format(
                secs) + "{:02d}".format(frac)


class Car:
    def __init__(self, position=vec(0, 0, 0), velocity=vec(0, 0, 0), colour=color.green, draw=True):
        self._position = position
        self._velocity = velocity
        self._car = box(pos=position, length=2.5, height=1, width=1, color=colour) if draw else None
        self._label = label(pos=vec(position.x, position.y + 2, position.z), text="Select my perspective", color=colour,
                            line=True) if draw else None
        self._x_axis = arrow(pos=position, axis=vec(2, 0, 0), color=color.magenta, shaftwidth=0.15) if draw else None
        self._x_axis_label = label(pos=vec(position.x + 2, position.y, position.z), text="x",
                                   color=colour) if draw else None
        self._y_axis = arrow(pos=position, axis=vec(0, 2, 0), color=color.magenta, shaftwidth=0.15) if draw else None
        self._y_axis_label = label(pos=vec(position.x, position.y + 2, position.z), text="y",
                                   color=colour) if draw else None
        self._z_axis = arrow(pos=position, axis=vec(0, 0, 2), color=color.magenta, shaftwidth=0.15) if draw else None
        self._z_axis_label = label(pos=vec(position.x, position.y, position.z + 2), text="z",
                                   color=colour) if draw else None

    def show_axis(self):
        self._x_axis.visible = True
        self._y_axis.visible = True
        self._z_axis.visible = True
        self._x_axis_label.visible = True
        self._y_axis_label.visible = True
        self._z_axis_label.visible = True

    def hide_axis(self):
        self._x_axis.visible = False
        self._y_axis.visible = False
        self._z_axis.visible = False
        self._x_axis_label.visible = False
        self._y_axis_label.visible = False
        self._z_axis_label.visible = False

    def show_label(self):
        self._label.visible = True

    def hide_label(self):
        self._label.visible = False

    def _draw(self):
        if self._label:
            self._car.pos = self._position
            self._label.pos = vec(self._position.x, self._position.y + 2, self._position.z)
            self._x_axis.pos = self._position
            self._x_axis_label.pos = vec(self._position.x + 2, self._position.y, self._position.z)
            self._y_axis.pos = self._position
            self._y_axis_label.pos = vec(self._position.x, self._position.y + 2, self._position.z)
            self._z_axis.pos = self._position
            self._z_axis_label.pos = vec(self._position.x, self._position.y, self._position.z + 2)

    def move(self, dt):
        self._position += self._velocity * dt
        self._draw()

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity


green_car = Car(position=vec(-10, 0, -5), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 5), colour=color.red)
red_car.hide_label()
green_car.hide_axis()

axis_green_car = Axis(green_car._car, num_labels=6, length=20, start_pos=vec(-10, 0, -5), label_orientation="down")
axis_red_car = Axis(red_car._car, num_labels=6, length=20, start_pos=vec(-10, 0, 5), label_orientation="down")

timer = PhysTimer(x=0, y=5)

space_time_graph_red = graph(width=350, height=150, title="Space-time graph for red inertial frame", xtitle="Position",
                             ytitle="Time", ymax=20, xmin=-10, xmax=10)
red_curve_green_car = gcurve(graph=space_time_graph_red, color=color.green)
red_curve_red_car = gcurve(graph=space_time_graph_red, color=color.red)

space_time_graph_green = graph(width=350, height=150, title="Space-time for green inertial frame", xtitle="Position",
                               ytitle="Time", ymax=20, xmin=-10, xmax=10)
green_curve_green_car = gcurve(graph=space_time_graph_green, color=color.green)
green_curve_red_car = gcurve(graph=space_time_graph_green, color=color.red)

scene.title = "Relative motion: click on car to change camera"
scene.center = vec(0, 0, 0)
scene.forward = vec(0.0726397, -0.41687, -0.906058)
scene.range = 11
scene.caption = "Galilean transformation \\(  \\begin{pmatrix} x' \\\\ t'\\end{pmatrix} = \\begin{pmatrix} 1 & -v \\\\ 0 & 1 \\end{pmatrix} \\begin{pmatrix} x \\\\ t \\end{pmatrix} \\)"
MathJax.Hub.Queue(["Typeset", MathJax.Hub])


def select_car_in(my_scene):
    selected_object = my_scene.mouse.pick
    if selected_object is None:
        return
    my_scene.camera.follow(selected_object)
    if selected_object.color == color.green:
        # scene.forward = vec(-0.00101513, -0.770739, 0.637151)
        scene.range = 11
        green_car.hide_label()
        green_car.show_axis()
        red_car.show_label()
        red_car.hide_axis()
    elif selected_object.color == color.red:
        # scene.forward = vec(0.00813912, -0.581035, -0.813838)
        scene.range = 8
        red_car.hide_label()
        red_car.show_axis()
        green_car.show_label()
        green_car.hide_axis()


def on_mouse_click():
    select_car_in(scene)


scene.bind('click', on_mouse_click)

dt = 0.01
t = 0
while green_car.position().x <= 10:
    rate(1 / dt)
    green_car.move(dt)
    red_curve_green_car.plot(green_car.position().x, t)
    red_curve_red_car.plot(red_car.position().x, t)

    green_curve_red_car.plot(-green_car.position().x, t)
    green_curve_green_car.plot(0, t)

    timer.update(t)

    t += dt

label(pos=vec(0, 7, 0), text="Galilean transformation: x'=x - vt", color=color.yellow)
scene.waitfor('click')

