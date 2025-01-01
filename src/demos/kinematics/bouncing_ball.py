from vpython import vec, rate, box, color, graph, gcurve, scene
from ..toolbox.ball import Ball
from ..toolbox.timer import Timer

ball = Ball(position=vec(0, 20, 0), velocity=vec(1, 0, 0), radius=2, elasticity=0.9, color=color.red)
floor = box(pos=vec(25, 0, 0), length=50, height=1, width=10, color=color.green)
position_plot = graph(title="Bouncing ball", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.red)
timer = Timer(position=vec(-10, 0, 0))

scene.title = "Click mouse button to drop ball"
scene.waitfor('click')

t = 0
dt = 0.01
while ball.position.x < floor.length:
    rate(3 / dt)
    timer.update(t / 3)

    force = vec(0, -9.8, 0) * ball.mass
    ball.move(force, dt)
    if ball.lies_on_floor():
        ball.bounce_from_floor(dt)

    curve.plot(t * dt, ball.position.y)
    t += dt
