#
# https://github.com/possibly-wrong/vturtle/
#

"""VPython-based robot simulator and turtle graphics engine."""

from vpython import *

def vec2(pos, y=None):
    # Helper function to convert 2D x,y or tuple (x,y) to 3D vector.
    if not y is None:
        pos = (pos, y)
    if isinstance(pos, vector):
        pos = (pos.x, pos.y, 0)
    return vector(pos[0], pos[1], 0)

class Robot:
    """Robot with drawing pen and stall and proximity sensors."""

    def __init__(self, pos=(0, 0), sensors=[90, 0, -90], obstacles=[]):
        """Create a robot.

        Create a robot at the given (x,y) position (cm) and facing along
        the positive x-axis, with a yellow pen for drawing a trail as
        the robot moves.

        Any specified sensors and obstacles are added using add_sensor()
        and add_obstacle(), respectively.
        """
        self._radius = 9 # cm
        self._range = 10 # cm
        self._speed = 15 # cm/s
        self._ff = 1
        self._fps = 24

        # Create robot body.
        parts = []
        parts.append(cylinder(pos=vec(0, 0, 2), axis=vec(0, 0, 4),
                              radius=self._radius, color=color.blue))

        # Add lights.
        parts.append(sphere(pos=vec(6, 3, 6), radius=0.5, color=color.red))
        for y in [-2.5, -1, 0.5]:
            parts.append(sphere(pos=vec(5.5, y, 6), radius=0.5,
                                color=color.green))

        # Add side wheels with tread.
        for y in [-1, 1]:
            parts.append(cylinder(pos=vec(0, 7 * y, 4), axis=vec(0, y, 0),
                                  radius=4, color=color.gray(0.5)))
            parts.append(ring(pos=vec(0, 7.5 * y, 4), axis=vec(0, y, 0),
                              radius=4, thickness=0.25,
                              color=color.gray(0.25)))

        # Add front tricycle wheel.
        parts.append(cylinder(pos=vec(7.5, -0.5, 1.5), axis=vec(0, 1, 0),
                              radius=1.5, color=color.gray(0.5)))

        # Add pen.
        self._pen_color = color.yellow
        parts.append(cylinder(pos=vec(0, 0, 0), axis=vec(0, 0, 14), radius=0.5,
                              color=self._pen_color))
        self._frame = compound(parts, pos=vec2(pos), origin=vec(0, 0, 0))

        # Initialize drawing trails and sensors, and register obstacles.
        self._trail = curve(pos=[vec2(pos)], color=self._pen_color)
        self._trails = []
        self._stalled = False
        self._sensors = []
        for sensor in sensors:
            self.add_sensor(sensor)
        self._obstacles = []
        for obstacle in obstacles:
            self.add_obstacle(obstacle)

    def forward(self, distance):
        """Move forward the given distance (cm).

        The robot will stall if it runs into an obstacle before moving
        the given distance.
        """
        self.position(self._frame.pos + distance * norm(self._frame.axis))

    def backward(self, distance):
        """Move backward the given distance (cm).

        The robot will stall if it runs into an obstacle before moving
        the given distance.
        """
        self.forward(-distance)
        
    def left(self, angle):
        """Turn left through angle (deg)."""
        if self._speed == inf:
            self._frame.rotate(angle=radians(angle), axis=vec(0, 0, 1))
        else:
            psi = self.heading() + angle
            dpsi = sign(angle) * self._speed / self._fps / 7.5
            for r in arange(0, radians(angle), dpsi):
                if self._ff < inf:
                    rate(self._fps * self._ff)
                self._frame.rotate(angle=dpsi, axis=vec(0, 0, 1))
            self._frame.rotate(angle=radians(psi - self.heading()),
                               axis=vec(0, 0, 1))

    def right(self, angle):
        """Turn right through angle (deg)."""
        self.left(-angle)

    def pen_up(self):
        """Pick up drawing pen to move without leaving a trail."""
        if self._trail:
            self._trails.append(self._trail)
            self._trail = False

    def pen_down(self):
        """Put down drawing pen to leave a trail when moving."""
        if not self._trail:
            self._trail = curve(pos=[self._frame.pos], color=self._pen_color)

    def color(self, color=None, g=None, b=None):
        """Return or set drawing pen color.

        Specify color as (red, green, blue) values in [0, 1], either as
        separate arguments or as a tuple or vector.

        Changing the pen color while the pen is down will cause the next
        move to leave a "blended" trail from the previous drawing color
        to the new color.
        """
        if color is None:
            return self._pen_color
        if not g is None:
            color = vec(color, g, b)
        if not isinstance(color, vector):
            color = vector(*color)
        self._pen_color = color

    def clear(self):
        """Clear all of this robot's drawing trails."""
        if self._trail:
            self._trail.visible = False
        for trail in self._trails:
            trail.visible = False
        self._trail = False
        self._trails = []
        self.pen_down()

    def show(self):
        """Show robot, making it visible."""
        self._frame.visible = True

    def hide(self):
        """Hide robot, making it invisible."""
        self._frame.visible = False

    def position(self, pos=None, y=None):
        """Get position or move to position without changing heading.

        Specify position either as separate (x,y) arguments (cm) or as a
        tuple.

        The robot will stall if it runs into an obstacle before reaching
        the given destination.
        """
        if pos is None:
            return (self._frame.pos.x, self._frame.pos.y)
        if self._trail:
            self._trail.append(pos=self._frame.pos, color=self._pen_color)
        pos = vec2(pos, y)
        last_pos = vector(self._frame.pos)
        dx = self._speed / self._fps
        while not self._check_stall() and mag(pos - self._frame.pos) > dx:
            if self._ff < inf:
                rate(self._ff * self._fps)
            last_pos = vector(self._frame.pos)
            direction = norm(pos - self._frame.pos)
            self._frame.pos = self._frame.pos + direction * dx
            if self._trail:
                self._trail.modify(-1, pos=self._frame.pos)
        if not self._stalled:
            last_pos = vector(self._frame.pos)
            self._frame.pos = pos
            self._check_stall()
        if self._stalled:
            self._frame.pos = last_pos
        if self._trail:
            self._trail.modify(-1, pos=self._frame.pos)

    def heading(self, angle=None):
        """Get current heading (deg) or turn to given heading."""
        current = degrees(atan2(self._frame.axis.y, self._frame.axis.x)) % 360
        if angle is None:
            return current
        self.left(((angle - current + 180) % 360) - 180)

    def distance(self, pos, y=None):
        """Return distance (cm) to given position.

        Specify position either as separate (x,y) arguments (cm) or as a
        tuple.
        """
        return mag(vec2(pos, y) - self._frame.pos)

    def towards(self, pos, y=None):
        """Return heading (deg) to given position.

        Specify position either as separate (x,y) arguments (cm) or as a
        tuple.
        """
        dv = vec2(pos, y) - self._frame.pos
        return degrees(atan2(dv.y, dv.x)) % 360

    def speed(self, speed=None):
        """Return or set robot speed (cm/s).

        Setting speed to inf causes the robot to move and turn
        instantaneously.

        Changing speed affects whether and how the robot encounters or
        detects obstacles, by changing how far the robot moves in each
        frame of animation.

        To control speed of execution when not using obstacles or
        sensors, use speed(). To control animation frame rate with
        reproducible obstacle navigation behavior, use fast_forward().
        """
        if speed is None:
            return self._speed
        self._speed = speed

    def fast_forward(self, speedup=None):
        """Return or set robot animation speedup.

        Specify speedup as a frame rate multiplier. For example, 1 is
        the default normal speed, and 2 is twice normal speed. Setting
        speedup to inf causes the animation to move as fast as possible.

        Changing animation speedup only affects the delay between frames
        of animation, not whether or how the robot encounters or detects
        obstacles.

        To control speed of execution when not using obstacles or
        sensors, use speed(). To control animation frame rate with
        reproducible obstacle navigation behavior, use fast_forward().
        """
        if speedup is None:
            return self._ff
        self._ff = speedup

    def stalled(self):
        """Return True iff robot has run into an obstacle."""
        return self._stalled

    def sensor(self, sensor_id):
        """Return state of given proximity sensor.

        Return True iff an obstacle is in range in the direction of the
        given sensor.
        """
        x1 = self._frame.pos
        dx = (self._radius + self._range) * rotate(norm(self._frame.axis),
                                                   self._sensors[sensor_id])
        x2 = x1 + dx
        for obstacle in self._obstacles:
            if obstacle._intersect_segment(x1, x2):
                return True
        return False

    def add_sensor(self, bearing):
        """Add proximity sensor mounted at given bearing (deg).

        The integer id of the sensor is returned, for use with sensor().
        Three sensors are available by default, with ids 0 (left,
        bearing 90), 1 (front, bearing 0), and 2 (right, bearing -90).
        """
        self._sensors.append(radians(bearing))
        return len(self._sensors) - 1

    def sensor_range(self, distance=None):
        """Get or set proximity sensor range (cm).

        The sensors are mounted on the circumference of the robot's
        cylindrical chassis (radius 9 cm).
        """
        if distance is None:
            return self._range
        self._range = distance

    def add_obstacle(self, obstacle):
        """Register obstacle (Wall or another Robot)."""
        self._obstacles.append(obstacle)
        self._check_stall()

    def _check_stall(self):
        for obstacle in self._obstacles:
            self._stalled = obstacle._intersect_circle(self._frame.pos,
                                                       self._radius)
            if self._stalled:
                break
        return self._stalled

    def _intersect_circle(self, center, radius):
        radius = radius + self._radius + 0.05
        return mag2(center - self._frame.pos) <= radius * radius

    def _intersect_segment(self, x1, x2):
        v = x1 - self._frame.pos
        w = x2 - x1
        a = mag2(w)
        b = 2 * dot(v, w)
        c = mag2(v) - self._radius * self._radius
        d = b * b - 4 * a * c
        if d >= 0:
            d = sqrt(d)
            return (0 <= -b + d <= 2 * a) or (0 <= -b - d <= 2 * a)
        return False

