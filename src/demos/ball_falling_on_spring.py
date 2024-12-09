# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=ExxDuRTIe0E
# - https://trinket.io/glowscript/58d3d4ba0b

from vpython import vector, rate, box, graph, gcurve, color, mag

from toolbox.ball import Ball
from toolbox.spring import Spring 


g1 = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.blue)

spring_size = 0.4
spring_rest_position = vector(0, spring_size, 0)
floor = box(pos=vector(0, 0, 0), size=vector(2, 0.05, 1))
ball = Ball(position=vector(0, 2 + spring_size, 0))
gravitational_force = vector(0, -9.8 * ball.mass, 0)
spring = Spring(axis=spring_rest_position, spring_constant=1000, equilibrium_size=spring_size, radius=0.07)#, thickness=0.04)

def main():
  dt = 0.01
  for i in range(0, 500):
    rate(1 / (2 * dt))

    ball.move(spring.force + gravitational_force, dt)
    spring.update_position(ball.position if mag(ball.position) - spring_size < 0 else spring_rest_position)

    curve.plot(i * dt, ball.position.y)

if __name__=="__main__":
    main()
