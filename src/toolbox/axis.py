from vpython import vector, points, label, curve, color, box, pyramid, sphere


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
        self.start_position = start_pos if (start_pos is not None) else vector(-obj_size(attached_to).x / 2,
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
                self.interval_markers.modify(i, pos = diff)
                self.interval_labels[i].pos += diff
            self.axisCurve.modify(0, pos=diff)
            self.axisCurve.modify(1, pos=diff)

            #self.axisCurve.pos = [x + diff for x in self.axisCurve.pos]

            self.lastPos = vector(self.obj.pos.x, self.obj.pos.y, self.obj.pos.z)

    def reorient(self, axis=None, start_pos=None, length=None, labels=None, label_orientation=None):
        # Determine which, if any, parameters are being modified
        self.axis = axis if axis is not None else self.axis
        self.start_position = start_pos if start_pos is not None else self.start_position
        self.length = length if length is not None else self.length
        self.labelText = labels if labels is not None else self.interval_labels

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
        final = self.start_position + (self.length * self.axis)
        interval = (self.length / (self.numLabels - 1)) * self.axis

        # Loop for each interval marker, setting up or updating the markers and labels
        i = 0
        while i < self.numLabels:
            interval_pos = self.start_position + (i * interval)

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
            self.axisCurve.pos = [self.start_position, final]
        else:
            self.axisCurve = curve(pos=[self.start_position, final], color=self.axisColor)