class Wall:
    """Wall obstacle."""

    def __init__(self, x1, x2, **args):
        """Create wall with (x,y) endpoints x1 and x2.

        A wall is a VPython box 1 cm wide, 15 cm tall, with optional
        additional box() arguments, e.g. texture=textures.wood.
        """
        height = 15
        x1, x2 = vec2(x1), vec2(x2)
        x1.z = height / 2
        x2.z = x1.z
        self._wall = box(pos=((x1 + x2) / 2), axis=(x2 - x1),
                         height=1, width=height, **args)
        x1.z = 0
        x2.z = 0
        self._x1, self._x2 = x1, x2
        self._a = mag2(self._wall.axis)

    def _intersect_circle(self, center, radius):
        radius = radius + 0.55
        v = self._x1 - center
        b = 2 * dot(v, self._wall.axis)
        c = mag2(v) - radius * radius
        d = b * b - 4 * self._a * c
        if d >= 0:
            d = sqrt(d)
            return (0 <= -b + d <= 2 * self._a) or (0 <= -b - d <= 2 * self._a)
        return False

    def _intersect_segment(self, x1, x2):
        return ((self._ccw(self._x1, x1, x2) != self._ccw(self._x2, x1, x2))
                and (self._ccw(self._x1, self._x2, x1) !=
                     self._ccw(self._x1, self._x2, x2)))

    def _ccw(self, a, b, c):
        return (b.x - a.x) * (c.y - a.y) > (c.x - a.x) * (b.y - a.y)

