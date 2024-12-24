from vpython import vec, rate, graph, gcurve, color, scene, label, arrow

from ..toolbox.physics_axis import PhysAxis
from ..toolbox.timer import PhysTimer
from ..toolbox.car import Car

green_car = Car(position=vec(-10, 0, -5), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 5), colour=color.red)
red_car.hide_label()
green_car.hide_axis()

axis_green_car = PhysAxis(green_car._label, numLabels=6, length=20, startPos=vec(-10, 0, -5))
axis_red_car = PhysAxis(red_car._label, numLabels=6, length=20, startPos=vec(-10, 0, 5))

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

# scene.forward = vec(0.00813912, -0.581035, -0.813838)
# scene.forward = vec(-0.00101513, -0.770739, 0.637151)
scene.forward = vec(-0.451646, 0.416871, -0.788818)
scene.range = 9


def select_car_in(my_scene):
    selected_object = my_scene.mouse.pick
    if selected_object is None:
        return
    my_scene.camera.follow(selected_object)
    if selected_object.color == color.green:
        # scene.forward = vec(-0.00101513, -0.770739, 0.637151)
        scene.range = 12
        green_car.hide_label()
        green_car.show_axis()
        red_car.show_label()
        red_car.hide_axis()
    elif selected_object.color == color.red:
        # scene.forward = vec(0.00813912, -0.581035, -0.813838)
        scene.range = 9
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

label(pos=vec(0, 6, 0), text="The transformation from one perspective to the other is a Galilean transformation",
      color=color.yellow)
scene.waitfor('click')
