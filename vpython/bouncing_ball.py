#Web VPython 3.2
from vpython import *

title = """&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/kinematics/code/bouncing_ball.py">bouncing_ball.py</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; Click mouse button to drop ball

"""

display = canvas(title=title, range=25, forward=vec(-0.359679, -0.505533, -0.784262), width=600, height=400, background=color.gray(0.075))

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("x", "y", "z")

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


class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=20, num_tick_marks=None, axis_labels=label_text):
        self._position = position
        num_tick_marks = length - 1 if not num_tick_marks else num_tick_marks
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200

        self._axis, self._arrows, self._arrow_labels, self._tick_marks, self._tick_labels = [], [], [], [], []
        for base_vec in base:
            self._axis += [
                cylinder(pos=position - length * base_vec / 2, axis=length * base_vec, radius=radius, color=axis_color)]
            self._arrows += [
                arrow(pos=position + length * base_vec / 2, axis=base_vec, color=axis_color, shaftwidth=radius)]

        for i in range(len(base)):
            self._arrow_labels.append(label(pos=position + base[i] * (length / 2 + tick_increment), text=axis_labels[i],
                                            color=tick_marks_color, box=False))

        offset = [-0.05 * length * y_hat, 0.05 * length * x_hat, -0.05 * length * y_hat]
        positions = []
        for i in range(len(base)):
            for j in range(num_tick_marks):
                pos = position - base[i] * (length / 2 - j * tick_increment)
                positions.append(pos)
                label_value = pos.x - position.x if i == 0 else pos.y - position.y if i == 1 else pos.z - position.z
                label_value = "" if int(num_tick_marks / 2) == j else str(int(label_value))
                marker = label(pos=pos + offset[i], text=label_value, color=color.gray(0.5), box=False)
                self._tick_labels.append(marker)
                a_box = box(pos=pos, width=2 * radius, height=0.5, length=2 * radius, color=tick_marks_color)
                if i == 1:
                    a_box.rotate(angle=0.5 * pi, axis=vec(0, 0, 1))
                self._tick_marks.append(a_box)

        self._xy_mesh, self._zx_mesh, self._xz_mesh, self._yx_mesh = [], [], [], []
        for j in range(num_tick_marks):
            self._xy_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y + j * tick_increment - length / 2, position.z),
                         axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            self._yx_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y - length / 2, position.z),
                         axis=y_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            self._xz_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y, position.z - length / 2),
                         axis=z_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]
            self._zx_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y, position.z - length / 2 + j * tick_increment),
                         axis=x_hat * length, color=color.gray(.5), radius=radius / 2, visible=False)]

    def show_axis(self):
        self.axis_visible(True)

    def hide_axis(self):
        self.axis_visible(False)

    def show_tick_labels(self):
        self.tick_labels_visible(True)

    def hide_tick_labels(self):
        self.tick_labels_visible(False)

    def show_tick_marks(self):
        self.tick_marks_visible(True)

    def hide_tick_marks(self):
        self.tick_marks_visible(False)

    def axis_visible(self, visible):
        for i in range(len(base)):
            self._arrow_labels[i].visible = visible
            self._arrows[i].visible = visible
            self._axis[i].visible = visible
        self.tick_labels_visible(visible)
        self.tick_marks_visible(visible)

    def tick_labels_visible(self, visible):
        for a_label in self._tick_labels:
            a_label.visible = visible

    def tick_marks_visible(self, visible):
        for tick_mark in self._tick_marks:
            tick_mark.visible = visible

    def xy_mesh_visible(self, visible):
        for i in range(len(self._xy_mesh)):
            self._xy_mesh[i].visible = visible
            self._yx_mesh[i].visible = visible

    def xz_mesh_visible(self, visible):
        for i in range(len(self._xz_mesh)):
            self._xz_mesh[i].visible = visible
            self._zx_mesh[i].visible = visible

    def show_xy_mesh(self):
        self.xy_mesh_visible(True)

    def hide_xy_mesh(self):
        self.xy_mesh_visible(False)

    def show_xz_mesh(self):
        self.xz_mesh_visible(True)

    def hide_xz_mesh(self):
        self.xz_mesh_visible(False)


class Moveable:
    def __init__(self, pos=vec(0, 0, 0), velocity=vec(0, 0, 0), mass=1.0):
        self._position = pos
        self._velocity = velocity
        self._mass = mass
        self._start_position = pos
        self._start_velocity = velocity

    # To be implemented by each movable
    def render(self):
        pass

    def reset(self):
        self._position = self._start_position
        self._velocity = self._start_velocity
        self.render()

    def move_due_to(self, force_vector=vec(0, 0, 0), dt=0.01):
        # Newton's second law: F = m * a
        acceleration_vector = force_vector / self._mass
        self._velocity += acceleration_vector * dt
        self._position += self._velocity * dt
        self.render()

    def position(self):
        return self._position

    def mass(self):
        return self._mass


class Ball(Moveable):
    def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, colour=color.yellow, elasticity=1.0, make_trail=True, draw=True):
        Moveable.__init__(self, pos=position, velocity=velocity, mass=mass)

        self._ball = self._vpython_ball(mass, position, velocity, radius, colour, elasticity, make_trail) if draw else None
        self._radius = radius
        self._elasticity = elasticity

    def _vpython_ball(self, mass, position, velocity, radius, colour, elasticity, make_trail):
        return sphere(pos=position, radius=radius, color=colour, velocity=velocity, mass=mass, elasticity=elasticity, make_trail=make_trail, trail_type="points", retain=50, interval=5)

    def render(self):
        if self._ball:
            self._ball.pos = self._position

    def lies_on_floor(self):
        return self.position().y - self.radius() <= 0.5

    def bounce_from_floor(self, dt):
        self._velocity.y *= -self.elasticity()
        self._position += self._velocity * dt

        # if the velocity is too slow, stay on the ground
        if self._velocity.y <= 0.1:
            self._position.y = self.radius() + self.radius() / 10

        self.render()

    def radius(self):
        return self._radius

    def elasticity(self):
        return self._elasticity


ball = Ball(position=vec(-10, 20, -10), velocity=vec(1, 0, 1), radius=1, elasticity=0.9, colour=color.cyan)
position_plot = graph(title="Bouncing ball", xtitle="Time", ytitle="Height", width=600, height=250, background=color.black)
curve = gcurve(color=color.red)
timer = Timer(position=vec(20, 20, 0))
axis = Base(length=40)
axis.hide_tick_labels()
axis.show_xz_mesh()

t = 0
dt = 0.01
display.waitfor('click')
while ball.position().x < 20:
    rate(2 / dt)
    timer.update(t / 2)

    force = vec(0, -9.8, 0) * ball.mass()
    ball.move_due_to(force, dt)
    if ball.lies_on_floor():
        ball.bounce_from_floor(dt)

    curve.plot(t / 2, ball.position().y)
    t += dt