def table(center=(0,0), length=200, width=200):
    """Create a table with walled edges.

    This is a convenience function for creating a standard "tabletop"
    with Wall() edge obstacles for use with add_obstacle(). The list of
    walls is returned.
    """
    c = vec2(center)
    dx = vec(length / 2, 0, 0)
    dy = vec(0, width / 2, 0)
    box(pos=vec(c.x, c.y, -1.1), length=length, height=width, width=2,
        color=color.gray(0.25), texture=textures.wood)
    walls = []
    walls.append(Wall(c - dx + dy, c + dx + dy, texture=textures.wood))
    walls.append(Wall(c - dx - dy, c + dx - dy, texture=textures.wood))
    walls.append(Wall(c + dx - dy, c + dx + dy, texture=textures.wood))
    walls.append(Wall(c - dx - dy, c - dx + dy, texture=textures.wood))
    return walls

def maze(pos=(0,0), rows=8, columns=8, cell_size=30):
    """Create a maze on a table with walled edges.

    This is a convenience function for creating a simply connected
    binary tree maze with Wall() edge obstacles for use with
    add_obstacle(). The list of walls is returned.

    The given (x,y) position specifies the location of the center of the
    lower left cell of the maze.
    """
    dx = vec(cell_size, 0, 0)
    dy = vec(0, cell_size, 0)
    pos = vec2(pos) + (dx + dy) / 2
    walls = table(center=pos + dx * (columns / 2 - 1) + dy * (rows / 2 - 1),
                  length=columns * cell_size, width=rows * cell_size)
    for row in range(rows - 1):
        for col in range(columns - 1):
            c = pos + dx * col + dy * row
            if random() < 0.5:
                walls.append(Wall(c, c - dy))
            else:
                walls.append(Wall(c - dx, c))
    animation.center = pos + (columns / 2 - 1) * dx + (rows / 2 - 1) * dy
    return walls

if __name__ == '__main__':
    #robot = Robot(obstacles=table())
    robot = Robot(obstacles=maze())
    robot.forward(200) # run into wall
    robot.left(90)
    robot.forward(200) # run into wall
    stalled = robot.stalled()
    while True:
        pass