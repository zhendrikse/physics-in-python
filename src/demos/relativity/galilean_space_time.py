from vpython import vec, rate, graph, gcurve, color, canvas, label, box, cylinder

from ..toolbox.timer import Timer
from ..toolbox.car import Car
from ..toolbox.axis import x_hat, z_hat

animation_time = 15  # seconds

scene = canvas(width="800", height="600")
scene.title = "Relative motion"
scene.center = vec(0, 0, -5)
scene.forward = vec(-1, -0.45, -0.04)
scene.range = 12.5

class Mesh:
    def __init__(self, position=vec(0, 0, 0), length = 20, num_tick_marks=None):
        num_tick_marks = length - 1 if not num_tick_marks else num_tick_marks
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200
        self._zx_mesh, self._xz_mesh = [], []
        for j in range(num_tick_marks):
            self._xz_mesh += [
                cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y, position.z - length / 2),
                         axis=z_hat * length, color=color.gray(0.4), radius=radius / 2, visible=True)]
            self._zx_mesh += [
                cylinder(pos=vec(position.x - length / 2, position.y, position.z - length / 2 + j * tick_increment),
                         axis=x_hat * length, color=color.gray(0.4), radius=radius / 2, visible=True)]

    def shift_by(self, a_shift):
        for j in range(len(self._xz_mesh)):
            self._xz_mesh[j].pos += a_shift
            self._zx_mesh[j].pos += a_shift


green_car = Car(position=vec(-animation_time, 0, -5), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 5), colour=color.red)
red_car.hide_label()

mesh = Mesh(position=vec(-animation_time / 2, -1, 0), length = 2 * animation_time)

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
    if selected_object is None or type(selected_object) is cylinder:
        return
    my_scene.camera.follow(selected_object)
    if selected_object.color == color.green:
        green_car.hide_label()
        red_car.show_label()
    elif selected_object.color == color.red:
        red_car.hide_label()
        green_car.show_label()


def on_mouse_click():
    select_car_in(scene)


scene.bind('click', on_mouse_click)
#scene.waitfor("click")

timer = Timer(position=vec(0, 5, 0))
dt = 0.01
t = 0
while green_car.position.x <= animation_time:
    rate(1 / dt)
    green_car.move(dt)
    mesh.shift_by(x_hat * dt / 2)

    red_curve_green_car.plot(green_car.position.x, t)
    red_curve_red_car.plot(red_car.position.x, t)

    green_curve_red_car.plot(-green_car.position.x, t)
    green_curve_green_car.plot(-red_car.position.x, t)

    timer.update(t)
    t += dt

label(pos=vec(0, 7, 0), text="Galilean transformation: x'=x - vt", color=color.yellow)
