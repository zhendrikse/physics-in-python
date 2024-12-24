from vpython import vector, points, label, curve, color, box, pyramid, sphere


def obj_size(obj):
    if type(obj) == box or type(obj) == pyramid:
        return obj.size
    elif type(obj) == sphere:
        return vector(obj.radius, obj.radius, obj.radius)


class PhysAxis:
    """
    This class assists students in creating dynamic axes for their models.
    """

    def __init__(self, obj, numLabels, axisType="x", axis=vector(1, 0, 0), startPos=None,
                 length=None, labels=None, labelOrientation="down", axisColor=color.yellow, labelColor=color.white):
        # PhysAxis
        # obj - Object which axis is oriented based on by default
        # numLabels - number of labels on axis
        # axisType - sets whether this is a default axis of x or y, or an arbitrary axis
        # axis - unit vector defining the orientation of the axis to be created IF axisType = "arbitrary"
        # startPos - start position for the axis - defaults to (-obj_size(obj).x/2,-4*obj_size(obj).y,0)
        # length - length of the axis - defaults to obj_size(obj).x
        # labelOrientation - how labels are placed relative to axis markers - "up", "down", "left", or "right"

        try:
            self.interval_markers = []
            self.interval_labels = []
            self.labelText = labels
            self.obj = obj
            self.lastPos = vector(self.obj.pos.x, self.obj.pos.y, self.obj.pos.z)
            self.numLabels = numLabels
            self.axisType = axisType
            self.axis = axis if axisType != "y" else vector(0, 1, 0)
            self.length = length if (length is not None) else obj_size(obj).x
            self.startPos = startPos if (startPos is not None) else vector(-obj_size(obj).x / 2, -4 * obj_size(obj).y,
                                                                           0)
            self.axisColor = axisColor
            self.labelColor = labelColor

            if labelOrientation == "down":
                self.labelShift = vector(0, -0.05 * self.length, 0)
            elif labelOrientation == "up":
                self.labelShift = vector(0, 0.05 * self.length, 0)
            elif labelOrientation == "left":
                self.labelShift = vector(-0.1 * self.length, 0, 0)
            elif labelOrientation == "right":
                self.labelShift = vector(0.1 * self.length, 0, 0)

            self.__reorient()
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print(
                "Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def update(self):
        try:
            # Determine if reference obj. has shifted since last update, if so shift us too
            if self.obj.pos != self.lastPos:
                diff = self.obj.pos - self.lastPos

                for i in range(len(self.interval_markers)):
                    self.interval_markers[i].pos += diff
                    self.interval_labels[i].pos += diff
                self.axisCurve.pos = [x + diff for x in self.axisCurve.pos]

                self.lastPos = vector(self.obj.pos.x, self.obj.pos.y, self.obj.pos.z)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print(
                "Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def reorient(self, axis=None, startPos=None, length=None, labels=None, labelOrientation=None):
        try:
            # Determine which, if any, parameters are being modified
            self.axis = axis if axis is not None else self.axis
            self.startPos = startPos if startPos is not None else self.startPos
            self.length = length if length is not None else self.length
            self.labelText = labels if labels is not None else self.labels

            # Re-do label orientation as well, if it has been set
            if labelOrientation == "down":
                self.labelShift = vector(0, -0.05 * self.length, 0)
            elif labelOrientation == "up":
                self.labelShift = vector(0, 0.05 * self.length, 0)
            elif labelOrientation == "left":
                self.labelShift = vector(-0.1 * self.length, 0, 0)
            elif labelOrientation == "right":
                self.labelShift = vector(0.1 * self.length, 0, 0)

            self.__reorient()
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print(
                "Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def __reorient(self):
        # Actual internal axis setup code... determines first whether we are creating or updating
        updating = True if len(self.interval_markers) > 0 else False

        # Then determines the endpoint of the axis and the interval
        final = self.startPos + (self.length * self.axis)
        interval = (self.length / (self.numLabels - 1)) * self.axis

        # Loop for each interval marker, setting up or updating the markers and labels
        i = 0
        while i < self.numLabels:
            intervalPos = self.startPos + (i * interval)

            # Determine text for this label
            if self.labelText is not None:
                labelText = self.labelText[i]
            elif self.axisType == "y":
                labelText = "%.2f" % intervalPos.y
            else:
                labelText = "%.2f" % intervalPos.x

            if updating:
                self.interval_markers[i].pos = intervalPos
                self.interval_labels[i].pos = intervalPos + self.labelShift
                self.interval_labels[i].text = str(labelText)
            else:
                self.interval_markers.append(points(pos=intervalPos, color=self.axisColor, radius=5))
                self.interval_labels.append(
                    label(pos=intervalPos + self.labelShift, text=str(labelText), box=False, height=10,
                          color=self.labelColor))
            i = i + 1

        # Finally, create / update the line itself!
        if updating:
            self.axisCurve.pos = [self.startPos, final]
        else:
            self.axisCurve = curve(pos=[self.startPos, final], color=self.axisColor)
