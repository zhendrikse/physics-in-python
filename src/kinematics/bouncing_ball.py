from vpython import vec, rate, box, color, graph, gcurve, scene
from src.toolbox.ball import Ball
from src.toolbox.timer import Timer
from src.toolbox.axis import Base

ball = Ball(position=vec(-10, 20, -10), velocity=vec(1, 0, 1), radius=1, elasticity=0.9, colour=color.cyan)
position_plot = graph(title="Bouncing ball", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.red)
timer = Timer(position=vec(20, 20, 0))
base = Base(length=40)
base.hide_tick_labels()
base.show_xz_mesh()

scene.title = "Click mouse button to drop ball"
scene.forward= vec(-0.359679, -0.505533, -0.784262)
scene.range= 25

t = 0
dt = 0.01
scene.waitfor('click')
while ball.position().x < 20:
    rate(2 / dt)
    timer.update(t / 2)

    force = vec(0, -9.8, 0) * ball.mass()
    ball.move_due_to(force, dt)
    if ball.lies_on_floor():
        ball.bounce_from_floor(dt)

    curve.plot(t / 2, ball.position().y)
    t += dt
