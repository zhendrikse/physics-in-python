from vpython import vector, rate, box, graph, gcurve, color, sphere, helix, mag, hat
from toolbox.ball import Ball
from toolbox.spring import Spring

g1 = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.blue)

ball = Ball(mass=1.0, position=vector(1.25, 0, 0), radius=0.1, color=color.yellow)
spring = Spring(position=vector(0, 0, 0), axis=ball.position, spring_constant=1.0, equilibrium_size=1.0, radius=0.05)

dt = 0.1
for t in range(0, 200):
  rate(1/dt)
  ball.move(spring.force, dt)
  spring.update_position(ball.position)
  curve.plot(t * dt, ball.position.x)

print("finished!")