from vpython import vec, rate, graph, gcurve, color, scene, label

from ..toolbox.axis import Axis
from ..toolbox.timer import PhysTimer
from ..toolbox.car import Car

green_car = Car(position=vec(-10, 0, -5), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 5), colour=color.red)
red_car.hide_label()
green_car.hide_axis()

axis_green_car = Axis(green_car._car, num_labels=6, length=20, start_pos=vec(-10, 0, -5), label_orientation="down")
axis_red_car = Axis(red_car._car, num_labels=6, length=20, start_pos=vec(-10, 0, 5), label_orientation="down")

timer = PhysTimer(x=0, y=5)

space_time_graph_red = graph(width=350, height=150, title="Space-time graph for red inertial frame", xtitle="Position",
                             ytitle="Time", ymax=20,
                             xmin=-10, xmax=10)
red_curve_green_car = gcurve(graph=space_time_graph_red, color=color.green)
red_curve_red_car = gcurve(graph=space_time_graph_red, color=color.red)

space_time_graph_green = graph(width=350, height=150, title="Space-time for green inertial frame", xtitle="Position",
                               ytitle="Time", ymax=20,
                               xmin=-10, xmax=10)
green_curve_green_car = gcurve(graph=space_time_graph_green, color=color.green)
green_curve_red_car = gcurve(graph=space_time_graph_green, color=color.red)

scene.title = "Relative motion"
scene.center= vec(0, 0, 0)
scene.forward= vec(0.0726397, -0.41687, -0.906058  )
scene.range= 11


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
while green_car.position.x <= 10:
    rate(1 / dt)
    green_car.move(dt)
    red_curve_green_car.plot(green_car.position.x, t)
    red_curve_red_car.plot(red_car.position.x, t)

    green_curve_red_car.plot(-green_car.position.x, t)
    green_curve_green_car.plot(0, t)

    timer.update(t)

    t += dt

print("scene.center=", scene.center)
print("scene.forward=", scene.forward)
print("scene.range=", scene.range)
print("t={}\n".format(t))

label(pos=vec(0, 10, 0), text="Galilean transformation: x''=x - vt",
      color=color.yellow)
scene.waitfor('click')
