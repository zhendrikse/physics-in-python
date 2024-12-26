from vpython import vec, rate, graph, gcurve, color, canvas, label

from ..toolbox.axis import Axis
from ..toolbox.timer import Timer
from ..toolbox.car import Car

animation_time = 15  # seconds

scene = canvas(width="800", height="600")
scene.title = "Relative motion"
scene.center = vec(0, 0, 0)
scene.forward = vec(0, -0.35, -1)
scene.range = 11

green_car = Car(position=vec(-animation_time, 0, -5), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 5), colour=color.red)
red_car.hide_label()

axis_green_car = Axis(num_tick_marks=11, length=2 * animation_time, position=vec(-animation_time, 0, -5),
                      offset=animation_time)
axis_red_car = Axis(num_tick_marks=11, length=2 * animation_time, position=vec(0, 0, 5), offset=0)
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
t = 0
while green_car.position.x <= animation_time:
    rate(1 / dt)
    green_car.move(dt)
    red_curve_green_car.plot(green_car.position.x, t)
    red_curve_red_car.plot(red_car.position.x, t)

    green_curve_red_car.plot(-green_car.position.x, t)
    green_curve_green_car.plot(-red_car.position.x, t)

    timer.update(t)
    axis_green_car.reorient_with(green_car)

    t += dt

print("scene.center=", scene.center)
print("scene.forward=", scene.forward)
print("scene.range=", scene.range)
print("t={}\n".format(t))

label(pos=vec(0, 7, 0), text="Galilean transformation: x'=x - vt",
      color=color.yellow)
scene.waitfor('click')
