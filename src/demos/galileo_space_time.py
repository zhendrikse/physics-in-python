
from vpython import vec, rate, graph, gcurve, color, scene, label, arrow

from toolbox.physics_axis import PhysAxis
from toolbox.timer import PhysTimer
from toolbox.car import Car

green_car = Car(position=vec(-10, 0, -3), velocity=vec(1, 0, 0))
red_car = Car(position=vec(0, 0, 3), colour=color.red)

axis_green_car = PhysAxis(green_car._label, numLabels=0, length=20, startPos=vec(-10, 0, -3))
axis_red_car = PhysAxis(red_car._label, numLabels=0, length=20, startPos=vec(-10, 0, 3))

timer = PhysTimer(x=0, y=5)

space_time_graph_red = graph(title="Space-time graph for red observer", xtitle="Position", ytitle="Time", ymax=20, xmin=-10, xmax=10)
space_time_graph_green = graph(title="Space-time graph for green observer", xtitle="Position", ytitle="Time", ymax=20, xmin=-10, xmax=10)

red_curve_green_car = gcurve(graph=space_time_graph_red, color=color.green)
red_curve_red_car = gcurve(graph=space_time_graph_red, color=color.red)

green_curve_green_car = gcurve(graph=space_time_graph_green, color=color.green)
green_curve_red_car = gcurve(graph=space_time_graph_green, color=color.red)

scene.forward = vec(0.00813912, -0.581035, -0.813838)
# screen.forward = vec(-0.00101513, -0.770739, 0.637151)
scene.range= 8.859641550339338

dt = 0.01
t = 0
while green_car.position.x <= 10:
    rate(1/dt)
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

label(pos=vec(0, 6, 0), text="The transformation from one perspective to the other is a Galilean transformation", color=color.yellow)
scene.waitfor('click')