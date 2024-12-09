from vpython import vector, rate, box, graph, gcurve, color, sphere, helix, mag, hat
from toolbox.ball import Ball
from toolbox.spring import Spring

position_plot = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)

left_ball  = Ball(mass=1.0, position=vector(-0.75, 0, 0), radius=0.1, color=color.red)
right_ball = Ball(mass=1.0, position=vector( 0.75, 0, 0), radius=0.1, color=color.blue)
distance = left_ball.distance_to(right_ball)
spring = Spring(position=-distance / 2, axis=distance, spring_constant=1.0, equilibrium_size=1.0, radius=0.05)

dt = 0.1
for t in range(0, 200):
  rate(2/dt)
  right_ball.move(spring.force, dt)
  left_ball.move(-spring.force, dt)
  distance = left_ball.distance_to(right_ball)
  spring.update(distance, -distance / 2)
  curve_left.plot(t * dt, left_ball.position.x)
  curve_right.plot(t * dt, right_ball.position.x)
