from vpython import vec, rate, graph, gcurve, color, canvas, label, box, cylinder

from src.toolbox.timer import Timer
from src.toolbox.car import Car
from src.toolbox.axis import x_hat, z_hat, Base

animation_time = 15  # seconds

scene = canvas(width="800", height="600")
scene.title = "Relative motion"
scene.center = vec(0, 0, -5)
scene.forward = vec(-1, -0.45, -0.04)
scene.range = 12.5

green_car = Car(pos=vec(-animation_time, 2, -5), velocity=vec(1, 0, 0), scale=0.25)
red_car = Car(pos=vec(0, 2, 5), colour=color.red, scale=0.25)
red_car_label = label(pos=red_car.position(), xoffset=3, yoffset=2, text="Select my\nperspective", color=color.red, visible=False)
green_car_label = label(pos=green_car.position(), xoffset=3, yoffset=2, text="Select my\nperspective", color=color.green, visible=True)
axis = Base(length=2 * animation_time)
axis.hide_axis()
axis.show_xz_mesh()

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
        green_car_label.visible = False
        red_car_label.visible = True
    elif selected_object.color == color.red:
        red_car_label.visible = False
        green_car_label.visible = True


def on_mouse_click():
    select_car_in(scene)


scene.bind('click', on_mouse_click)
#scene.waitfor("click")

timer = Timer(position=vec(0, 5, 0))
dt = 0.01
t = 0
while green_car.position().x <= animation_time:
    rate(1 / dt)
    green_car.move_due_to(vec(0, 0, 0), dt)
    #mesh.shift_by(x_hat * dt / 2)

    red_curve_green_car.plot(green_car.position().x, t)
    red_curve_red_car.plot(red_car.position().x, t)

    green_curve_red_car.plot(-green_car.position().x, t)
    green_curve_green_car.plot(-red_car.position().x, t)

    timer.update(t)
    t += dt

label(pos=vec(0, 7, 0), text="Galilean transformation: x'=x - vt", color=color.yellow)
