from vpython import vec, rate, box, color, graph, gcurve
from toolbox.ball import Ball
from toolbox.timer import PhysTimer

ball = Ball(position=vec(0, 20, 0), velocity=vec(1, 0, 0), radius=2, elasticity=0.9, color=color.red)
floor = box(pos=vec(25, -.5, 0), length=50, height=1, width=10, color=color.green)
position_plot = graph(title="Bouncing ball", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.red)
timer = PhysTimer(-10, 0)

t = 0
dt = 0.01
while True:
    rate(3/dt)
    timer.update(t/3)

    force = vec(0, -9.8, 0) * ball.mass
    ball.move(force, dt)
    if ball.is_on_ground():
        if abs(ball.velocity.y) > 0.1:
            ball.bounce_from_ground(dt)
        else:
            ball._ball.velocity.x = 0

    curve.plot(t * dt, ball.position.y)
    t += dt

 